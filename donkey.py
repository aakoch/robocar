# This file is part of the OpenMV project.
# Copyright (c) 2013-2017 Ibrahim Abdelkader <iabdalkader@openmv.io> & Kwabena W. Agyeman <kwagyeman@openmv.io>
# This work is licensed under the MIT license, see the file LICENSE for details.

import sensor, image, time, math, pyb, uio
from pyb import Pin, Timer


###########
# Settings
###########

WRITE_FILE = False
REVERSE = False
COLOR_LINE_FOLLOWING = False # False to use grayscale thresholds, true to use color thresholds.
JUMP_START_THROTTLE_INCREASE = 10
DEBUG_PRINT_UART = False # whether to write UART debug
DEBUG_LINE_STATUS = True
#COLOR_THRESHOLDS = [( 85, 100,  -40,  127,   20,  127)] # Yellow Line.
COLOR_THRESHOLDS = [(16, 88, -25, 27, -53, -14)] # Blue tape line
GRAYSCALE_THRESHOLDS = [(240, 255)] # White Line.
BINARY_VIEW = False # Helps debugging but costs FPS if on.
DO_NOTHING = False # Just capture frames...
FRAME_SIZE = sensor.QQVGA # Frame size.
FRAME_REGION = 0.8 # Percentage of the image from the bottom (0 - 1.0).
FRAME_WIDE = 1.0 # Percentage of the frame width.
BOTTOM_PX_TO_REMOVE = 4 # maybe I screwed something up with my camera, but the last few rows are just noise

AREA_THRESHOLD = 0 # Raise to filter out false detections.
PIXELS_THRESHOLD = 40 # Raise to filter out false detections.
MAG_THRESHOLD = 5 # Raise to filter out false detections.
MIXING_RATE = 0.9 # Percentage of a new line detection to mix into current steering.

# Tweak these values for your robocar.
THROTTLE_CUT_OFF_ANGLE = 3.0 # Maximum angular distance from 90 before we cut speed [0.0-90.0).
THROTTLE_CUT_OFF_RATE = 0.5 # How much to cut our speed boost (below) once the above is passed (0.0-1.0].
THROTTLE_GAIN = 20.0 # e.g. how much to speed up on a straight away
THROTTLE_OFFSET = 12.0 # e.g. default speed (0 to 100)
THROTTLE_P_GAIN = 1.0
THROTTLE_I_GAIN = 0.0
THROTTLE_I_MIN = -0.0
THROTTLE_I_MAX = 0.0
THROTTLE_D_GAIN = 0.0

# Tweak these values for your robocar.
STEERING_OFFSET = 90 # Change this if you need to fix an imbalance in your car (0 to 180).
STEERING_P_GAIN = -53.0 # Make this smaller as you increase your speed and vice versa.
STEERING_I_GAIN = 0.0
STEERING_I_MIN = -0.0
STEERING_I_MAX = 0.0
STEERING_D_GAIN = -9 # Make this larger as you increase your speed and vice versa.

# Tweak these values for your robocar.
THROTTLE_SERVO_MIN_US = 1540
THROTTLE_SERVO_MAX_US = 2000

# Tweak these values for your robocar.
STEERING_SERVO_MIN_US = 1270
# back/right max
STEERING_SERVO_MAX_US = 1800

FRAME_REGION = max(min(FRAME_REGION, 1.0), 0.0)
FRAME_WIDE = max(min(FRAME_WIDE, 1.0), 0.0)
MIXING_RATE = max(min(MIXING_RATE, 1.0), 0.0)

THROTTLE_CUT_OFF_ANGLE = max(min(THROTTLE_CUT_OFF_ANGLE, 89.99), 0)
THROTTLE_CUT_OFF_RATE = max(min(THROTTLE_CUT_OFF_RATE, 1.0), 0.01)

THROTTLE_OFFSET = max(min(THROTTLE_OFFSET, 100), 0)
STEERING_OFFSET = max(min(STEERING_OFFSET, 180), 0)

# Handle if these were reversed...
tmp = max(THROTTLE_SERVO_MIN_US, THROTTLE_SERVO_MAX_US)
THROTTLE_SERVO_MIN_US = min(THROTTLE_SERVO_MIN_US, THROTTLE_SERVO_MAX_US)
THROTTLE_SERVO_MAX_US = tmp

# Handle if these were reversed...
tmp = max(STEERING_SERVO_MIN_US, STEERING_SERVO_MAX_US)
STEERING_SERVO_MIN_US = min(STEERING_SERVO_MIN_US, STEERING_SERVO_MAX_US)
STEERING_SERVO_MAX_US = tmp

# This function maps the output of the linear regression function to a driving vector for steering
# the robocar. See https://openmv.io/blogs/news/linear-regression-line-following for more info.


old_cx_normal = None
def figure_out_my_steering(line, img):
    global old_cx_normal

    # Rho is computed using the inverse of this code below in the actual OpenMV Cam code.
    # This formula comes from the Hough line detection formula (see the wikipedia page for more).
    # Anyway, the output of this calculations below are a point centered vertically in the middle
    # of the image and to the left or right such that the line goes through it (cx may be off the image).
    cy = img.height() / 2
    cx = (line.rho() - (cy * math.sin(math.radians(line.theta())))) / math.cos(math.radians(line.theta()))

    # "cx_middle" is now the distance from the center of the line. This is our error method to stay
    # on the line. "cx_normal" normalizes the error to something like -1/+1 (it will go over this).
    cx_middle = cx - (img.width() / 2)
    cx_normal = cx_middle / (img.width() / 2)

    if old_cx_normal != None: old_cx_normal = (cx_normal * MIXING_RATE) + (old_cx_normal * (1.0 - MIXING_RATE))
    else: old_cx_normal = cx_normal
    return old_cx_normal

# Solve: THROTTLE_CUT_OFF_RATE = pow(sin(90 +/- THROTTLE_CUT_OFF_ANGLE), x) for x...
#        -> sin(90 +/- THROTTLE_CUT_OFF_ANGLE) = cos(THROTTLE_CUT_OFF_ANGLE)
t_power = math.log(THROTTLE_CUT_OFF_RATE) / math.log(math.cos(math.radians(THROTTLE_CUT_OFF_ANGLE)))
# cos(0) = 1 -> log 0
# cos(2) = 0.999390827019096 -> log = -0.000264641078415
# log(.5) = -0.301029995663981
# 0.301029995663981 / 0.000264641078415 = 1137.502905697495267 (t_power)???

def figure_out_my_throttle(steering): # steering -> [0:180]

    # pow(sin()) of the steering angle is only non-zero when driving straight... e.g. steering ~= 90
    t_result = math.pow(math.sin(math.radians(max(min(steering, 179.99), 0.0))), t_power)
    # 180 degrees = pi radians
    # sin(0 deg) = 0
    # sin(90 deg) = 1
    # sin(180 deg) = 0

    return (t_result * THROTTLE_GAIN) + THROTTLE_OFFSET

# Servo Control Code
device = pyb.UART(3, 19200, timeout_char = 1000)

## throttle [0:100] (101 values) -> [THROTTLE_SERVO_MIN_US, THROTTLE_SERVO_MAX_US]
# throttle [-100:100] (201 values) -> [THROTTLE_SERVO_MIN_US, THROTTLE_SERVO_MAX_US]
# steering [0:180] (181 values) -> [STEERING_SERVO_MIN_US, STEERING_SERVO_MAX_US]
def set_servos(throttle, steering):
    if throttle < 0:
        throttle = 1000 + ((throttle * (THROTTLE_SERVO_MIN_US - 1000 + 1)) / 101)
    else:
        throttle = THROTTLE_SERVO_MIN_US + ((throttle * (THROTTLE_SERVO_MAX_US - THROTTLE_SERVO_MIN_US + 1)) / 101)

    steering = STEERING_SERVO_MIN_US + ((steering * (STEERING_SERVO_MAX_US - STEERING_SERVO_MIN_US + 1)) / 181)
    device.write("{%05d,%05d}\r\n" % (throttle, steering))
    if DEBUG_PRINT_UART:
        if device.any():
            print("wrote: {%05d,%05d}, read: %s" % (throttle, steering, device.read()))
        else:
            print("wrote: {%05d,%05d}, read: nothing" % (throttle, steering))

def invert_steering(steering_in):
    return ((steering_in - 90) * -1) + 90

def repeat_stars(num):
    count = round(num / 2)
    char = ""
    for i in range(count):
        char = char + "*"
    return char

green_led = pyb.LED(2)
def turn_green_led_on(timer):
    green_led.on()

def turn_green_led_off(timer):
    green_led.off()

green_led_timer = Timer(4, freq=200)      # create a timer object using timer 4 - trigger at 1Hz
green_led_timer.callback(turn_green_led_on)          # set the callback to our tick function
green_led_timer_channel = green_led_timer.channel(1, Timer.PWM, callback=turn_green_led_off, pulse_width_percent=50)


#green_led_on = False
#magnitude = 0

#def tick(timer):            # we will receive the timer object when being called
    #global green_led_on
    ##if magnitude > 20:
        ##green_led_on = True
    ##else:
        ##green_led_on = False
    #pyb.LED(2).toggle()

#tim = Timer(4, freq=1000)      # create a timer object using timer 4 - trigger at 1Hz
#tim.callback(tick)          # set the callback to our tick function

# Camera Control Code
sensor.reset()
sensor.set_pixformat(sensor.RGB565 if COLOR_LINE_FOLLOWING else sensor.GRAYSCALE)
sensor.set_framesize(FRAME_SIZE)
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_windowing((int((sensor.width() / 2) - ((sensor.width() / 2) * FRAME_WIDE)), int(sensor.height() * (1.0 - FRAME_REGION)), \
                     int((sensor.width() / 2) + ((sensor.width() / 2) * FRAME_WIDE)), int(sensor.height() * FRAME_REGION) - BOTTOM_PX_TO_REMOVE))
sensor.skip_frames(time = 200)
if COLOR_LINE_FOLLOWING: sensor.set_auto_gain(False)
if COLOR_LINE_FOLLOWING: sensor.set_auto_whitebal(False)
clock = time.clock()

old_time = pyb.millis()

throttle_old_result = None
throttle_i_output = 0
throttle_output = THROTTLE_OFFSET

steering_old_result = None
steering_i_output = 0
steering_output = STEERING_OFFSET


if COLOR_LINE_FOLLOWING:
    if BINARY_VIEW:
        threshold5 = [(50, 100, -128, 127, -128, 127)]
    else:
        threshold5 = COLOR_THRESHOLDS
else:
    if BINARY_VIEW:
        threshold5 = [(127, 255)]
    else:
        threshold5 = GRAYSCALE_THRESHOLDS

if COLOR_LINE_FOLLOWING:
    lineColor = (127, 127, 127)
else:
    lineColor = 127


if WRITE_FILE:
    f = uio.open("out.txt", "at")
else:
    f = None

usb = pyb.USB_VCP() # This is a serial port object that allows you to
# communciate with your computer. While it is not open the code below runs.
usb_is_connected = usb.isconnected()

line_lost_count = 0
delta_time = 0

start_time = pyb.millis()
jump_start_counter = 10

while True:
    clock.tick()
    img = sensor.snapshot()#.lens_corr(3, .7)#.logpolar()#.linpolar()#.illuminvar().chrominvar().histeq()

    if BINARY_VIEW: img = img.binary(COLOR_THRESHOLDS if COLOR_LINE_FOLLOWING else GRAYSCALE_THRESHOLDS)
    if BINARY_VIEW: img.erode(1, threshold = 3).dilate(1, threshold = 1)
    if DO_NOTHING: continue

    # We call get regression below to get a robust linear regression of the field of view.
    # This returns a line object which we can use to steer the robocar.

    line = img.get_regression(threshold5, \
        area_threshold = AREA_THRESHOLD, pixels_threshold = PIXELS_THRESHOLD, \
        robust = True)

    print_string = ""

    if line and (line.magnitude() >= MAG_THRESHOLD):
        line_lost_count = 0
        jump_start_counter = jump_start_counter - 1

        if usb_is_connected:
            img.draw_line(line.line(), color = lineColor)

        new_time = pyb.millis()
        delta_time = new_time - old_time
        old_time = new_time

        if delta_time > 110:
            pyb.LED(3).on()
        else:
            pyb.LED(3).off()

        # Figure out steering and do steering PID
        steering_new_result = figure_out_my_steering(line, img)
        # error = setpoint - measured_value
        steering_delta_result = (steering_new_result - steering_old_result) if (steering_old_result != None) else 0
        steering_old_result = steering_new_result

        steering_p_output = steering_new_result # Standard PID Stuff here... nothing particularly interesting :)
        # integral = integral + error * dt
        steering_i_output = max(min(steering_i_output + steering_new_result, STEERING_I_MAX), STEERING_I_MIN)
        # STEERING_I_MAX = 0
        # STEERING_I_MIN = -0
        # derivative = (error - previous_error) / dt
        steering_d_output = ((steering_delta_result * 1000) / delta_time) if delta_time else 0
        steering_pid_output = (STEERING_P_GAIN * steering_p_output) + \
                              (STEERING_I_GAIN * steering_i_output) + \
                              (STEERING_D_GAIN * steering_d_output)
        # STEERING_P_GAIN = -23.0 # Make this smaller as you increase your speed and vice versa.
        # STEERING_I_GAIN = 0.0
        # STEERING_D_GAIN = -9 # Make this larger as you increase your speed and vice versa.

        # Steering goes from [-90,90] but we need to output [0,180] for the servos.
        steering_output = STEERING_OFFSET + max(min(round(steering_pid_output), 180 - STEERING_OFFSET), STEERING_OFFSET - 180)

        # Figure out throttle and do throttle PID
        throttle_new_result = figure_out_my_throttle(steering_output)
        throttle_delta_result = (throttle_new_result - throttle_old_result) if (throttle_old_result != None) else 0
        throttle_old_result = throttle_new_result

        throttle_p_output = throttle_new_result # Standard PID Stuff here... nothing particularly interesting :)
        # limit to THROTTLE_I_MIN < throttle < THROTTLE_I_MAX
        throttle_i_output = max(min(throttle_i_output + throttle_new_result, THROTTLE_I_MAX), THROTTLE_I_MIN) # always 0 if we don't change THROTTLE_I_MAX or THROTTLE_I_MIN
        # THROTTLE_I_MAX = 0
        # THROTTLE_I_MIN = -0
        throttle_d_output = ((throttle_delta_result * 1000) / delta_time) if delta_time else 0
        throttle_pid_output = (THROTTLE_P_GAIN * throttle_p_output) + \
                              (THROTTLE_I_GAIN * throttle_i_output) + \
                              (THROTTLE_D_GAIN * throttle_d_output)
        # THROTTLE_P_GAIN = 1.0
        # THROTTLE_I_GAIN = 0.0
        # THROTTLE_D_GAIN = 0.0
        # output = Kp * error + Ki * integral + Kd * derivative

        # Throttle goes from 0% to 100%.
        throttle_output = max(min(round(throttle_pid_output), 100), 0)

        if jump_start_counter > 0:
            throttle_output = throttle_output + JUMP_START_THROTTLE_INCREASE

        print_string = "Line Ok - throttle %d, steering %d - line t: %d, r: %d, x1: %d, y1: %d, x2: %d, y2: %d, 1/2way: %d, mag: %d" % \
            (throttle_output , steering_output, line.theta(), line.rho(), line.x1(), line.y1(), line.x2(), line.y2(), sensor.width() / 2, line.magnitude())
        #tup = (min(line.x1(), line.x2()), line.y1(), abs(line.x1() - line.x2()), abs(line.y1() - line.y2()))
        #img.draw_rectangle(tup)

        pyb.LED(1).off()
        #pyb.LED(2).on()
        green_led_timer_channel.pulse_width_percent(min(line.magnitude() * 4, 100))
        pyb.LED(3).off()
    else:
        line_lost_count = line_lost_count + 1

        if REVERSE:
            throttle_output = throttle_output - 1

            if line_lost_count > 10:
                if line_lost_count == 11:
                    #throttle_output = -1
                    steering_output = invert_steering(steering_output)

                #if line_lost_count > 11:
                    #throttle_output = throttle_output - 1

                if line_lost_count > 100:
                    #throttle_output = 0
                    pyb.LED(3).off()
                else:
                    pyb.LED(3).toggle()
            else:
                if line_lost_count == 3:
                    steering_output = steering_output - 10 if steering_output < 90 else steering_output + 10
                steering_output = max(min(steering_output, 180), 0)
        else:
            throttle_output = throttle_output * .92 if (throttle_output > .1) else 0
        print_string = "Line Lost - throttle %d, steering %d" % (throttle_output , steering_output)

        pyb.LED(1).on()
        pyb.LED(2).off()
        green_led_timer_channel.pulse_width_percent(0)

    #print(throttle_output)
    if WRITE_FILE:
        f.write(str(throttle_output) + "," + str(steering_output) + "\r")
    set_servos(throttle_output, steering_output)
    if DEBUG_LINE_STATUS:
        print("FPS %f - %s" % (clock.fps(), print_string))

    if (WRITE_FILE and pyb.millis() - start_time > 2000):
        f.flush()
        start_time = pyb.millis()

if WRITE_FILE:
    f.close()
