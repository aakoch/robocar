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
from log import *

_AREA_THRESHOLD = const(35)
_PIXELS_THRESHOLD = const(35)
FRAME_REGION = 0.8 # Percentage of the image from the bottom (0 - 1.0).
FRAME_WIDE = 1.0 # Percentage of the frame width.
BOTTOM_PX_TO_REMOVE = const(4) # maybe I screwed something up with my camera, but the last few rows are just noise
MILLIS_BETWEEN_GLARE_CHECK = const(2000)


class Camera():

    def __init__(self):
        info("initializing  Camera")
        self.reset_sensor()
        self.SHOW_BINARY_VIEW = False
        self.CHROMINVAR = False
        self.line_color = (0, 255, 0)
        self.skipped_frames = False
        self.threshold = self.old_threshold = Threshold.BLUE
        self.use_hist = False
        self.line_roi = (0, round(sensor.height() / 15), sensor.width(), round(sensor.height() / 2))
        self.blobs_roi = (0, 0, sensor.width(), round(sensor.height() / 3))
        self.snapshot = None
        self.glare_check_millis = MILLIS_BETWEEN_GLARE_CHECK

    def reset_sensor(self):
        sensor.reset()
        sensor.set_pixformat(sensor.RGB565)
        sensor.set_framesize(sensor.QQVGA)
        sensor.set_vflip(True)
        sensor.set_hmirror(True)

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

    def set_chrominvar(self, b):
        self.CHROMINVAR = b

    def decrease_exposure(self):
        sensor.set_auto_exposure(False, exposure_us = sensor.get_exposure_us() - 1000)
        sensor.set_auto_gain(False)

    def increase_exposure(self):
        sensor.set_auto_exposure(False, exposure_us = sensor.get_exposure_us() + 1000)
        sensor.set_auto_gain(False)

    def set_threshold(self, threshold):
        self.threshold = threshold

    def _check_glare(self):
        blobs = self.snapshot.find_blobs([(95, 100, -128, 127, -4, 5)], roi=self.blobs_roi)

        if (blobs):
            trace("blobs found")
            pixel_count = 0
            for blob in blobs:
                if usb_is_connected:
                    trace("drawing rect...")
                    self.snapshot.draw_rectangle(blob.rect(), color=(255, 0, 0))
                    sensor.flush()
                pixel_count += blob.pixels()

            self.CHROMINVAR = pixel_count > 700
            if (self.CHROMINVAR):
                self.old_threshold = self.threshold
                self.threshold = [(29, 38, 0, 34, -66, -33)]
                # glare threshold: (30, 59, -5, 16, -60, -34)
                info("glare pixel_count=", pixel_count)
            else:
                self.threshold = self.old_threshold
                debug("glare pixel_count=", pixel_count)
        else:
            self.threshold = self.old_threshold
            self.CHROMINVAR = False
        trace("CHROMINVAR=", self.CHROMINVAR)
        trace("exiting detect_glare...")

    def take(self):
        trace("entering take...")
        try:
            self.watchdog.feed()
        except AttributeError:
            pass # no watchdog to feed

        if (not self.skipped_frames):
            trace("skipping frames...")
            sensor.skip_frames(time = 2000)
            self.skipped_frames = True
        # after taking a picture: img.binary(COLOR_THRESHOLDS if COLOR_LINE_FOLLOWING else GRAYSCALE_THRESHOLDS)
        trace("taking snapshot...")
        self.snapshot = sensor.snapshot()

        if (pyb.elapsed_millis(self.glare_check_millis) > MILLIS_BETWEEN_GLARE_CHECK):
            self._check_glare()
            self.glare_check_millis = pyb.millis()

        if usb_is_connected:
            self.snapshot.draw_rectangle(self.line_roi, color = (150, 150, 150))

        if self.SHOW_BINARY_VIEW:
            trace("calling binary...")
            self.snapshot.binary(self.threshold)
        elif self.use_hist:
            trace("calling histeq...")
            self.snapshot.histeq()
        elif self.CHROMINVAR:
            trace("calling chrominvar...")
            self.snapshot.chrominvar()

        sensor.flush()
        trace("returing snapshot...")
        return self.snapshot

    def get_img(self):
        return self.snapshot

    def find_line(self):
        trace("entering find_line...")
        trace("calling get_regression... threshold=", self.threshold)
        self.line = self.snapshot.get_regression(self.threshold, \
            area_threshold = _AREA_THRESHOLD, pixels_threshold = _PIXELS_THRESHOLD, \
            robust = True, roi = self.line_roi)
        if usb_is_connected and self.line:
            trace("line found")
            self.snapshot.draw_line(self.line.line(), color = self.line_color)
            sensor.flush()

        trace("returing line=", self.line)
        return self.line

    def find_menu_item(self):
        sensor.set_framesize(sensor.QQVGA) # camera will run out of memory if in QVGA
        found_tag = False
        tag = None
        while(not found_tag):
            self.snapshot = self.take()
            tags = self.snapshot.find_apriltags()
            if len(tags) > 0:
                found_tag = True
                for tag in tags:
                    tag = tag.id()
        return tag

#camera = Camera()
##camera.set_threshold([(29, 38, 0, 34, -66, -33)])
##print("taking picture")
##camera.take()
#for j in range(200):
    ##print("j=",j)
    #camera.take()
    #camera.find_line()
    ##camera.detect_glare()
##camera.get_img()
##for i in range(0, 100):
    ##camera.increase_exposure()
    ##sensor.skip_frames(10, 1000)
##print("exit")
##print("found %i" % camera.find_menu_item())
