# This file is part of the OpenMV project.
# Copyright (c) 2013-2017 Ibrahim Abdelkader <iabdalkader@openmv.io> & Kwabena W. Agyeman <kwagyeman@openmv.io>
# This work is licensed under the MIT license, see the file LICENSE for details.

import sensor, image, time, math, pyb, uio, machine, sys, gc, os
from pyb import Pin, Timer
from pyb import ADC
from file_utils import ConfigFile
from util_functions import *
from machine import WDT
#from pulse_led import run_leds
from micropython import const

#try:
if (True):
    usb = pyb.USB_VCP() # This is a serial port object that allows you to
    # communciate with your computer. While it is not open the code below runs.
    usb_is_connected = usb.isconnected()
    usb = None

    #if (machine.reset_cause() == machine.PWRON_RESET):
        #print("reset was caused by PWRON_RESET")
    #elif (machine.reset_cause() == machine.HARD_RESET):
        #print("reset was caused by HARD_RESET")
    #elif (machine.reset_cause() == machine.DEEPSLEEP_RESET):
        #print("reset was caused by DEEPSLEEP_RESET")
    #elif (machine.reset_cause() == machine.SOFT_RESET):
        #print("reset was caused by SOFT_RESET")


    ## run the pulse_led.py script if the board was reset because of the watchdog
    #if (machine.reset_cause() == machine.WDT_RESET):
        #print("reset was caused by WDT_RESET")
        #if (usb_is_connected):
            #run_leds(1000)
        #else:
            #run_leds(10000)
            #machine.reset()

    #elif not usb_is_connected:
        #wdt = WDT(timeout=10000)  # enable it with a timeout of 10s

    ## after running LEDs?
    #gc.collect()

    def remap(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    def constrain(val, min_val, max_val):
        return min(max_val, max(min_val, val))

    ###########
    # Settings
    ###########

    WRITE_FILE = False
    REVERSE = False
    COLOR_LINE_FOLLOWING = True # False to use grayscale thresholds, true to use color thresholds.
    JUMP_START_THROTTLE_INCREASE = 1
    DEBUG_PRINT_UART = False # whether to write UART debug
    DEBUG_LINE_STATUS = False
    #COLOR_THRESHOLDS = [( 85, 100, -40, 127, 20, 127)] # Yellow Line.
    #COLOR_THRESHOLDS =[(85, 100, -3, 127, -9, 94)] # do space
    #COLOR_THRESHOLDS = [(1, 80, -25, 28, -58, -10)] # Blue tape line
    #COLOR_THRESHOLDS = [(1, 80, -25, 37, -76, -47)] # Blue tape line 2 - upstairs - sunny
    #COLOR_THRESHOLDS = [(1, 80, -25, 37, -76, 0)] # Blue tape line 2 - upstairs - cloudy
    #COLOR_THRESHOLDS = [(19, 81, -24, 21, -35, -8)] # with sensor.set_auto_exposure(False, exposure_us=20000)

    # when L min, mean, medium, max was 26, 47, 48, 70, this didn't work: COLOR_THRESHOLDS = [(19, 81, -24, 21, -35, -8)]
    #COLOR_THRESHOLDS = [(36, 55, -19, 39, -77, -25)] # for when L is 26, 47, 48, 70

    #COLOR_THRESHOLDS = [(36, 80, -19, 39, -77, -25)] # for when L is 5, 44, 46, 93
    COLOR_THRESHOLDS = [(36, 80, -19, 39, -77, -9)] # for when L is 37, 70, 70, 100

    #kitchen table:
    #COLOR_THRESHOLDS = [(30, 78, -18, 28, -70, -19)]
    GRAYSCALE_THRESHOLDS = [(240, 255)] # White Line.
    BINARY_VIEW = False # Helps debugging but costs FPS if on.
    DO_NOTHING = False # Just capture frames...
    FRAME_SIZE = sensor.QQVGA # Frame size.
    FRAME_REGION = 0.8 # Percentage of the image from the bottom (0 - 1.0).
    FRAME_WIDE = 1.0 # Percentage of the frame width.
    BOTTOM_PX_TO_REMOVE = const(4) # maybe I screwed something up with my camera, but the last few rows are just noise

    AREA_THRESHOLD = const(20) # Raise to filter out false detections.
    PIXELS_THRESHOLD = const(20) # Raise to filter out false detections.
    MAG_THRESHOLD = const(6) # Raise to filter out false detections.
    MIXING_RATE = 0.8 # Percentage of a new line detection to mix into current steering.

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
    MIN_THROTTLE = 10

    # Tweak these values for your robocar.
    STEERING_FACTOR = 1 # 1-
    STEERING_OFFSET = 90 # Change this if you need to fix an imbalance in your car (0 to 180).
    STEERING_P_GAIN = -40.0 # Make this smaller as you increase your speed and vice versa.
    STEERING_I_GAIN = 0.0
    STEERING_I_MIN = 0.0
    STEERING_I_MAX = 0.0
    STEERING_D_GAIN = -9 # Make this larger as you increase your speed and vice versa.

    # Tweak these values for your robocar.
    THROTTLE_SERVO_MIN_US = const(1268) # from output_throttle Arduino sketch
    THROTTLE_SERVO_MAX_US = const(1692)

    # Tweak these values for your robocar.
    STEERING_SERVO_MIN_US = const(1276)
    STEERING_SERVO_MAX_US = const(1884)

    FRAME_REGION = max(min(FRAME_REGION, 1.0), 0.0)
    FRAME_WIDE = max(min(FRAME_WIDE, 1.0), 0.0)
    MIXING_RATE = max(min(MIXING_RATE, 1.0), 0.0)

    THROTTLE_CUT_OFF_ANGLE = max(min(THROTTLE_CUT_OFF_ANGLE, 89.99), 0)
    THROTTLE_CUT_OFF_RATE = max(min(THROTTLE_CUT_OFF_RATE, 1.0), 0.01)

    # This function maps the output of the linear regression function to a driving vector for steering
    # the robocar. See https://openmv.io/blogs/news/linear-regression-line-following for more info.


    def figure_out_my_steering(line, img):
        center = round(img.width() / 2)

        #angle_1 = remap(line.x1() * 1.1, 0, img.width(), -90, 90)
        angle_1 = -math.degrees(math.atan((center - line.x1()) / (img.height() - BOTTOM_PX_TO_REMOVE)))
        #if (line.x1() < img.width()):
            #angle_1 = -angle_1
        angle_2 = theta(line) / 1.6
        print("angle_1=%.3f, angle_2=%.3f" % (angle_1, angle_2))
        steering = angle_1 + angle_2

        #steering = remap(line.x1(), 0, img.width(), 180, 0)
        img.draw_string(10, 10, str(round(steering)))
        return constrain(90 - steering, 0, 180)
        #x1 = (line.x1() - center) * 2.5
        #x2 = line.x2() - center

        ##x1_norm = (line.x1() - center) / center
        ##print(str(math.sinh(x1_norm * math.pi) * 8))

        #distance_x2_from_center = center - x2
        ##img.draw_string(10, 10, str(round(x1 - x2)))
        ##steering = remap(line.x1(), 0, img.width(), 0, 180)
        ##img.draw_string(10, 30, str(steering + (distance_x2_from_center) / 3))
        ##img.draw_string(10, 50, str(line.theta() - 180 if line.theta() > 90 else line.theta()))

        #diff = x1 - x2

        ##if (x1 - x2 > 0 and x1 < 0):
            ### line is on the left side going to the right, so car will auto-correct itself by going straight
            ##for i in range(-1, 1):
                ##img.draw_line((round(img.width() / 2 + i), 0, round(img.width() / 2 + i), img.height()), color = (0, 0, 255))
            ##for i in range(0, 9):
                ##img.draw_line((i, 0, i, img.height()), color = (255, 0, 0))
            ##steering = 90# + (diff / 2)
        ##elif (x1 - x2 < 0 and x1 > 0):
            ### line is on the right side going to the left, so car will auto-correct itself by going straight
            ##for i in range(-1, 1):
                ##img.draw_line((round(img.width() / 2 + i), 0, round(img.width() / 2 + i), img.height()), color = (0, 0, 255))
            ##for i in range(1, 10):
                ##img.draw_line((img.width() - i, 0, img.width() - i, img.height()), color = (255, 0, 0))
            ##steering = 90# + (diff / 2)
        ##else:

        ##steering = remap(line.x1(), 0, img.width(), 180, 0)
        #steering = 180 - (1 - math.cos(line.x1() / img.width() * math.pi)) * 90


        #return steering #constrain(steering, 0, 180)

    # Solve: THROTTLE_CUT_OFF_RATE = pow(sin(90 +/- THROTTLE_CUT_OFF_ANGLE), x) for x...
    #        -> sin(90 +/- THROTTLE_CUT_OFF_ANGLE) = cos(THROTTLE_CUT_OFF_ANGLE)
    t_power = math.log(THROTTLE_CUT_OFF_RATE) / math.log(math.cos(math.radians(THROTTLE_CUT_OFF_ANGLE)))
    # cos(0) = 1 -> log 0
    # cos(2) = 0.999390827019096 -> log = -0.000264641078415
    # log(.5) = -0.301029995663981
    # 0.301029995663981 / 0.000264641078415 = 1137.502905697495267 (t_power)???

    def figure_out_my_throttle(steering, factor): # steering -> [0:180]
        dist_from_90 = abs(steering - 90)
        throttle_linear = max((90 - dist_from_90) / 6, MIN_THROTTLE)
        #normalized = throttle_linear / 12.9
        #throttle_out = (-math.cos(normalized * math.pi) + 1) * 6.5
        return throttle_linear

        ## pow(sin()) of the steering angle is only non-zero when driving straight... e.g. steering ~= 90
        #t_result = math.pow(math.sin(math.radians(max(min(steering, 179.99), 0.0))), t_power)
        ## 180 degrees = pi radians
        ## sin(0 deg) = 0
        ## sin(90 deg) = 1
        ## sin(180 deg) = 0

        ## the bigger the factor, the more we slow
        ##return max(MIN_THROTTLE, (t_result * THROTTLE_GAIN) + THROTTLE_OFFSET - (factor / 10)) + 15
        #return ((t_result * THROTTLE_GAIN) + THROTTLE_OFFSET)

    # Servo Control Code
    device = pyb.UART(3, 19200, timeout_char = 100)

    def read_from_uart():
        read_count = 15
        chars = ""
        if not usb_is_connected:
            while device.any() and chars[:-1] != "\n" and read_count > 0:
                read_char = str(device.read(1).decode("utf-8"))
                chars = chars + read_char
                read_count = read_count - 1
        return chars


    def set_servos(throttle, steering):
        throttle = remap(throttle, 0, 100, 1580, 1760) # (input * 15.8) + 180

        steering = remap(steering, 0, 180, STEERING_SERVO_MIN_US, STEERING_SERVO_MAX_US)

        device.write("{%05d,%05d}\r\n" % (throttle, steering))
        if DEBUG_PRINT_UART:
            if device.any():
                chars = read_from_uart()

                if chars:
                    print("wrote: {%05d,%05d}, read: %s" % (throttle, steering, chars[:-2] ))
                else:
                    print("wrote: {%05d,%05d}, read: nothing" % (throttle, steering))
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

    red_led = pyb.LED(1)
    green_led = pyb.LED(2)
    blue_led = pyb.LED(3)
    def turn_green_led_on(timer):
        green_led.on()

    def turn_green_led_off(timer):
        green_led.off()

    green_led_timer = Timer(4, freq=200)      # create a timer object using timer 4 - trigger at 1Hz
    green_led_timer.callback(turn_green_led_on)          # set the callback to our tick function
    green_led_timer_channel = green_led_timer.channel(1, Timer.PWM, callback=turn_green_led_off, pulse_width_percent=50)

    green_led_on = False
    magnitude = 0

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
    def reset_sensor():
        sensor.reset()
        sensor.set_pixformat(sensor.RGB565 if COLOR_LINE_FOLLOWING else sensor.GRAYSCALE)
        sensor.set_framesize(FRAME_SIZE)
        sensor.set_vflip(True)
        sensor.set_hmirror(True)
        sensor.set_windowing((int((sensor.width() / 2) - ((sensor.width() / 2) * FRAME_WIDE)), int(sensor.height() * (1.0 - FRAME_REGION)), \
                             int((sensor.width() / 2) + ((sensor.width() / 2) * FRAME_WIDE)), int(sensor.height() * FRAME_REGION) - BOTTOM_PX_TO_REMOVE))
        sensor.set_auto_exposure(True)
        #sensor.set_auto_exposure(False, exposure_us=500)
        sensor.skip_frames(time = 1400)
        if COLOR_LINE_FOLLOWING: sensor.set_auto_gain(False)
        if COLOR_LINE_FOLLOWING: sensor.set_auto_whitebal(False)

    def capture_image22222():
        if not "temp" in os.listdir(): os.mkdir("temp") # Make a temp directory

        print("About to save background image...")
        sensor.skip_frames(time = 500) # Give the user time to get ready.
        sensor.snapshot().save("temp/bg.bmp")
        print("Saved background image - Now frame differencing!")

    reset_sensor()
    capture_image22222()

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
        lineColor = (255, 127, 127)
    else:
        lineColor = 127


    if WRITE_FILE:
        f = uio.open("out.txt", "at")
    else:
        f = None


    line_lost_count = 0
    delta_time = 0

    start_time = pyb.millis()
    start_time2 = pyb.millis()
    jump_start_counter = 10
    use_hist = False

    adc = ADC("P6") # Must always be "P6".

    bad_values = set()
    min_pulse_sensor = 9999
    max_pulse_sensor = 0
    previous_steering = 90

    while True:
        clock.tick()

        #print('1 Garbage collect free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))

        #if not usb_is_connected:
            #wdt.feed()

        #pulse_sensor = adc.read()
        ##print("ADC = %d" % (pulse_sensor))
        #if  pyb.millis() - start_time2 > 5000:
            #min_pulse_sensor = pulse_sensor
            #max_pulse_sensor = pulse_sensor
            #start_time2 = pyb.millis()
        #else:
            #min_pulse_sensor = min(min_pulse_sensor, pulse_sensor)
            #max_pulse_sensor = max(max_pulse_sensor, pulse_sensor)
            #print(str(min_pulse_sensor) + " - " + str(max_pulse_sensor))

        ##if ((pulse_sensor > 3622 and pulse_sensor < 3711)):
            ##detected_movement = True
            ###print("ADC = %d - detected movement =%s" % (pulse_sensor, detected_movement))
        ##else:
            ##detected_movement = False


        #if line_lost_count > 5 and use_hist:
            #use_hist = False

        #if line_lost_count > 50 and not use_hist:
            ##reset_sensor() # I think I was just using this to force auto white balance or auto gain
            #line_lost_count = 0
            #use_hist = True

        if use_hist:
            img = sensor.snapshot().histeq()
        #elif use_binary:
            #img = sensor.snapshot().binary(0)
        else:
            img = sensor.snapshot()#.histeq()#.lens_corr(3, .7)#.logpolar()#.linpolar()#.illuminvar().chrominvar().histeq()


        #stats = img.get_statistics()

        #if (stats.l_max() - stats.l_min() < 26):
            #sensor.set_auto_exposure(False, exposure_us=20000)
        #elif (stats.l_max() - stats.l_min() > 30):
            #sensor.set_auto_exposure(True)


        # Replace the image with the "abs(NEW-OLD)" frame difference.
        img.difference("temp/bg.bmp")

        hist = img.get_histogram()
        # This code below works by comparing the 99th percentile value (e.g. the
        # non-outlier max value against the 90th percentile value (e.g. a non-max
        # value. The difference between the two values will grow as the difference
        # image seems more pixels change.
        diff = hist.get_percentile(0.99).l_value() - hist.get_percentile(0.90).l_value()
        #triggered = diff > 5
        print(diff, hist)
        if (diff < 5):
            print("same")

        hist = None
        gc.collect()
        #print(clock.fps(), triggered) # Note: Your OpenMV Cam runs about half as fast while
        # connected to your computer. The FPS should increase once disconnected.


        # 74, 98, 100, 100 was too bright, but the camera thought 25, 50, 50, 61 was too low. I
        # probably need to change the condition for when it changes the exposure.
        # 26, 55, 55, 67 didn't look too dark


        if use_hist:
            img = sensor.snapshot().histeq()
        #elif use_binary:
            #img = sensor.snapshot().binary(0)
        else:
            img = sensor.snapshot()#.histeq()#.lens_corr(3, .7)#.logpolar()#.linpolar()#.illuminvar().chrominvar().histeq()




        #if BINARY_VIEW: img = img.binary(COLOR_THRESHOLDS if COLOR_LINE_FOLLOWING else GRAYSCALE_THRESHOLDS)
        #if BINARY_VIEW: img.erode(1, threshold = 3).dilate(1, threshold = 1)
        #if DO_NOTHING: continue

        # We call get regression below to get a robust linear regression of the field of view.
        # This returns a line object which we can use to steer the robocar.

        line = img.get_regression(threshold5, \
            area_threshold = AREA_THRESHOLD, pixels_threshold = PIXELS_THRESHOLD, \
            robust = True, roi=(0, 0, img.width(), round(img.height() / 2)))

        img.draw_line((round(img.width() / 2), 0, round(img.width() / 2), img.height()), color=(0, 0, 255))
        print_string = ""

        if line and (line.magnitude() >= MAG_THRESHOLD):
            #print('2 Garbage collect free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
            line_lost_count = max(0, line_lost_count - 2)
            #if (line_lost_count <= 0):
                #sensor.set_auto_whitebal(True)
            jump_start_counter = jump_start_counter - 1

            if usb_is_connected:
                img.draw_line(line.line(), color = lineColor)
                img.draw_string(img.width() - 30, 10, str(line.magnitude()))

            new_time = pyb.millis()
            delta_time = new_time - old_time
            old_time = new_time

            #if delta_time > 110:
                #pyb.LED(3).on()
            #else:
                #pyb.LED(3).off()

            steering_output = (figure_out_my_steering(line, img) + previous_steering) / 2
            previous_steering = steering_output

            # Figure out throttle and do throttle PID
            factor = abs(line.x2() - 90)
            throttle_new_result = figure_out_my_throttle(steering_output, factor)
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

            # y1 is ALWAYS 0
            # y2 is ALWAYS 91
            print_string = "Line Ok - throttle %d, steering %d - line t: %d°, r: %d, x1: %d, y1: %d, x2: %d, y2: %d, 1/2: %d, mag: %d" % \
                (throttle_output , steering_output, line.theta(), line.rho(), line.x1(), line.y1(), line.x2(), line.y2(), sensor.width() / 2, line.magnitude())
            #tup = (min(line.x1(), line.x2()), line.y1(), abs(line.x1() - line.x2()), abs(line.y1() - line.y2()))
            #img.draw_rectangle(tup)

            pyb.LED(1).off()
            #pyb.LED(2).on()
            green_led_timer_channel.pulse_width_percent(min(line.magnitude() * 4, 100))
            pyb.LED(3).off()

            #print('3 Garbage collect free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
        else:
            line_lost_count = line_lost_count + 1


            #print("%s, %i" % (stats, sensor.get_exposure_us()))
            stats = img.get_statistics()

            if stats.l_mean() > 70:
                new_exposure_us = sensor.get_exposure_us() - 500
            else:
                new_exposure_us = sensor.get_exposure_us() + 500

            sensor.set_auto_exposure(False, exposure_us = new_exposure_us)

            if (line_lost_count == 1):
                rgb_gain = sensor.get_rgb_gain_db()
                sensor.set_auto_whitebal(False, rgb_gain_db = (rgb_gain[0], 0, 6))
            elif (line_lost_count > 30 and line_lost_count < 100):
                sensor.set_auto_whitebal(True)
            # for times when it loses the line, but momentum keeps it going
            elif (line_lost_count == 100):
                rgb_gain = sensor.get_rgb_gain_db()
                sensor.set_auto_whitebal(False, rgb_gain_db = (rgb_gain[0], 0, 6))

            #if (sensor.get_exposure_us() > 10000 or (line_lost_count > 10 and line_lost_count < 50)):
                #print("increasing blue gain")
                #rgb_gain = sensor.get_rgb_gain_db()
                #sensor.set_auto_whitebal(False, rgb_gain_db = (rgb_gain[0], 0, 6))
            #if (line_lost_count >= 50):
                #sensor.set_auto_whitebal(True)

            pyb.udelay(200)

            #if REVERSE:
                #throttle_output = throttle_output - 1

                #if line_lost_count > 30:
                    #if line_lost_count == 11:
                        ##throttle_output = -1
                        #steering_output = invert_steering(steering_output)

                    ##if line_lost_count > 11:
                        ##throttle_output = throttle_output - 1

                    #if line_lost_count > 100:
                        ##throttle_output = 0
                        #pyb.LED(3).off()
                    #else:
                        #pyb.LED(3).toggle()
                #else:
                    #if line_lost_count == 3:
                        #steering_output = steering_output - 10 if steering_output < 90 else steering_output + 10
                    #steering_output = max(min(steering_output, 180), 0)
            #else:
            throttle_output = throttle_output * .95 if (throttle_output > .1) else 0
            print_string = "Line Lost - throttle %d, steering %d, exposure %d, count %d" % \
                    (throttle_output, steering_output, sensor.get_exposure_us(), line_lost_count)

            pyb.LED(1).on()
            green_led.off()
            green_led_timer_channel.pulse_width_percent(0)

        #print('4 Garbage collect free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))

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
#except Exception as exc:
    #print(exc)
