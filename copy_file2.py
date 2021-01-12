__filename__ = "copy_file2.py"
###############################################################
# Copy file
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-13
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################
import uos, machine, log
from led_functions import *
from class_led_controller import *

# ############################################
# Copies *text* files
# ############################################
def copy_file(inFilename, outFilename):
    with open(inFilename, "rt") as f1:
        with open(outFilename, "wt") as f2:
            for line in f1:
                f2.write(line)
            f1.close()
            f2.close()

def file_exists(filename):
    for file in uos.ilistdir():
        if (file[0] == filename):
            return True

    return False

def read_first_line(filename):
    if file_exists:
        file = open(filename, "rt")
        line = file.readline()
        file.close()
        return line
    else:
        raise ArgumentError(filename + " doesn't exist")


def read_first_line_or_blank(filename):
    try:
        line = read_first_line(filename)
        return line
    except RuntimeError:
        warn("File", filename, "doesn't exist")
        return ""

# ########################################################
# Swaps what is currently in main.py into the original
# file name as determined by the first line of the
# script.
# 'filename' is the name of the file to copy into main.py
# ########################################################
def swap_main(filename):
    first_line_in_main = read_first_line("main.py")

    # assert that the first line starts with "#" and ends with ".py"
    if (first_line_in_main and first_line_in_main[0] == "#" and \
            len(first_line_in_main) > 3 and first_line_in_main.strip()[-3:] == ".py"):
        main_original_filename = first_line_in_main[1:-3]

        if file_exists(filename):
            pass
        elif file_exists(filename + ".py"):
            filename += ".py"

        if file_exists(filename):
            copy_file("main.py", main_original_filename)
            copy_file(filename, "main.py")
        else:
            raise RuntimeError(filename, "not found")

    elif (first_line_in_main and len(first_line_in_main) > 12 and \
            first_line_in_main[0:12] == "__filename__"):

        exec(first_line_in_main)

        main_original_filename = __filename__

        if file_exists(filename):
            pass
        elif file_exists(filename + ".py"):
            filename += ".py"

        if file_exists(filename):
            copy_file("main.py", main_original_filename)
            copy_file(filename, "main.py")
        else:
            raise RuntimeError(filename, "not found")
    else:
        raise RuntimeError("Could not determine what file to move main.py to. first_line_in_main=" + first_line_in_main)



#pyb.delay(200)
#LedController().pulse(5000)

#red_led.off()
#green_led.off()
#blue_led.off()

#blue_led.on()
#pyb.delay(2000)
#swap_main("class_led_controller.py")
#machine.reset()

#print(uos.listdir())
#first_line_in_main = read_first_line("main.py")
#print("the first line is", first_line_in_main)

### to trim a string in python, use strip()
##if (line.strip() == "#copy_file.py" and file_exists("pulse_led.py")):
    ##print("main file is copy_file.py")

    ##copy_file("main.py", "copy_file.py")
    ##copy_file("pulse_led.py", "main.py")
    ##machine.reset()

##elif not file_exists("pulse_led.py"):
    ##print("pulse_led.py file does not exist")

##elif line.strip() != "#copy_file.py":
    ##print("the first line in main.py is not this script")

#print(uos.listdir())
