# AprilTags
#
# Rotates the image based on the AprilTag
# Tested with TAG36H11

import sensor, image, time, math

sensor.reset()
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
#sensor.set_lens_correction(True, 400, 10)
sensor.skip_frames()
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

def degrees(radians):
    return (180 * radians) / math.pi

x_rot = 0
y_rot = 0
z_rot = 0
while(True):
    img = sensor.snapshot().rotation_corr(x_rotation = 0, \
                                          y_rotation = 0, \
                                          z_rotation = 0, \
                                          x_translation = 0, \
                                          y_translation = 0, \
                                          zoom = 1)
    for tag in img.find_apriltags():
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        print_args = (tag.x_translation(), tag.y_translation(), tag.z_translation(), \
            degrees(tag.x_rotation()), degrees(tag.y_rotation()), degrees(tag.z_rotation()))

        x_rot += 180 - degrees(tag.x_rotation())
        y_rot -= degrees(tag.y_rotation())
        z_rot += degrees(tag.z_rotation())
        print("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args)
