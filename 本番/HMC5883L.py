import os
import csv
import RPi.GPIO as GPIO
import smbus
import time

filename = "/home/pi/python_output/compass.csv"

header = "compass"


if not os.path.exists(filename):
    with open(filename, mode = "w") as f:
        f.write(header + "\n")


with open(filename, mode = "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    result = "".join(header)
    print(result)

    for row in reader:
        result = "".join(row)
        print(result)


# HMC5883L class
class HMC5883L():
    address = 0x1E
    myBus = ""
    if GPIO.RPI_INFO["P1_REVISION"] == 1:
        myBus = 0
    else:
        myBus = 1

    b = smbus.SMBus(myBus)

    def setUP(self):
        self.b.write_byte_data(self.address, 0x00, 0xF0)
        self.b.write_byte_data(self.address, 0x02, 0x00)

    def getValueX(self):
        return self.getValue(0x03)

    def getValueY(self):
        return self.getValue(0x07)

    def getValueZ(self):
        return self.getValue(0x05)

    def getValue(self, adr):
        tmp = self.b.read_byte_data(self.address, adr)
        sign = tmp & 0x80
        tmp = tmp & 0x7F
        tmp = tmp<<8
        tmp = tmp | self.b.read_byte_data(self.address, adr + 1)

        if sign > 0:
            tmp = tmp -32768

        return tmp


# MAIN
myHMC5883L = HMC5883L()
myHMC5883L.setUP()

# LOOP
while 1:

    x = myHMC5883L.getValueX()
    y = myHMC5883L.getValueY()
    z = myHMC5883L.getValueZ()
    os.system("clear")
    print("X = ", x)
    print("Y = ", y)
    print("Z = ", z)
    time.sleep(0.5)

    with open(filename, "a") as f:
        X = str(x)
        Y = str(y)
        Z = str(z)
        counter = f.write(X)
        f.write(",")
        f.write(Y)
        f.write(",")
        f.write(Z)
        f.write("\n")
