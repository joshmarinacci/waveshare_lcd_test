import time
import board
import displayio
import vectorio
import adafruit_imageload
from waveshare128 import setup_display

TARGET_FPS = 100
display = setup_display()

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




