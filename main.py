#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Stop, SoundFile
from pybricks.tools import DataLog, StopWatch, wait
from pybricks.media.ev3dev import Font
import argparse

parser = argparse.ArgumentParser(description='Generate logfile of rotation angle vs reflectivity data on an EV3')
parser.add_argument('--rotations', help='number of rotations to perform', default='10')
parser.add_argument('--speed', help='speed of rotation (degrees/second)', default='200')
parser.add_argument('--interval', help='time between log readings (ms)', default='50')
parser.add_argument('--motor', help='the EV3 port attached to the platform motor', type=Port, default=Port.A)
parser.add_argument('--color', help='the EV3 port attached to the colour sensor', type=Port, default=Port.S4)
parser.add_argument('--touch', help='the EV3 port attached to the touch sensor', type=Port, default=Port.S1)
parser.add_argument('--label', help='the target value of the feature data', default='')
parser.add_argument('--filename', help='the log filename', default='log')
parser.add_argument('--predict', help='the predicted character')
args = parser.parse_args()


# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Display font, style and size
big = Font(family='Helvetica', size=24, bold=True)
ev3.screen.set_font(big)

if args.predict is None:

    # Initialize motors
    platform_motor = Motor(args.motor)

    # Initialise sensors
    platform_color_sensor = ColorSensor(args.color)
    trigger_button = TouchSensor(args.touch)

    # Initialise DataLog - append target label to filename if supplied
    filename = args.filename + args.label
    data = DataLog('angle', 'reflectivity', name=filename)

    # Initiate platform rotation and measurement on pressing the touch sensor
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
                print("Angle: {0} degrees, Reflectivity: {1}%".format(platform_motor.angle(),
                                                                      platform_color_sensor.reflection()))
                data.log(rotation_angle, character_reflectivity)

                # Wait some time so the motor can move a bit
                wait(log_interval)

                # Play another beep sound.
            ev3.speaker.beep(frequency=1000, duration=500)
            break

else:
    numbers = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE']
    number_dict = {i: val for i, val in enumerate(numbers)}
    prediction = number_dict[int(args.predict)]

    ev3.screen.clear()
    ev3.screen.draw_text(x=50, y=50, text=prediction)
    ev3.speaker.set_volume(100, which='PCM')
    ev3.speaker.say(prediction)
    wait(5000)
