#!/usr/bin/env python3
import os, sys, math, time
import cv2
import neopixel, board
from adafruit_servokit import ServoKit
from revolute_robot import RevoluteRobot
from vision_manager import FaceTracker

# Initialize RGB LED
led = neopixel.NeoPixel(board.D18, 1)
tracker = FaceTracker(resolution=(800, 600), display=True, brightness=100)
kit = ServoKit(channels=16)
program_running = True

claw = True

hard_limits = [(-15, 15), (0, 25), (15, 30)]

rest_pos = (0, 10, 15)
shutdown = False

def init_robot_pos(robo):
    start_pos = [160, 100, 45, 180, 50, 90]
    s = 0
    # Activate Servos
    for pos in start_pos:
        kit.servo[s].angle = pos
        s += 1
    # Force the starting position
    s = len(start_pos)-1
    for joint in range(len(robo.theta['theta'])):
        robo.theta['theta'][joint] = math.radians(start_pos[s])
        s -= 1
    robo.update_posture()

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

def map_range(value, old_min, old_max, new_min, new_max):
    old_span = old_max - old_min
    new_span = new_max - new_min
    scale_val = float(value - old_min) / float(old_span)
    return new_min + (scale_val * new_span)

def recover_robot(robo):
    recover = [90.0, 40.0, 90.0, 40.0]
    offset = [1.0, 2.0, 1.0, 0.5]
    while True:
        angles = robo.get_angles()
        joint = 4
        valid = 0
        for i in range(1, len(angles)):
            if abs(angles[i] - recover[i]) < 0.01:
                valid += 1
            else:
                if abs(angles[i] - recover[i]) <= 1:
                    angles[i] = recover[i]
                elif angles[i] > recover[i]:
                    angles[i] -= offset[i]
                elif angles[i] < recover[i]:
                    angles[i] += offset[i]
                if joint == 2:
                    angle = 90 - angles[i]
                    if angle < 0:
                        angle = 0
                    kit.servo[joint].angle = angle
                elif joint == 3:
                    angle = map_range(angles[i], 0, 180, 90, 210)
                    kit.servo[joint].angle = angle
                else:
                    kit.servo[joint].angle = angles[i]
            joint -= 1
        print("Angles: ", angles)    
        robo.set_angles(angles)
        time.sleep(0.05)
        print("Valid", valid)
        if valid == len(angles)-1:
            break
    pos = robo.end_position['current']
    print("Pos: ", pos.x, pos.y, pos.z)
    robo.set_target(pos.x, pos.y, pos.z)
    

if __name__=="__main__":
    # Initialize RGB LED
    led[0] = (0, 255, 0)
    tracker.start()
    init_servos()
    myRobot = build_robot()
    # Set initial robot position
    init_robot_pos(myRobot)
    
