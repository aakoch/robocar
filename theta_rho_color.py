# Show theta and rho

#THRESHOLD = [(88, 147)] # Grayscale threshold for dark things...
THRESHOLD = [(221, 255)] # sunny/bright light
BINARY_VISIBLE = False # Does binary first so you can see what the linear regression
                      # is being run on... might lower FPS though.
COLOR_THRESHOLDS = [(1, 80, -25, 37, -76, 10)] # Blue tape line 2 - upstairs - cloudy
USE_COLOR = False

import sensor, image, time, pyb, math

sensor.reset()
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.GRAYSCALE)
#sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # 160 x 120
sensor.skip_frames(time = 1000)     # WARNING: If you use QQVGA it may take seconds
clock = time.clock()                # to process a frame sometimes.
old_cx_normal = None
MIXING_RATE = .8
CENTER_LINE = (80, 0, 80, 120)


def x_y(theta):
    return (math.cos(math.radians(line.theta())), math.sin(math.radians(line.theta())))

def figure_out_my_steering(line, img):
    #global old_cx_normal

    ## Rho is computed using the inverse of this code below in the actual OpenMV Cam code.
    ## This formula comes from the Hough line detection formula (see the wikipedia page for more).
    ## Anyway, the output of this calculations below are a point centered vertically in the middle
    ## of the image and to the left or right such that the line goes through it (cx may be off the image).
    #cy = img.height() / 2
    #y = math.sin(math.radians(line.theta()))  # y
    #x = math.cos(math.radians(line.theta())) # x
    #cx = (line.rho() - (cy * y)) / x
    #print("y=%f, x=%f, cx=%f" % (y * line.rho(), x * line.rho(), cx))

    ## "cx_middle" is now the distance from the center of the line. This is our error method to stay
    ## on the line. "cx_normal" normalizes the error to something like -1/+1 (it will go over this).
    #cx_middle = cx - (img.width() / 2)
    #cx_normal = cx_middle / (img.width() / 2)
    #print("cx=%f, cx_middle=%f, cx_normal=%f" % (cx, cx_middle, cx_normal))

    ##exp_cx_normal = (1 - cx_normal) / cx_normal
    ##print("cx_normal=%f, exp_cx_normal=%f" % (cx_normal, exp_cx_normal))

    #if old_cx_normal != None: old_cx_normal = (cx_normal * MIXING_RATE) + (old_cx_normal * (1.0 - MIXING_RATE))
    #else: old_cx_normal = cx_normal
    #return old_cx_normal

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
    print("cx=%f, cx_middle=%f, cx_normal=%f" % (cx, cx_middle, cx_normal))

    if old_cx_normal != None: old_cx_normal = (cx_normal * MIXING_RATE) + (old_cx_normal * (1.0 - MIXING_RATE))
    else: old_cx_normal = cx_normal
    return old_cx_normal


def line_to_theta_and_rho(line):
    if line.rho() < 0: # quadrant 3/4
        if line.theta() < 90: # quadrant 3 (unused)
            return (math.sin(math.radians(line.theta())),
                math.cos(math.radians(line.theta() + 180)) * -line.rho())
        else: # quadrant 4
            return (math.sin(math.radians(line.theta() - 180)),
                math.cos(math.radians(line.theta() + 180)) * -line.rho())
    else: # quadrant 1/2
        if line.theta() < 90: # quadrant 1
            if line.theta() < 45:
                return (math.sin(math.radians(180 - line.theta())),
                    math.cos(math.radians(line.theta())) * line.rho())
            else:
                return (math.sin(math.radians(line.theta() - 180)),
                    math.cos(math.radians(line.theta())) * line.rho())
        else: # quadrant 2
            return (math.sin(math.radians(180 - line.theta())),
                math.cos(math.radians(line.theta())) * line.rho())


def remap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def constrain(val, min_val, max_val):
    return float(min(max_val, max(min_val, val)))

def calculate_steering(line):
    rho = line.rho()
    theta = line.theta()
    if rho < 0:
        rho = abs(rho)
        theta += 180
    return abs(80 - line.x1()) * theta + 90
#print("theta, rho, x1, y1, x2, y2, dist. from center, calculated steering")
steering_i_output = 0
old_time = pyb.millis()
prev_error = 0
integral = 0
prev_steering = 0

while(True):
    clock.tick()
    img = sensor.snapshot().binary([THRESHOLD]) if BINARY_VISIBLE else sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)

    new_time = pyb.millis()
    delta_time = new_time - old_time
    old_time = new_time

    # Returns a line object similar to line objects returned by find_lines() and
    # find_line_segments(). You have x1(), y1(), x2(), y2(), length(),
    # theta() (rotation in degrees), rho(), and magnitude().
    #
    # magnitude() represents how well the linear regression worked. It means something
    # different for the robust linear regression. In general, the larger the value the
    # better...
    line = img.get_regression(COLOR_THRESHOLDS if USE_COLOR else THRESHOLD, robust = True)

    if (line):
        img.draw_line(line.line(), color = [255, 0, 0] if USE_COLOR else 255)
    #print("FPS %f, mag = %s" % (clock.fps(), str(line.magnitude()) if (line) else "N/A"))
        rho = line.rho()
        theta = line.theta()
        if rho < 0:
            rho = abs(rho)
            theta += 180



        # Rho is computed using the inverse of this code below in the actual OpenMV Cam code.
        # This formula comes from the Hough line detection formula (see the wikipedia page for more).
        # Anyway, the output of this calculations below are a point centered vertically in the middle
        # of the image and to the left or right such that the line goes through it (cx may be off the image).
        #cx1 = line.rho()
        #cx2 = (line.rho() - (img.height() * math.sin(math.radians(line.theta())))) / math.cos(math.radians(line.theta()))

        cx1 = line.x1()
        cx2 = line.x2()
        steering = constrain(remap(cx1, 0, img.width(), 0, 180), 0, 180)
        measured = remap(cx2, 0, img.width(), 0, 180)
        steering_err = (steering - measured) / 180.0
        #steering_i_output = max(min(steering_i_output + steering_new_result, STEERING_I_MAX), STEERING_I_MIN)
        #integral = integral + steering_err * delta_time
        integral = max(min(integral + steering, 1), -1)

        derivative = (steering - prev_steering) * 1000 / delta_time
        #steering_d_output = ((steering_delta_result * 1000) / delta_time) if delta_time else 0

        output = steering + 1 * integral + 0 * derivative

        print("%3i, %3i, %3i, %3i, %3i, %3i, %3i, %3f, %.3f, %.5f, %.3f, %.3f, %f" % \
            (theta, rho, line.x1(), line.y1(), line.x2(), line.y2(), abs(80 - line.x1()), \
            steering, measured, steering_err, integral, derivative, output))

        prev_error = steering_err
        prev_steering = steering
        #pyb.delay(100)

        #p_out = k_p  * steering_err_at_t
        #i_out = k_i * sum_steering_errors

        #previous_error = 0
        #integral = 0
        #loop:
          #error = setpoint - measured_value
          #integral = integral + error * dt
          #derivative = (error - previous_error) / dt
          #output = Kp * error + Ki * integral + Kd * derivative
          #previous_error = error
          #wait(dt)
          #goto loop

        ## "cx_middle" is now the distance from the center of the line. This is our error method to stay
        ## on the line. "cx_normal" normalizes the error to something like -1/+1 (it will go over this).
        #cx_middle = cx - (img.width() / 2)
        #cx_normal = cx_middle / (img.width() / 2)
        #print("cx=%f, cx_middle=%f, cx_normal=%f" % (cx, cx_middle, cx_normal))

        #if old_cx_normal != None: old_cx_normal = (cx_normal * MIXING_RATE) + (old_cx_normal * (1.0 - MIXING_RATE))
        #else: old_cx_normal = cx_normal
        #steering_i_output = steering_i_output + steering
        #steering_d_output = ((steering_err * 1000) / delta_time) if delta_time else 0

        #steering_pid_output = (10 * steering_err) + \
                              #(1 * steering_i_output) + \
                              #(1 * steering_d_output)

        #print("%3i, %3i, %3i, %3i, %3i, %3i, %3i, %f, %f, %f" % \
            #(theta, rho, line.x1(), line.y1(), line.x2(), line.y2(), abs(80 - line.x1()), \
            #steering, steering_err, steering_pid_output))


        #img.draw_circle(0, 0, rho, color=[0, 255, 255] if USE_COLOR else 255)
        #for i in range(0, 20):
            #img.draw_rectangle([img.width() - 80, 0, img.width(), 20 - i], color=[255,255,255] if USE_COLOR else 200)
        img.draw_string(img.width() - 80, 0, "theta=%f\n  rho=%f" % (theta, rho), color=[0,0,0] if USE_COLOR else 240)

        #steering = line_to_theta_and_rho(line)
        #steering = max(180, steering)
        #img.draw_line((round(math.sin(line.theta())), 0, 80, 120), color=[0, 0, 255] if USE_COLOR else  240)
        #img.draw_line(CENTER_LINE, 200)
        #pyb.delay(500)

# About negative rho values:
#
# A [theta+0:-rho] tuple is the same as [theta+180:+rho].
