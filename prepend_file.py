# prepend_file.py

###############################################################
# Code for OpenMV M7 camera
# Goal is to prepend the name of the file to the file - Work in progress
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-03
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import time, pyb, uio, uos

connectedToUsb = pyb.USB_VCP().isconnected()


def insert(originalfile,string):
    with open(originalfile,'r') as f:
        with open('newfile.txt','w') as f2:
            f2.write(string)
            f2.write(f.read())
    uos.rename('newfile.txt',originalfile)

#insert("main.py", "#main.py\n");


print("current directory=%s" % uos.getcwd())
print("directory contents=%s" % uos.listdir())

#if (connectedToUsb):
    #file = uio.open("main.py", "rt")
    ## if the first line is a comment with just the name of the original filename, then this will extract it
    #original_filename = file.readline()[1:].strip()
    #print(original_filename)
    #file.close()

#filename = "pulse_led.py"
#file = uio.open(filename, "wt")
#file.write("#" + filename + "\n")
#file.flush()
#file.close()

#uos.rename(filename, "main.py")
