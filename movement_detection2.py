###############################################################
# Find the lowest throttle value the car will move.
# !!! This should be replaced wth find_displacement() !!!
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-22
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import sensor, image, pyb, os, time, array
from util_functions import *
from file_utils import ConfigFile
from pyb import RTC

TRIGGER_THRESHOLD = const(5)
STEERING_SERVO_MIN_US = const(1276)
STEERING_SERVO_MAX_US = const(1884)
STEERING_SERVO_ZERO_US = round((STEERING_SERVO_MIN_US + STEERING_SERVO_MAX_US) / 2)

def create_time_based_filename():
    datetime = rtc.datetime()
    print(datetime)
    return "{0}{1:02d}{2:02d}{3:02d}{4:02d}{5:02d}".format(datetime[0], datetime[1], datetime[2], \
            datetime[4], datetime[5], datetime[6])


def set_servos(throttle):
    ## TODO: calculate this upfront
    #steering = remap(90, 0, 180, STEERING_SERVO_MIN_US, STEERING_SERVO_MAX_US)

    device.write("{%05d,%05d}\r\n" % (throttle, STEERING_SERVO_ZERO_US))


rtc = RTC()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.B128X128)
sensor.set_hmirror(True)
sensor.set_vflip(True)
sensor.skip_frames(time = 1500)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)
clock = time.clock()

print("STEERING_SERVO_ZERO_US", STEERING_SERVO_ZERO_US)

#sensor.set_auto_exposure(False, exposure_us=sensor.get_exposure_us() + 10000)

device = pyb.UART(3, 19200, timeout_char = 100)


print("sensor.height()=", sensor.height())


extra_fb = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.RGB565)


prev_throttle = int(ConfigFile().get_property("min_speed"))
print("previous min throttle=", str(prev_throttle))

print("About to save background image...")
sensor.skip_frames(time = 200)
extra_fb.replace(sensor.snapshot())

print("determining noise")

x_min = 100
x_max = -100

y_min = 100
y_max = -100

from pyb import RTC

rtc = RTC()

while(True):
    start = pyb.millis()
    while(pyb.elapsed_millis(start) < 5000):
        img = sensor.snapshot()
        displacement = img.find_displacement(extra_fb)
        #extra_fb.replace(img)
        x_min = min(x_min, displacement.x_translation())
        x_max = max(x_max, displacement.x_translation())
        y_min = min(y_min, displacement.y_translation())
        y_max = max(y_max, displacement.y_translation())

    print(rtc.datetime(), x_min, x_max, y_min, y_max)
    # -0.05934011 0.1411061 -0.09199938 0.1660026

print("============= Press throttle now =============")

for led_count in range(0, 20):
    set_servos(prev_throttle - 80)
    pyb.LED(1).toggle()
    pyb.delay(200 - (led_count * 10))

pyb.LED(1).off()

movement_found = False
throttle = prev_throttle - 20
start = pyb.millis()

while (not movement_found):
    clock.tick()
    print("throttle=", throttle)
    img = sensor.snapshot()

    displacement = img.find_displacement(extra_fb)

    #extra_fb.replace(img)

    # Offset results are noisy without filtering so we drop some accuracy.
    sub_pixel_x = displacement.x_translation()
    sub_pixel_y = displacement.y_translation()

    #print("displacement.response()=", displacement.response())
    if (displacement.response() > 0.1): # Below 0.1 or so (YMMV) and the results are just noise.
        print("{0:+f}x {1:+f}y {2}".format(sub_pixel_x, sub_pixel_y,
              displacement.response()))
        pad = 0.05598078
        if (sub_pixel_x < x_min - pad or sub_pixel_x > x_max + pad \
                or sub_pixel_y < y_min - pad or sub_pixel_y > y_max + pad):
            movement_found = True
        else:
            if (pyb.elapsed_millis(start) < 800):
                set_servos(throttle)
            elif (pyb.elapsed_millis(start) < 1000):
                set_servos(prev_throttle - 80)
            else:
                throttle += 2

                start = pyb.millis()
                set_servos(prev_throttle - 80)
    else:
        set_servos(prev_throttle - 80)


print(x_min, x_max, y_min, y_max)
set_servos(throttle - 80)

ConfigFile().set_property("min_speed", throttle)

img.save("movement_difference" + create_time_based_filename());

for led_count in range(0, 10):
    set_servos(throttle - 80)
    pyb.LED(2).toggle()
    pyb.delay(100)
pyb.LED(2).off()

