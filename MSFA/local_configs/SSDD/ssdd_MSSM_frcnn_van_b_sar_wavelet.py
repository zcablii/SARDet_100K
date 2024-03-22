_base_ = [
    '../../configs/_base_/models/faster-rcnn_r50_fpn.py', 
    '../../configs/_base_/datasets/SSDD.py',
    '../../configs/_base_/schedules/schedule_1x.py', '../../configs/_base_/default_runtime.py'
]# model settings

num_class = 1
model = dict(
    init_cfg=dict(type='Pretrained', checkpoint='work_dirs/pretrain_frcnn_dota_van_b_sar_wavelet/epoch_12.pth'),
    
    backbone=dict(
        _delete_ = True,
        type='MSFA',
        use_sar=True, 
        use_wavelet=True,
        # input_size = (512,512), 
        backbone=dict(
            type='VAN',
            embed_dims=[64, 128, 320, 512],
            drop_rate=0.1,
            drop_path_rate=0.1,
            depths=[3, 3, 12, 3],
            norm_cfg=dict(type='SyncBN', requires_grad=True)),
    ), 
    neck=dict(
        type='FPN',
        in_channels=[64, 128, 320, 512],
        out_channels=256,
        num_outs=5),
    roi_head=dict(
        bbox_head=dict(
            num_classes=num_class,)),
)


param_scheduler = [
    dict(
        type='LinearLR', start_factor=0.001, by_epoch=False, begin=0, end=30),
    dict(
        type='MultiStepLR',
        begin=0,
        end=12,
        by_epoch=True,
        milestones=[8, 11],
        gamma=0.1)
]


optim_wrapper = dict(
    optimizer=dict(
        _delete_=True,
        betas=(
            0.9,
            0.999,
        ), lr=0.00025, type='AdamW', weight_decay=0.05),
    type='OptimWrapper')


train_dataloader = dict(
    batch_size=4,
    num_workers=4,)