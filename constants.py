#constants.py
###############################################################
# Constants
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-05
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import micropython, pyb, math
from micropython import const
AREA_THRESHOLD = const(20)
PIXELS_THRESHOLD = const(20)

# This is a serial port object that allows you to
# communciate with your computer. While it is not open the code below runs.
usb_is_connected = pyb.USB_VCP().isconnected()

MAG_THRESHOLD = const(8)

DEG_120 = micropython.const(round(2 * math.pi / 3)) # 2PI/3 = 120º
DEG_240 = micropython.const(round(4 * math.pi / 3)) # 4PI/3 = 240º
RBG_MAX = micropython.const(97)
LED_TIMER_ID = micropython.const(4)
