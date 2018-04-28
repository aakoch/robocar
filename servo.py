# LED Control Example
#
# This example shows how to control your OpenMV Cam's built-in LEDs. Use your
# smart phone's camera to see the IR LEDs.

import time, utime, math, pyb

servo = pyb.Servo(1)
print(servo.pulse_width())
