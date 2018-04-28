import pyb, time
from pyb import LED

red_led  = LED(1)

adc = pyb.ADC(pyb.Pin("P6"))        # create an ADC on pin P6

tim = pyb.Timer(4, freq=200)         # create a timer running at 10Hz
#adc = pyb.ADCAll(12)
#v33 = 3.3 * 1.21 / adc.read_core_vref()
#print(v33)


while(True):
    red_led.off()
    buf = bytearray(16)                # creat a buffer to store the samples
    adc.read_timed(buf, tim)            # sample 100 values, taking 10s
    sums = 0
    for val in buf:                     # loop over all values
        print(val)
        sums += val
        if (val > 32):
            red_led.on()
            #time.sleep(100)
    print(sums)
    print(adc.read())

while(True):
    red_led.off()
    val = adc.read()          # sample 100 values, taking 10s
    if (val < 420 or val > 580):
        red_led.on()
        time.sleep(100)
    #for val in buf:                     # loop over all values
        #print(val)

#pin = pyb.Pin("P6")
#adc = pyb.ADC(pin)              # create an analog object from a pin
##adc = pyb.ADCAll(12)    # create an ADCAll object
#while(True):
    #val = adc.read()    # read an analog value
    ##if (val < 420 or val > 596):
    #print(val)
    ###val = adc.read_channel(channel) # read the given channel
    ###val = adc.read_core_temp()      # read MCU temperature
    ###val = adc.read_core_vbat()      # read MCU VBAT
    ###val = adc.read_core_vref()

###adc = pyb.ADCAll(resolution)    # create an ADCAll object
###val = adc.read_channel(channel) # read the given channel
###val = adc.read_core_temp()      # read MCU temperature
###val = adc.read_core_vbat()      # read MCU VBAT
###val = adc.read_core_vref()      # read MCU VREF

##adc = pyb.ADC(pyb.Pin("P6"))        # create an ADC on pin P6
##tim = pyb.Timer(4, freq=10)         # create a timer running at 10Hz
##buf = bytearray(10)                # creat a buffer to store the samples
##adc.read_timed(buf, tim)            # sample 100 values, taking 10s
##print(buf)
