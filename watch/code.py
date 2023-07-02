import asyncio
import time
import rtc
from adafruit_bitmap_font import bitmap_font
import joshutils
import terminalio
import displayio
from waveshare128 import setup_display, Touch_CST816T, Battery
import adafruit_logging as logging
from vectorio import Circle, Rectangle
from adafruit_display_text.bitmap_label import Label
from adafruit_displayio_layout.layouts.page_layout import PageLayout
from clock import ClockScreen, SetDatetimeScreen
from battery import BatteryScreen
from adafruit_bitmapsaver import save_pixels
import traceback

clock = rtc.RTC()

BLACK = 0
WHITE = 1
RED = 2
BLUE = 3

class WatchSystem:
    def __init__(self) -> None:
        self.pal = displayio.Palette(4)
        self.pal[0] = 0x000000
        self.pal[1] = 0xFFFFFF
        self.pal[2] = 0xFF0000
        self.pal[3] = 0x0000FF
        self.font = bitmap_font.load_font("chivo10.bdf")
        self.logger = logging.getLogger('default')
        self.logger.addHandler(joshutils.JoshLogger('/log.txt','a'))
        self.logger.setLevel(logging.DEBUG)
        self.layout = PageLayout(x=0, y=0)
        self.main = displayio.Group()
        self.main.append(self.layout)
        self.display = setup_display()
        self.display.show(self.main)
        self.touch = Touch_CST816T()
        self.battery = Battery()
        self.clock = clock
        self.prevnum = 0
        self.last_input = time.monotonic()

    def handle_swipe(self):
        if self.touch.fingerNum == 0 and self.prevnum == 1:
            self.last_input = time.monotonic()
            if self.touch.gestureId == 3:
                # swipe left
                self.logger.info("swipe left")
                if self.layout.showing_page_index < len(self.layout.page_content_list)-1:
                    self.layout.showing_page_index += 1
            if self.touch.gestureId == 4:
                self.logger.info("swipe right")
                if self.layout.showing_page_index > 0:
                    self.layout.showing_page_index -= 1

    def take_screenshot(self):
        self.logger.info("taking screenshot")
        try:
            save_pixels('/screenshot.bmp',pixel_source=self.display)
            self.logger.info("saved the screenshot")
        except BaseException as e:
            self.logger.error("couldnt take screenshot")
            self.logger.error(''.join(traceback.format_exception(e)))
        self.display.brightness = 0.1
        time.sleep(0.2)
        self.display.brightness = 1.0




def setup_start_screen():
    global start_screen
    global start_screen_label
    start_screen = displayio.Group()
    start_screen_bg = Rectangle(pixel_shader=pal, x=0,y=0,width=240,height=240)
    start_screen_bg.color_index = BLUE
    start_screen.append(start_screen_bg)
    start_screen_label = Label(
        font=terminalio.FONT,
        text='starting...',
        x=120-40,
        y=100,
    )
    start_screen.append(start_screen_label)
    main.append(start_screen)


async def main():
    # load  fonts
    global font
    global logger
    
    system = WatchSystem()
    clockScreen = ClockScreen(system)
    datetime = SetDatetimeScreen(system)
    battery = BatteryScreen(system)

    system.display.brightness = 1.0
    system.touch.gestureId = 0
    print("setup done")

    while True:
        system.touch.update()
        system.handle_swipe()
        if system.layout.showing_page_name == 'clock':
            clockScreen.update(system)
        if system.layout.showing_page_name == 'settime':
            datetime.update(system)
        if system.layout.showing_page_name == 'battery':
            battery.update(system)

        system.battery._update()
        system.prevnum = system.touch.fingerNum
        system.display.refresh()
asyncio.run(main())
