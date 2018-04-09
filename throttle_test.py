#throttle_test.py
###############################################################
# Find the lowest throttle value the car will move.
# This only works on specialized code on the Arduino. ***
# The steering output of the Arduino interferes with the
# pulse sensor readings. You can re-program the Arduino to
# not output then you have to re-program it for regular
# runing of the car.
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-03-22
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import sensor, image, time, math, pyb, uio
from pyb import Pin, Timer
from pyb import ADC
from file_utils import ConfigFile
#from util_functions import *

def remap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

###########
# Settings
###########

# Tweak these values for your robocar.
THROTTLE_SERVO_MIN_US = 1268 # from output_throttle Arduino sketch
THROTTLE_SERVO_MAX_US = 1692

# Tweak these values for your robocar.
STEERING_SERVO_MIN_US = 1276
STEERING_SERVO_MAX_US = 1884

# Handle if these were reversed...
tmp = max(THROTTLE_SERVO_MIN_US, THROTTLE_SERVO_MAX_US)
THROTTLE_SERVO_MIN_US = min(THROTTLE_SERVO_MIN_US, THROTTLE_SERVO_MAX_US)
THROTTLE_SERVO_MAX_US = tmp

# Handle if these were reversed...
tmp = max(STEERING_SERVO_MIN_US, STEERING_SERVO_MAX_US)
STEERING_SERVO_MIN_US = min(STEERING_SERVO_MIN_US, STEERING_SERVO_MAX_US)
STEERING_SERVO_MAX_US = tmp

# This function maps the output of the linear regression function to a driving vector for steering
# the robocar. See https://openmv.io/blogs/news/linear-regression-line-following for more info.


# Servo Control Code
device = pyb.UART(3, 19200, timeout_char = 100)

## throttle [0:100] (101 values) -> [THROTTLE_SERVO_MIN_US, THROTTLE_SERVO_MAX_US]
# throttle [-100:100] (201 values) -> [THROTTLE_SERVO_MIN_US, THROTTLE_SERVO_MAX_US]
# steering [0:180] (181 values) -> [STEERING_SERVO_MIN_US, STEERING_SERVO_MAX_US]
def set_servos(throttle, steering):
    throttle = remap(throttle, -100, 100, THROTTLE_SERVO_MIN_US, THROTTLE_SERVO_MAX_US)
    steering = remap(steering, 0, 180, STEERING_SERVO_MIN_US, STEERING_SERVO_MAX_US)

    device.write("{%05d,%05d}\r\n" % (throttle, steering))
    print("wrote: {%05d,%05d}" % (throttle, steering))

def invert_steering(steering_in):
    return ((steering_in - 90) * -1) + 90

usb = pyb.USB_VCP() # This is a serial port object that allows you to
# communciate with your computer. While it is not open the code below runs.
usb_is_connected = usb.isconnected()

start_time = pyb.millis()

adc = ADC("P6") # Must always be "P6".
i = 0
throttle_output = i

print("min_speed = " + ConfigFile().get_property("min_speed"))

pyb.delay(500)
pulse_sensor_prev = adc.read()
sensed_movement = False
while not sensed_movement:

    print("throttle %d, steering %d" % (throttle_output , 100))
    set_servos(throttle_output, 100)

    pulse_sensor = adc.read()
    sensed_movement =  abs(pulse_sensor_prev - pulse_sensor) > 50
    print("pulse_sensor_prev = %d, pulse_sensor = %d, sensed_movement = %s" % (pulse_sensor_prev, pulse_sensor, sensed_movement))
    pulse_sensor_prev = round((pulse_sensor_prev + pulse_sensor) / 2.0)

    if i > 45:
        print("hit failsafe")
        sensed_movement = True
    else:
        if (sensed_movement):
            print("moved at %d" % (i - 1))
        else:
            throttle_output = max(min(round(i), 100), 0)
            i += 1
            pyb.delay(500)

for j in range(5):
    set_servos(0, 100)
    pyb.delay(200)

ConfigFile().set_property("min_speed", i)
