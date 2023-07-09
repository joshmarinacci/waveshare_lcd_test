import displayio
import time
from vectorio import Circle, Rectangle
from adafruit_display_text.bitmap_label import Label
from adafruit_displayio_layout.widgets.flip_input import FlipInput
from adafruit_button import Button
import terminalio

class ClockScreen:
    def __init__(self, system) -> None:
        self.name = 'clock'
        self.view = displayio.Group()
        rect = Rectangle(pixel_shader=system.pal, x=0,y=0,width=240,height=240)
        rect.color_index = 2
        self.view.append(rect)

        self.time_label = Label(
            font=system.font,
            text="The time is here",
            x=120-40,
            y=100,
            scale=1,
        )
        self.time_label.anchored_position = (120,120)
        self.time_label.anchor_point = (0.5,1.0)

        self.view.append(self.time_label)


    def update(self, system):
        # time_label.text = 'foo time'
        hour = system.clock.datetime.tm_hour
        minute = system.clock.datetime.tm_min
        if hour > 12:
            hour = hour - 12
        h1 = int(hour / 10)
        h2 = hour % 10
        m1 = int(minute / 10)
        m2 = minute % 10
        self.time_label.text = str(h1)+str(h2)+':'+str(m1)+str(m2)

class SetDatetimeScreen:
    def __init__(self, system) -> None:
        self.view = displayio.Group()
        self.name = 'settime'
        bg = Rectangle(pixel_shader=system.pal,x=0,y=0,width=240,height=240)
        bg.color_index = 3
        self.view.append(bg)
        self.hour_setter = FlipInput(
            system.display,
            value_list=["{0:02d}".format(x) for x in range(1, 12)],
            # use a list of strings from 01 through 31
            # use the {0:02d} format string to always use two digits (e.g. '03')
            font=terminalio.FONT,
            horizontal=False,  # use vertical arrows
            # animation_time=0.4,
        )
        self.hour_setter.x = 50
        self.hour_setter.y = 80
        self.view.append(self.hour_setter)

        separator_label = Label(
            font=system.font,
            text=":",
            x=110,
            y=85,
        )
        self.view.append(separator_label)

        self.min_setter = FlipInput(
            system.display,
            value_list=["{0:02d}".format(x) for x in range(0, 60)],
            # use a list of strings from 01 through 31
            # use the {0:02d} format string to always use two digits (e.g. '03')
            font=terminalio.FONT,
            horizontal=False,  # use vertical arrows
            # animation_time=0.4,
        )
        self.min_setter.x = 130
        self.min_setter.y = 80
        self.view.append(self.min_setter)

        self.save_button = Button(
            x=70,
            y=180,
            width=100,
            height=40,
            style=Button.ROUNDRECT,
            label='Save',
            label_font=terminalio.FONT,
        )
        self.view.append(self.save_button)


    def update(self, system):
        p = (system.touch.x,system.touch.y,0)
        if system.touch.gestureId == 0 and system.touch.fingerNum == 1 and system.prevnum == 0:
            # print('touched',p,touch.gestureId, touch.fingerNum)
            if self.hour_setter.contains(p):
                self.hour_setter.selected(p)
                time.sleep(0.10)  # add a short delay to reduce accidental press
            if self.min_setter.contains(p):
                self.min_setter.selected(p)
                time.sleep(0.10)  # add a short delay to reduce accidental press
            if self.save_button.contains(p):
                self.save_button.selected = True
                time.sleep(0.10)
                self.save_button.selected = False
                print('setting the time to',self.hour_setter.value,self.min_setter.value)
                system.clock.datetime = time.struct_time((2023, 1, 1, self.hour_setter.value+1, self.min_setter.value, 15, 0, -1, -1))
