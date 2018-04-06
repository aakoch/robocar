#rename_files.py
###############################################################
# Code for OpenMV M7 camera
# Goal is to rename the "pulse_led.py" file to "main.py" and reset the camera - Work in progress
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-03
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import uos, machine, pyb

uos.sync()

print("current directory=%s" % uos.getcwd())
print("directory contents=%s" % uos.listdir())

undo = False

if (undo):
    uos.rename("main.py", "pulse_led.py")
    uos.rename("main_backup.py", "main.py")
else:
    uos.rename("main.py", "main_backup.py")
    uos.rename("pulse_led.py", "main.py")
uos.sync()

print("current directory=%s" % uos.getcwd())
print("directory contents=%s" % uos.listdir())


if (not undo):
    pyb.delay(500)
    machine.reset()
