import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

from stereovision.calibration import StereoCalibrator
from stereovision.calibration import StereoCalibration
from stereovision.exceptions import ChessboardNotFoundError

"""
# Load image to rectify 
imgLeft = cv.imread('./images/left3.jpeg', cv.IMREAD_GRAYSCALE)
imgRight = cv.imread('./images/right3.jpeg', cv.IMREAD_GRAYSCALE)


# Load the calibration results
calibration = StereoCalibration(input_folder='calib_result')

# Rectify a pair of left and right images (example using the last pair)
rectified_pair = calibration.rectify((imgLeft, imgRight))

# Display the rectified images
#cv.imshow('Left Calibrated!', rectified_pair[0])
#cv.imshow('Right Calibrated!', rectified_pair[1])

cv.imwrite('left_calibrated.jpg', rectified_pair[0])
cv.imwrite('right_calibrated.jpg', rectified_pair[1])


stereo = cv.StereoBM_create(numDisparities=32, blockSize=5)
disparity = stereo.compute(rectified_pair[0],rectified_pair[1])
plt.imshow(disparity,'gray')
plt.show()
"""


# Load image to rectify 
left_image = cv.imread('./images/left2.jpeg', cv.IMREAD_GRAYSCALE)
right_image = cv.imread('./images/right2.jpeg', cv.IMREAD_GRAYSCALE)

left_image = cv.resize(right_image, (500, 500))
right_image = cv.resize(left_image, (500, 500))


# Load the calibration results
calibration = StereoCalibration(input_folder='calib_result')

# Rectify a pair of left and right images (example using the last pair)
rectified_pair = calibration.rectify((left_image, right_image))

# Display the rectified images
#cv.imshow('Left Calibrated!', rectified_pair[0])
#cv.imshow('Right Calibrated!', rectified_pair[1])

cv.imwrite('left_calibrated.jpg', rectified_pair[0])
cv.imwrite('right_calibrated.jpg', rectified_pair[1])

right_image = cv.imread("./left_calibrated.jpg", cv.IMREAD_GRAYSCALE)
left_image = cv.imread("./right_calibrated.jpg", cv.IMREAD_GRAYSCALE)

# Get the blur level from the scale
blur_level = 15
# Apply Gaussian blur with the chosen kernel size
blur_kernel_size = (blur_level, blur_level)
left_image_blurred = cv.GaussianBlur(left_image, blur_kernel_size, 0)
right_image_blurred = cv.GaussianBlur(right_image, blur_kernel_size, 0)

num_disparities = 16
block_size = 13

# Ensure num_disparities is positive and divisible by 16
num_disparities = max(16, num_disparities)
num_disparities = num_disparities + (16 - (num_disparities % 16)) if num_disparities % 16 != 0 else num_disparities

stereo = cv.StereoBM_create(numDisparities=num_disparities, blockSize=block_size)
disparity_map = stereo.compute(left_image_blurred, right_image_blurred)

min_disparity = disparity_map.min()
max_disparity = disparity_map.max()
normalized_disparity = (disparity_map - min_disparity) / (max_disparity - min_disparity)
normalized_disparity = (normalized_disparity * 255).astype(np.uint8)

plt.imshow(normalized_disparity, 'gray')

plt.show()



 
