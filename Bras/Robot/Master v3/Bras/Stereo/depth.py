import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
imgL = cv.imread('./rubiks_cube_camera1.4.jpg', cv.IMREAD_GRAYSCALE)
imgR = cv.imread('./rubiks_cube_camera2.4.jpg', cv.IMREAD_GRAYSCALE)

#Pour calculer le bloc size et le STEREO : 
distance_base_cm = 0.01
image_width = 500
image_height = 500
block_size_factor = 0.05
block_size = int(image_width * block_size_factor)
stereo = cv.StereoBM_create(numDisparities=16, blockSize=block_size)


baseline_pixels = int(distance_base_cm * (image_width / 2))
focal = 1000

#stereo.setFocalLength(focal)
#stereo.setbaseline(baseline_pixels)



disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')



depth_map = np.zeros_like(disparity, dtype=np.float32)
for y in range(disparity.shape[0]):
    for x in range(disparity.shape[1]):
        disparite = disparity[y, x]
        if disparite > 0:
            depth_map[y, x] = (distance_base_cm * focal) / disparite


#cv2.imwrite('depth_map.png', depth_map)
plt.imshow(depth_map,'gray')





plt.show()



"""
import cv2

#Mesure de la distance de base en centimètres
distance_base_cm = 1.0

#Résolution de l'image de la caméra (1 mégapixel = 1 000 000 pixels)
image_width = 1000  # Largeur de l'image en pixels
image_height = 1000  # Hauteur de l'image en pixels

#Calcul de la taille de la fenêtre en fonction de la distance de base
#Vous pouvez ajuster ce facteur en fonction de vos besoins
block_size_factor = 0.05  # 5% de la largeur de l'image
block_size = int(image_width * block_size_factor)

#Créez un objet StereoBM
stereo = cv2.StereoBM_create()

#Définissez la taille de la fenêtre SAD en pixels
stereo.setBlockSize(block_size)
"""
