import displayio
import time
import math
from vectorio import Circle, Rectangle
from adafruit_display_text.bitmap_label import Label
from adafruit_displayio_layout.widgets.flip_input import FlipInput
from adafruit_button import Button
import terminalio

class TimerScreen:
    def __init__(self, system) -> None:
        self.name = 'timer'
        self.view = displayio.Group()
        self.timer_running = False
        rect = Rectangle(pixel_shader=system.pal, x=0,y=0,width=240,height=240)
        rect.color_index = 2
        self.view.append(rect)

        self.button_view = displayio.Group()
        self.button_30s = Button(
            x=70,
            y=80,
            width=100,
            height=40,
            style=Button.ROUNDRECT,
            label='30 sec',
            label_font=terminalio.FONT,
        )
        self.button_view.append(self.button_30s)
        self.button_1m = Button(
            x=70,
            y=120,
            width=100,
            height=40,
            style=Button.ROUNDRECT,
            label='1 min',
            label_font=terminalio.FONT,
        )
        self.button_view.append(self.button_1m)
        self.button_5m = Button(
            x=70,
            y=160,
            width=100,
            height=40,
            style=Button.ROUNDRECT,
            label='5 min',
            label_font=terminalio.FONT,
        )
        self.button_view.append(self.button_5m)

        self.view.append(self.button_view)
        self.button_view.hidden = False

        self.time_view = displayio.Group()
        self.time_label = Label(
            font=terminalio.FONT,
            text="the time is",
            anchor_point=(0.5,0.5),
            anchored_position=(120,120),
        )
        self.time_view.append(self.time_label)
        self.view.append(self.time_view)
        self.time_view.hidden = True


    def update(self, system):
        # time_label.text = 'foo time'
        if self.timer_running:
            diff = math.floor(self.timer_end - time.monotonic())
            if diff < 0:
                self.stop_timer()
            else:
                self.time_label.text = str(diff)
        else:
            p = (system.touch.x,system.touch.y,0)
            if system.touch.gestureId == 0 and system.touch.fingerNum == 1 and system.prevnum == 0:
                print('touched',p)
                if self.button_30s.contains(p):
                    print('30s')
                    self.start_timer(30)
                if self.button_1m.contains(p):
                    print('1m')
                    self.start_timer(60)
                if self.button_5m.contains(p):
                    print('5m')
                    self.start_timer(60*5)

    def start_timer(self, sec):
        self.timer_running = True
        self.timer_start = time.monotonic()
        self.timer_end =  time.monotonic() + sec
        self.button_view.hidden = True
        self.time_view.hidden = False
    def stop_timer(self):
        self.timer_running = False
        self.button_view.hidden = False
        self.time_view.hidden = True


