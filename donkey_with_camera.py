# This file is part of the OpenMV project.
# Copyright (c) 2013-2017 Ibrahim Abdelkader <iabdalkader@openmv.io> & Kwabena W. Agyeman <kwagyeman@openmv.io>
# This work is licensed under the MIT license, see the file LICENSE for details.

import sensor, image, time, math, pyb, uio, machine, sys, gc
from pyb import Pin, Timer
from pyb import ADC
from file_utils import ConfigFile
from util_functions import *
from machine import WDT
#from pulse_led import run_leds
from micropython import const
from class_camera import Camera

#class Tricks():
    #sensr = None
    #counter = 0
    #use_chromivar = False

    #def set_sensor(self, sensr):
        #self.sensr = sensr

    #def should_try_next_trick(self, count):
        #return count % 2

    #def set_to_next_trick(self):
        #self.counter += 1
        #if (self.counter == 1):


        #if (not use_chromivar and 10 < line_lost_count < 20):
            #use_chromivar = True
        #else:
            #use_chromivar = False

            #if (stats.l_mean() > 80):
                #new_exposure_us = sensor.get_exposure_us() - 5000
                #sensor.set_auto_exposure(False, exposure_us = new_exposure_us)

try:
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
    COLOR_THRESHOLDS = [[(60, 55, -33, 0, -60, -21)], \
            [(6, 55, -33, -10, -60, -23)], \
            [(48, 68, -16, 6, -61, -18)], \
            [(61, 71, -16, -1, -57, -8)]]

    CHROMIVAR_THRESHOLD = [(32, 41, -4, 94, -79, -29)]

    #kitchen table:
    #COLOR_THRESHOLDS = [(30, 78, -18, 28, -70, -19)]
    GRAYSCALE_THRESHOLDS = [(240, 255)] # White Line.
    BINARY_VIEW = False # Helps debugging but costs FPS if on.
    DO_NOTHING = False # Just capture frames...
    FRAME_SIZE = sensor.QQVGA # Frame size.
    FRAME_REGION = 0.8 # Percentage of the image from the bottom (0 - 1.0).
    FRAME_WIDE = 1.0 # Percentage of the frame width.
    BOTTOM_PX_TO_REMOVE = const(8) # maybe I screwed something up with my camera, but the last few rows are just noise

    AREA_THRESHOLD = const(25) # Raise to filter out false detections.
    PIXELS_THRESHOLD = const(25) # Raise to filter out false detections.
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
    MIN_THROTTLE = 0

    # Tweak these values for your robocar.
    STEERING_FACTOR = 1 # 1-
    STEERING_OFFSET = 90 # Change this if you need to fix an imbalance in your car (0 to 180).
    STEERING_P_GAIN = -40.0 # Make this smaller as you increase your speed and vice versa.
    STEERING_I_GAIN = 0.0
    STEERING_I_MIN = 0.0
    STEERING_I_MAX = 0.0
    STEERING_D_GAIN = -9 # Make this larger as you increase your speed and vice versa.

    # Tweak these values for your robocar.
    #THROTTLE_SERVO_MIN_US = const(1268) # from output_throttle Arduino sketch (power low?)
    #THROTTLE_SERVO_MAX_US = const(1692)

    # With LiPo battery (testing)
    THROTTLE_SERVO_MIN_US = const(1580) # from output_throttle Arduino sketch (power low?)
    THROTTLE_SERVO_MAX_US = const(1600)

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
        #print("angle_1=%.3f, angle_2=%.3f" % (angle_1, angle_2))
        steering = angle_1 + angle_2

        #steering = remap(line.x1(), 0, img.width(), 180, 0)
        #img.draw_string(10, 10, str(round(steering)))
        return constrain(90 - steering, 0, 180)

    t_power = math.log(THROTTLE_CUT_OFF_RATE) / math.log(math.cos(math.radians(THROTTLE_CUT_OFF_ANGLE)))


    def figure_out_my_throttle(steering, factor): # steering -> [0:180]
        dist_from_90 = abs(steering - 90)
        throttle_linear = max((90 - dist_from_90) / 6, MIN_THROTTLE)
        #normalized = throttle_linear / 12.9
        #throttle_out = (-math.cos(normalized * math.pi) + 1) * 6.5
        return throttle_linear

    # Servo Control Code
    device = pyb.UART(3, 19200, timeout_char = 100)
    prev_throttle = int(ConfigFile().get_property("min_speed"))

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
        if (throttle == 0):
            throttle = 1580
        else:
            throttle = remap(throttle, 1, 100, prev_throttle, THROTTLE_SERVO_MAX_US) # (input * 15.8) + 180

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

    def find_brightest_area(img):
        max_mean = 0
        rect_x = 0
        width = 10
        for x in range(0, img.width() - width, width):
            stats = img.get_statistics(roi = (x, 0, 11, width))
            #print("bright stats=", x, width, stats)
            if (stats.l_mean() > max_mean):
                rect_x = x
                max_mean = stats.l_mean()
        return (rect_x, 0, 11, width)

    camera = Camera()
    camera.reset_sensor()

    clock = time.clock()

    old_time = pyb.millis()

    throttle_old_result = None
    throttle_i_output = 0
    throttle_output = THROTTLE_OFFSET

    steering_old_result = None
    steering_i_output = 0
    steering_output = STEERING_OFFSET


    threshold5 = COLOR_THRESHOLDS[0]

    if WRITE_FILE:
        f = uio.open("out.txt", "at")
    else:
        f = None


    line_lost_count = 0
    delta_time = 0

    start_time = pyb.millis()
    start_time2 = pyb.millis()
    jump_start_counter = 10
    use_hist = use_chromivar =False

    adc = ADC("P6") # Must always be "P6".

    bad_values = set()
    min_pulse_sensor = 9999
    max_pulse_sensor = 0
    previous_steering = 90


    while True:
        clock.tick()

        img = camera.take()
        line = camera.find_line()

        stats = img.get_statistics()
        if (stats.l_mean() > 70):
            new_exposure_us = sensor.get_exposure_us() - 1000
            sensor.set_auto_exposure(False, exposure_us = new_exposure_us)
            #sensor.skip_frames(5)
            #stats = sensor.snapshot().get_statistics()

        camera.detect_glare()

        print_string = ""

        if line and (line.magnitude() >= MAG_THRESHOLD):
            #print('2 Garbage collect free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
            line_lost_count = max(0, line_lost_count - 2)
            #if (line_lost_count <= 0):
                #sensor.set_auto_whitebal(True)
            jump_start_counter = jump_start_counter - 1

            new_time = pyb.millis()
            delta_time = new_time - old_time
            old_time = new_time

            #if delta_time > 110:
                #pyb.LED(3).on()
            #else:
                #pyb.LED(3).off()

            steering_output = (figure_out_my_steering(line, camera.get_img()) + previous_steering) / 2
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


            #if (camera.get_img().get_statistics().l_mean() > 70):
                #camera.decrease_exposure()
            #elif (camera.get_img().get_statistics().l_mean() < 30):
                #camera.increase_exposure()
            #el
            if (line_lost_count > 5):
                camera.set_threshold(COLOR_THRESHOLDS[1])


            #if (tricks.should_try_next_trick(line_lost_count)):
                #tricks.set_to_next_trick()



            ##print("%s, %i" % (stats, sensor.get_exposure_us()))

            #print("(line_lost_count % len(COLOR_THRESHOLDS)) - 1=", (line_lost_count * 2 % len(COLOR_THRESHOLDS)))
            #threshold5 = COLOR_THRESHOLDS[(line_lost_count % len(COLOR_THRESHOLDS))]

            #if (line_lost_count / len(COLOR_THRESHOLDS) > 1):
                #use_hist = math.ceil(line_lost_count / len(COLOR_THRESHOLDS)) % 2 == 0
                #print("setting use_hist to", use_hist)

            #if (line_lost_count % (len(COLOR_THRESHOLDS) * 4) == 0):
                #use_hist = False
                #rgb_gain = sensor.get_rgb_gain_db()
                #sensor.set_auto_whitebal(False, rgb_gain_db = (rgb_gain[0], 0, 5))


            #if (stats.b_mean() < -10):
                #sensor.set_auto_whitebal(True)
                #sensor.skip_frames(2)

            #elif (line_lost_count == 15):
                #use_hist = True
            #elif (line_lost_count == 20):
                #sensor.set_auto_whitebal(True)
                #sensor.set_auto_exposure(True)
                #sensor.skip_frames(5)
            #elif (line_lost_count == 30):
                #use_hist = False
                #sensor.set_auto_whitebal(False)
                #sensor.set_auto_exposure(False)

                #sensor.skip_frames(5)
                #stats = sensor.snapshot().get_statistics()

            #elif (line_lost_count == 35):
                #use_hist = True
            #elif (line_lost_count == 40):
                #use_hist = False
                #if (stats.l_mean() < 70):
                    #new_exposure_us = sensor.get_exposure_us() + 5000
                    #sensor.set_auto_exposure(False, exposure_us = new_exposure_us)
                    ##sensor.skip_frames(5)
                    ##stats = sensor.snapshot().get_statistics()

            #elif (line_lost_count == 45):
                #use_hist = True
            #elif (line_lost_count == 50):
                #line_lost_count = 1


            #if (sensor.get_exposure_us() > 10000 or (line_lost_count > 10 and line_lost_count < 50)):
                #print("increasing blue gain")
                #rgb_gain = sensor.get_rgb_gain_db()
                #sensor.set_auto_whitebal(False, rgb_gain_db = (rgb_gain[0], 0, 6))
            #if (line_lost_count >= 50):
                #sensor.set_auto_whitebal(True)

            pyb.udelay(200)

            if REVERSE:
                throttle_output = throttle_output - 1

                if line_lost_count > 30:
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
            print("FPS %f - %s" % (clock.fps(), print_string), ", threshold=", threshold5)

        if (WRITE_FILE and pyb.millis() - start_time > 2000):
            f.flush()
            start_time = pyb.millis()

    if WRITE_FILE:
        f.close()
except Exception as exc:
    print(exc)
