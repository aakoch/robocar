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
# 6) (removed)
# 7) Enable recording
# 8) Disable recording
# 9) Calibrate throttle
# 10) Calibrate steering
# 11) Run


#watchdog = WDT(timeout=5000)
#camera.set_watchdog(watchdog)

#camera.set_camera_pixel_format_to_rgb()
#camera.set_camera_thresholds(Threshold.BLUE)


def set_leds_to_waiting(two_second_timer):
    global blue_led, green_led
    blue_led.on()
    green_led.off()
    if (two_second_timer):
        two_second_timer.deinit()

def main():
    global red_led, blue_led, green_led, camera

    try:
        red_led.toggle()
    except NameError:
        red_led   = pyb.LED(1)

    try:
        green_led.toggle()
    except NameError:
        green_led   = pyb.LED(2)

    try:
        blue_led.toggle()
    except NameError:
        blue_led   = pyb.LED(3)

    #if (not hasattr(globals(), "red_led")):
        #red_led   = pyb.LED(1)
    #if (not hasattr(globals(), "green_led")):
        #green_led = pyb.LED(2)
    #if (not hasattr(globals(), "blue_led")):
        #blue_led  = pyb.LED(3)

    camera = Camera()
    camera.set_framesize(sensor.QVGA)

    set_leds_to_waiting(None)

    run_menu_not_selected = True

    while(run_menu_not_selected):
        menu_option = camera.find_menu_item()
        print("menu item " + str(menu_option) + " found")
        if menu_option == 5:
            print("person's head")
            camera.set_camera_threshold(Threshold.BLUE)

        elif menu_option == 6:
            print("fish")
            print("calibrate throttle")

        elif menu_option == 173:
            print("h1")
            camera.set_camera_pixel_format_to_rgb()

        elif menu_option == 177:
            print("MTV")
            camera.set_camera_threshold(Threshold.YELLOW)

        elif menu_option == 256:
            print("AC/DC")
            print("calibrate steering")

        elif menu_option == 292:
            print("dog or cat")
            watchdog_enabled = True

        elif menu_option == 301:
            print("ghost")
            camera.set_camera_pixel_format_to_black_and_white()

        elif menu_option == 315:
            print("unknown")

        elif menu_option == 403:
            print("shoe")
            print("run")
            run_menu_not_selected = False

        if run_menu_not_selected:
            blue_led.off()
            green_led.on()
            two_second_timer = pyb.Timer(12)
            two_second_timer.init(freq=.5)
            two_second_timer.callback(set_leds_to_waiting)

    #for n in range(50):
        #line = camera.find_line()

        #if line and (line.magnitude() >= MAG_THRESHOLD):
            #print(line.magnitude())

    # Steps when starting
    # 1) Boot
    # 2) Settings
    # 3) Init
    # 4) Run


main()

camera.set_framesize(sensor.QVGA)

exec(open("pulse_led.py").read())
