# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 15:43:29 2017

@author: zhaoy
"""
import numpy as np
import cv2

from scipy.linalg import lstsq
from scipy.ndimage import geometric_transform#, map_coordinates

dft_normalized_5points = [
        [ 30.29459953,  51.69630051],
        [ 65.53179932,  51.50139999],
        [ 48.02519989,  71.73660278],
        [ 33.54930115,  92.3655014 ],
        [ 62.72990036,  92.20410156]
    ];

dft_crop_size = (96, 112)

def _get_transform_matrix(src_pts, dst_pts):
    tfm = np.float32([[1, 0, 0], [0, 1, 0]])
    n_pts = src_pts.shape[0]
    ones = np.ones((n_pts, 1), src_pts.dtype)
    src_pts_ = np.hstack([src_pts, ones])
    dst_pts_ = np.hstack([dst_pts, ones])

#    print('src_pts_:\n' + str(src_pts_))
#    print('dst_pts_:\n' + str(dst_pts_))

    A, res, rank, s = np.linalg.lstsq(src_pts_, dst_pts_)

#    print('np.linalg.lstsq return A: \n' + str(A))
#    print('np.linalg.lstsq return res: \n' + str(res))
#    print('np.linalg.lstsq return rank: \n' + str(rank))
#    print('np.linalg.lstsq return s: \n' + str(s))

    if rank==3:
        tfm = np.float32([
                [A[0,0], A[1,0], A[2, 0]],
                [A[0,1], A[1,1], A[2, 1]]
            ])
    elif rank==2:
        tfm = np.float32([
            [A[0,0], A[1,0], 0],
            [A[0,1], A[1,1], 0]
            ])

    return tfm


def warp_and_crop_face(src_img, facial_pts, normalized_pts=dft_normalized_5points, crop_size=dft_crop_size):
    pts_dst = np.float32(normalized_pts)
    if pts_dst.shape[0]==2:
        pts_dst = pts_dst.transpose()

    pts_src = np.float32(facial_pts)
    if pts_src.shape[0]==2:
        pts_src = pts_src.transpose()

#    tfm = cv2.getAffineTransform(pts_src[0:3], pts_dst[0:3])
#    print('cv2.getAffineTransform returns tfm=\n' + str(tfm))
#    print('type(tfm):' + str(type(tfm)))
#    print('tfm.dtype:' + str(tfm.dtype))

    tfm = _get_transform_matrix(pts_src, pts_dst)
#    print('_get_transform_matrix returns tfm=\n' + str(tfm))
#    print('type(tfm):' + str(type(tfm)))
#    print('tfm.dtype:' + str(tfm.dtype))

    dst_img = cv2.warpAffine(src_img, tfm, (crop_size[0], crop_size[1]))

    return dst_img
