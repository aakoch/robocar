import sensor, image, time, pyb, math, micropython
micropython.alloc_emergency_exception_buf(2000)

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames()
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)


flag = False
started = False
def findTags(timer2):
    global flag
    global started
    #print(timer2)
    if (started):
        print(img)
        if (img.find_apriltags()):
            flag = True
        #for tag in img.find_apriltags():
            #print(tag)
            #img.draw_rectangle(tag.rect(), color = (255, 0, 0))

timer1 = pyb.Timer(4)              # create a timer object using timer 4
timer1.init(freq=1)                # trigger at 2Hz
timer1.callback(findTags)


while(True):
    img = sensor.snapshot()
    started = True
    #findTags(None)
    time.sleep(100)
