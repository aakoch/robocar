#file_utils.py
"""Utility methods for files."""

__author__ = "Adam A. Koch (aakoch)"
__date__ = "2018-05-01"
__copyright__ = "Copyright (c) 2018 Adam A. Koch"
__license__ = "MIT"
__filename__ = "file_utils.py"

import uos
import machine
import log
from led_functions import *

def copy_file(inFilename, outFilename):
    """Copies *text* files."""
    with open(inFilename, "rt") as f1:
        with open(outFilename, "wt") as f2:
            for line in f1:
                f2.write(line)
            f1.close()
            f2.close()

def file_exists(filename):
    """Tests for the existence of a file"""
    for file in uos.ilistdir():
        if (file[0] == filename):
            return True

    return False

def read_first_line(filename):
    """Read the first line from a text file or throws a RuntimeError if not found"""
    if file_exists(filename):
        file = open(filename, "rt")
        line = file.readline()
        file.close()
        return line
    else:
        raise RuntimeError(filename + " doesn't exist")

def read_first_line_or_blank(filename):
    """Read the first line from a text file or if not found returns an
    empty string"""
    try:
        line = read_first_line(filename)
        return line
    except RuntimeError:
        warn("File", filename, "doesn't exist")
        return ""

def swap_main(filename):
    """Swaps what is currently in main.py into the original file name as
    determined by the first line of the script.

    Parameters
       ----------
       filename : str
           Name of the file to copy into main.py"""

    first_line_in_main = read_first_line("main.py")

    # assert that the first line starts with "#" and ends with ".py"
    if (first_line_in_main and first_line_in_main[0] == "#" and \
            len(first_line_in_main) > 3 and first_line_in_main.strip()[-3:] == ".py"):
        main_original_filename = first_line_in_main[1:-3].strip() # if there is a space between # and the filename

        if file_exists(filename + ".py"):
            filename += ".py"

        if file_exists(filename):
            copy_file("main.py", main_original_filename)
            copy_file(filename, "main.py")
        else:
            raise RuntimeError(filename, "not found")
    else:
        raise RuntimeError("Could not determine what file to move main.py to. first_line_in_main=" + first_line_in_main)

#green_led.on()
#pyb.delay(1000)
#swap_main("copy_file.py")
#machine.reset()
