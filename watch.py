import board
import time
import displayio
from adafruit_displayio_layout.layouts.page_layout import PageLayout
from adafruit_display_text.bitmap_label import Label
from adafruit_displayio_layout.widgets.flip_input import FlipInput
from vectorio import Circle, Rectangle
from waveshare128 import setup_display, Touch_CST816T
from adafruit_button import Button

import rtc
import terminalio

# setup the RTC and time
r = rtc.RTC()
# r.datetime = time.struct_time((2023, 6, 12,   22, 10, -1,   0, -1, -1))

display = setup_display()

# setup the screens
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


layout = PageLayout(x=0, y=0)


# setup page 1
view_time_page = displayio.Group()
rect = Rectangle(pixel_shader=pal, x=0,y=0,width=240,height=240)
rect.color_index = RED
view_time_page.append(rect)

time_label = Label(
    font=terminalio.FONT,
    text="The time is here",
    x=120-40,
    y=100,
    scale=3,
)
view_time_page.append(time_label)
layout.add_content(view_time_page, page_name='page 1')


# setup page 2
page2 = displayio.Group()
page2bg = Rectangle(pixel_shader=pal,x=0,y=0,width=240,height=240)
page2bg.color_index = BLUE
page2.append(page2bg)
hour_setter = FlipInput(
    display,
    value_list=["{0:02d}".format(x) for x in range(1, 12)],
    # use a list of strings from 01 through 31
    # use the {0:02d} format string to always use two digits (e.g. '03')
    font_scale=4,
    horizontal=False,  # use vertical arrows
    # animation_time=0.4,
)
hour_setter.x = 60
hour_setter.y = 80
page2.append(hour_setter)

separator_label = Label(
    font=terminalio.FONT,
    text=":",
    x=100,
    y=100,
    scale=3,
)
page2.append(separator_label)

min_setter = FlipInput(
    display,
    value_list=["{0:02d}".format(x) for x in range(0, 60)],
    # use a list of strings from 01 through 31
    # use the {0:02d} format string to always use two digits (e.g. '03')
    font_scale=4,
    horizontal=False,  # use vertical arrows
    # animation_time=0.4,
)
min_setter.x = 120
min_setter.y = 80
page2.append(min_setter)

save_button = Button(
    x=70,
    y=180,
    width=100,
    height=40,
    style=Button.ROUNDRECT,
    label='Save',
    label_font=terminalio.FONT,
)
page2.append(save_button)
layout.add_content(page2, page_name='page 2')



main.append(layout)

display.show(main)

touch = Touch_CST816T()
prevnum = 0
while True:
    time_label.text = 'foo time'
    hour = r.datetime.tm_hour
    minute = r.datetime.tm_min
    if hour > 12:
        hour = hour - 12
    h1 = int(hour / 10)
    h2 = hour % 10
    m1 = int(minute / 10)
    m2 = minute % 10
    time_label.text = str(h1)+str(h2)+':'+str(m1)+str(m2)



    touch.update()
    p = (touch.x,touch.y,0)
    if touch.gestureId == 0 and touch.fingerNum == 1 and prevnum == 0:
        # print('touched',p,touch.gestureId, touch.fingerNum)
        if hour_setter.contains(p):
            hour_setter.selected(p)
            time.sleep(0.15)  # add a short delay to reduce accidental press
        if min_setter.contains(p):
            min_setter.selected(p)
            time.sleep(0.15)  # add a short delay to reduce accidental press
        if save_button.contains(p):
            save_button.selected = True
            time.sleep(0.15)
            save_button.selected = False
            print('setting the time to',hour_setter.value,min_setter.value)

    if touch.fingerNum == 0 and prevnum == 1:
        # print("end gesture", touch.gestureId)
        if touch.gestureId == 3:
            # print("going to the right", layout.showing_page_index, len(layout.page_content_list))
            if layout.showing_page_index < len(layout.page_content_list)-1:
                layout.showing_page_index += 1
        if touch.gestureId == 4:
            # print("going to the left", layout.showing_page_index, len(layout.page_content_list))
            if layout.showing_page_index > 0:
                layout.showing_page_index -= 1
    prevnum = touch.fingerNum
    display.refresh()


