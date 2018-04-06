# reset_cause.py

import machine, pyb
from machine import WDT
wdt = WDT(timeout=4000)  # enable it with a timeout of 5s

i = 0

# run the pulse_led.py script if the board was reset because of the watchdog
if (machine.reset_cause() == machine.WDT_RESET):
    exec(open("pulse_led.py").read())
# otherwise, cause the watchdog to reset (don't really do this)
else:
    while True:
        wdt.feed()
        print("going to wait " + str(i) + " second/s...")
        pyb.delay(1000 * i)
        i += 1
