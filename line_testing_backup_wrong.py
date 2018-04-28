# In Memory Basic Frame Differencing Example
#
# This example demonstrates using frame differencing with your OpenMV Cam. It's
# called basic frame differencing because there's no background image update.
# So, as time passes the background image may change resulting in issues.

import sensor, image, pyb, os, time, array, math
from util_functions import *
from file_utils import ConfigFile

TRIGGER_THRESHOLD = 5
STEERING_SERVO_MIN_US = const(1276)
STEERING_SERVO_MAX_US = const(1884)
BOTTOM_PX_TO_REMOVE = const(0)

sensor.reset() # Initialize the camera sensor.
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 1500) # Let new settings take affect.
sensor.set_auto_whitebal(False) # Turn off white balance.
sensor.set_auto_gain(False)
clock = time.clock() # Tracks FPS.

COLOR_THRESHOLDS = [(36, 80, -19, 39, -77, -9)] # for when L is 37, 70, 70, 100
AREA_THRESHOLD = const(20) # Raise to filter out false detections.
PIXELS_THRESHOLD = const(20) # Raise to filter out false detections.
MAG_THRESHOLD = const(3) # Raise to filter out false detections.
device = pyb.UART(3, 19200, timeout_char = 100)

throttle = int(ConfigFile().get_property("min_speed")) + 3

def figure_out_my_steering(line, img):
    center = round(img.width() / 2)

    #angle_1 = remap(line.x1() * 1.1, 0, img.width(), -90, 90)
    angle_1 = -math.degrees(math.atan((center - line.x1()) / (img.height() - BOTTOM_PX_TO_REMOVE)))
    #if (line.x1() < img.width()):
        #angle_1 = -angle_1
    angle_2 = theta(line) / 1.6
    #print("angle_1=%.3f, angle_2=%.3f" % (angle_1, angle_2))
    steering = angle_1 + angle_2

    #steering = remap(line.x1(), 0, img.width(), 180, 0)
    img.draw_string(10, 10, str(round(steering)))
    return constrain(90 - steering, 0, 180)

def set_servos(throttle, steering):
    throttle = remap(throttle, 0, 100, 1580, 1760) # (input * 15.8) + 180

    steering = remap(steering, 0, 180, STEERING_SERVO_MIN_US, STEERING_SERVO_MAX_US)

    device.write("{%05d,%05d}\r\n" % (throttle, steering))
    print("{%05d,%05d}" % (throttle, steering))


class ThresholdHolder:

    l_min = a_min = b_min = l_max = a_max = b_max = 0

    def set_l_range(self, l_range):
        self.l_min = 0
        self.l_max = l_range


    def set_a_range(self, a_range):
        self.a_min = 0
        self.a_max = a_range

    def set_b_range(self, b_range):
        self.b_min = 0
        self.b_max = b_range

    def get_thresholds(self, l_count, a_count, b_count):
        tmp = [(self.l_min + l_count, self.l_max + l_count, \
                self.a_min + a_count, self.a_max + a_count, \
                self.b_min + b_count, self.b_max + b_count)]
        return tmp

img = sensor.snapshot()

while (img.get_statistics().l_mean() < 60):
    sensor.set_auto_exposure(False, exposure_us=sensor.get_exposure_us() + 200)
    img = sensor.snapshot()

thresholdHolder = ThresholdHolder()
list_of_thresholds = []

print("looping")

l_min = 100
l_max = 0
a_min = 120
a_max = -120
b_min = 120
b_max = -120


#(23, 76, -23, 43, -76, 15)
#(11, 76, -31, 41, -73, 14)
#(11, 79, -31, 43, -69, 14)
#(12, 83, -31, 41, -59, 14)
#COLOR_THRESHOLDS = [(1, 80, -25, 28, -58, -10)] # Blue tape line
#COLOR_THRESHOLDS = [(1, 80, -25, 37, -76, -47)] # Blue tape line 2 - upstairs - sunny
#COLOR_THRESHOLDS = [(1, 80, -25, 37, -76, 0)] # Blue tape line 2 - upstairs - cloudy
#COLOR_THRESHOLDS = [(19, 81, -24, 21, -35, -8)] # with sensor.set_auto_exposure(False, exposure_us=20000)
total = 0

stats = img.get_statistics()

for i in range(0, 20, 2):
    inc = 20 - i
    print("incrementing by ", inc)
    for l_range in range(60, 80, 10):
        for a_range in range(50, 62, 2):
            for b_range in range(48, 76, 2):
                for l_count in range(1, 23, inc):
                    for a_count in range(-31, -25, inc):
                        for b_count in range(-76, 15, inc):
                            total += 1

print("est. total=", total)

count = 0
for i in range(0, 20, 2):
    inc = 20 - i
    print("incrementing by ", inc)
    for l_range in range(60, 80, 10):
        thresholdHolder.set_l_range(l_range)
        #for a_range in range(stats.a_stdev(), stats.a_max() - stats.a_min(), stats.a_stdev()):
        for a_range in range(50, 62, 2):
            thresholdHolder.set_a_range(a_range)
            #for b_range in range(stats.b_stdev(), min(15, stats.b_max())- max(-76, stats.b_min()), round(stats.b_stdev() / 2)):
            for b_range in range(48, 76, 2):
                thresholdHolder.set_b_range(b_range)
                for l_count in range(max(-31, stats.l_min()), min(90, stats.l_max()), inc):
                    for a_count in range(max(-31, stats.a_min()), min(43, stats.b_max()), inc):
                        stats = img.get_statistics()
                        for b_count in range(max(-76, stats.b_min()), min(15, stats.b_max()), inc):
                            clock.tick()
                            thresholds = COLOR_THRESHOLDS#thresholdHolder.get_thresholds(l_count, a_count, b_count)
                            img = sensor.snapshot()#.binary(thresholds)
                            rect = (round(img.width() / 2) - 10, 0, 28, img.height())
                            line = img.get_regression(thresholds, \
                                area_threshold = AREA_THRESHOLD, pixels_threshold = PIXELS_THRESHOLD, \
                                robust = True, roi=rect)
                            img.draw_rectangle(rect)
                            if (line):
                                #img.draw_string(0, 10, repr(stats))
                                img.draw_string(0, img.height() - 10, repr(thresholds))
                                if ((line.theta() > 160 or line.theta() < 17) and line.x1() > rect[0] and line.x1() < rect[0] + rect[3]):
                                    img.draw_line(line.line(), color=(0, line.magnitude() * 4 + 100, 0))
                                    msg = "Found line inside range - " + repr(thresholds) + " - " + repr(line)
                                    #list_of_thresholds.append(thresholds)
                                    print(msg)
                                    l_min = min(l_min, thresholds[0][0])
                                    l_max = max(l_max, thresholds[0][1])
                                    a_min = min(a_min, thresholds[0][2])
                                    a_max = max(a_max, thresholds[0][3])
                                    b_min = min(b_min, thresholds[0][4])
                                    b_max = max(b_max, thresholds[0][5])
                                else:
                                    img.draw_line(line.line(), color=(line.magnitude() * 4 + 100, 0, 0))
                                    msg = "Found line outside range - " + repr(thresholds) + " - " + repr(line)
                                    print(msg)
                                img.save("snapshot" + str(pyb.millis()) + ".jpg", quality=50)
                            else:
                                count += 1
                                if (count % 100 == 0):
                                    print("another", count, "images with no lines")
                                    count = 0
                                img.draw_circle(round(img.width() / 2), round(img.height() / 2), 20, color=(255, 0, 0))
                                img.draw_line((round(img.width() / 2) + 18, round(img.height() / 2) - 13, round(img.width() / 2) - 18, round(img.height() / 2) + 13), color=(255, 0, 0))
                                #msg = "Line lost - " + repr(thresholds)
                                #print(msg)

            print("l_min=%d, l_max=%d, a_min=%d, a_max=%d, b_min=%d, b_max=%d" % \
                    (l_min, l_max, a_min, a_max, b_min, b_max))
                            #if (len(list_of_thresholds) > 1000):
                                #for j in range(0, len(list_of_thresholds)):
                                    #print(list_of_thresholds[j])
                                #del list_of_thresholds[:]
print("***************************************************************")
print("l_min=%d, l_max=%d, a_min=%d, a_max=%d, b_min=%d, b_max=%d" % \
        (l_min, l_max, a_min, a_max, b_min, b_max))

for l_range in range(1, l_max - l_min):
    thresholdHolder.set_l_range(l_range)
    for a_range in range(1, a_max - a_min):
        thresholdHolder.set_a_range(a_range)
        for b_range in range(1, b_max - b_min):
            thresholdHolder.set_b_range(b_range)
            for l_count in range(l_min, l_max):
                for a_count in range(a_min, a_max):
                    for b_count in range(b_min, b_max):
                        clock.tick()
                        thresholds = thresholdHolder.get_thresholds(l_count, a_count, b_count)
                        img = sensor.snapshot()
                        line = img.get_regression(thresholds, \
                            area_threshold = AREA_THRESHOLD, pixels_threshold = PIXELS_THRESHOLD, \
                            robust = True)
                        if (line):
                            #img.draw_string(0, 10, repr(stats))
                            img.draw_string(0, img.height() - 10, repr(thresholds))
                            if ((line.theta() > 174 or line.theta() < 3) and line.x1() > (img.width() / 2) - 10 and line.x1() < (img.width() / 2) + 5):
                                img.draw_line(line.line(), color=(0, line.magnitude() * 10, 0))
                                msg = "Found line inside range - " + repr(thresholds) + " - " + repr(line)
                                #list_of_thresholds.append(thresholds)
                                print(msg)
                            else:
                                img.draw_line(line.line(), color=(line.magnitude() * 10, 0, 0))
                                #msg = "Found line outside range - " + repr(thresholds) + " - " + repr(line)

                            img.save("snapshot" + str(pyb.millis()) + ".jpg", quality=50)
                        else:
                            img.draw_circle(round(img.width() / 2), round(img.height() / 2), 20, color=(255, 0, 0))
                            img.draw_line((round(img.width() / 2) + 18, round(img.height() / 2) - 13, round(img.width() / 2) - 18, round(img.height() / 2) + 13), color=(255, 0, 0))
                            #msg = "Line lost - " + repr(thresholds)
                            #print(msg)



#print("*********************************************")
#for j in range(0, len(list_of_thresholds)):
    #print(list_of_thresholds[j])


#good_lines_in_a_row = 0
#while(good_lines_in_a_row < 20):
    #print("good_lines_in_a_row=",good_lines_in_a_row)
    #if (not line or line.magnitude() < MAG_THRESHOLD):
        #good_lines_in_a_row = 0
        #sensor.set_auto_exposure(False, exposure_us=sensor.get_exposure_us() + 1000)
        #rgb_gain = sensor.get_rgb_gain_db()
        #sensor.set_auto_whitebal(False, rgb_gain_db = (rgb_gain[0], 0, 6))
        #img = sensor.snapshot() # Take a picture and return the image.
        #line = img.get_regression(COLOR_THRESHOLDS, \
            #area_threshold = AREA_THRESHOLD, pixels_threshold = PIXELS_THRESHOLD, \
            #robust = True)
    #else:
        #img.draw_line(line.line(), color=(100,25,100))
        #good_lines_in_a_row += 1
    #sensor.skip_frames(10)

##sensor.set_auto_exposure(False, exposure_us=sensor.get_exposure_us() + 1000)

#print(line)
#count = 0
#while(count < 20):
    #if (line and (line.magnitude() >= MAG_THRESHOLD)):
        #count -= 1
    #else:
        #count += 1
    #print("in loop. ", count, line)

    #if (line):
        #img.draw_line(line.line(), color=(10,255,10))
        #set_servos(throttle, figure_out_my_steering(line, img))
    #img = sensor.snapshot() # Take a picture and return the image.

    #line = img.get_regression(COLOR_THRESHOLDS, \
        #area_threshold = AREA_THRESHOLD, pixels_threshold = PIXELS_THRESHOLD, \
        #robust = True)
    #print(line)
    #sensor.flush()

#set_servos(throttle - 2, 90)
