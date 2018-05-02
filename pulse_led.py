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
from constants import *
from led_functions import *

pyb.delay(200)

class LedController():
    def __init__(self):
        self.led_timer = Timer(LED_TIMER_ID, freq=50, callback=leds_on)

        self.red_channel =   self.led_timer.channel(1, Timer.PWM, callback=red_led_off,   pulse_width_percent=0)
        self.green_channel = self.led_timer.channel(2, Timer.PWM, callback=green_led_off, pulse_width_percent=0)
        self.blue_channel =  self.led_timer.channel(3, Timer.PWM, callback=blue_led_off,  pulse_width_percent=0)

    def pulse(self):
        startTime = pyb.millis()
        while (pyb.elapsed_millis(startTime) < 12000):
            set_pw_colors(pyb.millis() / 1000, self.red_channel, self.green_channel, self.blue_channel)
            pyb.udelay(self.led_timer.period())

LedController().pulse()
