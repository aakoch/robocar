#copy_file.py
###############################################################
# Copy file
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-13
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import sensor, image, time, uos, uio

print(uos.listdir())

def copy_file(inFilename, outFilename):
    with uio.open(inFilename, "rt") as f1:
        with uio.open(outFilename, "wt") as f2:
            for line in f1:
                f2.write(line)
            f1.close()
            f2.close()

copy_file("donkey.py", "test.py")

print(uos.listdir())
