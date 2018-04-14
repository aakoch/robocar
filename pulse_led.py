#pulse_led.py
###############################################################
# Code for OpenMV M7 camera
# Pulsates LEDs between red, green, blue
# Author: Adam A. Koch (aakoch)
# Date: 2018-03-22
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import time, pyb, math, micropython
from pyb import Timer

DEG_120 = micropython.const(round(2 * math.pi / 3)) # 2PI/3 = 120º
DEG_240 = micropython.const(round(4 * math.pi / 3)) # 4PI/3 = 240º
RBG_MAX = micropython.const(97)

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

# old
#if (not hasattr(globals(), "red_led")):
    #red_led   = pyb.LED(1)
#if (not hasattr(globals(), "green_led")):
    #green_led = pyb.LED(2)
#if (not hasattr(globals(), "blue_led")):
    #blue_led  = pyb.LED(3)

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

def set_pw_colors(i):
    red_on =   max(0, math.sin(i) * RBG_MAX)
    green_on = max(0, math.sin(i - DEG_120) * RBG_MAX)
    blue_on =  max(0, math.sin(i - DEG_240) * RBG_MAX)

    print("%f %f %f" % (red_on, blue_on, green_on))

    red_channel.  pulse_width_percent(red_on)
    green_channel.pulse_width_percent(green_on)
    blue_channel. pulse_width_percent(blue_on)

tim = Timer(4, freq=50, callback=leds_on)

red_channel =   tim.channel(1, Timer.PWM, callback=red_led_off,   pulse_width_percent=0)
green_channel = tim.channel(2, Timer.PWM, callback=green_led_off, pulse_width_percent=0)
blue_channel =  tim.channel(3, Timer.PWM, callback=blue_led_off,  pulse_width_percent=0)

while (True):
    set_pw_colors(pyb.millis() / 1000)
    pyb.udelay(tim.period())
