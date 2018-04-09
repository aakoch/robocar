#menu.py
###############################################################
# Writing down thoughts.
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-06
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import sensor, image, time, sys, constants
from class_camera import *
from class_threshold import *
from constants import *
from machine import WDT

#sensor.reset()
#sensor.set_pixformat(sensor.RGB565)
#sensor.set_framesize(sensor.QVGA)
#sensor.skip_frames(time = 2000)

#clock = time.clock()

#while(True):
    #clock.tick()
    #img = sensor.snapshot()
    #print(clock.fps())


# Settings:
# 1) B/W
# 2) Color
# 3) Yellow thresholds
# 4) Blue thresholds
# 5) Enable watchdog
# 6) Disable watchdog
# 7) Enable recording
# 8) Disable recording
# 9) Calibrate throttle
# 10) Calibrate steering


camera = Camera()

watchdog = WDT(timeout=5000)
camera.set_watchdog(watchdog)

#camera.set_camera_pixel_format_to_rgb()
#camera.set_camera_thresholds(Threshold.BLUE)

for n in range(50):
    line = camera.find_line()

    if line and (line.magnitude() >= MAG_THRESHOLD):
        print(line.magnitude())

# Steps when starting
# 1) Boot
# 2) Settings
# 3) Init
# 4) Run

while(True):
    watchdog.feed()
    pyb.delay(4000)
