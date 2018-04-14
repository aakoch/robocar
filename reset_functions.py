#reset_functions.py
###############################################################
# Functions to check why the last reset took place.
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-05
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import machine, pyb

def check_reset_cause():

    # run the pulse_led.py script if the board was reset because of the watchdog
    if (machine.reset_cause() == machine.WDT_RESET):
        print("reset was caused by watchdog")
        exec(open("pulse_led.py").read())
        pyb.delay(2000)
        machine.reset()
        pyb.delay(1000)
    elif (machine.reset_cause() == machine.PWRON_RESET):
        print("reset was caused by PWRON_RESET")
    elif (machine.reset_cause() == machine.HARD_RESET):
        print("reset was caused by HARD_RESET")
    elif (machine.reset_cause() == machine.DEEPSLEEP_RESET):
        print("reset was caused by DEEPSLEEP_RESET")
    elif (machine.reset_cause() == machine.SOFT_RESET):
        print("reset was caused by SOFT_RESET")
    else:
        print("reset cause is unknown number=" + str(machine.reset_cause()))

    return machine.reset_cause()
