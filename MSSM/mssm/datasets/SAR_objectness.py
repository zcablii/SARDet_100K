# Copyright (c) OpenMMLab. All rights reserved.
import copy
import os.path as osp
from typing import List, Union

from mmengine.fileio import get_local_path
from mmdet.registry import DATASETS
from mmdet.datasets.api_wrappers import COCO
from .SAR_Det import SAR_Det_Finegrained_Dataset


@DATASETS.register_module()
class SAR_Objectness_Dataset(SAR_Det_Finegrained_Dataset):
    """Dataset for COCO."""

    METAINFO = {
        'classes': (),
        # palette is a list of color tuples, which is used for visualization.
        'palette':
        [ (0, 182, 0)]
    }