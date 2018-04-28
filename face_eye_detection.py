# Face Eye Detection Example
#
# This script uses the built-in frontalface detector to find a face and then
# the eyes within the face. If you want to determine the eye gaze please see the
# iris_detection script for an example on how to do that.

import sensor, time, image

from pyb import LED

red_led   = LED(1)

# Reset sensor
sensor.reset()

# Sensor settings
sensor.set_contrast(1)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.HQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.skip_frames()

# Load Haar Cascade
# By default this will use all stages, lower satges is faster but less accurate.
face_cascade = image.HaarCascade("frontalface", stages=30)
eyes_cascade = image.HaarCascade("eye", stages=24)
print(face_cascade, eyes_cascade)

# FPS clock
clock = time.clock()

def circle_from_rect(rect):
    x = round(rect[2] / 2) + rect[0]
    y = round(rect[3] / 2) + rect[1]
    r = round(rect[3] / 2)
    return (x, y, r)

notFound = True
while (notFound):
    clock.tick()

    # Capture snapshot
    img = sensor.snapshot()

    # Find a face !
    # Note: Lower scale factor scales-down the image more and detects smaller objects.
    # Higher threshold results in a higher detection rate, with more false positives.
    objects = img.find_features(face_cascade, threshold=0.5, scale_factor=1.4)

    # Draw faces
    for face in objects:
        print(face)
        #img.draw_rectangle(face)
        (x,y, r) = circle_from_rect(face)
        img.draw_circle(x, y, r)
        # Now find eyes within each face.
        # Note: Use a higher threshold here (more detections) and lower scale (to find small objects)
        eyes = img.find_features(eyes_cascade, threshold=0.5, scale_factor=1.2, roi=face)
        for e in eyes:
            print("found eyes")
            print(e)
            #(x, y, r) = circle_from_rect(e)
            #img.draw_circle(x, y, r)
            img.draw_rectangle(e)
            red_led.on()
            notFound = False

sensor.flush()
time.sleep(5000)

    # Print FPS.
    # Note: Actual FPS is higher, streaming the FB makes it slower.
    #print(clock.fps())
