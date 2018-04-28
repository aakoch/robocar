# LED Control Example
#
# This example shows how to control your OpenMV Cam's built-in LEDs. Use your
# smart phone's camera to see the IR LEDs.

import time, utime, math, pyb

from pyb import Pin, ExtInt
from pyb import LED

red_led   = LED(1)

old = utime.ticks_us()
#old2 = utime.ticks_us()
#new = utime.ticks_ms()
#i = 0
diff = 1

sum = 0
count = 0

def callback(e):
    print(e)
    #global diff, old #, count
    #diff = utime.ticks_diff(old, utime.ticks_us())
    #if (diff > 13):
        #print(diff)
    #old = utime.ticks_us()
    ##count += 1
    ##red_led.on()
    ##utime.sleep_us(10)

max1 = 0

ext = ExtInt(Pin('P7'), ExtInt.IRQ_RISING, Pin.PULL_NONE, callback)

def redledon(pct):
    red_led.on()
    utime.sleep_us(max1)
    red_led.off()
    utime.sleep_us(100 - max1)


while(True):
    #print(str(count) + " times")
    #print(1 / (diff - 10) * 500)
    #redledon(round(1 / (diff - 10) * 500))
    #red_led.off()
    time.sleep(100)
    #count = 0
    #redledon(50)
    #max1 = max(count, max1)
    #print(max1)
    #count = 0


#servo = pyb.Servo(1)
#print(servo.pulse_width())
#print(servo.speed())
#print(servo.angle())

#i = 0;


#servo.pulse_width(1000)

#servo.speed(50)

##while i < 2421:
    ##print(i)
    ##servo.pulse_width(i)
    ##time.sleep(10)
    ##i += 1

###servo.pulse_width(2420)
##servo.calibration(0, 2420, 500)

###servo.angle(50)
### original calibration: 640, 2420, 1500, 2470, 2200
##servo.speed(100, 2)

##print(servo.pulse_width())
##print(servo.speed())
##print(servo.angle())

#time.sleep(2000)
###servo.speed(0)

###print(servo.pulse_width())
###print(servo.speed())
###print(servo.angle())
##servo.calibration(640, 2420, 1500) #, 2470, 2200)
