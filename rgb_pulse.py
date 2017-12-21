###############################################################
# Code for OpenMV M7 camera
# Pulsates LEDs between red, green, blue
# Author: Adam A. Koch (aakoch)
# Date: 2017-12-20
# Copyright (c) 2017 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import utime as time, pyb, math, micropython

red_led   = pyb.LED(1)
green_led = pyb.LED(2)
blue_led  = pyb.LED(3)

deg_120 = round(2 * math.pi / 3) # 2PI/3 = 120º
deg_240 = round(4 * math.pi / 3) # 4PI/3 = 240º
CONST_RBG_MAX = micropython.const(255)

i = math.pi / 2 # offset with red on at full to start

while(True):

    i += .0015 # nice, slow speed -- set it to whatever you like

    red_on = max(0, round(math.sin(i) * CONST_RBG_MAX))
    green_on = max(0, round(math.sin(i - deg_120) * CONST_RBG_MAX))
    blue_on = max(0, round(math.sin(i - deg_240) * CONST_RBG_MAX))

    print(red_on, green_on, blue_on)

    red_led.on()
    time.sleep_us(red_on)

    red_led.off()
    time.sleep_us(255 - red_on)

    green_led.on()
    time.sleep_us(green_on)

    green_led.off()
    time.sleep_us(255 - green_on)

    blue_led.on()
    time.sleep_us(blue_on)

    blue_led.off()
    time.sleep_us(255 - blue_on)
