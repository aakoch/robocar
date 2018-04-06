import pyb
from machine import WDT
wdt = WDT(timeout=5000)  # enable it with a timeout of 5s

i = 0
while True:
    wdt.feed()
    print("going to wait " + str(i) + " second/s...")
    pyb.delay(1000 * i)
    i += 1
