#!/usr/bin/env python3

from calibration_utility import load_coefficients
import cv2


def undistort_camera(frame):
    # Load coefficients
    mtx, dist = load_coefficients('calibration_chessboard.yml')
    undistorted_frame = cv2.undistort(frame, mtx, dist, None, None)
    return undistorted_frame
