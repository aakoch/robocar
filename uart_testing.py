# UART Control
#
# This example shows how to use the serial port on your OpenMV Cam. Attach pin
# P4 to the serial input of a serial LCD screen to see "Hello World!" printed
# on the serial LCD display.

import time, pyb
from pyb import UART

# Always pass UART 3 for the UART number for your OpenMV Cam.
# The second argument is the UART baud rate. For a more advanced UART control
# example see the BLE-Shield driver.
uart = UART(3, 19200, timeout = 1000)

pyb.LED(3).off()
pyb.LED(1).on()
time.sleep(1000)
pyb.LED(1).off()

while(True):
    #pyb.LED(2).toggle()
    uart.write("Hello World!\n")
    time.sleep(200)
    if (uart.any()):
        pyb.LED(3).toggle()
        uartInput = uart.read()
        print(uartInput.decode("utf-8") )
