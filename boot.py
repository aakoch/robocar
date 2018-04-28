#boot.py
###############################################################
# First thing ran by robot
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-05
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import machine, pyb
from machine import WDT
from constants import *
from reset_functions import *
from file_utils import *

# Steps when starting
# 1) Boot
# 2) Settings
# 3) Init
# 4) Run

# this will check, and then if the reset was due to the watchdog, it will run the pulse LED file
check_reset_cause()

conf = ConfigFile()
boot = conf.get_property("boot")

print("boot=%s" % boot)

if (boot == "menu"):
    print("display menu")
    conf.delete_property("boot")
    exec(open("menu.py").read())
    conf.set_property("boot", "run")
elif (boot == "run"):
    print("run car")
    conf.delete_property("boot")
    #copy_file("donkey.py", "main.py")
else:
    print("no boot. setting to menu")
    conf.set_property("boot", "menu")


