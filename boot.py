#boot.py
###############################################################
# First thing ran by robot
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-05
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import machine, pyb
from machine import WDT
from constants import *
from reset_functions import *
from class_camera import *
from settings import Settings

# Steps when starting
# 1) Boot
# 2) Settings
# 3) Init
# 4) Run

# this will check, and then if the reset was due to the watchdog, it will run the pulse LED file
check_reset_cause()

#def setup_settings():
    #settings = Settings()
    #return settings

#settings = setup_settings()

camera = Camera()

#if (settings.is_watchdog_enabled):
    #watchdog = WDT(timeout=5000)
    #camera.set_watchdog(watchdog)

#camera.set_camera_pixel_format_to_rgb()
#camera.set_camera_thresholds(Threshold.BLUE)

for n in range(50):
    line = camera.find_line()

    if line and (line.magnitude() >= MAG_THRESHOLD):
        print(line.magnitude())

# ...

# run
