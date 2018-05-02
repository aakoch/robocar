# reset_cause.py

import machine, pyb

print("reset cause=%s" % machine.reset_cause())

# run the pulse_led.py script if the board was reset because of the watchdog
if (machine.reset_cause() == machine.WDT_RESET):
    print("reset was caused by WDT_RESET")
    exec(open("pulse_led.py").read())
else:
    pass
    wdt = machine.WDT(timeout=5000)  # enable it with a timeout of 5s

if (machine.reset_cause() == machine.PWRON_RESET):
    print("reset was caused by PWRON_RESET")
elif (machine.reset_cause() == machine.HARD_RESET):
    print("reset was caused by HARD_RESET")
elif (machine.reset_cause() == machine.DEEPSLEEP_RESET):
    print("reset was caused by DEEPSLEEP_RESET")
elif (machine.reset_cause() == machine.SOFT_RESET):
    print("reset was caused by SOFT_RESET")
# otherwise, cause the watchdog to reset (don't really do this)

while True:

    wdt.feed()
    print("going to wait 1 second/s...")
    pyb.delay(1000)
