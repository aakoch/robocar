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

MIN_T = 1599
MAX_T = 1650

throttle = 1550
steering = 1500

t = 0

def t2throttle(t):
    return t * ((MAX_T - MIN_T) / 100) + MIN_T


def read_from_uart():
    read_count = 15
    chars = ""
    while uart.any() and chars[:-1] != "\n" and read_count > 0:
        read_char = str(uart.read(1).decode("utf-8"))
        chars = chars + read_char
        read_count = read_count - 1
    return chars


while(t <= 100):
    throttle = t2throttle(t)
    #print("%f %f" % (t, throttle))
    #pyb.LED(2).toggle()
    #uart.write("{000020,121113}\n")
    #i = 0
#while i < 3:
    uart.write("{%05d,%05d}\r\n" % (throttle, steering))
    if uart.any():
        received_from_uart = read_from_uart()
        if (received_from_uart):
            pyb.LED(3).toggle()
            print("received=" + received_from_uart[:-1])
        if uart.any():
            uart.read()

    print("throttle @ %02d -> sent={%05d,%05d}\r" % (t, throttle, steering))

        #i = i + 1

    #throttle = throttle + 10
    #steering = steering - 1
    t = t + 1
