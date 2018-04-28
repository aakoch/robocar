# LED Control Example
#
# This example shows how to control your OpenMV Cam's built-in LEDs. Use your
# smart phone's camera to see the IR LEDs.

import time, utime, math, pyb

from pyb import Pin, ExtInt

old = utime.ticks_us()
#new = utime.ticks_ms()
#i = 0

def callback(e):
    print(utime.ticks_diff(old, utime.ticks_us()))
    #old = utime.ticks_ms()



ext = ExtInt(Pin('P7'), ExtInt.IRQ_RISING, Pin.PULL_NONE, callback)

while(True):
    old = utime.ticks_us()
    #time.sleep(1000)

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
