import sensor, image, pyb, os, time, array, math, micropython, gc
sensor.reset()
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.set_windowing((round(sensor.width() / 3) - round(sensor.width() / 6), 0, round(sensor.width() / 3), sensor.height()))

sensor.skip_frames(time = 1500)
extra_fb = sensor.alloc_extra_fb(round(sensor.width() / 3), sensor.height(), sensor.RGB565)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)
clock = time.clock()
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
        return [(self.l_min + l_count, self.l_max + l_count, \
                self.a_min + a_count, self.a_max + a_count, \
                self.b_min + b_count, self.b_max + b_count)]
COLOR_THRESHOLDS = [(17, 69, -40, -13, -15, 20)]
img = sensor.snapshot()
while (img.get_statistics().l_mean() < 60):
    sensor.set_auto_exposure(False, exposure_us=sensor.get_exposure_us() + 200)
    img = sensor.snapshot()
stats = img.get_statistics()
count = 0
inc = 2
thresholdHolder = ThresholdHolder()
extra_fb.replace(sensor.snapshot())
l_min = 100
l_max = 0
a_min = 120
a_max = -120
b_min = 120
b_max = -120
for l_range in range(60, 80, 10):
    thresholdHolder.set_l_range(l_range)
    for a_range in range(50, 62, 2):
        thresholdHolder.set_a_range(a_range)
        for b_range in range(48, 76, 2):
            thresholdHolder.set_b_range(b_range)
            for l_count in range(max(-31, stats.l_min()), min(90, stats.l_max()), inc):
                for a_count in range(max(-31, stats.a_min()), min(43, stats.b_max()), inc):
                    for b_count in range(max(-76, stats.b_min()), min(15, stats.b_max()), inc):
                        for k in range(0, 10):
                            clock.tick()
                            thresholds = thresholdHolder.get_thresholds(l_count, a_count, b_count)
                            img = extra_fb.copy()
                            img.binary(thresholds)
                            rect = (round(img.width() / 2) - 10, 0, 28, img.height())
                            img.erode(1, threshold = 3).dilate(1, threshold = 1)
                            img.draw_rectangle(rect)
                            rect_stats = img.get_statistics(roi=rect)
                            img_stats = img.get_statistics()
                            print("rect stats=", rect_stats, ",\n img stats=", img_stats, "\n", clock.fps())
                            img.draw_string(0, img.height() - 10, repr(thresholds))
                            img.save("binary" + str(pyb.millis()) + ".jpeg", quality=50)
                            if (rect_stats.l_mean() > 40 and img_stats.l_mean() < 30):
                                cross_color = (0,255,0)
                                l_min = min(l_min, thresholds[0][0])
                                l_max = max(l_max, thresholds[0][1])
                                a_min = min(a_min, thresholds[0][2])
                                a_max = max(a_max, thresholds[0][3])
                                b_min = min(b_min, thresholds[0][4])
                                b_max = max(b_max, thresholds[0][5])
                            else:
                                cross_color = (255,0,0)
                                count += 1
                                if (count % 100 == 0):
                                    print("another", count, "images with no lines")
                                    count = 0
                            img.draw_cross(round(img.width()/2), round(img.height()/2), 20,color= cross_color)
        print("l_min=%d, l_max=%d, a_min=%d, a_max=%d, b_min=%d, b_max=%d" % \
                (l_min, l_max, a_min, a_max, b_min, b_max))
