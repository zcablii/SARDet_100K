# Copyright (c) Meta Platforms, Inc. and affiliates.

# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from mmdet.registry import MODELS
from mmengine.model import BaseModule
from scipy.signal import gaussian
import torch.nn.functional as F
import numpy as np
from kymatio.torch import Scattering2D
import torchhaarfeatures

class Canny_layer(BaseModule):
    def __init__(self, threshold=3, init_cfg=None):
        super(Canny_layer, self).__init__(init_cfg=None)

        self.threshold = threshold

        filter_size = 5
        self.gaussian_filter_horizontal = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=(1,filter_size), padding=(0,filter_size//2))
        self.gaussian_filter_vertical = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=(filter_size,1), padding=(filter_size//2,0))
        self.sobel_filter = np.array([[1, 0, -1],
                                 [2, 0, -2],
                                 [1, 0, -1]])

        self.sobel_filter_horizontal = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=self.sobel_filter.shape, padding=self.sobel_filter.shape[0]//2)
        self.sobel_filter_vertical = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=self.sobel_filter.shape, padding=self.sobel_filter.shape[0]//2)
        # filters were flipped manually

        self.directional_filter = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=self.sobel_filter.shape, padding=self.sobel_filter.shape[-1] // 2)
        
    @torch.no_grad()
    def forward(self, img):
        batch_size = img.shape[0]
        blurred_img_r = self.gaussian_filter_vertical(self.gaussian_filter_horizontal(img[:, 0:1]))
        # blurred_img = torch.stack([blurred_img_r],dim=1)
        # blurred_img = torch.stack([torch.squeeze(blurred_img)])

        grad_x_r = self.sobel_filter_horizontal(blurred_img_r)
        grad_y_r = self.sobel_filter_vertical(blurred_img_r)

        # COMPUTE THICK EDGES

        grad_mag = torch.sqrt(grad_x_r**2 + grad_y_r**2)
        grad_orientation = (torch.atan2(grad_y_r, grad_x_r) * (180.0/3.14159))
        grad_orientation += 180.0
        grad_orientation =  torch.round( grad_orientation / 45.0 ) * 45.0

        # THIN EDGES (NON-MAX SUPPRESSION)

        all_filtered = self.directional_filter(grad_mag)

        inidices_positive = (grad_orientation / 45) % 8
        inidices_negative = ((grad_orientation / 45) + 4) % 8

        height = inidices_positive.size()[2]
        width = inidices_positive.size()[3]
        pixel_count = height * width
        pixel_range = torch.cuda.FloatTensor([range(pixel_count)])
        
        indices = (inidices_positive.view(-1).data * pixel_count + pixel_range.repeat(1, batch_size)).squeeze()
        channel_select_filtered_positive = all_filtered.view(-1)[indices.long()].view(batch_size, 1, height, width)
        indices = (inidices_negative.view(-1).data * pixel_count + pixel_range.repeat(1, batch_size)).squeeze()
        channel_select_filtered_negative = all_filtered.view(-1)[indices.long()].view(batch_size, 1, height, width)
        channel_select_filtered = torch.cat([channel_select_filtered_positive,channel_select_filtered_negative], 1)
        is_max = channel_select_filtered.min(dim=1)[0] > 0.0
        is_max = torch.unsqueeze(is_max, dim=1)

        thin_edges = grad_mag.clone()
        thin_edges[is_max==0] = 0.0

        # THRESHOLD

        thresholded = thin_edges.clone()
        thresholded[thin_edges<self.threshold] = 0.0
        thresholded[thin_edges>=self.threshold] = 1.0

        early_threshold = grad_mag.clone()
        early_threshold[grad_mag<self.threshold] = 0.0

        assert grad_mag.size() == grad_orientation.size() == thin_edges.size() == thresholded.size() == early_threshold.size()

        return [blurred_img_r, grad_mag, grad_orientation, thin_edges, thresholded, early_threshold]
    
    def init_weights(self):
        filter_size = 5
        generated_filters = gaussian(filter_size,std=1.0).reshape([1,filter_size])
        self.gaussian_filter_horizontal.weight.data.copy_(torch.from_numpy(generated_filters))
        self.gaussian_filter_horizontal.bias.data.copy_(torch.from_numpy(np.array([0.0])))
        self.gaussian_filter_vertical.weight.data.copy_(torch.from_numpy(generated_filters.T))
        self.gaussian_filter_vertical.bias.data.copy_(torch.from_numpy(np.array([0.0])))
        filter_0 = np.array([   [ 0, 0, 0],
                                [ 0, 1, -1],
                                [ 0, 0, 0]])

        filter_45 = np.array([  [0, 0, 0],
                                [ 0, 1, 0],
                                [ 0, 0, -1]])

        filter_90 = np.array([  [ 0, 0, 0],
                                [ 0, 1, 0],
                                [ 0,-1, 0]])

        filter_135 = np.array([ [ 0, 0, 0],
                                [ 0, 1, 0],
                                [-1, 0, 0]])

        filter_180 = np.array([ [ 0, 0, 0],
                                [-1, 1, 0],
                                [ 0, 0, 0]])

        filter_225 = np.array([ [-1, 0, 0],
                                [ 0, 1, 0],
                                [ 0, 0, 0]])

        filter_270 = np.array([ [ 0,-1, 0],
                                [ 0, 1, 0],
                                [ 0, 0, 0]])

        filter_315 = np.array([ [ 0, 0, -1],
                                [ 0, 1, 0],
                                [ 0, 0, 0]])

        all_filters = np.stack([filter_0, filter_45, filter_90, filter_135, filter_180, filter_225, filter_270, filter_315])
        self.directional_filter.weight.data.copy_(torch.from_numpy(all_filters[:, None, ...]))
        self.directional_filter.bias.data.copy_(torch.from_numpy(np.zeros(shape=(all_filters.shape[0],))))

        self.sobel_filter_horizontal.weight.data.copy_(torch.from_numpy(self.sobel_filter))
        self.sobel_filter_horizontal.bias.data.copy_(torch.from_numpy(np.array([0.0])))
        self.sobel_filter_vertical.weight.data.copy_(torch.from_numpy(self.sobel_filter.T))
        self.sobel_filter_vertical.bias.data.copy_(torch.from_numpy(np.array([0.0])))


    
    def train(self, mode: bool = True):
        for module in self.children():
            module.eval()
        for param in self.gaussian_filter_horizontal.parameters():
            param.requires_grad = False
        for param in self.gaussian_filter_vertical.parameters():
            param.requires_grad = False
        for param in self.sobel_filter_vertical.parameters():
            param.requires_grad = False
        for param in self.sobel_filter_horizontal.parameters():
            param.requires_grad = False
        for param in self.directional_filter.parameters():
            param.requires_grad = False
        return self

class HOGLayerC(nn.Module):
    """Generate hog feature for each batch images. This module is used in
    Maskfeat to generate hog feature. This code is borrowed from.
    <https://github.com/facebookresearch/SlowFast/blob/main/slowfast/models/operators.py>
    Args:
        nbins (int): Number of bin. Defaults to 9.
        pool (float): Number of cell. Defaults to 8.
        gaussian_window (int): Size of gaussian kernel. Defaults to 16.
    """

    def __init__(self,
                 nbins: int = 9,
                 pool: int = 8,
                 gaussian_window: int = 16,
                 norm_out: bool = False,
                 in_channels: int = 1) -> None:
        super().__init__()
        self.nbins = nbins
        self.pool = pool
        self.pi = math.pi
        self.in_channels = in_channels
        weight_x = torch.FloatTensor([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
        weight_x = weight_x.view(1, 1, 3, 3).repeat(self.in_channels, 1, 1, 1)
        weight_y = weight_x.transpose(2, 3)
        self.register_buffer('weight_x', weight_x)
        self.register_buffer('weight_y', weight_y)

        self.gaussian_window = gaussian_window
        if gaussian_window:
            gkern = self.get_gkern(gaussian_window, gaussian_window // 2)
            self.register_buffer('gkern', gkern)
        self.norm_out = norm_out

    def get_gkern(self, kernlen: int, std: int) -> torch.Tensor:
        """Returns a 2D Gaussian kernel array."""

        def _gaussian_fn(kernlen: int, std: int) -> torch.Tensor:
            n = torch.arange(0, kernlen).float()
            n -= n.mean()
            n /= std
            w = torch.exp(-0.5 * n**2)
            return w

        gkern1d = _gaussian_fn(kernlen, std)
        gkern2d = gkern1d[:, None] * gkern1d[None, :]
        return gkern2d / gkern2d.sum()


    @torch.no_grad()
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Generate hog feature for each batch images.
        Args:
            x (torch.Tensor): Input images of shape (N, 3, H, W).
        Returns:
            torch.Tensor: Hog features.
        """
        # input is RGB image with shape [B 3 H W]
        hw = x.shape[-2], x.shape[-1]  
        x = F.pad(x, pad=(1, 1, 1, 1), mode='reflect')
        gx_rgb = F.conv2d(
            x, self.weight_x, bias=None, stride=1, padding=0, groups=self.in_channels)
        gy_rgb = F.conv2d(
            x, self.weight_y, bias=None, stride=1, padding=0, groups=self.in_channels)
        norm_rgb = torch.stack([gx_rgb, gy_rgb], dim=-1).norm(dim=-1)
        phase = torch.atan2(gx_rgb, gy_rgb)
        phase = phase / self.pi * self.nbins  # [-9, 9]

        b, c, h, w = norm_rgb.shape
        out = torch.zeros((b, c, self.nbins, h, w),
                          dtype=torch.float,
                          device=x.device)
        phase = phase.view(b, c, 1, h, w)
        norm_rgb = norm_rgb.view(b, c, 1, h, w)
        if self.gaussian_window:
            if h != self.gaussian_window:
                assert h % self.gaussian_window == 0, 'h {} gw {}'.format(
                    h, self.gaussian_window)
                repeat_rate = h // self.gaussian_window
                temp_gkern = self.gkern.repeat([repeat_rate, repeat_rate])
            else:
                temp_gkern = self.gkern
            norm_rgb *= temp_gkern

        out.scatter_add_(2, phase.floor().long() % self.nbins, norm_rgb)

        out = out.unfold(3, self.pool, self.pool)
        out = out.unfold(4, self.pool, self.pool)
        out = out.sum(dim=[-1, -2])

        if self.norm_out:
            out = F.normalize(out, p=2, dim=2)
        if out.shape[1] == 1: # single channel for SAR images
            out = out.squeeze(1)
        
        out = nn.functional.interpolate(out, hw, mode='bilinear')

        return out
    

class Grad_edge(nn.Module):
    def __init__(self, kensize=5,):
        super(Grad_edge, self).__init__()
        self.k = kensize
        def creat_gauss_kernel(r=1):
            M_13 = np.concatenate([np.ones([r+1, 2*r+1]), np.zeros([r, 2*r+1])], axis=0)
            M_23 = np.concatenate([np.zeros([r, 2 * r + 1]), np.ones([r+1, 2 * r + 1])], axis=0)

            M_11 = np.concatenate([np.ones([2*r+1, r+1]), np.zeros([2*r+1, r])], axis=1)
            M_21 = np.concatenate([np.zeros([2 * r + 1, r]), np.ones([2 * r + 1, r+1])], axis=1)
            return torch.from_numpy((M_13)).float(), torch.from_numpy((M_23)).float(), torch.from_numpy((M_11)).float(), torch.from_numpy((M_21)).float()
        M13, M23, M11, M21 = creat_gauss_kernel(self.k)
        weight_x1 = M11.view(1, 1, self.k*2+1, self.k*2+1)
        weight_x2 = M21.view(1, 1, self.k*2+1, self.k*2+1)
        weight_y1 = M13.view(1, 1, self.k*2+1, self.k*2+1)
        weight_y2 = M23.view(1, 1, self.k*2+1, self.k*2+1)
        self.register_buffer("weight_x1", weight_x1)
        self.register_buffer("weight_x2", weight_x2)
        self.register_buffer("weight_y1", weight_y1)
        self.register_buffer("weight_y2", weight_y2)

    @torch.no_grad()
    def forward(self, x):
        # input is RGB image with shape [B 3 H W]
        x = F.pad(x, pad=(self.k, self.k, self.k, self.k), mode="reflect") + 1e-2
        gx_1 = F.conv2d(
            x, self.weight_x1, bias=None, stride=1, padding=0, groups=1
        )
        gx_2 = F.conv2d(
            x, self.weight_x2, bias=None, stride=1, padding=0, groups=1
        )
        gy_1 = F.conv2d(
            x, self.weight_y1, bias=None, stride=1, padding=0, groups=1
        )
        gy_2 = F.conv2d(
            x, self.weight_y2, bias=None, stride=1, padding=0, groups=1
        )
        gx_rgb = torch.log((gx_1) / (gx_2))
        gy_rgb = torch.log((gy_1) / (gy_2))
        # norm_rgb = torch.cat([gx_rgb,gy_rgb],dim=1)
        norm_rgb = torch.stack([gx_rgb, gy_rgb], dim=-1).norm(dim=-1)
        # return torch.tensor(norm_rgb.nan_to_num().cpu().numpy().astype(np.uint8), dtype=torch.float, device=gy_rgb.device)
        return norm_rgb.nan_to_num().type(torch.uint8).type(torch.float)



@MODELS.register_module()
class MSFA(BaseModule):
    def __init__(self, backbone, use_sar=True, use_hog=False, use_canny=False, use_wavelet=False, use_haar=False, use_grad_edge=False, backbone2=None, input_size=(800,800), init_cfg=None):
        super().__init__(init_cfg=init_cfg)
        self.use_sar = use_sar
        self.use_hog = use_hog
        self.use_canny = use_canny
        self.use_wavelet = use_wavelet
        self.use_haar = use_haar
        self.use_grad_edge = use_grad_edge
        self.input_size=input_size
        if use_sar and not (use_hog or use_canny or use_wavelet or use_haar or use_grad_edge):
            self.in_channels = 3 
        elif use_sar and (use_hog or use_canny or use_wavelet or use_haar or use_grad_edge):
            self.in_channels = 1
        elif not use_sar:
            self.in_channels = 0
        if use_canny:
            self.in_channels += 6
            self.canny_trans = Canny_layer()
        if use_hog:
            self.in_channels += 9
            self.hog_trans = HOGLayerC(in_channels = 1)
        if use_wavelet:
            self.in_channels += 81
            self.wavelet_trans = Scattering2D(J=2, shape=self.input_size)
        if use_haar:
            self.in_channels += 12
            self.haar_trans = torchhaarfeatures.HaarFeatures2d(kernel_size=(9, 9), stride=1)
        if use_grad_edge:
            self.in_channels += 1
            self.grad_edge_trans = Grad_edge()
        backbone['in_channels'] = self.in_channels
        self.backbone = MODELS.build(backbone)
        self.backbone2 = None
        if backbone2 is not None:
            self.backbone2 = MODELS.build(backbone2)

    def forward(self, x):
        xs = []
        if self.use_sar and not (self.use_hog or self.use_canny or self.use_wavelet or self.use_haar or self.use_grad_edge):
            return self.backbone(x)
        x_ = x.mean(1,keepdim=True)
        with torch.no_grad():
            if self.use_sar and (self.use_hog or self.use_canny or self.use_wavelet or self.use_haar or self.use_grad_edge):
                xs.append(x_)
            if self.use_canny:
                xs.append(torch.cat(self.canny_trans(x_),1)) 
            if self.use_hog:
                xs.append(self.hog_trans(x_))
            if self.use_wavelet:
                out = nn.functional.interpolate(self.wavelet_trans(x_).squeeze(1), self.input_size, mode='bilinear')
                xs.append(out)
            if self.use_haar:
                xs.append(self.haar_trans(x_))
            if self.use_grad_edge:
                xs.append(self.grad_edge_trans(x_))
            x = torch.cat(xs,1)
        x = self.backbone(x)
        if self.backbone2 is not None:
            x2 = self.backbone2(x)
            for i in range(len(x)):
                x[i] = x[i] + x2[i]
        return x


    def init_weights(self):
        super(MSFA, self).init_weights()


