#reset.py

###############################################################
# Code for OpenMV M7 camera
# Save the reset status to a file named "reset_status.txt". No luck with anything but "False" being written.
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-03
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################
import time, pyb, uio, uos, machine
from pyb import RTC

rtc = RTC()

filename = "reset_status.txt"
connectedToUsb = pyb.USB_VCP().isconnected()

if (connectedToUsb):
    print("current directory=%s" % uos.getcwd())
    print("directory contents=%s" % uos.listdir())

    file = uio.open(filename, "rt")
    #print("file contents:")
    #print(file.read());
    lines = str.split(file.read());

    powerOnReset = str.split(lines[0], "=")[1]
    externalReset = str.split(lines[1], "=")[1]
else:
    powerOnReset = rtc.info() & 0x00010000 != 0;
    externalReset = rtc.info() & 0x00020000 != 0;
    file = uio.open(filename, "wt")
    file.write("powerOnReset=%s\n" % powerOnReset);
    file.write("externalReset=%s\n" % externalReset);
    file.flush()

file.close()


if (connectedToUsb):
    print("powerOnReset=%s, externalReset=%s" %(powerOnReset, externalReset))

    rtc.wakeup(5000)

    # Enter Deepsleep Mode.
    #machine.deepsleep()
