import board
import time
import displayio
import vectorio
from waveshare128 import setup_display
import rtc

r = rtc.RTC()
# r.datetime = time.struct_time((2023, 6, 12,   22, 10, -1,   0, -1, -1))

r.datetime = time.struct_time((2023, 1, 1, 8, 9, 15, 0, -1, -1))


display = setup_display()

main = displayio.Group()

bgpalette = displayio.Palette(1)
bgpalette[0] = 0xFFffFF # black
bgrect = vectorio.Rectangle(pixel_shader=bgpalette, width=240, height=240)
bgrect.color_index = 0
main.append(bgrect)

# load spritesheet
bitmap = displayio.OnDiskBitmap("/digits.bmp")
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader,
                               width=2, height=2,
                               tile_width=80, tile_height=80)
tile_grid.x = 120-80
tile_grid.y = 120-80
tile_grid[0,0] = 1
tile_grid[1,0] = 2
tile_grid[0,1] = 5
tile_grid[1,1] = 7


main.append(tile_grid)

display.show(main)

while True:
    print("datetime", r.datetime)
    hour = r.datetime.tm_hour
    minute = r.datetime.tm_min
    if hour > 12:
        hour = hour - 12
    h1 = int(hour / 10)
    h2 = hour % 10
    tile_grid[0,0] = h1
    tile_grid[1,0] = h2
    m1 = int(minute / 10)
    m2 = minute % 10
    tile_grid[0,1] = m1
    tile_grid[1,1] = m2

    display.refresh()
    time.sleep(1)
