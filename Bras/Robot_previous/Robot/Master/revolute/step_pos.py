#!/usr/bin/env python3

import os, sys, time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

for i in range(6):
	if i > 0:
		kit.servo[i].set_pulse_width_range(500, 2500)
kit.servo[0].set_pulse_width_range(1800, 2300)

def set_position(servo, angle):
	print("Servo {}: set to {} degrees".format(servo, angle))
	kit.servo[servo].angle=angle

def get_command():
	val = input()
	if val == 'q':
		sys.exit(0)
	a, b = val.split('/')
	servo = int(a)
	angle = int(b)
	return servo, angle

if __name__=="__main__":
	while True:
		servo, angle = get_command()
		set_position(servo, angle)
