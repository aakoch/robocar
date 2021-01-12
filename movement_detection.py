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
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 1500)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)
clock = time.clock()

print("STEERING_SERVO_ZERO_US", STEERING_SERVO_ZERO_US)

#sensor.set_auto_exposure(False, exposure_us=sensor.get_exposure_us() + 10000)

device = pyb.UART(3, 19200, timeout_char = 100)


print("sensor.height()=", sensor.height())


extra_fb = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.RGB565)


prev_throttle = 0 #int(ConfigFile().get_property("min_speed"))
print("previous min throttle=", str(prev_throttle))

print("About to save background image...")
sensor.skip_frames(time = 200)
extra_fb.replace(sensor.snapshot())
print("determining noise")

i = 0

min_min = 1
max_min = -1

min_max = 1
max_max = -1

while(i < 50):
    clock.tick()
    img = sensor.snapshot()

    sim = img.get_similarity(extra_fb)
    min_min = min(min_min, sim.min())
    max_min = max(max_min, sim.min())
    min_max = min(min_max, sim.max())
    max_max = max(max_max, sim.max())
    i += 1

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

    sim = img.get_similarity(extra_fb)
    if (sim.min() < min_min - .3 or sim.min() > max_min + .09 or sim.max() > max_max + .01 or sim.max() < min_max - .01):
        print("min_min=", min_min, ", max_min=", max_min)
        print("min_max=", min_max, ", max_max=", max_max)
        print("difference", sim)
        print("prev min throttle=", prev_throttle)
        print("new min throttle=", throttle)
        movement_found = True
        img.difference(extra_fb)
        sensor.flush()
    else:
        if (pyb.elapsed_millis(start) < 800):
            set_servos(throttle)
        elif (pyb.elapsed_millis(start) < 1000):
            set_servos(prev_throttle - 80)
        else:
            throttle += 2

            start = pyb.millis()
            set_servos(prev_throttle - 80)

set_servos(throttle - 80)

ConfigFile().set_property("min_speed", throttle)

img.save("movement_difference" + create_time_based_filename());

for led_count in range(0, 10):
    set_servos(throttle - 80)
    pyb.LED(2).toggle()
    pyb.delay(100)
pyb.LED(2).off()

