import time
import board
import displayio
import bitmaptools
from waveshare128 import setup_display, Touch_CST816T

display = setup_display()

# make the main group
main = displayio.Group()
display.root_group = main

# setup accel
touch = Touch_CST816T()

pal = displayio.Palette(6)
pal[0] = 0xFF0000
pal[1] = 0xCC0000
pal[2] = 0x880000
pal[3] = 0x660000
pal[4] = 0x330000
pal[5] = 0x000000

bitmap = displayio.Bitmap(240,240,len(pal))
bitmap.fill(5)
tilemap = displayio.TileGrid(bitmap,pixel_shader=pal)

main.append(tilemap)

def kline(pt1, pt2, color):
    bitmaptools.draw_line(bitmap, pt1['x'], pt1['y'], pt2['x'], pt2['y'], color)
    bitmaptools.draw_line(bitmap, 240-pt1['x'], pt1['y'], 240-pt2['x'], pt2['y'], color)
    bitmaptools.draw_line(bitmap, pt1['x'], 240-pt1['y'], pt2['x'], 240-pt2['y'], color)
    bitmaptools.draw_line(bitmap, 240-pt1['x'], 240-pt1['y'], 240-pt2['x'], 240-pt2['y'], color)

prev = { 'x':0, 'y':0,}
color = 3
while True:
    time.sleep(0.01)
    touch.update()
    curr = { 'x':touch.x, 'y':touch.y}
    color += 1
    if color > 5:
        color = 2
    kline(prev, curr, color)
    prev = curr
    display.refresh()



