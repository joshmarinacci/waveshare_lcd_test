import time
import board, busio
import displayio
import gc9a01
import gifio
import vectorio
import bitmaptools
import gc
import adafruit_imageload
import math

# SPEED = 1_000_000 # 1.38s/f  6.9/10
# SPEED = 2_000_000 # 0.82s/f  4.2/10
# SPEED = 3_000_000 # 0.63s/f  3.2/10 
# SPEED = 5_000_000 # 0.48s/f  2.5/10 = 4fps
# SPEED = 10_000_000 # 0.38s/f  1.97/10  = 5fps
# SPEED = 15_000_000 # 0.34  1.79/10
# SPEED = 20_000_000 # 0.325s/f  1.7s / 10
# SPEED = 48_000_000 # 1.523/10
# SPEED = 100_000_000 # 1.44s / 10
# SPEED = 200_000_000 # 1.44s / 10
SPEED = 64_000_000 # 1.53/10
# SPEED = 99_000_000 
# setup the display
displayio.release_displays()
spi = busio.SPI(clock=board.LCD_CLK, MOSI=board.LCD_DIN)
# LCD_RST is 12 in the regular, but 13 for the touch version
display_bus = displayio.FourWire(spi, command=board.LCD_DC, 
                                 chip_select=board.LCD_CS,reset=board.GP13, baudrate=SPEED)
display = gc9a01.GC9A01(display_bus, width=240, height=240, 
                        backlight_pin=board.LCD_BL, rotation=0, auto_refresh=False)

main = displayio.Group()

bgpal = displayio.Palette(8)
bgpal[0] = 0x000000
bgpal[1] = 0xFFFFFF
bgpal[2] = 0xFF0000
bgpal[3] = 0x00FF00
bgpal[4] = 0x0000FF
bgpal[5] = 0xFFFF00
bgpal[6] = 0x00FFFF
bgpal[7] = 0xFFFFFF

BLACK = 0
WHITE = 1
RED = 2            
GREEN = 3
BLUE = 4
YELLOW = 5
CYAN = 6

bgbit = displayio.Bitmap(240,250,len(bgpal))
bgbit.fill(0)
size = 20

def fillRect(left,right,top,bottom, color):
    for i in range(left, right):
        for j in range(top, bottom):
            bgbit[i,j] = color

for i in range(0,240):
    for j in range(0,250):
        if (i % size < size/2) and (j % size < size/2):
            bgbit[i,j] = 1
        if (i % size >= size/2) and (j % size >= size/2):
            bgbit[i,j] = 1

fillRect(0,240, 0, 40, BLACK)
fillRect(0,240, 40, 80, RED)
fillRect(0,240, 80, 120, GREEN)
fillRect(0,240, 120, 160, BLUE)
fillRect(0,240, 160, 200, YELLOW)
fillRect(0,240, 200, 240, WHITE)

bg_tile_grid = displayio.TileGrid(bgbit, pixel_shader=bgpal)
main.append(bg_tile_grid)

display.show(main)
# display.refresh()

tfa = 40
scroll = 40
vsa = 240-100
tfb = 0
# set screen def     tft.vscrdef(tfa, height, tfb)

VSCRDEF = int(0x33)
VSCSAD = int(0x37)
# tfa, vsa, and bfa, each as two bytes, MSB
bts = bytearray([0,tfa,0,vsa])
display.bus.send(VSCRDEF,bts)
    # (tfa << 8 | tfa).to_bytes(2, 'big')
# display.bus.send(VSCRDEF, b"\x00\x2F\x00\x7F\x00\x00")

CASET = int(0x2a)
PASET = int(0x2b)
MEMWRITE = 0x2c
# display.bus.send(CASET, bytearray([0,100, 0,240])) # set cols to 20 -> 240
# display.bus.send(PASET, bytearray([0,100, 0,240])) # set rows to 20 -> 240
# display.bus.send(0x2c, bytearray([200,200,200,200]))

def set_window(x0,y0,x1,y1):
    display.bus.send(CASET, bytearray([0,x0, 0,x1])) # set cols to 20 -> 240
    display.bus.send(PASET, bytearray([0,y0, 0,y1])) # set rows to 20 -> 240
    display.bus.send(MEMWRITE, bytearray([]))

display.refresh()
# for i in range(100, 120):
#     for j in range(100, 120):
#         set_window(i,j,i,j)
#         display.bus.send(MEMWRITE, bytearray([123,123]))
#         # display.bus.send(MEMWRITE, bytearray([255,255]))
# print("wrote out white to whole FB")
# display.refresh()

# invert the display constantly
# while True:
#     display.bus.send(0x21,bytearray([]))    
#     time.sleep(0.5)
#     display.bus.send(0x20,bytearray([]))    
#     time.sleep(0.5)

checker_pattern_2_2 = bytearray([0,0, 255,255, 255,255, 0,0])

# vertical 
while True:
    # on every tick
    # set scroll offset  tft.vscsad(scroll+tfa)
    scroll += 2
    if scroll >= 240:
        print('wrap')
        scroll = 40
    # off = (scroll << 8 | scroll).to_bytes(2, 'big')
    # print("off",off)
    # print(scroll)
    # fillRect(0,120, scroll, scroll+1, CYAN)
    # display.refresh()

    # display.refresh()
    display.bus.send(VSCSAD, bytearray([0,scroll]))
    for i in range(0,120):
        j = scroll+158
        if j > 200:
            j -= 160;
        set_window(i*2,j,i*2+1,j+1)
        display.bus.send(MEMWRITE, checker_pattern_2_2)

    # time.sleep(0.1)




