_base_ = [
    '../../../configs/_base_/datasets/dota.py',
    '../../../configs/_base_/schedules/schedule_1x.py', '../../../configs/_base_/default_runtime.py'
]
num_classes = 6
# model settings
model = dict(
    type='FCOS',
    init_cfg=dict(type='Pretrained', checkpoint='work_dirs/pretrain_fcos_r50_sar_wavelet/epoch_12.pth'),
    
    data_preprocessor=dict(
        type='DetDataPreprocessor',
        mean=[123.675, 116.28, 103.53],
        std=[58.395, 57.12, 57.375],
        bgr_to_rgb=True,
        pad_size_divisor=1),
    backbone=dict(
        _delete_ = True,
        type='MSFA',
        use_sar=True, 
        use_wavelet=True, 
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
    ),
    neck=dict(
        type='FPN',
        in_channels=[256, 512, 1024, 2048],
        out_channels=256,
        start_level=1,
        add_extra_convs='on_output',  # use P5
        num_outs=5,
        relu_before_extra_convs=True),
    bbox_head=dict(
        type='FCOSHead',
        num_classes=num_classes,
        in_channels=256,
        stacked_convs=4,
        feat_channels=256,
        strides=[8, 16, 32, 64, 128],
        loss_cls=dict(
            type='FocalLoss',
            use_sigmoid=True,
            gamma=2.0,
            alpha=0.25,
            loss_weight=1.0),
        loss_bbox=dict(type='IoULoss', loss_weight=1.0),
        loss_centerness=dict(
            type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0)),
    # testing settings
    test_cfg=None)


find_unused_parameters = True








# _base_ = [
#     '../../../configs/_base_/datasets/sar_det_finegrained.py',
#     '../../../configs/_base_/schedules/schedule_1x.py', '../../../configs/_base_/default_runtime.py'
# ]
# num_classes = 6
# # model settings
# model = dict(
#     type='FCOS',
#     init_cfg=dict(type='Pretrained', checkpoint='work_dirs/pretrain_fcos_r50_sar/epoch_12.pth'),
#     data_preprocessor=dict(
#         type='DetDataPreprocessor',
#         mean=[123.675, 116.28, 103.53],
#         std=[58.395, 57.12, 57.375],
#         bgr_to_rgb=True,
#         pad_size_divisor=1),

#     backbone=dict(
#         # _delete_ = True,
#         type='MSFA',
#         use_sar=True,
#         use_haar=True,
#         backbone=dict(
#             type='ResNet',
#             depth=50,
#             num_stages=4,
#             out_indices=(0, 1, 2, 3),
#             frozen_stages=1,
#             norm_cfg=dict(type='BN', requires_grad=True),
#             norm_eval=True,
#             style='pytorch',
#             init_cfg=None
#         ),
#         init_cfg=None,
#     ), 
#     neck=dict(
#         type='FPN',
#         in_channels=[256, 512, 1024, 2048],
#         out_channels=256,
#         start_level=1,
#         add_extra_convs='on_output',  # use P5
#         num_outs=5,
#         relu_before_extra_convs=True),
#     bbox_head=dict(
#         type='FCOSHead',
#         num_classes=num_classes,
#         in_channels=256,
#         stacked_convs=4,
#         feat_channels=256,
#         strides=[8, 16, 32, 64, 128],
#         loss_cls=dict(
#             type='FocalLoss',
#             use_sigmoid=True,
#             gamma=2.0,
#             alpha=0.25,
#             loss_weight=1.0),
#         loss_bbox=dict(type='IoULoss', loss_weight=1.0),
#         loss_centerness=dict(
#             type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0)),
#     # testing settings
#     test_cfg=dict(
#         nms_pre=1000,
#         min_bbox_size=0,
#         score_thr=0.05,
#         nms=dict(type='nms', iou_threshold=0.5),
#         max_per_img=100))


# find_unused_parameters = True
# optim_wrapper = dict(
#     optimizer=dict(
#         _delete_=True,
#         betas=(
#             0.9,
#             0.999,
#         ), lr=0.0001, type='AdamW', weight_decay=0.05),
#     type='OptimWrapper')