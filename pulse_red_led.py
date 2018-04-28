# Timer Control Example
#
# This example shows how to use a timer for callbacks.

import time, pyb
from pyb import Pin, Timer

red_led   = pyb.LED(1)

def tick(timer):            # we will receive the timer object when being called
    red_led.on()

def tick2(timer):            # we will receive the timer object when being called
    red_led.off()

tim = Timer(4, freq=200)      # create a timer object using timer 4 - trigger at 1Hz
tim.callback(tick)          # set the callback to our tick function
channel = tim.channel(1, Timer.PWM, callback=tick2, pulse_width_percent=50)
i = 0
increment = True

while (True):
    time.sleep(10)
    channel.pulse_width_percent(i)
    #tim.period(i)
    if increment:
        i = i + 1
    else:
        i = i - 1

    print(i)
    if i > 98:
        increment = False
    if i < 2:
        increment = True
