#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Stop
from pybricks.tools import DataLog, StopWatch, wait
import argparse
import time

parser = argparse.ArgumentParser(description='Generate logfile of rotation angle vs reflectivity data on an EV3')
parser.add_argument('--rotations', help='number of rotations to perform', default='10')
parser.add_argument('--speed', help='speed of rotation (degrees/second)', default='200')
parser.add_argument('--interval', help='time between log readings (ms)', default='50')
parser.add_argument('--motor', help='the EV3 port attached to the platform motor', type=Port, default=Port.A)
parser.add_argument('--color', help='the EV3 port attached to the colour sensor', type=Port, default=Port.S4)
parser.add_argument('--touch', help='the EV3 port attached to the touch sensor', type=Port, default=Port.S1)
parser.add_argument('--label', help='the target value of the feature data', default='')
parser.add_argument('--filename', help='the log filename', default='log')
args = parser.parse_args()

# Create your objects here

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize motors
platform_motor = Motor(args.motor)

# Initialise sensors
platform_color_sensor = ColorSensor(args.color)
trigger_button = TouchSensor(args.touch)

# Initialise DataLog - append target label to filename if supplied
filename = args.filename + args.label
data = DataLog('angle','reflectivity',name=filename)



# Write your program here
print(trigger_button.pressed())
while True:
    if trigger_button.pressed():

        # Play a sound.
        ev3.speaker.beep()
        
        # Calculate rotation angle
        total_rotation = int(args.rotations) * 360
        rotation_speed = int(args.speed)
        log_interval = int(args.interval)

        # Run the platform motor
        platform_motor.run_angle(speed=rotation_speed, rotation_angle=total_rotation, then=Stop.HOLD, wait=False)

        wait(100)
        # print('Platform Speed: {0}'.format(platform_motor.speed()))

        # Log the time and the sensor readings 10 times
        while platform_motor.speed() > 0:
            rotation_angle = platform_motor.angle()
            character_reflectivity = platform_color_sensor.reflection()
            print("Angle: {0} degrees, Reflectivity: {1}%".format(platform_motor.angle(), platform_color_sensor.reflection()))
            data.log(rotation_angle, character_reflectivity)

            # Wait some time so the motor can move a bit
            wait(log_interval)  

        # Play another beep sound.
        ev3.speaker.beep(frequency=1000, duration=500)
        break

