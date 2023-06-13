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
import board
import displayio
import gifio
from waveshare128 import setup_display

display = setup_display()

main = displayio.Group()


display.show(main) # put main group on display, everything goes in maingroup

# load up the big bitmap containing all the tiles
# bitmap = displayio.OnDiskBitmap(open("deathstar_tile.bmp", "rb"))
# deathstar = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, tile_width=240, tile_height=240 )

odg = gifio.OnDiskGif('eye.gif')

face = displayio.TileGrid(odg.bitmap,
                          pixel_shader=displayio.ColorConverter
                          (input_colorspace=displayio.Colorspace.RGB565_SWAPPED))

main.append(face)
display.refresh()

# i=0
# i_inc = 1
while True:
    time.sleep(0.1)
    odg.next_frame()

    # print("deathstar ranging ", i)
    # deathstar[0] = i  # animate it
    # i = i + i_inc
    # if i==39 or i==0 : i_inc = -i_inc # bounce animation back-n-forth
    # display.refresh(target_frames_per_second=24)

