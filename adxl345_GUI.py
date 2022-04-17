import tkinter as tk
import smbus

bus = smbus.SMBus(1)

address = 0x1d

x_adr = 0x32
y_adr = 0x34
Z_adr = 0x36

root = tk.Tk()

c = tk.Canvas(root, width = 500, height = 500)

c.pack()



cc = c.create_oval(200, 200, 220, 220, fill = 'green')


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

def movement(val):
    m_val = 0
    if val > 0.5:
        m_val = 10
    elif val > 0.2:
        m_val = 5
    elif val < -0.5:
        m_val = -10
    elif val < -0.2:
        m_val = -5

    return m_val

def check_acc():
    x_acc = measure_acc(x_adr) * -1
    y_acc = measure_acc(y_adr)
    return [movement(x_acc), movement(y_acc)]

def draw():
    diff = check_acc()
    c.move(cc, diff[0], diff[1])
    root.after(50, draw)

init_ADXL345()

draw()

root.mainloop()
