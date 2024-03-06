_base_ = [
    '../../../configs/_base_/models/faster-rcnn_r50_fpn.py', 
    '../../../configs/_base_/datasets/SARDet_100k.py', # sar_detection   sar_objectness
    '../../../configs/_base_/schedules/schedule_1x.py', '../../../configs/_base_/default_runtime.py'
]# model settings
num_class = 6
# model settings
model = dict(
    init_cfg=dict(type='Pretrained', checkpoint='work_dirs/pretrain_frcnn_dota_van_t_sar_wavelet/epoch_12.pth'),
    
    backbone=dict(
        _delete_ = True,
        type='MSFA',
        use_sar=True, 
        use_wavelet=True,
        backbone=dict(
            type='VAN',
            embed_dims=[32, 64, 160, 256],
            drop_rate=0.1,
            drop_path_rate=0.1,
            depths=[3, 3, 5, 2],
            norm_cfg=dict(type='SyncBN', requires_grad=True)),
    ), 
    neck=dict(
        type='FPN',
        in_channels=[32, 64, 160, 256],
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
