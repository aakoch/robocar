# Untitled - By: aakoch - Sun Apr 22 2018

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 200)

sensor.__write_reg(0xC, sensor.__read_reg(0x0C) | 0xC0) # flips and mirrors
sensor.skip_frames(time = 200)

#sensor.__write_reg(0xC, sensor.__read_reg(0x0C) | 0x1) # color bars
#sensor.skip_frames(time = 200)

#sensor.__write_reg(0xC, sensor.__read_reg(0x0C) & 0xFE) # color bars off
#sensor.skip_frames(time = 2000)

#sensor.__write_reg(0xE, sensor.__read_reg(0x0E) | 0x80) # "night mode"? - I can't tell a differenct
#sensor.skip_frames(time = 2000)

#sensor.__write_reg(0xE, sensor.__read_reg(0x0E) & 0x7F) # "night mode" off?
#sensor.skip_frames(time = 2000)

sensor.set_auto_whitebal(False, (10, 0, 0))

sensor.set_auto_gain(False, 10)
sensor.skip_frames(time = 2000)
sensor.snapshot()

print("0x0=", hex(sensor.__read_reg(0x0)))
print("0x2=", hex(sensor.__read_reg(0x0)))


sensor.set_auto_gain(False)

print("0x0=", hex(sensor.__read_reg(0x0)))
print("0x2=", hex(sensor.__read_reg(0x0)))

sensor.set_auto_gain(False, 10)
sensor.skip_frames(time = 2000)
sensor.snapshot()

print("0x0=", hex(sensor.__read_reg(0x0)))
print("0x2=", hex(sensor.__read_reg(0x0)))
print("0x0=", hex(sensor.__read_reg(0x0)))
print("0x2=", hex(sensor.__read_reg(0x0)))

sensor.set_auto_gain(False, 6, 10)
sensor.skip_frames(time = 2000)
sensor.snapshot()

    #sensor.__write_reg(0x0, j)#0x44) # red auto gain off ?
    #sensor.skip_frames(time = 10)

    #for i in range(256):
        #print("i=",i)
        #sensor.__write_reg(0x2, i)#0xFF) # red gain
        #sensor.skip_frames(time = 40)

        #img = sensor.snapshot()
        #img.draw_string(10, 10, str(j))
        #img.draw_string(30, 10, str(i))
        #img.save(str(j) + "-" + str(i))

#sensor.__write_reg(0x2, 0x00) # red gain
#sensor.skip_frames(time = 2000)
