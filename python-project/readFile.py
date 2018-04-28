inFile = open("out.txt", "rt")
outFile = open("out2.txt", "wt")

line = inFile.readline()[:-1].split(",")
line2 = inFile.readline()[:-1].split(",")

def avg(i):
    total = int(line[i]) + int(line2[i])
    average = str(total / 2)
    print(line[i] + " + " + line2[i] + " = " + str(total) + " / 2 = " + average)
    return average


while (len(line2) > 1):
    throttle_avg = avg(0)
    steering_avg = avg(1)
    line = line2
    line2 = inFile.readline()[:-1].split(",")
    outFile.write(str(throttle_avg) + "," + str(steering_avg) + "\r")

inFile.close()
outFile.close()

# if current speed is 10 and read speed is 20, then
# read steering / (read speed / current speed)