# LED Control Example
#
# This example shows how to control your OpenMV Cam's built-in LEDs. Use your
# smart phone's camera to see the IR LEDs.

import time, utime, math
from pyb import LED

red_led   = LED(1)
green_led = LED(2)
blue_led  = LED(3)
#ir_led    = LED(4)

i = 0.
up = True


while(True):
    i += .005

    j = abs(round(math.sin(i) * 400))
    k = abs(round(math.sin(i + .3) * 400))
    m = abs(round(math.sin(i + .3) * 400))
    print(i, j, k)
    red_led.on()
    utime.sleep_us(abs(j - (k + m)))
    blue_led.on()
    utime.sleep_us(abs(k - (j + m)))
    green_led.on()
    utime.sleep_us(abs(m - (j + k)))

    red_led.off()
    utime.sleep_us(1000 - abs(j - (k + m)))
    blue_led.off()
    utime.sleep_us(1000 - abs(k - (j + m)))
    green_led.off()
    utime.sleep_us(1000 - abs(m - (j + k)))

