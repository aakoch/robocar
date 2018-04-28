# Untitled - By: aakoch - Sun Apr 22 2018

import sensor, image, time
from pyb import Pin, Timer

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
#sensor.set_vflip(True)
#sensor.set_hmirror(True)
sensor.skip_frames(time = 2000)

clock = time.clock()

while (True):
    img = sensor.snapshot()

    stats = img.get_statistics()
    if (stats.l_mean() > 70):
        new_exposure_us = sensor.get_exposure_us() - 1000
        sensor.set_auto_exposure(False, exposure_us = new_exposure_us)
        #sensor.skip_frames(5)
        #stats = sensor.snapshot().get_statistics()

    blobs = img.find_blobs([(97, 100, -7, 127, -5, 127)])

    #if (blobs):
        #img.chrominvar()
    for blob in blobs:
        print(blob)
        img.draw_rectangle(blob.rect(), color=(255, 0, 0))
# check for bright lights
#rect = find_brightest_area(img)
#img.draw_rectangle(rect, color=(255,0,0))
#stats = img.get_statistics(roi=rect)
#print("bright stats=", stats)
#if (True or stats.l_mean() > 82):
    #height = img.height() - 12 - BOTTOM_PX_TO_REMOVE;
    #height = height - height % 16
    #print(height)
    #sensor.set_windowing((0, 0, img.width(), 120))
    #sensor.skip_frames(10)
    #img = sensor.snapshot()
    #while(True):
        #sensor.snapshot()
        #sensor.flush()

#for y in range(0, 51, 10):
    #for x in range(sensor.width() - 10):
        #img = sensor.snapshot()
        #roi = (x, y, 10, 10)
        #img.draw_rectangle((0, 0, sensor.width(), 50))
        #img.draw_string(20, 10, "Scanning...")
        #img.draw_rectangle(roi)
        #blobs = img.find_blobs([(96, 100, -7, 127, -5, 127)], roi=roi)

        #for blob in blobs:
            #print(blob)
            #img.draw_rectangle(blob.rect(), color=(255, 0, 0))
    #stats = img.get_statistics(roi=(0, y, sensor.width(), 1))
    #hist = img.get_histogram()
    #threshold = hist.get_threshold()
    #img.binary(threshold)
    #print(hist.l_bins())

#shiney_floor = stats.l_lq() == 60 and stats.l_uq() == 72 and stats.a_stdev() == 10
#print("shiney_floor=", shiney_floor)

#print(clock.fps())
