#read_analog_pin6.py

###############################################################
# Code for OpenMV M7 camera
# Read the analog input on pin 6
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-03
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################
from pyb import ADC

adc = ADC("P6") # Must always be "P6".

while(True):
    # The ADC has 12-bits of resolution for 4096 values.
    print("ADC = %d" % round(adc.read() / 200))
    time.sleep(100)
