#constants.py
###############################################################
# Constants
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-05
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import micropython, pyb
from micropython import const
AREA_THRESHOLD = const(20)
PIXELS_THRESHOLD = const(20)

# This is a serial port object that allows you to
# communciate with your computer. While it is not open the code below runs.
usb_is_connected = pyb.USB_VCP().isconnected()

MAG_THRESHOLD = const(8)
