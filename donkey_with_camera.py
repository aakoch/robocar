# This file is part of the OpenMV project.
# Copyright (c) 2013-2017 Ibrahim Abdelkader <iabdalkader@openmv.io> & Kwabena W. Agyeman <kwagyeman@openmv.io>
# This work is licensed under the MIT license, see the file LICENSE for details.

import sensor, image, time, math, pyb, uio, machine, sys, gc
from pyb import Pin, Timer, RTC
from file_utils import ConfigFile
from util_functions import *
from constants import *
from machine import WDT
#from pulse_led import run_leds
from micropython import const
from class_camera import Camera
from thresholds_holder import ThresholdsHolder
from log import *
from clock import set_time
from pid import SteeringPid

def time_correct():
    (year, month, day, weekday, hours, minutes, seconds, subseconds) = RTC().datetime()
    return year >= 2018 and month >= 5 and day >= 5 and hours >= 23 and minutes >= 30

if not time_correct():
    print("Time is incorrect.", RTC().datetime())
    set_time(2018, 5, 6, 20, 55)

## run the pulse_led.py script if the board was reset because of the watchdog
if (machine.reset_cause() == machine.WDT_RESET):
    wdt_reset_str = ConfigFile().get_property("wdt_reset")
    error("reset was caused by WDT_RESET")
    if (reset_str == None):
        num_of_watchdog_resets = 1
    else:
        num_of_watchdog_resets = int(wdt_reset_str) + 1

    error("This has happened", str(num_of_watchdog_resets), "times")
    ConfigFile().set_property("wdt_reset", str(num_of_watchdog_resets))

def remap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

WRITE_FILE = True
REVERSE = False
COLOR_LINE_FOLLOWING = True # False to use grayscale thresholds, true to use color thresholds.
DEBUG_PRINT_UART = True # whether to write UART debug
DEBUG_LINE_STATUS = True
#COLOR_THRESHOLDS = [( 85, 100, -40, 127, 20, 127)] # Yellow Line.
#COLOR_THRESHOLDS =[(85, 100, -3, 127, -9, 94)] # do space
#COLOR_THRESHOLDS = [(1, 80, -25, 28, -58, -10)] # Blue tape line
#COLOR_THRESHOLDS = [(1, 80, -25, 37, -76, -47)] # Blue tape line 2 - upstairs - sunny
#COLOR_THRESHOLDS = [(1, 80, -25, 37, -76, 0)] # Blue tape line 2 - upstairs - cloudy
#COLOR_THRESHOLDS = [(19, 81, -24, 21, -35, -8)] # with sensor.set_auto_exposure(False, exposure_us=20000)

# when L min, mean, medium, max was 26, 47, 48, 70, this didn't work: COLOR_THRESHOLDS = [(19, 81, -24, 21, -35, -8)]
#COLOR_THRESHOLDS = [(36, 55, -19, 39, -77, -25)] # for when L is 26, 47, 48, 70

#COLOR_THRESHOLDS = [(36, 80, -19, 39, -77, -25)] # for when L is 5, 44, 46, 93
#COLOR_THRESHOLDS = [(36, 80, -19, 39, -77, -9)] # for when L is 37, 70, 70, 100
#COLOR_THRESHOLDS = \
        #[[(55, 60, -33, 0, -63, -21)], \
        #[(6, 55, -33, -10, -60, -23)], \
        #[(48, 68, -16, 6, -61, -18)], \
        #[(61, 71, -16, -1, -57, -8)], \
        #[(48, 62, -36, 9, -17, 25)], \
        #[(22, 67, -28, -9, -8, 17)], \
        #[(48, 77, -13, 5, -51, -13)], \
        #[(45, 76, -17, 19, -58, -12)], \
        #[(43, 90, -25, 8, -43, -9)], \
        #[(57, 72, -4, 20, -69, -31)]]

COLOR_THRESHOLDS = [[(42, 52, -1, 23, -61, -31)], \
                    [(44, 69, -3, 18, -72, -39)], \
                    [(44, 69, -3, 18, -72, -39)], \
                    [(16, 54, 2, 24, -52, -23)], \
                    [(35, 96, -60, -4, -52, -22)], \
                    [(35, 96, -60, -4, -52, 3)], \
                    [(3, 30, -4, 36, -68, -4)], \
                    [(30, 56, -33, -18, -34, 25)]]

thresholds_holder = ThresholdsHolder()
thresholds_holder.set_thresholds(COLOR_THRESHOLDS)
#thresholds_holder.set_thresholds([[(73, 80, -33, -21, -2, 32)], [(57, 83, -15, 0, 9, 38)], [(88, 100, -27, -12, -1, 24)], [(66, 84, -23, -14, 5, 25)], [(72, 86, -30, -13, -2, 32)]])

#no lines - don't use:
#thresholds_holder.set_thresholds([[(57, 93, -53, -7, -2, 37)]])

CHROMIVAR_THRESHOLD = [(32, 41, -4, 94, -79, -29)]

#kitchen table:
#COLOR_THRESHOLDS = [(30, 78, -18, 28, -70, -19)]
GRAYSCALE_THRESHOLDS = [(240, 255)] # White Line.
BINARY_VIEW = False # Helps debugging but costs FPS if on.
DO_NOTHING = False # Just capture frames...
FRAME_SIZE = sensor.QQVGA # Frame size.
BOTTOM_PX_TO_REMOVE = const(8) # maybe I screwed something up with my camera, but the last few rows are just noise

#AREA_THRESHOLD = const(25) # Raise to filter out false detections.
#PIXELS_THRESHOLD = const(25) # Raise to filter out false detections.
MAG_THRESHOLD = const(6) # Raise to filter out false detections.

# Tweak these values for your robocar.
THROTTLE_CUT_OFF_ANGLE = 2.5 # Maximum angular distance from 90 before we cut speed [0.0-90.0).
THROTTLE_CUT_OFF_RATE = .6 # How much to cut our speed boost (below) once the above is passed (0.0-1.0].
THROTTLE_GAIN = 11.0 # e.g. how much to speed up on a straight away

#read_value = ConfigFile().get_property("min_speed")
#if read_value:
    #THROTTLE_OFFSET = int(read_value)
#else:
THROTTLE_OFFSET = 0 # e.g. default speed (0 to 100)
THROTTLE_P_GAIN = 1.0
THROTTLE_I_GAIN = 0.0
THROTTLE_I_MIN = -0.0
THROTTLE_I_MAX = 0.0
THROTTLE_D_GAIN = 0.0
MIN_THROTTLE = 0

STEERING_OFFSET = 90 # Change this if you need to fix an imbalance in your car (0 to 180).

# Tweak these values for your robocar.
#THROTTLE_SERVO_MIN_US = const(1268) # from output_throttle Arduino sketch (power low?)
#THROTTLE_SERVO_MAX_US = const(1692)

# With LiPo battery (testing)
#THROTTLE_SERVO_MIN_US = const(1580) # from output_throttle Arduino sketch (power low?)
THROTTLE_SERVO_MAX_US = const(1600)
#THROTTLE_SERVO_MAX_US = const(1582)

# Tweak these values for your robocar.
STEERING_SERVO_MIN_US = const(1276)
STEERING_SERVO_MAX_US = const(1884)

THROTTLE_CUT_OFF_ANGLE = max(min(THROTTLE_CUT_OFF_ANGLE, 89.99), 0)
THROTTLE_CUT_OFF_RATE = max(min(THROTTLE_CUT_OFF_RATE, 1.0), 0.01)

def figure_out_my_steering(line, img):
    center = round(img.width() / 2)
    angle_1 = -math.degrees(math.atan((center - line.x1()) / (img.height() - BOTTOM_PX_TO_REMOVE)))
    angle_2 = theta(line) / 1.6
    steering = angle_1 + angle_2
    return constrain(90 - steering, 0, 180)

def figure_out_my_throttle(steering, fps): # steering -> [0:180]
    dist_from_90 = abs(steering - 90)
    throttle_linear = max((90 - dist_from_90) / 6, MIN_THROTTLE)
    return throttle_linear * math.log(fps*fps) / 4

device = pyb.UART(3, 19200, timeout_char = 100)
min_throttle_from_file = int(ConfigFile().get_property("min_speed"))
print("min_throttle_from_file=", min_throttle_from_file)

def set_servos(throttle, steering):
    if (throttle == 0):
        throttle = 1580
    else:
        throttle = remap(throttle, 1, 100, min_throttle_from_file, THROTTLE_SERVO_MAX_US)

    steering = remap(steering, 0, 180, STEERING_SERVO_MIN_US, STEERING_SERVO_MAX_US)

    device.write("{%05d,%05d}\r\n" % (throttle, steering))
    if DEBUG_PRINT_UART:
        print("{%05d,%05d}" % (throttle, steering))

def invert_steering(steering_in):
    # 180 - steering_in ?
    return ((steering_in - 90) * -1) + 90

magnitude = 0

# Camera Control Code

clock = time.clock()

old_time = pyb.millis()

throttle_old_result = None
throttle_i_output = 0
throttle_output = THROTTLE_OFFSET

steering_old_result = None
steering_i_output = 0
steering_output = STEERING_OFFSET

if WRITE_FILE:
    f = uio.open("out.txt", "at")
else:
    f = None

line_lost_count = 0
delta_time = 0

start_time = pyb.millis()
start_time2 = pyb.millis()
use_hist = use_chromivar =False

#bad_values = set()
#min_pulse_sensor = 9999
#max_pulse_sensor = 0
previous_steering = 90
steering_old_result = None
steering_i_output = 0

camera = Camera()
camera.set_log_level(INFO_LOG_LEVEL)
camera.take()
camera.adjust_exposure(60)

steeringPID = SteeringPid()

threshold5 = thresholds_holder.get_threshold()
camera.set_threshold(threshold5)

#try:
while(True):
    clock.tick()

    img = camera.take()
    (line, confidence) = camera.find_line_and_confidence()
    top_stats = img.get_statistics()
    print("top_stats=", top_stats)

    if (top_stats.l_mean() - 60 > 10):
        print("before", sensor.get_exposure_us(), "subtracting", int(sensor.get_exposure_us() / 5))
        sensor.set_auto_exposure(False, exposure_us = min(40000, sensor.get_exposure_us() - int(sensor.get_exposure_us() / 5)))
        print("after", sensor.get_exposure_us())
    elif (top_stats.l_mean() - 60 < -10):
        print("adding", int(sensor.get_exposure_us() / 10))
        sensor.set_auto_exposure(False, exposure_us = min(40000, sensor.get_exposure_us() + int(sensor.get_exposure_us() / 10)))
    #print("line=", line, ", confidence=", confidence)
    #stats = img.get_statistics()
    #print("stats=", stats)
    #if (stats.l_mean() > 70):
        #new_exposure_us = sensor.get_exposure_us() - 500
        #sensor.set_auto_exposure(False, exposure_us = new_exposure_us)
        ##sensor.skip_frames(5)
        ##stats = sensor.snapshot().get_statistics()

    print_string = ""
    magnitude = 0
    if line and line.magnitude() >= MAG_THRESHOLD:
        magnitude = line.magnitude()
        line_lost_count = max(0, line_lost_count - 2)

        #steering_output = steeringPID.calculate(figure_out_my_steering(line, camera.get_img()))
        steering_output = figure_out_my_steering(line, camera.get_img())

        throttle_new_result = figure_out_my_throttle(steering_output, clock.fps())

        # Throttle goes from 0% to 100%.
        throttle_output = max(min(round(throttle_new_result), 100), 0)

        print_string = "Line Ok - throttle %d, steering %d - line t: %d°, r: %d, x1: %d, y1: %d, x2: %d, y2: %d, 1/2: %d, mag: %d, conf: %.3f, exp: %d" % \
            (throttle_output , steering_output, line.theta(), line.rho(), line.x1(), line.y1(), line.x2(), line.y2(), sensor.width() / 2, line.magnitude(), \
            confidence, sensor.get_exposure_us())

    else:
        line_lost_count = line_lost_count + 1

        #if (line_lost_count > 5):
            #camera.set_threshold(COLOR_THRESHOLDS[round((line_lost_count % (len(COLOR_THRESHOLDS) * 5)) / 5)])

        #print(len(img.find_lines(threshold = 1000, theta_margin = 25, rho_margin = 25)))


        if (top_stats.l_lq() > 11 and top_stats.l_lq() < 25 \
                and top_stats.l_uq() > 47 and top_stats.l_uq() < 52 \
                and top_stats.l_mean() > 31 and top_stats.l_mean() < 37 \
                and top_stats.l_stdev() > 14 and top_stats.l_stdev() < 23 \
                and top_stats.l_mode() > 7 and top_stats.l_mode() < 29):
            threshold5 = [(50, 76, -16, -1, -41, -8)]
        else:
            threshold5 = thresholds_holder.get_threshold()
        camera.set_threshold(threshold5)

        if (line_lost_count > 50):
            set_servos(0, steering_output)
            camera.adjust_exposure(60)
        #if (stats.l_mean() < 70):
            #new_exposure_us = sensor.get_exposure_us() + 500
            #sensor.set_auto_exposure(False, exposure_us = new_exposure_us)
            ##sensor.skip_frames(5)
            ##stats = sensor.snapshot().get_statistics()

        throttle_output = throttle_output * .90 if (throttle_output > .1) else 0
        print_string = "Line Lost - throttle %d, steering %d, exposure %d, count %d, mag: %d, conf: %.3f" % \
                (throttle_output, steering_output, sensor.get_exposure_us(), line_lost_count, magnitude, confidence)


    if WRITE_FILE:
        f.write(print_string + "\n\r")
    set_servos(throttle_output, steering_output)
    if DEBUG_LINE_STATUS:
        print("FPS %f - %s" % (clock.fps(), print_string), ", threshold=", threshold5)

    if (WRITE_FILE and pyb.elapsed_millis(start_time) > 2000):
        f.flush()
        start_time = pyb.millis()

if WRITE_FILE:
    f.close()
#except Exception as exc:
    #raise exc
