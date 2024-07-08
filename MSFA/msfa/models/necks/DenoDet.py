# Copyright (c) OpenMMLab. All rights reserved.
from typing import List, Tuple, Union

import torch.nn as nn
import torch.nn.functional as F
from mmcv.cnn import ConvModule
from mmengine.model import BaseModule
from torch import Tensor

from mmdet.registry import MODELS
from mmdet.utils import ConfigType, MultiConfig, OptConfigType
import torch
import math

class DCT2DSpatialTransformLayer(nn.Module):
    def __init__(self, height, width):
        super(DCT2DSpatialTransformLayer, self).__init__()
        self.dct_x = DCT2DSpatialTransformLayer_x(width)
        self.dct_y = DCT2DSpatialTransformLayer_y(height)

    def forward(self, x):
        # x = x.double()
        y = self.dct_x(x)
        y = self.dct_y(y)

        return y


class IDCT2DSpatialTransformLayer(nn.Module):
    def __init__(self, height, width):
        super(IDCT2DSpatialTransformLayer, self).__init__()
        self.idct_x = IDCT2DSpatialTransformLayer_x(width)
        self.idct_y = IDCT2DSpatialTransformLayer_y(height)

    def forward(self, x):
        y = self.idct_x(x)
        y = self.idct_y(y)
        # y = y.float()

        return y


class FastDCT2DSpatialTransformLayer(nn.Module):
    def __init__(self, height, width):
        super(FastDCT2DSpatialTransformLayer, self).__init__()
        self.dct_x = FastDCT2DSpatialTransformLayer_x(width)
        self.dct_y = FastDCT2DSpatialTransformLayer_y(height)

    def forward(self, x):
        # x = x.double()
        # b,c,h,w
        y = self.dct_x(x.permute(0, 3, 2, 1))  # channel 和 width 互换 b,w,h,c
        y = self.dct_y(y.permute(0, 2, 1, 3))  # width 和 height 互换 b,h,w,c
        y = y.permute(0, 3, 1, 2)  # 复原 b,c,h,w

        return y


class FastIDCT2DSpatialTransformLayer(nn.Module):
    def __init__(self, height, width):
        super(FastIDCT2DSpatialTransformLayer, self).__init__()
        self.idct_x = FastIDCT2DSpatialTransformLayer_x(width)
        self.idct_y = FastIDCT2DSpatialTransformLayer_y(height)

    def forward(self, x):
        # b,c,h,w
        y = self.idct_x(x.permute(0, 3, 2, 1))  # channel 和 width 互换 b,w,h,c
        y = self.idct_y(y.permute(0, 2, 1, 3))  # width 和 height 互换 b,h,w,c
        y = y.permute(0, 3, 1, 2)  # 复原 b,c,h,w
        # y = y.float()

        return y


class DCT2DSpatialTransformLayer_x(nn.Module):
    def __init__(self, width):
        super(DCT2DSpatialTransformLayer_x, self).__init__()
        self.register_buffer('weight', self.get_dct_filter(width))

    def get_dct_filter(self, width):
        # dct_filter = torch.zeros(width, width, dtype=torch.float64)
        dct_filter = torch.zeros(width, width)
        for v in range(width):
            for j in range(width):
                DCT_base_x = math.cos(math.pi * (0.5 + j) * v / width) / math.sqrt(width)
                if v != 0:
                    DCT_base_x = DCT_base_x * math.sqrt(2)
                dct_filter[v, j] = DCT_base_x

        return dct_filter

    def forward(self, x):
        dct_components = []

        for weight in self.weight.split(1, dim=0):
            dct_component = x * weight.view(1, 1, 1, x.shape[3]).expand_as(x)
            dct_components.append(dct_component.sum(3).unsqueeze(3))

        result = torch.concat(dct_components, dim=3)

        return result


class FastDCT2DSpatialTransformLayer_x(nn.Module):
    def __init__(self, width):
        super(FastDCT2DSpatialTransformLayer_x, self).__init__()
        self.register_buffer('weight', self.get_dct_filter(width))

    def get_dct_filter(self, width):
        # dct_filter = torch.zeros(width, width, dtype=torch.float64)
        dct_filter = torch.zeros(width, width)
        for v in range(width):
            for j in range(width):
                DCT_base_x = math.cos(math.pi * (0.5 + j) * v / width) / math.sqrt(width)
                if v != 0:
                    DCT_base_x = DCT_base_x * math.sqrt(2)
                dct_filter[v, j] = DCT_base_x

        return dct_filter

    def forward(self, input):
        result = F.conv2d(input, self.weight.unsqueeze(2).unsqueeze(3))
        return result


class IDCT2DSpatialTransformLayer_x(nn.Module):
    def __init__(self, width):
        super(IDCT2DSpatialTransformLayer_x, self).__init__()
        self.register_buffer('weight', self.get_dct_filter(width))

    def get_dct_filter(self, width):
        # dct_filter = torch.zeros(width, width, dtype=torch.float64)
        dct_filter = torch.zeros(width, width)
        for v in range(width):
            for j in range(width):
                DCT_base_x = math.cos(math.pi * (0.5 + v) * j / width) / math.sqrt(width)
                if j != 0:
                    DCT_base_x = DCT_base_x * math.sqrt(2)
                dct_filter[v, j] = DCT_base_x

        return dct_filter

    def forward(self, x):
        dct_components = []

        for weight in self.weight.split(1, dim=0):
            dct_component = x * weight.view(1, 1, 1, x.shape[3]).expand_as(x)
            dct_components.append(dct_component.sum(3).unsqueeze(3))

        result = torch.concat(dct_components, dim=3)

        return result


class FastIDCT2DSpatialTransformLayer_x(nn.Module):
    def __init__(self, width):
        super(FastIDCT2DSpatialTransformLayer_x, self).__init__()
        self.register_buffer('weight', self.get_dct_filter(width))

    def get_dct_filter(self, width):
        # dct_filter = torch.zeros(width, width, dtype=torch.float64)
        dct_filter = torch.zeros(width, width)
        for v in range(width):
            for j in range(width):
                DCT_base_x = math.cos(math.pi * (0.5 + v) * j / width) / math.sqrt(width)
                if j != 0:
                    DCT_base_x = DCT_base_x * math.sqrt(2)
                dct_filter[v, j] = DCT_base_x

        return dct_filter

    def forward(self, input):
        result = F.conv2d(input, self.weight.unsqueeze(2).unsqueeze(3))
        return result


class DCT2DSpatialTransformLayer_y(nn.Module):
    def __init__(self, height):
        super(DCT2DSpatialTransformLayer_y, self).__init__()
        self.register_buffer('weight', self.get_dct_filter(height))

    def get_dct_filter(self, height):
        # dct_filter = torch.zeros(height, height, dtype=torch.float64)
        dct_filter = torch.zeros(height, height)
        for k in range(height):
            for i in range(height):
                DCT_base_y = math.cos(math.pi * (0.5 + i) * k / height) / math.sqrt(height)
                if k != 0:
                    DCT_base_y = DCT_base_y * math.sqrt(2)
                dct_filter[k, i] = DCT_base_y

        return dct_filter

    def forward(self, x):
        dct_components = []

        for weight in self.weight.split(1, dim=0):
            dct_component = x * weight.view(1, 1, x.shape[2], 1).expand_as(x)
            dct_components.append(dct_component.sum(2).unsqueeze(2))

        result = torch.concat(dct_components, dim=2)

        return result


class FastDCT2DSpatialTransformLayer_y(nn.Module):
    def __init__(self, height):
        super(FastDCT2DSpatialTransformLayer_y, self).__init__()
        self.register_buffer('weight', self.get_dct_filter(height))

    def get_dct_filter(self, height):
        # dct_filter = torch.zeros(height, height, dtype=torch.float64)
        dct_filter = torch.zeros(height, height)
        for k in range(height):
            for i in range(height):
                DCT_base_y = math.cos(math.pi * (0.5 + i) * k / height) / math.sqrt(height)
                if k != 0:
                    DCT_base_y = DCT_base_y * math.sqrt(2)
                dct_filter[k, i] = DCT_base_y

        return dct_filter

    def forward(self, input):
        result = F.conv2d(input, self.weight.unsqueeze(2).unsqueeze(3))
        return result


class IDCT2DSpatialTransformLayer_y(nn.Module):
    def __init__(self, height):
        super(IDCT2DSpatialTransformLayer_y, self).__init__()
        self.register_buffer('weight', self.get_dct_filter(height))

    def get_dct_filter(self, height):
        # dct_filter = torch.zeros(height, height, dtype=torch.float64)
        dct_filter = torch.zeros(height, height)
        for k in range(height):
            for i in range(height):
                DCT_base_y = math.cos(math.pi * (0.5 + k) * i / height) / math.sqrt(height)
                if i != 0:
                    DCT_base_y = DCT_base_y * math.sqrt(2)
                dct_filter[k, i] = DCT_base_y

        return dct_filter

    def forward(self, x):
        dct_components = []

        for weight in self.weight.split(1, dim=0):
            dct_component = x * weight.view(1, 1, x.shape[2], 1).expand_as(x)
            dct_components.append(dct_component.sum(2).unsqueeze(2))

        result = torch.concat(dct_components, dim=2)

        return result


class FastIDCT2DSpatialTransformLayer_y(nn.Module):
    def __init__(self, height):
        super(FastIDCT2DSpatialTransformLayer_y, self).__init__()
        self.register_buffer('weight', self.get_dct_filter(height))

    def get_dct_filter(self, height):
        # dct_filter = torch.zeros(height, height, dtype=torch.float64)
        dct_filter = torch.zeros(height, height)
        for k in range(height):
            for i in range(height):
                DCT_base_y = math.cos(math.pi * (0.5 + k) * i / height) / math.sqrt(height)
                if i != 0:
                    DCT_base_y = DCT_base_y * math.sqrt(2)
                dct_filter[k, i] = DCT_base_y

        return dct_filter

    def forward(self, input):
        result = F.conv2d(input, self.weight.unsqueeze(2).unsqueeze(3))
        return result

class GroupAttentionlayer(nn.Module):
    def __init__(self, channel, groups):
        super(GroupAttentionlayer, self).__init__()
        self.fc1 = nn.Conv1d(channel, channel, 1, groups=groups)
        self.relu = nn.ReLU()
        self.fc2 = nn.Conv1d(channel, channel, 1, groups=groups)
        self.sig = nn.Sigmoid()
        
    def forward(self, x):
        b,c,h,w = x.size()
        y = (x.mean(1) + x.max(1)[0]).view(b,h*w,1)
        y = self.fc1(y)
        y = self.relu(y)
        y = self.fc2(y)
        y = self.sig(y).view(b, 1, h, w).expand_as(x)
        return y * x

class SelectBlock(nn.Conv1d):
    def __init__(self, channels, branches):
        super(SelectBlock, self).__init__(channels,branches,1, bias=False)
        self.eps = 1e-15
        self.branches = branches
        self.softmax = nn.Softmax(1)

    def forward(self, origin_tensor, branch_tensors):
        branch_offsets = super().forward(origin_tensor)
        branch_offsets = branch_offsets - branch_offsets.min(1,keepdim=True)[0] + self.eps
        branch_offsets = branch_offsets / branch_offsets.max(1,keepdim=True)[0] * (branch_tensors.size(1) - 1)

        b,c,h,w = branch_tensors.size()
        y = branch_tensors.clone()
        branch_min = (branch_offsets.floor().long()).view(b, self.branches, 1, 1).expand(b, self.branches, h, w)
        branch_max = branch_offsets.ceil().long().view(b, self.branches, 1, 1).expand(b, self.branches, h, w)
        min_offset = (branch_offsets - branch_offsets.floor()).view(b, self.branches, 1, 1).expand(b,self.branches, h, w)
        max_offset = (branch_offsets.ceil() - branch_offsets).view(b, self.branches, 1, 1).expand(b,self.branches, h, w)
        offset = self.softmax(torch.cat([min_offset,max_offset],dim=1)).split(self.branches,dim=1)
        min_offset = offset[0]
        max_offset = offset[1]
        for i in range(self.branches):
            y[:,i,...] = (torch.gather(branch_tensors, 1, branch_min[:,i,...].unsqueeze(1)).squeeze(1) * min_offset[:,i,...]
                          + torch.gather(branch_tensors, 1, branch_max[:,i,...].unsqueeze(1)).squeeze(1) * max_offset[:,i,...])

        return y.sum(1)

class SelectGroupFClayer(nn.Module):
    def __init__(self, channel):
        super(SelectGroupFClayer, self).__init__()
        self.fc1 = nn.Sequential(
            nn.Conv1d(channel, channel, 1, groups=2),
            nn.ReLU(),
        )
        self.fc2 = nn.Sequential(
            nn.Conv1d(channel, channel, 1, groups=4),
            nn.ReLU(),
        )
        self.fc3 = nn.Sequential(
            nn.Conv1d(channel, channel, 1, groups=8),
            nn.ReLU(),
        )
        self.fc4 = nn.Sequential(
            nn.Conv1d(channel, channel, 1, groups=16),
            nn.ReLU(),
        )
        self.select1 = SelectBlock(channel,4)
        
        self.fc5 = nn.Sequential(
            nn.Conv1d(channel, channel, 1, groups=2),
            nn.Sigmoid(),
        )
        self.fc6 = nn.Sequential(
            nn.Conv1d(channel, channel, 1, groups=4),
            nn.Sigmoid(),
        )
        self.fc7 = nn.Sequential(
            nn.Conv1d(channel, channel, 1, groups=8),
            nn.Sigmoid(),
        )
        self.fc8 = nn.Sequential(
            nn.Conv1d(channel, channel, 1, groups=16),
            nn.Sigmoid(),
        )
        self.select2 = SelectBlock(channel,4)

        
    def forward(self, x):
        b,c,h,w = x.size()
        y = x.clone().reshape(b,h*w,c)
        y = y.mean(2, keepdim=True) + y.max(2, keepdim=True)[0]

        y1 = self.fc1(y).unsqueeze(1)
        y2 = self.fc2(y).unsqueeze(1)
        y3 = self.fc3(y).unsqueeze(1)
        y4 = self.fc4(y).unsqueeze(1)
        temp = self.select1(y, torch.cat([y1,y2,y3,y4],dim=1)) 
        
        y5 = self.fc5(temp).unsqueeze(1)
        y6 = self.fc6(temp).unsqueeze(1)
        y7 = self.fc7(temp).unsqueeze(1)
        y8 = self.fc8(temp).unsqueeze(1)
        att = self.select2(temp, torch.cat([y5,y6,y7,y8],dim=1)) 
        
        return att.view(b,1,h,w).expand_as(x) * x

class SpatialFCAttentionlayer(nn.Module):
    def __init__(self, channel, reduction):
        super(SpatialFCAttentionlayer, self).__init__()
        self.fc1 = nn.Linear(channel, channel // reduction)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(channel // reduction, channel)
        self.sig = nn.Sigmoid()
        
    def forward(self, x):
        b,c,h,w = x.size()
        y = (x.mean(1) + x.max(1)[0]).view(b,h*w)
        y = self.fc1(y)
        y = self.relu(y)
        y = self.fc2(y)
        y = self.sig(y)
        y = y.view(b, 1, h, w).expand_as(x)
        return y * x

class groupspatiallayer(nn.Module):
    def __init__(self, channel, groups):
        super(groupspatiallayer, self).__init__()
        self.fc1 = nn.Conv1d(channel, channel, 1, groups=groups)
        self.sig = nn.Sigmoid()
        
    def forward(self, x):
        b,c,h,w = x.size()
        y = (x.mean(1) + x.max(1)[0]).view(b,h*w,1)
        y = self.fc1(y)
        y = self.sig(y)
        y = y.view(b, 1, h, w).expand_as(x)
        return y * x
    
class SElayer(nn.Module):
    def __init__(self, channel, reduction):
        super(SElayer, self).__init__()
        self.fc1 = nn.Linear(channel, channel // reduction)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(channel // reduction, channel)
        self.sig = nn.Sigmoid()
    def forward(self, x):
        b,c,h,w = x.size()
        y = x.mean(dim=[2,3])
        y = self.fc1(y)
        y = self.relu(y)
        y = self.fc2(y)
        y = self.sig(y)
        x = y.unsqueeze(2).unsqueeze(3).expand_as(x) * x
        return x

    
@MODELS.register_module()
class FrequencySpatialFPN(BaseModule):
    r"""Feature Pyramid Network.

    This is an implementation of paper `Feature Pyramid Networks for Object
    Detection <https://arxiv.org/abs/1612.03144>`_.

    Args:
        in_channels (list[int]): Number of input channels per scale.
        out_channels (int): Number of output channels (used at each scale).
        num_outs (int): Number of output scales.
        start_level (int): Index of the start input backbone level used to
            build the feature pyramid. Defaults to 0.
        end_level (int): Index of the end input backbone level (exclusive) to
            build the feature pyramid. Defaults to -1, which means the
            last level.
        add_extra_convs (bool | str): If bool, it decides whether to add conv
            layers on top of the original feature maps. Defaults to False.
            If True, it is equivalent to `add_extra_convs='on_input'`.
            If str, it specifies the source feature map of the extra convs.
            Only the following options are allowed

            - 'on_input': Last feat map of neck inputs (i.e. backbone feature).
            - 'on_lateral': Last feature map after lateral convs.
            - 'on_output': The last output feature map after fpn convs.
        relu_before_extra_convs (bool): Whether to apply relu before the extra
            conv. Defaults to False.
        no_norm_on_lateral (bool): Whether to apply norm on lateral.
            Defaults to False.
        conv_cfg (:obj:`ConfigDict` or dict, optional): Config dict for
            convolution layer. Defaults to None.
        norm_cfg (:obj:`ConfigDict` or dict, optional): Config dict for
            normalization layer. Defaults to None.
        act_cfg (:obj:`ConfigDict` or dict, optional): Config dict for
            activation layer in ConvModule. Defaults to None.
        upsample_cfg (:obj:`ConfigDict` or dict, optional): Config dict
            for interpolate layer. Defaults to dict(mode='nearest').
        init_cfg (:obj:`ConfigDict` or dict or list[:obj:`ConfigDict` or \
            dict]): Initialization config dict.

    Example:
        >>> import torch
        >>> in_channels = [2, 3, 5, 7]
        >>> scales = [340, 170, 84, 43]
        >>> inputs = [torch.rand(1, c, s, s)
        ...           for c, s in zip(in_channels, scales)]
        >>> self = FPN(in_channels, 11, len(in_channels)).eval()
        >>> outputs = self.forward(inputs)
        >>> for i in range(len(outputs)):
        ...     print(f'outputs[{i}].shape = {outputs[i].shape}')
        outputs[0].shape = torch.Size([1, 11, 340, 340])
        outputs[1].shape = torch.Size([1, 11, 170, 170])
        outputs[2].shape = torch.Size([1, 11, 84, 84])
        outputs[3].shape = torch.Size([1, 11, 43, 43])
    """

    def __init__(
        self,
        in_channels: List[int],
        out_channels: int,
        num_outs: int,
        start_level: int = 0,
        end_level: int = -1,
        add_extra_convs: Union[bool, str] = False,
        relu_before_extra_convs: bool = False,
        no_norm_on_lateral: bool = False,
        conv_cfg: OptConfigType = None,
        norm_cfg: OptConfigType = None,
        act_cfg: OptConfigType = None,
        upsample_cfg: ConfigType = dict(mode='nearest'),
        init_cfg: MultiConfig = dict(
            type='Xavier', layer='Conv2d', distribution='uniform')
    ) -> None:
        super().__init__(init_cfg=init_cfg)
        assert isinstance(in_channels, list)
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.num_ins = len(in_channels)
        self.num_outs = num_outs
        self.relu_before_extra_convs = relu_before_extra_convs
        self.no_norm_on_lateral = no_norm_on_lateral
        self.fp16_enabled = False
        self.upsample_cfg = upsample_cfg.copy()

        if end_level == -1 or end_level == self.num_ins - 1:
            self.backbone_end_level = self.num_ins
            assert num_outs >= self.num_ins - start_level
        else:
            # if end_level is not the last level, no extra level is allowed
            self.backbone_end_level = end_level + 1
            assert end_level < self.num_ins
            assert num_outs == end_level - start_level + 1
        self.start_level = start_level
        self.end_level = end_level
        self.add_extra_convs = add_extra_convs
        assert isinstance(add_extra_convs, (str, bool))
        if isinstance(add_extra_convs, str):
            # Extra_convs_source choices: 'on_input', 'on_lateral', 'on_output'
            assert add_extra_convs in ('on_input', 'on_lateral', 'on_output')
        elif add_extra_convs:  # True
            self.add_extra_convs = 'on_input'

        self.lateral_convs = nn.ModuleList()
        self.fpn_convs = nn.ModuleList()

        for i in range(self.start_level, self.backbone_end_level):
            l_conv = ConvModule(
                in_channels[i],
                out_channels,
                1,
                conv_cfg=conv_cfg,
                norm_cfg=norm_cfg if not self.no_norm_on_lateral else None,
                act_cfg=act_cfg,
                inplace=False)
            fpn_conv = ConvModule(
                out_channels,
                out_channels,
                3,
                padding=1,
                conv_cfg=conv_cfg,
                norm_cfg=norm_cfg,
                act_cfg=act_cfg,
                inplace=False)

            self.lateral_convs.append(l_conv)
            self.fpn_convs.append(fpn_conv)

        # add extra conv layers (e.g., RetinaNet)
        extra_levels = num_outs - self.backbone_end_level + self.start_level
        if self.add_extra_convs and extra_levels >= 1:
            for i in range(extra_levels):
                if i == 0 and self.add_extra_convs == 'on_input':
                    in_channels = self.in_channels[self.backbone_end_level - 1]
                else:
                    in_channels = out_channels
                extra_fpn_conv = ConvModule(
                    in_channels,
                    out_channels,
                    3,
                    stride=2,
                    padding=1,
                    conv_cfg=conv_cfg,
                    norm_cfg=norm_cfg,
                    act_cfg=act_cfg,
                    inplace=False)
                self.fpn_convs.append(extra_fpn_conv)
        
        """
        self.DCTDenoAttention0 = nn.Sequential(
            DCT2DSpatialTransformLayer(32, 32),
            # SElayer(256,16),
            # GroupAttentionlayer(32 * 32, 16),
            # SelectGroupFClayer(32*32),
            # SpatialFCAttentionlayer(32*32, 16),
            IDCT2DSpatialTransformLayer(32, 32)
        )
        self.DCTDenoAttention1 = nn.Sequential(
            DCT2DSpatialTransformLayer(16, 16),
            # SElayer(256,16),
            # GroupAttentionlayer(16 * 16, 16),
            # SelectGroupFClayer(16 * 16),
            # SpatialFCAttentionlayer(16*16, 16),
            IDCT2DSpatialTransformLayer(16, 16),
        )
        """
        
        
        self.DCTDenoAttention0 = nn.Sequential(
            FastDCT2DSpatialTransformLayer(128, 128),
            # SElayer(256,16),
            # GroupAttentionlayer(64 * 64, 32),
            SelectGroupFClayer(128*128),
            # SpatialFCAttentionlayer(64*64, 16),
            FastIDCT2DSpatialTransformLayer(128, 128)
        )
        self.DCTDenoAttention1 = nn.Sequential(
            FastDCT2DSpatialTransformLayer(64, 64),
            # SElayer(256,16),
            # GroupAttentionlayer(32 * 32, 32),
            SelectGroupFClayer(64 * 64),
            # SpatialFCAttentionlayer(32*32, 16),
            FastIDCT2DSpatialTransformLayer(64, 64)
        )
        
        self.DCTDenoAttention = [self.DCTDenoAttention0, self.DCTDenoAttention1]

    def forward(self, inputs: Tuple[Tensor]) -> tuple:
        """Forward function.

        Args:
            inputs (tuple[Tensor]): Features from the upstream network, each
                is a 4D-tensor.

        Returns:
            tuple: Feature maps, each is a 4D-tensor.
        """
        assert len(inputs) == len(self.in_channels)


        # build laterals
        laterals = [
            lateral_conv(inputs[i + self.start_level])
            for i, lateral_conv in enumerate(self.lateral_convs)
        ]

        # build top-down path
        used_backbone_levels = len(laterals)
        for i in range(used_backbone_levels - 1, 0, -1):
            # In some cases, fixing `scale factor` (e.g. 2) is preferred, but
            #  it cannot co-exist with `size` in `F.interpolate`.
            if 'scale_factor' in self.upsample_cfg:
                # fix runtime error of "+=" inplace operation in PyTorch 1.10
                laterals[i - 1] = laterals[i - 1] + F.interpolate(
                    laterals[i], **self.upsample_cfg)
            else:
                prev_shape = laterals[i - 1].shape[2:]
                laterals[i - 1] = laterals[i - 1] + F.interpolate(
                    laterals[i], size=prev_shape, **self.upsample_cfg)
                laterals[i - 1] = self.DCTDenoAttention[i - 1](laterals[i - 1])

        # build outputs
        # part 1: from original levels
        outs = [
            self.fpn_convs[i](laterals[i]) for i in range(used_backbone_levels)
        ]
        # part 2: add extra levels
        if self.num_outs > len(outs):
            # use max pool to get more levels on top of outputs
            # (e.g., Faster R-CNN, Mask R-CNN)
            if not self.add_extra_convs:
                for i in range(self.num_outs - used_backbone_levels):
                    outs.append(F.max_pool2d(outs[-1], 1, stride=2))
            # add conv layers on top of original feature maps (RetinaNet)
            else:
                if self.add_extra_convs == 'on_input':
                    extra_source = inputs[self.backbone_end_level - 1]
                elif self.add_extra_convs == 'on_lateral':
                    extra_source = laterals[-1]
                elif self.add_extra_convs == 'on_output':
                    extra_source = outs[-1]
                else:
                    raise NotImplementedError
                outs.append(self.fpn_convs[used_backbone_levels](extra_source))
                for i in range(used_backbone_levels + 1, self.num_outs):
                    if self.relu_before_extra_convs:
                        outs.append(self.fpn_convs[i](F.relu(outs[-1])))
                    else:
                        outs.append(self.fpn_convs[i](outs[-1]))
        return tuple(outs)