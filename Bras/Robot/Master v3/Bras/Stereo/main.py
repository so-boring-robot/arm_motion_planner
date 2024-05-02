import cv2
import numpy as np

# Charger l'image

images = ['camera1.4.jpg', 'camera2.4.jpg']

for img in images:

	image = cv2.imread(f"./Cam/cam4/{img}")

	if image is not None:
		image = cv2.resize(image, (500, 500))

		hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		# Le reste du code pour isoler la couleur verte


		# Convertir l'image en espace colorimétrique HSV
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

		# Définir la plage de teintes (Hue) pour la couleur verte
		lower_green = np.array([60, 50, 210])
		upper_green = np.array([90, 255, 255])		


		# Filtrez l'image pour ne garder que les pixels verts dans la plage spécifiée
		mask = cv2.inRange(hsv, lower_green, upper_green)

		# Appliquez un masque à l'image d'origine pour extraire le Rubik's Cube vert
		green_cube = cv2.bitwise_and(image, image, mask=mask)

		# Enregistrez ou affichez le résultat final
		#cv2.imshow('Rubik\'s Cube Vert', green_cube)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		
		cv2.imwrite(f'rubiks_cube_{img}', green_cube)

	else:
		print("L'image n'a pas pu être chargée.")

