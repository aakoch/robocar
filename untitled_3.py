# Untitled - By: aakoch - Tue Dec 12 2017

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    dms = img.find_datamatrices()
    for dm in dms:
        img.draw_string(50, 50, dm.payload(), color=(255,0,0))
    print(clock.fps())
