#class_camera.py
###############################################################
# Camera class
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-05
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import sensor, pyb, sys
from micropython import const
from class_threshold import Threshold
from class_logger import *
from constants import *
from util_functions import *

top_area_theshold = const(400)
bottom_area_theshold = const(200)
_PIXELS_THRESHOLD = const(4)
_BOTTOM_PX_TO_REMOVE = const(4) # maybe I screwed something up with my camera, but the last few rows are just noise


class Camera():
    """Camera"""

    def __init__(self):
        self.logger = Logger()
        self.logger.set_level(DEBUG_LOG_LEVEL)
        self.logger.info("initializing  Camera")
        self.reset_sensor()
        self.SHOW_BINARY_VIEW = False
        #self.CHROMINVAR = True
        self.line_color = (0, 255, 0)
        # [(1, 80, -25, 28, -58, -10)]
        self.threshold = None # self.old_threshold = [(44, 87, -27, 23, -62, -15)] #Threshold.BLUE
        self.use_hist = True
        self.line_roi = (0, round(sensor.height() / 15), sensor.width(), round(sensor.height() / 2))
        #self.blobs_roi = (0, 0, sensor.width(), round(sensor.height() / 3))
        self.snapshot = None
        #self.glare_check_millis = MILLIS_BETWEEN_GLARE_CHECK
        self.adjuster = 16384

    def reset(self):
        """Alias for reset_sensor"""
        self.reset_sensor()

    def reset_sensor(self):
        sensor.reset()
        sensor.set_pixformat(sensor.RGB565)
        sensor.set_framesize(sensor.QVGA)
        sensor.set_vflip(True)
        sensor.set_hmirror(True)
        self.logger.trace("skipping frames...")
        sensor.skip_frames(time = 2000)

    def set_camera_pixel_format_to_black_and_white(self):
        self.logger.debug("Setting to grayscale")
        sensor.set_pixformat(sensor.GRAYSCALE)
        self.line_color = 127

    def set_camera_pixel_format_to_rgb(self):
        self.logger.debug("setting to RGB")
        sensor.set_pixformat(sensor.RGB565)
        self.line_color = (127, 127, 127)

    def set_camera_threshold(self, threshold):
        self.logger.debug("setting threshold: " + str(threshold))
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

    def set_log_level(self, level):
        self.logger.set_level(level)

    def calculate_bottom_bounding_box(self, top_line):
        if (top_line):
            self.logger.debug("top_line=", top_line)
            theta2 = theta(top_line)
            #self.logger.debug("theta=", theta2)
            self.logger.debug("x1 + x2=", top_line.x1() + top_line.x2())

            half_width = self.snapshot.width() >> 1
            if (top_line.x1() + top_line.x2() > sensor.width() and top_line.x1() > top_line.x2() and abs(theta2) > 45):
                x = top_line.x1()
            else:
                x = top_line.x2()
            #x = min(top_line.x1() - half_width, top_line.x2() - half_width) + half_width
            #x = top_line.x2() if abs(theta2) < 45 else top_line.x1()
            y = max(top_line.y1(), top_line.y2())
            height = min(self.snapshot.height() >> 2, self.snapshot.height() - y)
            width = max(abs(int(math.tan(math.radians(theta2)) * height)) * 2, 20)
            x = x - (width >> 1)
            if (x < 0):
                width += x
                x = 0

            self.logger.debug("x=", x, " y=", y, " width=", width, " height=", height)
            return (x, y, width, height)

        return (0, (self.snapshot.height() >> 1) + self.line_roi[1], self.snapshot.width(), (self.snapshot.height() >> 1) - self.line_roi[1])

    #def _check_glare(self):
        #blobs = self.snapshot.find_blobs([(95, 100, -128, 127, -4, 5)], roi=self.blobs_roi)

        #if (blobs):
            #trace("blobs found")
            #pixel_count = 0
            #for blob in blobs:
                #if usb_is_connected:
                    #trace("drawing rect...")
                    #self.snapshot.draw_rectangle(blob.rect(), color=(255, 0, 0))
                    #sensor.flush()
                #pixel_count += blob.pixels()

            #self.CHROMINVAR = pixel_count > 700
            #if (self.CHROMINVAR):
                #self.old_threshold = self.threshold
                #self.threshold = [(29, 38, 0, 34, -66, -33)]
                ## glare threshold: (30, 59, -5, 16, -60, -34)
                #info("glare pixel_count=", pixel_count)
            #else:
                #self.threshold = self.old_threshold
                #debug("glare pixel_count=", pixel_count)
        #else:
            #self.threshold = self.old_threshold
            #self.CHROMINVAR = False
        #trace("CHROMINVAR=", self.CHROMINVAR)
        #trace("exiting detect_glare...")

    def take(self):
        self.logger.trace("entering take...")
        try:
            self.watchdog.feed()
        except AttributeError:
            pass # no watchdog to feed

        # after taking a picture: img.binary(COLOR_THRESHOLDS if COLOR_LINE_FOLLOWING else GRAYSCALE_THRESHOLDS)
        self.logger.trace("taking snapshot...")
        self.snapshot = sensor.snapshot()

        #if (pyb.elapsed_millis(self.glare_check_millis) > MILLIS_BETWEEN_GLARE_CHECK):
            #self._check_glare()
            #self.glare_check_millis = pyb.millis()

        if usb_is_connected:
            self.snapshot.draw_rectangle(self.line_roi, color = (150, 150, 150))

        if self.SHOW_BINARY_VIEW:
            if (self.threshold == None):
                raise RuntimeError("Set threshold before trying to use binary view")
            self.logger.trace("calling binary...")
            self.snapshot.binary(self.threshold)
        elif self.use_hist:
            self.logger.trace("calling histeq...")
            self.snapshot.histeq()
        #elif self.CHROMINVAR:
            #trace("calling chrominvar...")
            #self.snapshot.chrominvar()

        sensor.flush()
        self.logger.trace("returing snapshot...")
        return self.snapshot

    def get_img(self):
        return self.snapshot

    def find_line(self, **keyword_parameters):
        global top_area_theshold , bottom_area_theshold
        self.logger.trace("entering find_line...")
        if (self.threshold == None):
            raise RuntimeError("Set threshold before trying to find a line")

        self.logger.debug("calling get_regression... threshold=", self.threshold)
        if ('roi' in keyword_parameters):
            roi = keyword_parameters['roi']
            #roi_stats = self.snapshot.get_statistics(roi = roi)
            #self.logger.debug("roi_stats=", roi_stats)
            area_theshold = bottom_area_theshold
        else:
            roi = self.line_roi
            area_theshold = top_area_theshold

        self.line = self.snapshot.get_regression(self.threshold, \
            area_threshold = area_theshold, pixels_threshold = _PIXELS_THRESHOLD, \
            robust = True, roi = roi)

        if ('roi' in keyword_parameters):
            pass
        elif usb_is_connected and self.line:
            self.logger.trace("line found")
            self.snapshot.draw_line(self.line.line(), color = self.line_color)
            sensor.flush()

        self.logger.trace("returing line=", self.line)
        return self.line

    def find_line_and_confidence(self):
        top_line = self.find_line()

        rect = self.calculate_bottom_bounding_box(top_line)
        if usb_is_connected:
            self.snapshot.draw_rectangle(rect, color=(255,255,255))
        self.logger.debug("rect=", rect)
        if (rect[1] < self.snapshot.height() >> 1):
            sensor.flush()
        bottom_line = self.find_line(roi = rect)
        if (bottom_line):
            if usb_is_connected:
                self.snapshot.draw_line(bottom_line.line(), color=(0, 0, 255))
            if (top_line):
                confidence = 1 - abs(bottom_line.x1() - top_line.x2()) / (self.snapshot.width() << 1)
            else:
                confidence = 1 - bottom_line.x1() / (self.snapshot.width() << 1)
            self.logger.debug("confidence=", confidence)
        else:
            confidence = 0

        self.logger.trace("returing line=", top_line, ", confidence=", confidence)
        return (top_line, confidence)

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


    def adjust_exposure(self, goal):
        """Adjust the exposure of the sensor until the average L (in LAB)
           value reaches the desired goal."""
        self.logger.debug("goal=", goal)
        direction = 0
        UP = 1
        DOWN = -1
        sensor.set_auto_gain(False)
        img = sensor.snapshot() if self.snapshot == None else self.snapshot
        stats = img.get_statistics()
        adjuster = self.adjuster
        while(abs(stats.l_mean() - goal) > 10 and adjuster > 2):
            self.logger.debug("adjuster=", adjuster, ", sensor.get_exposure_us()=", sensor.get_exposure_us())
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
            img = self.take()
            stats = img.get_statistics()
        self.adjuster = 16384

#from thresholds_holder import *
#thresholds_holder = ThresholdsHolder()
#thresholds_holder.set_thresholds([[(42, 52, -1, 23, -61, -31)], [(44, 69, -13, 18, -72, -39)]]) #(22, 67, -28, -9, -8, 17)],[(48, 77, -13, 5, -51, -13)],[(45, 76, -17, 19, -58, -12)], [(43, 90, -25, 8, -43, -9)]])

#camera = Camera()
#camera.set_threshold(thresholds_holder.get_threshold())
#camera.adjust_exposure(60)
##original_l = camera.get_img().get_statistics().l_mean()
#for j in range(500):
    #camera.take()
    #(line, confidence) = camera.find_line_and_confidence()
    ##print("confidence=", confidence)
