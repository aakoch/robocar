# MJPEG Video Recording Example
#
# Note: You will need an SD card to run this demo.
#
# You can use your OpenMV Cam to record mjpeg files. You can either feed the
# recorder object JPEG frames or RGB565/Grayscale frames. Once you've finished
# recording a Mjpeg file you can use VLC to play it. If you are on Ubuntu then
# the built-in video player will work too.

import sensor, image, time, mjpeg, pyb

RED_LED_PIN = 1
BLUE_LED_PIN = 3

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_framesize(sensor.QVGA) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
clock = time.clock() # Tracks FPS.

pyb.LED(RED_LED_PIN).on()
sensor.skip_frames(time = 2000) # Give the user time to get ready.

pyb.LED(RED_LED_PIN).off()
pyb.LED(BLUE_LED_PIN).on()

m = mjpeg.Mjpeg("example.mjpeg")

try:

    print("You're on camera!")
    start = pyb.millis()
    while (pyb.elapsed_millis(start) < 20000):
        clock.tick()
        m.add_frame(sensor.snapshot())
        print(clock.fps())

except Exception as exc:
    print(exc)
    m.close(clock.fps())
    pyb.LED(BLUE_LED_PIN).off()
    print("Done! Reset the camera to see the saved recording.")
