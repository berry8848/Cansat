import serial
import threading
import time
import micropyGPS

gps = micropyGPS.micropyGPS(9, 'dd')

def rungps():
    s = serial.Serial('/dev', 9600, timeout = 10)
    s.readline()
    while True:
        sentence = s.readline().decode('utf-8')
        if sentence[0] != '$':
            continue
        for x in sentence:
            gps.update(x)

gpsthread = threading.Thread(target=rungps, args=())
gpsthread.daemon = True
gpsthread.start()

while True:
    if gps.clean_sentences > 20:
        h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
        print('%2d:%02d:%04.1f' % (h, gps.timestamp[1], gps.timestamp[2]))
        print('緯度経度: %2.8f, %2.8f' % (gps.latitude[0], gps.longitude[0]))
        print('海抜: %f' % gps.altitude)
        print(gps.satellites_used)
        print('衛星番号: (仰角, 方位角, SN比)')
        for k, v in gps.satellite_data.items():
            print('%d: %s' % (k, v))
        print('')
    time.sleep(3.0)
