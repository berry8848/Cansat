import smbus
import time
import os

# Data Address
x_adr = 0x32
y_adr = 0x34
z_adr = 0x36

# ADXL345 class
class ADXL345():
    b = smbus.SMBus(1)
    address = 0x1D


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
myADXL345 = ADXL345()
myADXL345.setUp()


# LOOP
while 1:

    x = myADXL345.getValue(x_adr)
    y = myADXL345.getValue(y_adr)
    z = myADXL345.getValue(z_adr)
    #os.system("clear")
    print("X = %2.2f" % x, ",Y = %2.2f" % y, ",Z = %2.2f" % z)

    time.sleep(1)
