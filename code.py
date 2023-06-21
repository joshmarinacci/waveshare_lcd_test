import board
import time
import displayio
from vectorio import Circle
from waveshare128 import setup_display, Touch_CST816T

print("setting up the Wavehsare 1.28 RP2040")

display = setup_display()
main = displayio.Group()
circ_palette = displayio.Palette(2)
circ_palette[0] = (255,0,255)
circ_palette[1] = (255,255,255)
circ = Circle(pixel_shader=circ_palette, radius=30)
circ.x = 120
circ.y = 120
circ.color_index = 1
circ.hidden = False
main.append(circ)

display.show(main)

touch = Touch_CST816T()

while True:
    time.sleep(0.01)
    touch.update()
    print("state",touch.gestureId, "num",touch.fingerNum, "x", touch.x, "y", touch.y)
    circ.x = touch.x
    circ.y = touch.y
    # circ.hidden = (touch.fingerNum == 0)
    display.refresh()
