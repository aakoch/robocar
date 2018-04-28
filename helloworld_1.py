# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time, math, pyb

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames()     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
                                    # This file is part of the OpenMV project.
                                    # Copyright (c) 2013-2017 Ibrahim Abdelkader <iabdalkader@openmv.io> & Kwabena W. Agyeman <kwagyeman@openmv.io>
                                    # This work is licensed under the MIT license, see the file LICENSE for details.

print("1")


############
## Settings
############

#COLOR_LINE_FOLLOWING = False # False to use grayscale thresholds, true to use color thresholds.
#COLOR_THRESHOLDS = [(90, 100, -20, 127, 40, 127)] # Yellow Line.
#GRAYSCALE_THRESHOLDS = [(240, 255)] # White Line.
#BINARY_VIEW = True # Helps debugging but costs FPS if on.
#DO_NOTHING = True # Just capture frames...
#FRAME_SIZE = sensor.QQVGA # Frame size.
#FRAME_REGION = 0.75 # Percentage of the image from the bottom (0 - 1.0).
#MAG_THRESHOLD = 5 # Raise to filter out false detections.

## Tweak these values for your robocar.
#THROTTLE_CUT_OFF_ANGLE = 10.0 # Maximum angular distance from 90 before we cut speed [0.0-90.0).
#THROTTLE_CUT_OFF_RATE = 0.5 # How much to cut our speed boost (below) once the above is passed (0.0-1.0].
#THROTTLE_GAIN = 0.0 # e.g. how much to speed up on a straight away
#THROTTLE_OFFSET = 24.0 # e.g. default speed
#THROTTLE_P_GAIN = 1.0
#THROTTLE_I_GAIN = 0.0
#THROTTLE_I_MIN = -0.0
#THROTTLE_I_MAX = 0.0
#THROTTLE_D_GAIN = 0.0

## Tweak these values for your robocar.
#STEERING_THETA_GAIN = 30.0
#STEERING_RHO_GAIN = -30.0
#STEERING_P_GAIN = 0.6
#STEERING_I_GAIN = 0.0
#STEERING_I_MIN = -0.0
#STEERING_I_MAX = 0.0
#STEERING_D_GAIN = 0.2

## Selects servo controller module...
#ARDUINO_SERVO_CONTROLLER_ATTACHED = False

## Tweak these values for your robocar.
#THROTTLE_SERVO_MIN_US = 1500
#THROTTLE_SERVO_MAX_US = 2000

## Tweak these values for your robocar.
#STEERING_SERVO_MIN_US = 700
#STEERING_SERVO_MAX_US = 2300

############
## Setup
############

#THROTTLE_CUT_OFF_ANGLE = max(min(THROTTLE_CUT_OFF_ANGLE, 89.99), 0)
#THROTTLE_CUT_OFF_RATE = max(min(THROTTLE_CUT_OFF_RATE, 1.0), 0.01)

## Handle if these were reversed...
#tmp = max(THROTTLE_SERVO_MIN_US, THROTTLE_SERVO_MAX_US)
#THROTTLE_SERVO_MIN_US = min(THROTTLE_SERVO_MIN_US, THROTTLE_SERVO_MAX_US)
#THROTTLE_SERVO_MAX_US = tmp

## Handle if these were reversed...
#tmp = max(STEERING_SERVO_MIN_US, STEERING_SERVO_MAX_US)
#STEERING_SERVO_MIN_US = min(STEERING_SERVO_MIN_US, STEERING_SERVO_MAX_US)
#STEERING_SERVO_MAX_US = tmp

## This function maps the output of the linear regression function to a driving vector for steering
## the robocar. See https://openmv.io/blogs/news/linear-regression-line-following for more info.

#def figure_out_my_steering(line, img):

    ## The "slope_response" tries to turn the wheels in the direction of the line.
    ## It does not keep the car on the line but makes the car drive in the same direction.
    #slope_response = math.tan(math.radians(line.theta()))

    ## Rho is computed using the inverse of this code below in the actual OpenMV Cam code.
    ## This formula comes from the Hough line detection formula (see the wikipedia page for more).
    ## Anyway, the output of this calculations below are a point centered vertically in the middle
    ## of the image and to the left or right such that the line goes through it (cx may be off the image).
    #cy = img.height() / 2
    #cx = (line.rho() - (cy * math.sin(math.radians(line.theta())))) / math.cos(math.radians(line.theta()))

    ## "cx_middle" is now the distance from the center of the line. This is our error method to stay
    ## on the line. "cx_normal" normalizes the error to something like -1/+1 (it will go over this).
    #cx_middle = cx - (img.width() / 2)
    #cx_normal = cx_middle / (img.width() / 2)

    #return (slope_response * STEERING_THETA_GAIN) + (cx_normal * STEERING_RHO_GAIN)

## Solve: THROTTLE_CUT_OFF_RATE = pow(sin(90 +/- THROTTLE_CUT_OFF_ANGLE), x) for x...
##        -> sin(90 +/- THROTTLE_CUT_OFF_ANGLE) = cos(THROTTLE_CUT_OFF_ANGLE)
#t_power = math.log(THROTTLE_CUT_OFF_RATE) / math.log(math.cos(math.radians(THROTTLE_CUT_OFF_ANGLE)))

#def figure_out_my_throttle(steering): # steering -> [0:180]

    ## pow(sin()) of the steering angle is only non-zero when driving straight... e.g. steering ~= 90
    #t_result = math.pow(math.sin(math.radians(max(min(steering, 179.99), 0.0))), t_power)

    #return (t_result * THROTTLE_GAIN) + THROTTLE_OFFSET

##
## Servo Control Code
##

#device = None

#if ARDUINO_SERVO_CONTROLLER_ATTACHED:
    #device = pyb.UART(3, 19200, timeout_char = 1000)
#else:
    #import servo
    #import machine
    #device = servo.Servos(machine.I2C(sda = machine.Pin("P5"), scl = machine.Pin("P4")), address = 0x40, freq = 50)

## throttle [0:100] (101 values) -> [THROTTLE_SERVO_MIN_US, THROTTLE_SERVO_MAX_US]
## steering [0:180] (181 values) -> [STEERING_SERVO_MIN_US, STEERING_SERVO_MAX_US]
#def set_servos(throttle, steering):
    #throttle = THROTTLE_SERVO_MIN_US + ((throttle * (THROTTLE_SERVO_MAX_US - THROTTLE_SERVO_MIN_US + 1)) / 101)
    #steering = STEERING_SERVO_MIN_US + ((steering * (STEERING_SERVO_MAX_US - STEERING_SERVO_MIN_US + 1)) / 181)
    #if ARDUINO_SERVO_CONTROLLER_ATTACHED:
        #device.write("{%05d,%05d}\r\n" % (throttle, steering))
    #else:
        #device.position(0, us=throttle)
        #device.position(1, us=steering)
