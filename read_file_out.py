# Untitled - By: aakoch - Sun Mar 4 2018

import uio
#kwargs = {"newline": "\n"}
#f = uio.open("out.txt", "wt")
#f.write("")
#f.close()

f = uio.open("out.txt", "rt")
line = f.readline();
while(len(line) != 0):
    print(line)
    line = f.readline()

