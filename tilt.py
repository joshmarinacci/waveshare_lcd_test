import board
import time
import displayio
from vectorio import Rectangle, Circle, Polygon
from waveshare128 import setup_display, QMI8658_Accelerometer

# setup accel
qmi = QMI8658_Accelerometer()


display = setup_display()

main = displayio.Group()


circ_palette = displayio.Palette(1)
circ_palette[0] = (255,0,255)
circ = Circle(pixel_shader=circ_palette, radius=10, x=120, y=120)
circ.x = 120
circ.y = 120
main.append(circ)

display.show(main)

xsamples = []
ysamples = []

while True:
    display.refresh()
    time.sleep(0.08)
    xyz = qmi.read_xyz()
    accel = {}
    gyro = {}
        
    accel['x'] = xyz[1]
    accel['y'] = xyz[0]
    accel['z'] = xyz[2]
    gyro['x'] = xyz[3]
    gyro['y'] = xyz[4]
    gyro['z'] = xyz[5]       
    # print('accel',accel)
    xsamples.append(accel['x'])
    ysamples.append(accel['y'])
    if len(xsamples) > 5:
        xsamples.pop(0)
    if len(ysamples) > 5:
        ysamples.pop(0)
    xavg = sum(xsamples)/len(xsamples)
    yavg = sum(ysamples)/len(ysamples)
    circ.x = 120 + int(xavg*100)
    circ.y = 120 + int(yavg*100*-1)



