#class_camera.py
###############################################################
# Camera class
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-05
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import sensor, pyb
from micropython import const
from class_threshold import Threshold
from constants import *

_AREA_THRESHOLD = const(20)
_PIXELS_THRESHOLD = const(20)
FRAME_REGION = 0.8 # Percentage of the image from the bottom (0 - 1.0).
FRAME_WIDE = 1.0 # Percentage of the frame width.
BOTTOM_PX_TO_REMOVE = const(4) # maybe I screwed something up with my camera, but the last few rows are just noise

class Camera():

    def __init__(self):
        print("initializing  Camera")
        sensor.reset()
        sensor.set_vflip(True)
        sensor.set_hmirror(True)
        sensor.set_pixformat(sensor.RGB565)
        self.SHOW_BINARY_VIEW = False
        self.line_color = (127, 127, 127)
        self.skipped_frames = False
        self.threshold = Threshold.BLUE

        sensor.set_framesize(sensor.QQVGA)
        sensor.set_windowing((int((sensor.width() / 2) - ((sensor.width() / 2) * FRAME_WIDE)), int(sensor.height() * (1.0 - FRAME_REGION)), \
                     int((sensor.width() / 2) + ((sensor.width() / 2) * FRAME_WIDE)), int(sensor.height() * FRAME_REGION) - BOTTOM_PX_TO_REMOVE))


    def set_camera_pixel_format_to_black_and_white(self):
        print("Setting to grayscale")
        sensor.set_pixformat(sensor.GRAYSCALE)
        self.line_color = 127

    def set_camera_pixel_format_to_rgb(self):
        print("setting to RGB")
        sensor.set_pixformat(sensor.RGB565)
        self.line_color = (127, 127, 127)

    def set_camera_threshold(self, threshold):
        print("setting threshold: " + str(threshold))
        self.threshold = threshold

    def set_framesize(self, framesize):
        sensor.set_framesize(framesize)
        self.skipped_frames = False

    def set_windowing(self, window):
        sensor.set_windowing(window)
        self.skipped_frames = False

    def set_watchdog(self, watchdog):
        self.watchdog = watchdog

    def take(self):
        try:
            self.watchdog.feed()
        except AttributeError:
            pass # no watchdog to feed

        if (not self.skipped_frames):
            sensor.skip_frames(10, 1000)
            self.skipped_frames = True
        # after taking a picture: img.binary(COLOR_THRESHOLDS if COLOR_LINE_FOLLOWING else GRAYSCALE_THRESHOLDS)
        snapshot = sensor.snapshot()
        if self.SHOW_BINARY_VIEW:
            return snapshot.binary(self.threshold)
        else:
            return snapshot

    def find_line(self):
        self.img = self.take()
        self.line = self.img.get_regression(self.threshold, \
            area_threshold = _AREA_THRESHOLD, pixels_threshold = _PIXELS_THRESHOLD, \
            robust = True)
        if usb_is_connected:
            self.img.draw_line(self.line.line(), color = self.line_color)
        return self.line

    def find_menu_item(self):
        sensor.set_framesize(sensor.QQVGA) # camera will run out of memory if in QVGA
        found_tag = False
        tag = None
        while(not found_tag):
            self.img = self.take()
            tags = self.img.find_apriltags()
            if len(tags) > 0:
                found_tag = True
                for tag in tags:
                    tag = tag.id()
        return tag

#camera = Camera()
#print("found %i" % camera.find_menu_item())
