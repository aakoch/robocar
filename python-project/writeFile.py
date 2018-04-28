f = open("out.txt", "wt")
i = 1

while (i < 100):
    f.write(str(i * 10) + "," + str(100 - i * 10) + "\n")
    i = i + 1

f.close()