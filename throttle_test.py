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

import sensor, image, time, math, pyb, uio, sys, array
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

read_value = ConfigFile().get_property("min_speed")
print("min_speed = " + read_value if read_value else "unknown")

min_pulse_sensor = 9999
max_pulse_sensor = 0
start_time = pyb.millis()
start_time2 = pyb.millis()

#tim = pyb.Timer(4, freq=20)         # create a timer running at 10Hz
#buf = bytearray(100)                # creat a buffer to store the samples
#adc.read_timed(buf, tim)            # sample 100 values, taking 10s

#for val in buf:                     # loop over all values
    #print(val)                      # print the value out

for a in ('b' , 'B' , 'h', 'H' , 'i' , 'I' , 'l' , 'L' , 'q' , 'Q' , 'f' , 'd'):
#while True:
    print("read" + str(adc.read() / 16))
    #buf = bytearray(10) #array.array('h')                # create a buffer of 100 bytes
    buf = array.array(a)                # create a buffer of 100 bytes
    adc.read_timed(buf, 10)             # read analog values into buf at 10Hz
                                        #   this will take 10 seconds to finish
    print(buf)
    for val in buf:                     # loop over all values
        print(val)                      # print the value out

sys.exit()
start_time = pyb.millis()
while pyb.elapsed_millis(start_time) < 50:
    print(adc.read())

while pyb.elapsed_millis(start_time) < 5000 or abs(max_pulse_sensor - min_pulse_sensor) < 100:
    pulse_sensor = adc.read()
    #print("ADC = %d" % (pulse_sensor))
    if  pyb.elapsed_millis(start_time2) > 1000:
        min_pulse_sensor = pulse_sensor
        max_pulse_sensor = pulse_sensor
        start_time2 = pyb.millis()
    else:
        min_pulse_sensor = min(min_pulse_sensor, pulse_sensor)
        max_pulse_sensor = max(max_pulse_sensor, pulse_sensor)
        print(str(min_pulse_sensor) + " - " + str(max_pulse_sensor))
    pyb.delay(100)
    if (pyb.elapsed_millis(start_time) > 5000):
        start_time = pyb.millis()


pyb.delay(500)
pulse_sensor_prev = adc.read()

sensed_movement = False
while not sensed_movement:

    print("throttle %d, steering %d" % (throttle_output , 100))
    set_servos(throttle_output, 100)

    pulse_sensor = adc.read()
    sensed_movement =  abs(pulse_sensor_prev - pulse_sensor) > 50 and abs(pulse_sensor_prev - pulse_sensor) < 150 and \
        ((pulse_sensor > min_pulse_sensor - 100 and pulse_sensor < max_pulse_sensor) or pulse_sensor > min_pulse_sensor and (pulse_sensor < max_pulse_sensor + 100))
    print("pulse_sensor_prev = %d, pulse_sensor = %d, sensed_movement = %s" % (pulse_sensor_prev, pulse_sensor, sensed_movement))
    pulse_sensor_prev = round((pulse_sensor_prev + pulse_sensor) / 2.0)

    if i > 60:
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
