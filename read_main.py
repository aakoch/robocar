#read_main.py
###############################################################
# Code for OpenMV M7 camera
# Read contents of "main.py"
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-03
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import uio

file = uio.open("main.py", "rt")
print("file contents:")
print(file.read());
file.close()
