import time
import board, busio
import displayio
import gc9a01
import gifio
import vectorio
import bitmaptools
import gc
import adafruit_imageload

# SPEED = 24_000_000
SPEED = 100_000_000
# SPEED = 48000000
# SPEED = 99000000
TARGET_FPS = 100

# setup the display
displayio.release_displays()
spi = busio.SPI(clock=board.LCD_CLK, MOSI=board.LCD_DIN)
# LCD_RST is 12 in the regular, but 13 for the touch version
display_bus = displayio.FourWire(spi, command=board.LCD_DC, chip_select=board.LCD_CS,reset=board.GP13, baudrate=SPEED)
display = gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=board.LCD_BL, rotation=0, auto_refresh=False)



# make the main group
main = displayio.Group()
display.root_group = main

# load bg image
bitmap, bg_pal = adafruit_imageload.load("bg.bmp")
image = displayio.TileGrid(bitmap, pixel_shader=bg_pal)
# make white in the BG image be transparent
for n in range(len(bg_pal)):
    color = bg_pal[n]
    if color == 0xFFFFFF:
        bg_pal.make_transparent(n)


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
        display.refresh(target_frames_per_second=TARGET_FPS)
    time.sleep(1)
    for t in range(0,20,1):
        iris.x  = 120 - t
        pupil.x = 120 - t
        display.refresh(target_frames_per_second=TARGET_FPS)
    for t in range(0,40,1):
        iris.x  = 120 - 20 + t
        pupil.x = 120 - 20 + t
        display.refresh(target_frames_per_second=TARGET_FPS)
    for t in range(0,20,1):
        iris.x  = 120 + 20 - t
        pupil.x = 120 + 20 - t
        display.refresh(target_frames_per_second=TARGET_FPS)
    for t in range(0,46,3):
        top_lid.y = 120 - 90 + t - 40
        bot_lid.y = 120 - t + 40
        display.refresh(target_frames_per_second=TARGET_FPS)
    time.sleep(1)




