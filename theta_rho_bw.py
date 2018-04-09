#######################################################################
# Draws a line matching the line found using get_regression, then draws
# a circle with the same diameter as rho. The values for rho and theta
# are drawn too.
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-08
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
#
# See
# https://github.com/openmv/openmv/blob/master/usr/examples/09-Feature-Detection/linear_regression_robust.py
#######################################################################

import sensor, image, time, pyb

THRESHOLD = [(88, 147)] # works for my masking tape on my chalkboard wall

sensor.reset()
# if you have your camera mounted on a Donkey car, flip the image
#sensor.set_vflip(True)
#sensor.set_hmirror(True)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()

    line = img.get_regression(THRESHOLD, robust = True)

    if (line):
        img.draw_line(line.line(), 255)
        rho = line.rho()
        theta = line.theta()

        # we convert any negative rho to a positive rho and add 180 degrees so we can pass a
        # positive value as the radius when drawing our circle later
        if rho < 0:
            rho = abs(rho)
            theta += 180

        print("theta=%f, rho=%f, x1=%f, x2=%f, y1=%f, y2=%f" %  \
            (theta, rho, line.x1(), line.x2(), line.y1(), line.y2()))

        img.draw_circle(0, 0, rho, 240)
        img.draw_string(img.width() - 80, 0, "theta=%f\n  rho=%f" % (theta, rho), 240)
