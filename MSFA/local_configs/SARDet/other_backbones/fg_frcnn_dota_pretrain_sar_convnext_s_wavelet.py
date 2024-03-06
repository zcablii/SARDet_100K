_base_ = [
    '../../../configs/_base_/models/faster-rcnn_r50_fpn.py', 
    '../../../configs/_base_/datasets/SARDet_100k.py', # sar_detection   sar_objectness
    '../../../configs/_base_/schedules/schedule_1x.py', '../../../configs/_base_/default_runtime.py'
]# model settings
num_class = 6
# model settings
model = dict(
    init_cfg=dict(type='Pretrained', checkpoint='work_dirs/pretrain_frcnn_dota_convnext_s_sar_wavelet/epoch_12.pth'),
    
    backbone=dict(
        _delete_ = True,
        type='MSFA',
        use_sar=True, 
        use_wavelet=True,
        backbone=dict(
            type='ConvNeXt',
            depths=[3, 3, 27, 3], 
            dims=[96, 192, 384, 768], 
            drop_path_rate=0.4,
            layer_scale_init_value=1e-6,
            out_indices=[0, 1, 2, 3]
        ),
    ), 
    neck=dict(
        type='FPN',
        in_channels=[96, 192, 384, 768],
        out_channels=256,
        num_outs=5),
    roi_head=dict(
        bbox_head=dict(
            num_classes=num_class,)),
)


optim_wrapper = dict(
    optimizer=dict(
        _delete_=True,
        betas=(
            0.9,
            0.999,
        ), lr=0.0001, type='AdamW', weight_decay=0.05),
    type='OptimWrapper')

# optim_wrapper = dict(
#     type='OptimWrapper',
#     optimizer=dict(type='SGD', lr=0.02, momentum=0.9, weight_decay=0.0001))
