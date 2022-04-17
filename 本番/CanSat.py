import os
import csv
import RPi.GPIO as GPIO
import smbus
import time
import math
import numpy as np

# Data Address
x_adr = 0x32
y_adr = 0x34
z_adr = 0x36


# csv
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


# HMC5883L Class
class HMC5883L():
    address = 0x1E
    myBus = ""
    if GPIO.RPI_INFO["P1_REVISION"] == 1:
        myBus = 0
    else:
        myBus = 1

    b = smbus.SMBus(myBus)

    def setUp(self):
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


# ADXL345 Class
class ADXL345():
    address = 0x1D
    b = smbus.SMBus(1)


    def setUp(self):
        self.b.write_byte_data(self.address, 0x2D, 0x08)


    def getValue(self, adr):
        acc0 = self.b.read_byte_data(self.address, adr)
        acc1 = self.b.read_byte_data(self.address, adr + 1)

        acc = (acc1 << 8) + acc0

        if acc > 0x1FF:
            acc = (65536 - acc) * -1

        acc = acc * 3.9 / 1000

        return acc


# Forming Instance
H = HMC5883L()
H.setUp()

A = ADXL345()
A.setUp()


# Compass Function
def compass():
    Mx = H.getValueX()
    My = H.getValueY()
    Mz = H.getValueZ()

    Ax = A.getValue(x_adr)
    Ay = A.getValue(y_adr)
    Az = A.getValue(z_adr)


    r = np.rad2deg(math.asin(Ax))
    p = np.rad2deg(math.asin( Ay / (1 - Ax**2)**(1/2)))

    k1 = np.array([[math.cos(r) , math.sin(p)*math.sin(r) , (-1)*math.cos(p)*math.sin(r)], [0 , math.cos(p) , math.sin(p)], [math.sin(r) , (-1)*math.sin(p)*math.cos(r) , math.cos(p)*math.cos(r)]])
    k2 = np.array([[Mx], [My], [Mz]])
    k3 = np.matmul(k1, k2)

    Hx = k3[0][0]
    Hy = k3[1][0]
    V = k3[2][0]

    theta = np.rad2deg(math.atan((Hy)/(Hx)))

    return theta



# TEST

while 1:

    result = compass()
    print(result)
    time.sleep(1)

    with open(filename, "a") as f:
        X = str(result)
        counter = f.write(X)
        f.write("\n")
