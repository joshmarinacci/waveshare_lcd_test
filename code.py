import microcontroller
import board
import time
import board
import displayio
import analogio
import gc9a01
import busio
import math
import random
import terminalio
import os
import vectorio
import supervisor
# import ustack

from vectorio import Rectangle, Circle, Polygon
from adafruit_display_text import label

displayio.release_displays()

spi = busio.SPI(clock=board.LCD_CLK, MOSI=board.LCD_DIN)
# LCD_RST is 12 in the regular, but 13 for the touch version
display_bus = displayio.FourWire(spi, command=board.LCD_DC, chip_select=board.LCD_CS,reset=board.GP13)
display = gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=board.LCD_BL)

print('display size',display.width, display.height)
board_type = os.uname().machine
print('board type is',board_type)
print("uname",os.uname())
print("board id is",board.board_id)
print("mcu temp is",microcontroller.cpu.temperature)
print("mcu voltage is",microcontroller.cpu.voltage)


main = displayio.Group()


circ_palette = displayio.Palette(1)
circ_palette[0] = (255,0,255)
main.append(Circle(pixel_shader=circ_palette, radius=100, x=50, y=50))


text = "Hello\nWorld!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00,
                        anchor_point=(0.5,0.5), anchored_position=(0,0))
text_group = displayio.Group(scale=2)
text_group.append(text_area) 
main.append(text_group)

display.show(main)

display.brightness = 1
while True:
    display.refresh()
    time.sleep(1.0)


