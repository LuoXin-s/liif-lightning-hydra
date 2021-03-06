import os
from enum import Enum
from typing import Callable, Optional
from PIL import Image

import numpy as np

import torch
from torch.utils.data import Dataset

from ..utils.transforms import ToCoordColorPair

class ImplicitImageDataset(Dataset):
    """Example dataset class for loading images from folder."""

    def __init__(self, dataset: Dataset, sample_q = None):
        self.dataset = dataset
        self.sample_q = sample_q

    def __getitem__(self, idx):
        image = self.dataset[idx]

        if isinstance(image, tuple):
            lr, hr = image
        else:
            lr = hr = image

        hr_coord, hr_rgb = ToCoordColorPair()(hr)
        
        if self.sample_q is not None:
            sample_lst = np.random.choice(
                len(hr_coord), self.sample_q, replace=False)
            hr_coord = hr_coord[sample_lst]
            hr_rgb = hr_rgb[sample_lst]

        gt_size = torch.ones(2).int()
        gt_size[0] = hr.shape[-2]
        gt_size[1] = hr.shape[-1]

        return {
                'inp': lr,
                # 'hr': hr,
                'coord': hr_coord,
                'gt': hr_rgb,
                'gt_size': gt_size
                }

    def __len__(self):
        return len(self.dataset)