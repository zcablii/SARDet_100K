_base_ = [
    '../../../configs/_base_/models/retinanet_r50_fpn.py',
    '../../../configs/_base_/datasets/dota.py',
    '../../../configs/_base_/schedules/schedule_1x.py', '../../../configs/_base_/default_runtime.py'
]
num_classes = 15


model = dict(
    type='RetinaNet',
    backbone=dict(
        _delete_ = True,
        type='MSFA',
        use_sar=True,
        use_wavelet=True,
        input_size = (1024,1024), 
        backbone=dict(
            type='ResNet',
            depth=50,
            num_stages=4,
            out_indices=(0, 1, 2, 3),
            frozen_stages=1,
            norm_cfg=dict(type='BN', requires_grad=True),
            norm_eval=True,
            style='pytorch',
            init_cfg=None
        ),
        init_cfg=dict(type='Pretrained', prefix='backbone', checkpoint='/root/siton-gpfs-archive/yuxuanli/mmpretrain/work_dirs/r50_sar_wavelet/epoch_100.pth'),
    ),
    
    bbox_head=dict(
        num_classes=num_classes,)
)
# optimizer

test_cfg=None
find_unused_parameters = True
optim_wrapper = dict(
    optimizer=dict(
        _delete_=True,
        betas=(
            0.9,
            0.999,
        ), lr=0.0001, type='AdamW', weight_decay=0.05),
    type='OptimWrapper')
