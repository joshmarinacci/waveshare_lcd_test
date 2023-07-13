import time
import board, busio
import displayio
import gc9a01
from random import randint
from random import uniform

SPEED = 64_000_000 # 1.53/10
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
bgpal[1] = 0x555555
bgpal[2] = 0xAAAAAA
bgpal[3] = 0xFFFFFF
bgpal[4] = 0xFFAAAA
bgpal[5] = 0xFF8888
bgpal[6] = 0xAA4444
bgpal[7] = 0x880000

bgbit = displayio.Bitmap(240,240,len(bgpal))
bgbit.fill(0)
bg_tile_grid = displayio.TileGrid(bgbit, pixel_shader=bgpal)
main.append(bg_tile_grid)

display.show(main)

def make_particle():
    return {
        'x': 120.0,
        'y': 120.0,
        'dx': uniform(-3,3),
        'dy': uniform(-3,3),
        'age':0
    }
def reset_particle(pt):
    pt['x'] = 120.0
    pt['y'] = 120.0
    pt['dx'] = uniform(-3,3)
    pt['dy'] = uniform(-3,3)
    pt['age'] = 0

parts = []

while True:
    if len(parts) < 200:
        parts.append(make_particle())
    for pt in parts:
        bgbit[int(pt['x']),int(pt['y'])] = 0        
        pt['x'] += pt['dx']
        pt['y'] += pt['dy']
        pt['age'] += 0.5
        if pt['x'] < 0 or pt['x'] >= 240 or pt['y'] < 0 or pt['y'] >= 240 or pt['age'] > 20:
            display.refresh()
            reset_particle(pt)
        else:
            bgbit[int(pt['x']),int(pt['y'])] = min(7,int(pt['age']/3))
            display.refresh()






