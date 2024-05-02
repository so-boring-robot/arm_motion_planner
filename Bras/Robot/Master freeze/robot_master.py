#!/usr/bin/env python3
import os, sys, math, time
import cv2
import neopixel, board
from adafruit_servokit import ServoKit
from revolute_robot import RevoluteRobot
from vision_manager import FaceTracker

import os, sys, math, time
from adafruit_servokit import ServoKit
from revolute_robot import RevoluteRobot

kit = ServoKit(channels=16)
program_running = True
sim_running = False

def init_servos():
    for i in range(1, 6, 1):
        kit.servo[i].set_pulse_width_range(500, 2500)
    kit.servo[0].set_pulse_width_range(1800, 2300)

def build_robot():
    # Create robot object
    robot = RevoluteRobot()
    # Define its joints
    robot.add_joint_link(length=9.5,  min_theta= 0, max_theta=360, theta=90)
    robot.add_joint_link(length=11, min_theta= 0, max_theta=360, theta=180)
    robot.add_joint_link(length=10.5, min_theta= 0, max_theta=360, theta=90)
    robot.add_joint_link(length=10.0, min_theta= 0, max_theta=360, theta=0)
    return robot

def get_coordinates():
    global program_running
    global sim_running
    print("Enter desired robot end effector position:")
    val = input("Format: X,Y,Z\n")
    if val == 'q':
        program_running = False
        return False
    elif val == 'z':
        sim_running = True
        return False
    elif val == 'o':
        kit.servo[0].angle=0
        return False
    elif val == 'c':
        kit.servo[0].angle=180
        return False
    else:
        try:
            x, y, z = val.replace(' ', '').split(',')
            x = int(x)
            y = int(y)
            z = int(z)
            return x, y, z
        except:
            print("Error, Invalid coordinates received.")
            return False

def map_range(value, old_min, old_max, new_min, new_max):
    old_span = old_max - old_min
    new_span = new_max - new_min
    scale_val = float(value - old_min) / float(old_span)
    return new_min + (scale_val * new_span)

if __name__=="__main__":
    # Initialize RGB LED
    pixels = neopixel.NeoPixel(board.D18, 1)
    pixels[0] = (0, 255, 0)
    
    init_servos()
    myRobot = build_robot()
    myRobot.set_target(0, -20, 15)
    t = 0
    while not myRobot.on_target():
        myRobot.move_to_target()
        pass
    while program_running:
        if myRobot.on_target() and not sim_running:
            coordinates = get_coordinates()
            if coordinates:
                x, y, z = coordinates
                myRobot.set_target(x, -y, z)
        elif sim_running:
            x1 = 1.1 * math.cos(0.12 * t) * 10 * math.cos(t)
            y1 = -20
            z1 = 20 + (1.1 * math.cos(0.2 * t) * 10 * math.sin(t))
            myRobot.set_target(x1, y1, z1)
            t += 0.025
            if t > 31:
                t = 0
                sim_running = False
        if not myRobot.on_target():
            myRobot.move_to_target()
            joint = 5
            for theta in myRobot.theta['theta']:
                angle = math.degrees(theta)
                print("Origin {}: {}".format(joint, angle))
                if angle > 180:
                    angle = 180
                if angle < 0:
                    angle = 0
                if joint==2:
                    if angle > 90:
                        angle = 0
                    else:
                        angle = 90 - angle
                if joint == 3:
                    angle = map_range(angle, 0, 180, 90, 210)
                    if angle > 180:
                        angle = 180
                kit.servo[joint].angle = angle
                print("Joint {}: {} degees".format(joint, angle))
                joint -= 1
            time.sleep(0.05)




tracker = FaceTracker(display=False)
tracker.start()

while tracker.active:
    if tracker.face:
        print("Distance: {}mm".format(tracker.face.distance))
        x, y = tracker.get_center_offset()
        print("Face Offset: {}, {}".format(x, y))
    if tracker.hand:
        print("Hand: Closed")
    else:
        print("Hand: Open")

    hand_led = 255 * (tracker.hand_count * 0.1)
    if tracker.tracking:
        pixels[0] = (255-hand_led, 0, hand_led)
    else:
        pixels[0] = (0, 255-hand_led, hand_led)
    time.sleep(0.5)
