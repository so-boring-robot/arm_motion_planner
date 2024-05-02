#!/usr/bin/env python3

from calibration_utility import load_coefficients, save_coefficients, calibrate_chessboard
import time
import cv2
from threading import Thread

# Parameters
IMAGES_DIR = 'calibration_imgs'
IMAGES_FORMAT = '.jpg'
SQUARE_SIZE = 30.0
WIDTH = 8
HEIGHT = 5

class CountdownTimer:
    def __init__(self, count=10):
        self.count = count
        
    def update(self):
        while self.count > 0:
            time.sleep(1)
            self.count -= 1
    
    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self
    
    

# Take images
while 1:
    print("Enter 1 to take images manually (press space bar)")
    print("Enter 2 for timed image capture (10 sec delay for first and then 3 sec)")
    mode = input()
    if mode == "1" or mode == "2":
        mode = int(mode)
        break
        
font = cv2.FONT_HERSHEY_SIMPLEX
img_count = 1
cam = cv2.VideoCapture(0)
countdown = CountdownTimer()
countdown.start()
while 1:
    ret, image = cam.read()
    img = image.copy()
    cv2.putText(img, str(countdown.count), (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(img, str(img_count-1), (10,30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow("Camera", img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    if mode == 1:
        if k == 32:
            cv2.imwrite("{}/img_{}.jpg".format(IMAGES_DIR, img_count), image)
            img_count += 1
    else:
        if countdown.count == 0:
            cv2.imwrite("{}/img_{}.jpg".format(IMAGES_DIR, img_count), image)
            img_count += 1
            cv2.rectangle(img, (5,5), (img.shape[0]-5,img.shape[1]-5), (0,0,255), 5)
            cv2.imshow("Camera", img)
            time.sleep(0.5)
            countdown = CountdownTimer(count=3)
            countdown.start()
            

cam.release()
cv2.destroyAllWindows()

# Calibrate 
ret, mtx, dist, rvecs, tvecs = calibrate_chessboard(
    IMAGES_DIR, 
    IMAGES_FORMAT, 
    SQUARE_SIZE, 
    WIDTH, 
    HEIGHT
)
# Save coefficients into a file
save_coefficients(mtx, dist, "calibration_map.yml")
