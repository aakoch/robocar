#clock.py

###############################################################
# Utility for real-time clock operations and the creation of a
# time-based filename
#
# Some code was taken from stackoverflow.com. See comment
# below.
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-18
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################
import time
from pyb import RTC

rtc = RTC()

def create_time_based_filename():
    datetime = rtc.datetime()
    #print(datetime)
    return "{0}{1:02d}{2:02d}{3:02d}{4:02d}{5:02d}".format(datetime[0], datetime[1], datetime[2], \
            datetime[4], datetime[5], datetime[6])

def set_time(year, month, day, hour, minute):
    """Set the internal clock of the OpenMV camera"""

    # https://stackoverflow.com/a/17120430/137581
    #weekday is 1-7 for Monday through Sunday.
    offset = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    afterFeb = 1
    if month > 2: afterFeb = 0
    aux = year - 1700 - afterFeb
    # dayOfWeek for 1700/1/1 = 5, Friday
    dayOfWeek  = 5
    # partial sum of days betweem current date and 1700/1/1
    dayOfWeek += (aux + afterFeb) * 365
    # leap year correction
    dayOfWeek += aux / 4 - aux / 100 + (aux + 100) / 400
    # sum monthly and day offsets
    dayOfWeek += offset[month - 1] + (day - 1)
    dayOfWeek %= 7

    rtc.datetime((year, month, day, round(dayOfWeek), hour, minute, 0, 0))

#set_time(2018, 5, 5, 22, 25)
#print(create_time_based_filename())
#print(weekday(2018, 4, 18)[1])
#print(rtc.datetime())
