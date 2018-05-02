#class_led_controller.py
################################################################################
# Class to encapsulate the pulsating LED code I originally had in pulse_led.py.
#
# Pulsates LEDs between red, green, blue
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-05-01
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
################################################################################

import time, pyb, math, micropython
from pyb import Timer
from constants import *
from log import *

class LedController():

    def __init__(self):
        self.red_led =   pyb.LED(1)
        self.green_led = pyb.LED(2)
        self.blue_led =  pyb.LED(3)

        self.led_timer = Timer(LED_TIMER_ID, freq=50, callback=self.leds_on)

        self.red_channel =   self.led_timer.channel(1, Timer.PWM, callback=self.red_led_off,   pulse_width_percent=0)
        self.green_channel = self.led_timer.channel(2, Timer.PWM, callback=self.green_led_off, pulse_width_percent=0)
        self.blue_channel =  self.led_timer.channel(3, Timer.PWM, callback=self.blue_led_off,  pulse_width_percent=0)

    def leds_on(self, timer):
        self.red_led.on()
        self.green_led.on()
        self.blue_led.on()

    def red_led_off(self, timer):
        self.red_led.off()

    def green_led_off(self, timer):
        self.green_led.off()

    def blue_led_off(self, timer):
        self.blue_led.off()

    def set_pw_colors(self, i, red_channel, green_channel, blue_channel):
        red_on =   max(0, math.sin(i) * RBG_MAX)
        green_on = max(0, math.sin(i - DEG_120) * RBG_MAX)
        blue_on =  max(0, math.sin(i - DEG_240) * RBG_MAX)

        debug("%f %f %f" % (red_on, blue_on, green_on))

        self.red_channel.  pulse_width_percent(red_on)
        self.green_channel.pulse_width_percent(green_on)
        self.blue_channel. pulse_width_percent(blue_on)

    def pulse(self, duration_ms):
        startTime = pyb.millis()
        while (duration_ms < 0 or pyb.elapsed_millis(startTime) < duration_ms):
            self.set_pw_colors(pyb.millis() / 1000, self.red_channel, self.green_channel, self.blue_channel)
            pyb.udelay(self.led_timer.period())

pyb.delay(200)
LedController().pulse(12000)
