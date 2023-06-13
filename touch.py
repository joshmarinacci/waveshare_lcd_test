import board
import time
import displayio
from vectorio import Circle
from waveshare128 import setup_display, Touch_CST816T

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

# setup accel
touch = Touch_CST816T()
# print("setup teh touch", touch._read_byte(0xA7), touch._read_byte(0xA8), touch._read_byte(0xA9))
# print('pulse width', touch._read_byte(0xED))
# print('auto wake time', touch._read_byte(0xF4))
# print('auto sleep time', touch._read_byte(0xF9))
while True:
    time.sleep(0.01)
    touch.update()
    # state = touch._read_byte(0x01)
    # num = touch._read_byte(0x02)
    # xy_point = touch._read_block(0x03,4)
    # x_point= ((xy_point[0]&0x0f)<<8)+xy_point[1]
    # y_point= ((xy_point[2]&0x0f)<<8)+xy_point[3]
    # angle = touch._read_byte(0xEF)
    print("state",touch.gestureId, "num",touch.fingerNum, "x", touch.x, "y", touch.y)
    circ.x = touch.x
    circ.y = touch.y
    circ.hidden = (touch.fingerNum == 0)
    display.refresh()


