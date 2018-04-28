# PWM Control Example
#
# This example shows how to do PWM with your OpenMV Cam.

import time
from pyb import Pin, Timer

hz = 300
pw = 50
tim = Timer(4, freq=hz) # Frequency in Hz
#print("period=" + str(tim.period()))
#print("prescaler=" + str(tim.prescaler()))

while (True):
    print("hz=" + str(hz) + ", pw=" + str(pw))
    # Generate a 1KHz square wave on TIM4 with 50% and 75% duty cycles on channels 1 and 2, respectively.
    ch1 = tim.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=pw)
    #hz += 10
    print(ch1.pulse_width())
    time.sleep(1000)

# at 200hz with pw%=10, pw = 2160
# at 300hz with pw%=50, pw = 7200


#pw = 60
#while (pw < 90):
    #print("hz=" + str(hz) + ", pw=" + str(pw))
    #tim = Timer(4, freq=hz) # Frequency in Hz
    ## Generate a 1KHz square wave on TIM4 with 50% and 75% duty cycles on channels 1 and 2, respectively.
    #ch1 = tim.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=pw)
    ##ch2 = tim.channel(2, Timer.PWM, pin=Pin("P8"), pulse_width_percent=75)
    #time.sleep(50)
    #pw += 2
    ##hz += 10


#while (pw > 40):
    #print("hz=" + str(hz) + ", pw=" + str(pw))
    #tim = Timer(4, freq=hz) # Frequency in Hz
    ## Generate a 1KHz square wave on TIM4 with 50% and 75% duty cycles on channels 1 and 2, respectively.
    #ch1 = tim.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=pw)
    ##ch2 = tim.channel(2, Timer.PWM, pin=Pin("P8"), pulse_width_percent=75)
    #time.sleep(1000)
    #pw -= 1
    ##hz += 10

