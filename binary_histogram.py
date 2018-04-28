# Untitled - By: aakoch - Wed Dec 27 2017

import sensor, image, time

sensor.reset()
sensor.set_vflip(True)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

min_degree = -20
max_degree = 20

print("starting loop")
i = 255
j = 1
while j < 15:
    while i > 200:
        clock.tick()

        img = sensor.snapshot().binary([(220, 255)])
        lines = img.find_lines(threshold = 20000, theta_margin = 25, rho_margin = 25)
        print(len(lines))
        for l in lines:
            if (min_degree <= l.theta()) and (l.theta() <= max_degree):
                print(img.width())
                if (l.x1() < 40 or l.x1() > 180):
                    img.draw_line(l.line())

        #sensor.flush()
        #time.sleep(1000)
        #img = img.histeq()
        #print(img)
        ##print(hist_percent)
        ##for var in dir(histogram):
            ##val = getattr(histogram, var)
            ##print(str(var) + "=" + str(val))
        #img = img.binary([(220, 255)])
        #print(img)


        #histogram = img.get_histogram()
        ##img.erode(1, threshold = 2)
        ###img.dilate(round(i/2), threshold = j + 1)

        #percentile = 0.25
        #hist_percent = histogram.get_percentile(percentile)
        #print(hist_percent.value())
        #k = 0
        #while(hist_percent.value() > 100 and percentile > 0):
            #k += 1
            #img.erode(k, threshold = k + 1)
            ##percentile -= .01
            ##print(percentile)
            #hist_percent = histogram.get_percentile(percentile)
            #histogram = img.get_histogram()
        ##if(hist_percent.value() > 100 and percentile <= 0):
        ##print(k)


        #img.draw_string(0, 0, str(histogram.get_percentile(.25).value()))
        ##img.draw_string(0, 0, "i=" + str(i) + ", j=" + str(j))
        #sensor.flush()
        ##time.sleep(500)
        #i -= 1
    #j += 1
    #i = 255

