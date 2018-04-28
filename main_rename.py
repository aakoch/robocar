# main_rename.py
# Goal is to open the script "main.py" and rename it to the original name.

import time, pyb, uio, uos

connectedToUsb = pyb.USB_VCP().isconnected()

#if (connectedToUsb):
    #file = uio.open("main.py", "rt")
    ## if the first line is a comment with just the name of the original filename, then this will extract it
    #original_filename = file.readline()[1:].strip()
    #print(original_filename)
    #file.close()

filename = "pulse_led.py"
file = uio.open(filename, "wt")
file.write("#" + filename + "\n")
file.flush()
file.close()

uos.rename(filename, "main.py")
