# Timer - By: aakoch - Wed Dec 20 2017

# Arduino ref: https://www.arduino.cc/reference/en/language/functions/analog-io/analogread/
# This means that it will map input voltages between 0 and 5 volts into integer values
# between 0 and 1023. This yields a resolution between readings of: 5 volts / 1024 units
# or, .0049 volts (4.9 mV) per unit. The input range and resolution can be changed
# using analogReference().
# It takes about 100 microseconds (0.0001 s) to read an analog input, so the maximum
# reading rate is about 10,000 times a second.

# OpenMV ref: file:///Users/aakoch/.config/OpenMV/qtcreator/html/openmvcam/tutorial/analog_io.html?highlight=analog
# The OpenMV Cam has one analog I/O pin (P6) which can be used as an ADC input or DAC
# output. Here’s how to use it to read a voltage value between 0V and 3.3V:
# The ADC has 12-bits of resolution so it will output a value between 0 and 4095 for 0
# to 3.3 volts. Finally, note that while the pin is in ADC mode it is not 5V tolerant
# anymore.

# PulseSensor: https://pulsesensor.com/pages/open-hardware
# The only thing left to say about the electronics, on this inaugural version, is
# that it is optimized for both 5V and 3V. The circuit can be tuned by changing R1 & R3.
# R1 determines how much current goes to the LED, and R3 is the load resistor on the
# APDS output. To optimize for 5V, use higher R1 and higher R3 (R1:1K, R3:22K). For
# best results at 3V tweak the other way. 470 is as low as I have gone with R1. The
# super-brightness of the LED will saturate the sensor at higher currents, and it
# does get warm even when it's running at 20mA.

import pyb

adc = pyb.ADC(pyb.Pin('P6'))

while(True):
    pyb.delay(10) # wait 10 ms
    print("%f volts" % (((adc.read() * 3.3) + 2047.5) / 4095)) # read value, 0-4095


import sensor, image, time, pyb, stm

pin6 = pyb.Pin.board.P6

# The Arduino code uses a hardware Timer interrupt to measure the Pulse Sensor signal at an exact
# fixed rate (500Hz) in order to get high-quality BPM values.
global i, adc
i = None
adc = pyb.ADC(pin6)

def timerirq(v):
    global i
    i = adc.read()


tim = pyb.Timer(4)              # create a timer object using timer 4
tim.init(freq=500)                # trigger at 2Hz
tim.callback(lambda t:timerirq)

           # create an analog object from a pin


while(True):
    #print("v33=" + str(v33()))
    #print("vbat=" + str(vbat()))
    #print("vref=" + str(vref()))
    #print("temperature=" + str(temperature()))
    #print("ADC=" + str(adcread(16)))
    #print(pin6.value())
    if (i != None):
        print(i)

    time.sleep(50)
