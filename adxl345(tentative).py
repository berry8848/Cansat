#coding: utf-8

import smbus
import time

bus = smbus.SMBus(1)

#IC address
address = 0x1D

x_adr = 0x32
y_adr = 0x34
z_adr = 0x36

def init_ADXL345():
    bus.write_byte_data(address, 0x2D, 0x08)

def measure_acc(adr):
    acc0 = bus.read_byte_data(address, adr)
    acc1 = bus.read_byte_data(address, adr + 1)

    acc = (acc1 << 8) + acc0

    if acc > 0x1FF:
        acc = (65536 - acc) * -1

    acc = acc * 3.9 / 1000

    return acc0

try:
    init_ADXL345()

    while 1:
        x_acc = measure_acc(x_adr)
        y_acc = measure_acc(y_adr)
        z_acc = measure_acc(z_adr)

        print('X = %2.2f' % x_acc, '[g], Y = %2.2f' % y_acc, '[g], Z = %2.2f' % z_acc, '[g]')

        time.sleep(0.5)

except KeyboardInterrupt:
    pass
