import board
import time
import board
import displayio
import gc9a01
import busio

displayio.release_displays()

spi = busio.SPI(clock=board.LCD_CLK, MOSI=board.LCD_DIN)
# LCD_RST is 12 in the regular, but 13 for the touch version
display_bus = displayio.FourWire(spi, command=board.LCD_DC, chip_select=board.LCD_CS,reset=board.GP13)
display = gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=board.LCD_BL)

main = displayio.Group()
bitmap = displayio.OnDiskBitmap("/earth.bmp")
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
main.append(tile_grid)
display.show(main)
display.brightness = 1
while True:
    display.refresh()
    time.sleep(1.0)



