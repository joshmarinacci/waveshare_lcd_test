import board
import time
import board
import displayio
import gc9a01
import busio

from waveshare128 import setup_display

display = setup_display()

main = displayio.Group()
bitmap = displayio.OnDiskBitmap("/earth.bmp")
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
main.append(tile_grid)
display.show(main)
display.brightness = 1
while True:
    display.refresh()
    time.sleep(1.0)



