# AprilTags
#
# Rotates the image based on the AprilTag
# Tested with TAG36H11

import sensor, image, time, math, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...

flipped = True


sensor.set_hmirror(flipped)
sensor.set_vflip(flipped)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

def degrees(radians):
    return (180 * radians) / math.pi

def line_filter_call_back(src, dst):
  global length
  length = len(src)
  for i in range(len(src)):
    dst[i] = src[i>>1]

def pid(p, i, delta_time, err):
    d = (err / delta_time) if delta_time else 0
    print("%f, %f, %f" % (p, i, d))
    return (.5 * p) + (1 * i) + (.5 * d)


dst2 = [320]
x_rot = 0
y_rot = 0
z_rot = 0
x_prev_i = 0
y_prev_i = 0
z_prev_i = 0
last_millis = pyb.millis()
x_i = 1
y_i = 1
z_i = 1
tmp = 0
y_tmp = 0

while(True):
    img = sensor.snapshot().rotation_corr(x_rotation = x_rot, \
                                          y_rotation = y_rot, \
                                          z_rotation = z_rot, \
                                          x_translation = 0, \
                                          y_translation = 0, \
                                          zoom = 1)
    for tag in img.find_apriltags():
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))

        tmp = degrees(tag.z_rotation())
        if (tmp > 180):
            tmp -= 360
        y_tmp = degrees(tag.y_rotation()) - 45
        if (y_tmp > 180):
            y_tmp -= 360
        print_args = (tag.x_translation(), tag.y_translation(), tag.z_translation(), \
            degrees(tag.x_rotation()), y_tmp, tmp)
        print("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args)

        x_rot += 180 - degrees(tag.x_rotation())
        y_rot += y_tmp
        if (flipped):
            #z_rot += tmp
            #x_rot = min(320, max(0, pid(180-degrees(tag.x_rotation()), x_i + x_prev_i, pyb.millis() - last_millis, x_rot + degrees(tag.x_rotation()))))
            #y_rot = min(160, max(-160, pid(-degrees(tag.y_rotation()), y_i + y_prev_i, pyb.millis() - last_millis, y_rot + degrees(tag.y_rotation()))))
            z_rot += pid(tmp, z_i + z_prev_i, pyb.millis() - last_millis, tmp)
            ##z_rot = 0 #degrees(tag.z_rotation())
            last_millis = pyb.millis()
            #x_prev_i = x_i
            #y_prev_i = y_i
            z_prev_i = z_i

        else:
            z_rot -= degrees(tag.z_rotation())
            delta_time = 0

        print("x_rot: %f, y_rot %f, z_rot %f" % (x_rot, y_rot, z_rot))
