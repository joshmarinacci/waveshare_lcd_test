# revengeofthefifth_code.py -- deathstar animation for CircuitPython
# 5 May 2022 - @todbot / Tod Kurt
# uses one big tilegrid
# 
# ImageMagick commands used to go from GIF to TileGrid BMP:
#  convert -coalesce deathstar40.gif -resize 240x240 deathstar-%02d.bmp
#  montage -mode concatenate -tile x1 deathstar-*bmp deathstar_tile_tmp.bmp
#  convert deathstar_tile_tmp.bmp -colors 8 -type palette -compress none BMP3:deathstar_tile.bmp
# Copy resulting file to CIRCUITPY drive

import time
import board, busio
import displayio
import gc9a01
import gifio
import vectorio
import bitmaptools
import gc
import adafruit_imageload

displayio.release_displays()
spi = busio.SPI(clock=board.LCD_CLK, MOSI=board.LCD_DIN)

# try to switch to 24 mhz
# while not spi.try_lock():
#     pass
# spi.configure(baudrate=24000000) # Configure SPI for 24MHz
# spi.unlock()


# LCD_RST is 12 in the regular, but 13 for the touch version
display_bus = displayio.FourWire(spi, command=board.LCD_DC, chip_select=board.LCD_CS,reset=board.GP13)
display = gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=board.LCD_BL, rotation=0, auto_refresh=False)


main = displayio.Group()
display.root_group = main

# palette = displayio.Palette(3)
# palette[0] = 0xffffff
# palette[1] = 0x0000ff
# palette[2] = 0xff0000

# bmp = displayio.Bitmap(240,240, 3)
# bmp.fill(0)

# tilegrid = displayio.TileGrid(bitmap=bmp, pixel_shader=palette)
# main.append(tilegrid)

# bitmaptools.draw_line(bmp, 0,0, 240,240, 1)

# load bg image
bitmap, bg_pal = adafruit_imageload.load("bg.bmp")
# bitmap.pixel_shader.make_transparent(2)
image = displayio.TileGrid(bitmap, pixel_shader=bg_pal)
for n in range(len(bg_pal)):
    color = bg_pal[n]
    if color == 0xFFFFFF:
        print("found it")
        bg_pal.make_transparent(n)

print("Len is",len(bg_pal))

palette = displayio.Palette(4)
palette[0] = 0x000000 # black
palette[1] = 0xFFFFFF # white
palette[2] = 0xFF0000 # red
palette[3] = 0xECBE05 # gold

white = vectorio.Circle(pixel_shader=palette, radius=90, x=120, y=120)
white.color_index = 1
main.append(white)

iris = vectorio.Circle(pixel_shader=palette, radius=45, x=120, y=120)
iris.color_index = 2
main.append(iris)

pupil = vectorio.Circle(pixel_shader=palette, radius=25, x=120, y=120)
pupil.color_index = 0
main.append(pupil)

r = 80
top_lid = vectorio.Rectangle(pixel_shader=palette, width=r*2, height=90, x=120-78)
top_lid.color_index = 3
main.append(top_lid)

bot_lid = vectorio.Rectangle(pixel_shader=palette, width=r*2, height=90, x=120-78)
bot_lid.color_index = 3
main.append(bot_lid)



main.append(image) # shows the image

while True:
    iris.x = 120
    pupil.x = 120
    for t in range(0,41,2):
        top_lid.y = 120 - 90 - t
        bot_lid.y = 120 + t
        display.refresh(target_frames_per_second=30)
    time.sleep(1)
    for t in range(0,20,1):
        iris.x  = 120 - t
        pupil.x = 120 - t
        display.refresh(target_frames_per_second=30)
    for t in range(0,40,1):
        iris.x  = 120 - 20 + t
        pupil.x = 120 - 20 + t
        display.refresh(target_frames_per_second=30)
    for t in range(0,20,1):
        iris.x  = 120 + 20 - t
        pupil.x = 120 + 20 - t
        display.refresh(target_frames_per_second=30)
    for t in range(0,46,3):
        top_lid.y = 120 - 90 + t - 40
        bot_lid.y = 120 - t + 40
        display.refresh(target_frames_per_second=30)
    time.sleep(1)




