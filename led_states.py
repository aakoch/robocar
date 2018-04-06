#led_states.py
###############################################################
# Pulses blue LED until April tag is found.
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-05
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import sensor, image, time, pyb, micropython, math, machine
from pyb import Timer

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.skip_frames(time = 1200)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()

def degrees(radians):
    return (180 * radians) / math.pi

DEG_120 = micropython.const(round(2 * math.pi / 3)) # 2PI/3 = 120º
DEG_240 = micropython.const(round(4 * math.pi / 3)) # 4PI/3 = 240º
RBG_MAX = micropython.const(97)
PULSE_ALL = micropython.const(0)
READY_FOR_INPUT = micropython.const(1)
GOT_INPUT = micropython.const(2)

red_led   = pyb.LED(1)
green_led = pyb.LED(2)
blue_led  = pyb.LED(3)
led_timer = None
red_channel =  None
green_channel = None
blue_channel = None

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

def init_led_timers():
    global led_timer, red_channel, green_channel, blue_channel
    led_timer = Timer(4, freq=50, callback=leds_on)
    red_channel =   led_timer.channel(1, Timer.PWM, callback=red_led_off,   pulse_width_percent=0)
    green_channel = led_timer.channel(2, Timer.PWM, callback=green_led_off, pulse_width_percent=0)
    blue_channel =  led_timer.channel(3, Timer.PWM, callback=blue_led_off,  pulse_width_percent=0)

def set_pw_colors(i):
    i = i / 1000
    if (state == PULSE_ALL):
        red_on =   max(0, math.sin(i) * RBG_MAX)
        green_on = max(0, math.sin(i - DEG_120) * RBG_MAX)
        blue_on =  max(0, math.sin(i - DEG_240) * RBG_MAX)

    elif (state == READY_FOR_INPUT):
        red_on =   0
        green_on = 0
        blue_on = (math.sin(i * 3) + 1.0) / 2.0 * RBG_MAX

    #print("%f %f %f %f" % (i, red_on, blue_on, green_on))

    red_channel.  pulse_width_percent(red_on)
    green_channel.pulse_width_percent(green_on)
    blue_channel. pulse_width_percent(blue_on)

def ease(t):
    sqt = t * t;
    return sqt / (2.0 * (sqt - t) + 1.0)


init_led_timers()


def wait_for_april_tag():
    global state
    state = READY_FOR_INPUT
    while (state == READY_FOR_INPUT):
        set_pw_colors(time.ticks())

        # if not taking snapshots, delay
        #pyb.udelay(led_timer.period())

        clock.tick() # for fps()
        img = sensor.snapshot()

        for tag in img.find_apriltags():
            state = GOT_INPUT
            sensor.flush()
        #print(clock.fps())
    return tag.id();

def acknowledge_input():
    led_timer.deinit()
    red_led.off()
    green_led.on()
    blue_led.off()
    pyb.delay(2000)
    green_led.off()

#def woken_up(rtc):
    #red_led.toggle()
    #print("I woke up at %s" % rtc.datetime())

while (True):
    tagId = wait_for_april_tag()
    print("Found tag id %d" % tagId)

    acknowledge_input()

    if tagId == 347:
        pyb.delay(50)
        machine.reset()
    elif tagId == 346:
        #rtc = pyb.RTC()
        #rtc.wakeup(1000, woken_up)
        #machine.sleep()


