# PWM Control Example
#
# This example shows how to do PWM with your OpenMV Cam.

import time, pyb
from pyb import Pin, Timer

#tim = pyb.Timer(4)              # create a timer object using timer 4
#tim.init(freq=2)                # trigger at 2Hz
#tim.callback(lambda t:pyb.LED(1).toggle())

#while(True):
    #time.sleep(1000)


pin = Pin("P7")
tim = Timer(4, freq=50) # Frequency in Hz
i = 1
## Generate a 1KHz square wave on TIM4 with 50% and 75% duty cycles on channels 1 and 2, respectively.
ch1 = tim.channel(1, Timer.PWM, pin=pin, pulse_width_percent=50)
##ch2 = tim.channel(2, Timer.PWM, pin=Pin("P8"), pulse_width_percent=75)

#pin.debug(True)

while (i < 20):
    #ch1.pulse_width_percent(i)
    tim.freq(i)
    print(i)
    #pin.value(0)
    time.sleep(2000)
    i += 1
    #pin.value(0)
    #time.sleep(1000)
