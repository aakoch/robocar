# Untitled - By: aakoch - Fri Apr 20 2018

import sensor, image, time, uos, ubinascii, utime

def delete_files():
    for num, filename in enumerate(uos.listdir()):
        print(filename)
        if (len(filename) > 9 and filename[-8:] == ".jpg.bmp"):
            uos.remove(filename)

def list_files():
    for num, filename in enumerate(uos.listdir()):
        if (len(filename) > 9 and filename[-8:] == ".jpg.bmp"):
            print("found file", filename)
        else:
            print(filename)

list_files()

for file in uos.ilistdir():
    out_string = ""
    if (file[1] == 0x4000):
        print('d - -', file[0])
    else:
        print('-', str(utime.localtime(uos.stat(file[0])[8])), str(uos.stat(file[0])[6] )+ "B", file[0])

    #for num, thing in enumerate(uos.stat(file[0])):
        #out_string += ('0x{0:02x}, '.format(thing))

    #print(out_string)
