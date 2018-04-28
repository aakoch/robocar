# MJPEG Video Recording on Movement Example
#
# Note: You will need an SD card to run this example.
#
# You can use your OpenMV Cam to record mjpeg files. You can either feed the
# recorder object JPEG frames or RGB565/Grayscale frames. Once you've finished
# recording a Mjpeg file you can use VLC to play it. If you are on Ubuntu then
# the built-in video player will work too.
#
# This example demonstrates using frame differencing with your OpenMV Cam to do
# motion detection. After motion is detected your OpenMV Cam will take video.

import sensor, image, time, pyb, os, uio, micropython

micropython.alloc_emergency_exception_buf(100)

RED_LED_PIN = 1
BLUE_LED_PIN = 3

rtclock = pyb.RTC()
#rtclock.datetime((2017, 12, 24, 18, 41, 0, 0, 0))
#print(rtclock.datetime())

sensor.reset() # Initialize the camera sensor.
sensor.set_vflip(True)
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QQVGA) # or sensor.QQVGA (or others)
sensor.set_auto_whitebal(False) # Turn off white balance.
sensor.skip_frames() # Let new settings take affect.

#if not "temp" in os.listdir(): os.mkdir("temp") # Make a temp directory

#statsfile = open("temp/stats.txt", "w")

orig = sensor.snapshot()#.save("temp/bg.bmp")
#sensor.flush()
orig = orig.copy()
time.sleep(500)
img = sensor.snapshot().difference(orig)

i = 3
j = 0

#while(j < 10):

    #img =
    img = sensor.snapshot().difference(orig)
    #img.difference(orig)#"temp/bg.bmp")
    stats = img.statistics()
    print(stats)
    #avg = (stats.l_max() + stats.a_max() + stats.b_max()) / 3
    #print(stats.l_max(), stats.a_max(), stats.b_max(), avg)
    print(stats.max())

    #for var in dir(stats):
        #val = getattr(stats, var)
        #if type(val).__name__ == "str":
            #print(str(var) + "=" + val)
        #elif type(val).__name__ == "int" and val > stm.TIM2:
            #print(str(var) + "=" + str(hex(val)))
        #else:
            #print(str(var) + "=" + str(val))

        #Vars = {}
        #print(exec("stats." + var + "()", globals(), Vars))

    # Stats 5 is the max of the lighting color channel. The below code
    # triggers when the lighting max for the whole image goes above 20.
    # The lighting difference maximum should be zero normally.
    #if (avg > 40):
        #i = 3
        #pyb.LED(RED_LED_PIN).on()
        #orig = sensor.snapshot()#.save("temp/bg.bmp")
        #sensor.flush()
        ##break
    #else:
        #i -= 1
        #if (i <= 0):
            #pyb.LED(RED_LED_PIN).off()

    #time.sleep(500)
    #orig = sensor.snapshot()
    #sensor.flush()

    #time.sleep(500)

    #sensor.flush()
    #time.sleep(500)

    #j += 1

#statsfile.close()

