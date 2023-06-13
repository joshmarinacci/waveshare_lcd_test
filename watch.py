import board
import time
import displayio
from vectorio import Circle, Rectangle
from waveshare128 import setup_display, Touch_CST816T

display = setup_display()

main = displayio.Group()

pal = displayio.Palette(4)
pal[0] = 0x000000
pal[1] = 0xFFFFFF
pal[2] = 0xFF0000
pal[3] = 0x0000FF

BLACK = 0
WHITE = 1
RED = 2
BLUE = 3

screen1 = displayio.Group()
rect = Rectangle(pixel_shader=pal, x=50,y=50,width=200,height=200)
rect.color_index = RED
screen1.append(rect)

screen2 = displayio.Group()
circ = Circle(pixel_shader=pal, radius=30)
circ.x = 120
circ.y = 120
circ.color_index = BLUE
screen2.append(circ)

main.append(screen1)
main.append(screen2)

screen1.hidden = True
screen2.hidden = False

display.show(main)

touch = Touch_CST816T()
prevnum = 0
while True:
    touch.update()
    if touch.fingerNum == 0 and prevnum == 1:
        print("end gesture", touch.gestureId)
        if touch.gestureId == 3:
            screen1.hidden = False
            screen2.hidden = True
        if touch.gestureId == 4:
            screen1.hidden = True
            screen2.hidden = False
    prevnum = touch.fingerNum
    display.refresh()


