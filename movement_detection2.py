# movement_detection2.py
###############################################################
# Find the lowest throttle value the car will move.
# This is the second revision that uses find_displacement().
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-22
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import sensor, image, pyb, os
from util_functions import *
from file_utils import ConfigFile
from pyb import RTC
#from led_functions import leds_on

TRIGGER_THRESHOLD = const(5)
STEERING_SERVO_MIN_US = const(1276)
STEERING_SERVO_MAX_US = const(1884)
STEERING_SERVO_ZERO_US = round((STEERING_SERVO_MIN_US + STEERING_SERVO_MAX_US) / 2)

def create_time_based_filename():
    datetime = rtc.datetime()
    return "{0}{1:02d}{2:02d}{3:02d}{4:02d}{5:02d}".format(datetime[0], datetime[1], datetime[2], \
            datetime[4], datetime[5], datetime[6])

def set_servos(throttle):
    device.write("{%05d,%05d}\r\n" % (throttle, STEERING_SERVO_ZERO_US))

#leds_on(None)

rtc = RTC()
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.B128X128)
#sensor.set_windowing((20, 0, 150, 50))
sensor.set_hmirror(True)
sensor.set_vflip(True)
sensor.skip_frames(time = 2000)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)

device = pyb.UART(3, 19200, timeout_char = 100)
extra_fb = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.GRAYSCALE)
#extra_fb = sensor.alloc_extra_fb(150, 50, sensor.GRAYSCALE)

prev_throttle = int(ConfigFile().get_property("min_speed"))
print("Previous min throttle=", str(prev_throttle))
print("Taking pic...")
sensor.skip_frames(time = 200)
extra_fb.replace(sensor.snapshot().histeq())

print("Determining noise...")

(x_min, x_max) = (100, -100)
(y_min, y_max) = (100, -100)

start = pyb.millis()
while(pyb.elapsed_millis(start) < 5000):
    img = sensor.snapshot().histeq()
    displacement = img.find_displacement(extra_fb)
    (x_min, x_max) = (min(x_min, displacement.x_translation()), max(x_max, displacement.x_translation()))
    (y_min, y_max) = (min(y_min, displacement.y_translation()), max(y_max, displacement.y_translation()))

print(rtc.datetime(), x_min, x_max, y_min, y_max)
print("==============================================")
print("============= Press throttle now =============")
print("==============================================")

for led_count in range(0, 20):
    set_servos(prev_throttle - 80)
    pyb.LED(1).toggle()
    pyb.delay(200 - (led_count * 10))

pyb.LED(1).off()

(run_throttle_millis, stop_throttle_millis) = (690, 145)
throttle = prev_throttle - 10
number_of_rounds = 3
throttle_total = 0
for count in range(1, number_of_rounds + 1):
    print("starting round", count, "of", str(number_of_rounds), "at throttle", throttle)
    movement_found = False
    start = pyb.millis()

    while (not movement_found):
        img = sensor.snapshot().histeq()

        displacement = img.find_displacement(extra_fb)

        # Offset results are noisy without filtering so we drop some accuracy.
        sub_pixel_x = displacement.x_translation()
        sub_pixel_y = displacement.y_translation()

        print("displacement =", displacement)
        if (displacement.response() > .15): # Below 0.1 or so (YMMV) and the results are just noise.
            #print("{0:+f}x {1:+f}y {2}".format(sub_pixel_x, sub_pixel_y, displacement.response()))
            pad = 0.2
            if (sub_pixel_x < x_min - pad or sub_pixel_x > x_max + pad \
                    or sub_pixel_y < y_min - pad or sub_pixel_y > y_max + pad):
                movement_found = True
            else:
                if (pyb.elapsed_millis(start) < run_throttle_millis):
                    set_servos(throttle)
                elif (pyb.elapsed_millis(start) < run_throttle_millis + stop_throttle_millis):
                    set_servos(prev_throttle - 80)
                else:
                    throttle += 2

                    start = pyb.millis()
                    set_servos(prev_throttle - 80)
        else:
            set_servos(prev_throttle - 80)
            sensor.skip_frames(time = 200)
            extra_fb.replace(sensor.snapshot().histeq())
        print("throttle=", throttle)

    print("throttle=", throttle, "x_min=", x_min, x_max, y_min, y_max, "{0:+f}x {1:+f}y response={2}".format(sub_pixel_x, sub_pixel_y, displacement.response()))
    set_servos(throttle - 80)

    (x_min, x_max) = (min(x_min, displacement.x_translation()), max(x_max, displacement.x_translation()))
    (y_min, y_max) = (min(y_min, displacement.y_translation()), max(y_max, displacement.y_translation()))

    #img.save("movement_difference" + create_time_based_filename());
    #extra_fb.replace(img)
    sensor.skip_frames(time = 200)
    extra_fb.replace(sensor.snapshot().histeq())
    throttle_total += throttle
    throttle = prev_throttle - 6

print("==============================================")

throttle_avg = round(throttle_total / number_of_rounds)
print("average throttle=", throttle_avg)
ConfigFile().set_property("min_speed", throttle_avg)


for led_count in range(0, 10):
    print("=========== Disengage throttle now ===========")
    set_servos(throttle - 80)
    pyb.LED(2).toggle()
    pyb.delay(500)
pyb.LED(2).off()


# get the first line of the main.py script
#read_

# is it "movement_detection2.py"?

# copy main.py to movement_detection2.py

# copy boot.py to main.py


