import pyb, stm

def ctof(c):
    return c * 9 / 5 + 32

def adcread(chan):                              # 16 temp 17 vbat 18 vref
    assert chan >= 16 and chan <= 18, 'Invalid ADC channel'
    start = pyb.millis()
    timeout = 100
    stm.mem32[stm.RCC + stm.RCC_APB2ENR] |= 0x100 # enable ADC1 clock.0x4100
    stm.mem32[stm.ADC1 + stm.ADC_CR2] = 1       # Turn on ADC
    stm.mem32[stm.ADC1 + stm.ADC_CR1] = 0       # 12 bit
    if chan == 17:
        stm.mem32[stm.ADC1 + stm.ADC_SMPR1] = 0x200000 # 15 cycles
        stm.mem32[stm.ADC + 4] = 1 << 23
    elif chan == 18:
        stm.mem32[stm.ADC1 + stm.ADC_SMPR1] = 0x1000000
        stm.mem32[stm.ADC + 4] = 0xc00000
    else:
        stm.mem32[stm.ADC1 + stm.ADC_SMPR1] = 0x40000
        stm.mem32[stm.ADC + 4] = 1 << 23
    stm.mem32[stm.ADC1 + stm.ADC_SQR3] = chan
    stm.mem32[stm.ADC1 + stm.ADC_CR2] = 1 | (1 << 30) | (1 << 10) # start conversion
    while not stm.mem32[stm.ADC1 + stm.ADC_SR] & 2: # wait for EOC
        if pyb.elapsed_millis(start) > timeout:
            raise OSError('ADC timout')
    data = stm.mem32[stm.ADC1 + stm.ADC_DR]     # clear down EOC
    stm.mem32[stm.ADC1 + stm.ADC_CR2] = 0       # Turn off ADC
    return data

def v33():
    return 4096 * 1.21 / adcread(17)

def vbat():
    return  1.21 * 2 * adcread(18) / adcread(17)  # 2:1 divider on Vbat channel

def vref():
    return 3.3 * adcread(17) / 4096

def temperature():
    return 25 + 400 * (3.3 * adcread(16) / 4096 - 0.76)

print(v33())
print(vbat())
print(vref())
print(ctof(temperature()))
