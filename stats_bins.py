# Untitled - By: aakoch - Sat May 5 2018

import sensor, image, time
from class_camera import Camera
from log import *


def adjust_exposure(goal):
    direction = 0
    UP = 1
    DOWN = -1
    sensor.set_auto_gain(False)
    img = sensor.snapshot()
    stats = img.get_statistics()
    adjuster = 16384
    while(abs(stats.l_mean() - goal) > 10 and adjuster > 2):
        if(stats.l_mean() < goal):
            before_exposure_us = sensor.get_exposure_us()
            sensor.set_auto_exposure(False, exposure_us = before_exposure_us + adjuster)
            if (sensor.get_exposure_us() == before_exposure_us):
                adjuster = 2
            if(direction != UP):
                adjuster = adjuster >> 1
            direction = UP
        else:
            before_exposure_us = sensor.get_exposure_us()
            sensor.set_auto_exposure(False, exposure_us = before_exposure_us - adjuster)
            if (sensor.get_exposure_us() == before_exposure_us):
                adjuster = 2
            if(direction != DOWN or sensor.get_exposure_us() < adjuster):
                adjuster = adjuster >> 1
            direction = DOWN
        img = sensor.snapshot()
        stats = img.get_statistics()


sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.skip_frames(time = 2000)
sensor.set_auto_whitebal(False, rgb_gain_db=(-10, -10, 10))


clock = time.clock()

line_roi = (0, round(sensor.height() / 15), sensor.width(), round(sensor.height() / 2))

#camera = Camera()
#camera.set_log_level(INFO_LOG_LEVEL)
#camera.take()
adjust_exposure(60)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)

l_bins = 10
for r_gain in range(-20, 0):
    for g_gain in range(-20, 0):
        for b_gain in range(0, 20, 2):
            for i in range(0, 10):

                img = sensor.snapshot()
                #camera.adjust_exposure(60)
                img.draw_string(0, 0, "r{:.3f}, g{:.3f}, b{:.3f}".format(*sensor.get_rgb_gain_db()))
                sensor.set_auto_whitebal(False, rgb_gain_db=(r_gain, g_gain, b_gain))
            #hist = img.get_histogram()
    #print(hist.a_bins())

#for l_bins in range(2, 100, 10):
    #for a_bins in range(3, 100, 10):
        #for b_bins in range(3, 100, 10):
            #for i in range(1, 5000000):
                #clock.tick()
                #img = sensor.snapshot()
                #img.draw_rectangle(line_roi)
                ##stats = img.get_statistics(line_roi, l_bins=l_bins, a_bins=a_bins, b_bins=b_bins)
                ##img.binary([(57, 93, -53, -7, -2, 37)])
                ##print(l_bins, stats.l_bins(), b_bins, "stats=", stats)
                #hist = img.get_histogram(l_bins=l_bins, a_bins=a_bins, b_bins=b_bins)
                #print(hist.get_threhsold())
                ##print("l_bins=", len(hist.l_bins()), "a_bins=", len(hist.a_bins()), "b_bins=", len(hist.b_bins()), hist)
