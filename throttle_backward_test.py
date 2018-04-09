# This file is part of the OpenMV project.
# Copyright (c) 2013-2017 Ibrahim Abdelkader <iabdalkader@openmv.io> & Kwabena W. Agyeman <kwagyeman@openmv.io>
# This work is licensed under the MIT license, see the file LICENSE for details.

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
    #if throttle < 0:
        #throttle = 1000 + ((throttle * (THROTTLE_SERVO_MIN_US - 1000 + 1)) / 101)
    #else:
        #throttle = THROTTLE_SERVO_MIN_US + ((throttle * (THROTTLE_SERVO_MAX_US - THROTTLE_SERVO_MIN_US + 1)) / 101)

    steering = STEERING_SERVO_MIN_US + ((steering * (STEERING_SERVO_MAX_US - STEERING_SERVO_MIN_US + 1)) / 181)
    device.write("{%05d,%05d}\r\n" % (throttle, steering))
    print("wrote: {%05d,%05d}" % (throttle, steering))

def invert_steering(steering_in):
    return ((steering_in - 90) * -1) + 90

usb = pyb.USB_VCP() # This is a serial port object that allows you to
# communciate with your computer. While it is not open the code below runs.
usb_is_connected = usb.isconnected()

start_time = pyb.millis()

adc = ADC("P6") # Must always be "P6".
i = -50
throttle_output = i


read_value = ConfigFile().get_property("min_speed")
print("min_speed = " + read_value if read_value else "unknown")

pyb.delay(500)
pulse_sensor_prev = adc.read()
sensed_movement = False
while not sensed_movement:

    print("throttle %d, steering %d" % (throttle_output , 100))
    set_servos(throttle_output, 100)

    pulse_sensor = adc.read()
    sensed_movement =  abs(pulse_sensor_prev - pulse_sensor) > 100
    print("pulse_sensor_prev = %d, pulse_sensor = %d, sensed_movement = %s" % (pulse_sensor_prev, pulse_sensor, sensed_movement))
    pulse_sensor_prev = round((pulse_sensor_prev + pulse_sensor) / 2.0)

    if i < -65:
        print("hit failsafe")
        sensed_movement = True
    else:
        if (sensed_movement):
            print("moved at %d" % (i + 1))
        else:
            throttle_output = i
            i -= 1
            pyb.delay(200)

for j in range(5):
    set_servos(0, 100)
    pyb.delay(200)

ConfigFile().set_property("min_speed", i)
