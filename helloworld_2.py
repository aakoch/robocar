# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time
from pyb import LED

lightson = False


def turnonlights():
    lightsoff = False
    if (lightson == False):
        LED(1).on()
        LED(2).on()
        LED(3).on()
        LED(4).on()

lightsoff = False


def turnofflights():
    #lightson = False
    #if (lightsoff == False):
    LED(1).off()
    LED(2).off()
    LED(3).off()
    LED(4).off()
    lightsoff = True


sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    #print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
    stats = img.get_statistics()
    print(stats) # to the IDE. The FPS should increase once disconnected.
    max = stats.l_max()
    print(max)
    if (max < 20):
        turnonlights()
    elif(max > 90):
        turnofflights()
