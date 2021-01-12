# Untitled - By: aakoch - Wed Apr 18 2018

import sensor, image, time, pyb, math
from util_functions import *

COLOR_THRESHOLDS = [[(41, 67, -14, 12, -60, -31)], [(60, 80, -28, -8, -21, -1)], [(34, 60, -30, -12, -23, 5)]]

sensor.reset()
sensor.set_hmirror(True)
sensor.set_vflip(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((0, 50, sensor.width(), sensor.height() - 100))
#sensor.set_windowing((0, 100, 320, 100))
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)


def calculate_bottom_bounding_box(top_line):
    if (top_line):
        theta2 = theta(top_line)
        #print("theta=", theta2)
        x = top_line.x2()
        y = top_line.y2()
        height = img.height() >> 1
        width = abs(int(math.tan(math.radians(theta2)) * height))
        #print(x, y, height, width)
        return (x - width, y, max(width * 2, 1), height)
    return (0, img.height() >> 1, img.width(), img.height() >> 1)

clock = time.clock()

start_time = pyb.millis()
adjust_exposure(60)
print("time=", pyb.elapsed_millis(start_time))

i = 0
threshold = COLOR_THRESHOLDS[0]
while(True):
    clock.tick()
    start_us = pyb.micros()
    img = sensor.snapshot()
    snap_us = pyb.elapsed_micros(start_us)

    start_us = pyb.micros()
    line_all = img.get_regression(threshold, robust=True)
    all_us = pyb.elapsed_micros(start_us)
    if line_all:
        img.draw_line(line_all.line(), color=(255, 0, 0))

    start_us = pyb.micros()
    line_top = img.get_regression(threshold, robust=True, roi=(0, 0, img.width(), round(img.height() / 2)))
    top_us = pyb.elapsed_micros(start_us)
    if line_top:
        img.draw_line(line_top.line(), color=(0, 255, 0))
        img.draw_string(0, 5, str(theta(line_top)))

    start_us = pyb.micros()
    bottom_box = calculate_bottom_bounding_box(line_top)
    calc_us = pyb.elapsed_micros(start_us)
    print("bottom_box=", bottom_box)
    img.draw_rectangle(bottom_box, color=(255, 255, 255))

    start_us = pyb.micros()
    line_bottom = img.get_regression(threshold, robust=True, roi=bottom_box)
    bottom_us = pyb.elapsed_micros(start_us)
    if line_bottom:
        img.draw_line(line_bottom.line(), color=(0, 0, 250))
        img.draw_string(0, round(img.height() / 2) + 5, str(theta(line_bottom)))

        #print(theta(line))
    if (line_top and line_bottom):
        print("line_top.x2=", line_top.x2(), "line_bottom.x1=", line_bottom.x1(), "diff=", "{:2d}".format(int(line_bottom.x1() - line_top.x2())))
    else:
        print("line not found")
        i += 1
        print(i)
        threshold = COLOR_THRESHOLDS[i % 3]
        print(threshold)
    print("snap_us", snap_us, "all_us", all_us, "top_us", top_us, "bottom_us", bottom_us, "calc_us", calc_us)
