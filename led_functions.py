#led_functions.py
"""
###############################################################
# Functions for the LEDs
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-05-01
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################
"""

import pyb
from constants import *

try:
    red_led.toggle()
except NameError:
    red_led = pyb.LED(1)

try:
    green_led.toggle()
except NameError:
    green_led = pyb.LED(2)

try:
    blue_led.toggle()
except NameError:
    blue_led = pyb.LED(3)

def leds_on(timer):
    red_led.on()
    green_led.on()
    blue_led.on()

def red_led_off(timer):
    red_led.off()

def green_led_off(timer):
    green_led.off()

def blue_led_off(timer):
    blue_led.off()

def set_pw_colors(i, red_channel, green_channel, blue_channel):
    red_on =   max(0, math.sin(i) * RBG_MAX)
    green_on = max(0, math.sin(i - DEG_120) * RBG_MAX)
    blue_on =  max(0, math.sin(i - DEG_240) * RBG_MAX)

    print("%f %f %f" % (red_on, blue_on, green_on))

    red_channel.pulse_width_percent(red_on)
    green_channel.pulse_width_percent(green_on)
    blue_channel.pulse_width_percent(blue_on)
