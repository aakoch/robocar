# Servo Control Example
#
# This example shows how to use your OpenMV Cam to control servos.

import micropython, time
from pyb import Servo
micropython.alloc_emergency_exception_buf(100)

s1 = Servo(1) # P7

#s1.calibration(1000, 1500, 1100)
s1.calibration(640, 2420, 1500)
s1.angle(0)

time.sleep(2000)

print(s1.pulse_width())
print(s1.calibration())


i = -45
while(i < 45):
    print(i)
    s1.angle(i)
    print(s1.pulse_width())
    time.sleep(100)
    i += 1

# Car seems to start at 1390 PW which is speed -14 on default scale

# PWM:
# at 200hz with pw%=10, pw = 2160
# at 300hz with pw%=50, pw = 7200

#time.sleep(1000)

##s1.speed(5)
#s1.speed(0)

#print(s1.speed())
#print(s1.pulse_width())
#print(s1.calibration())

#i = 1
#while (True):
    #s1.speed(i)
    #print(i)
    #i -= 1
    #time.sleep(1000)

#0
#1500
#(
#min=640
#max=2420
#center=1500
#angle90=2470
#speed100=2200
#pulse_min is the minimum allowed pulse width.
#pulse_max is the maximum allowed pulse width.
#pulse_centre is the pulse width corresponding to the centre/zero position.
#pulse_angle_90 is the pulse width corresponding to 90 degrees.
#pulse_speed_100 is the pulse width corresponding to a speed of 100.
