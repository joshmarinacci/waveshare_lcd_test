import displayio
import time
from vectorio import Circle, Rectangle
from adafruit_display_text.bitmap_label import Label
import terminalio

class BatteryScreen:
    def __init__(self, system) -> None:
        self.name = 'battery'
        self.view = displayio.Group()
        bg = Rectangle(pixel_shader=system.pal,width=240,height=240)
        bg.color_index = 2
        self.view.append(bg)
        self.label = Label(
            font=terminalio.FONT,
            text='battery',
            scale=2,
            x=20,
            y=80,
        )
        self.view.append(self.label)

    def update(self, system):
        avg = sum(system.battery._samples)/len(system.battery._samples)
        self.label.text = "avg value " + str(int(avg)) + "\nvoltage: " + str(system.battery.voltage) + "\npercentage: " + str(system.battery.percent)
