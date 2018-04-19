# Untitled - By: aakoch - Wed Apr 18 2018

import sensor, image, time
from util_functions import *

COLOR_THRESHOLDS = [(41, 67, -14, 12, -60, -31)]

sensor.reset()
sensor.set_hmirror(True)
sensor.set_vflip(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()

    line = img.get_regression(COLOR_THRESHOLDS, robust=True)
    if line:
        img.draw_line(line.line(), color=(255, 0, 0))
        img.draw_string(0, 5, str(theta(line)))

    line = img.get_regression(COLOR_THRESHOLDS, robust=True, roi=(0, 0, img.width(), round(img.height() / 2)))
    if line:
        img.draw_line(line.line(), color=(0, 255, 0))
        img.draw_string(0, 5, str(theta(line)))

    line = img.get_regression(COLOR_THRESHOLDS, robust=True, roi=(0, round(img.height() / 2), img.width(), round(img.height() / 2)))
    if line:
        img.draw_line(line.line(), color=(0, 0, 250))
        img.draw_string(0, round(img.height() / 2) + 5, str(theta(line)))

        print(theta(line))
