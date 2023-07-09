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
from starfield import StarfieldScreen
from timer import TimerScreen

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
        self.main = displayio.Group()
        self.display = setup_display()
        self.display.show(self.main)
        self.touch = Touch_CST816T()
        self.battery = Battery()
        self.clock = clock
        self.prevnum = 0
        self.last_input = time.monotonic()
        self.screens = []
        self.currentScreen = None

    def add_screen(self, screen):
        self.screens.append(screen)
        # self.layout.add_content(screen.view, screen.name)

    def set_current_screen(self, screen):
        if self.currentScreen != None:
            self.main.remove(self.currentScreen.view)
        self.currentScreen = screen
        self.main.append(self.currentScreen.view)

    def update_screen(self):
        if self.currentScreen != None:
            self.currentScreen.update(self)

    def handle_swipe(self):
        if self.touch.fingerNum == 0 and self.prevnum == 1:
            self.last_input = time.monotonic()
            n = self.screens.index(self.currentScreen)
            if self.touch.gestureId == 3:
                if n < len(self.screens) - 1:
                    self.set_current_screen(self.screens[n+1])
            if self.touch.gestureId == 4:
                if n > 0:
                    self.set_current_screen(self.screens[n-1])

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
    system.add_screen(ClockScreen(system))
    system.add_screen(TimerScreen(system))
    system.add_screen(StarfieldScreen(system))
    system.add_screen(BatteryScreen(system))
    system.add_screen(SetDatetimeScreen(system))

    system.set_current_screen(system.screens[0])
    system.display.brightness = 1.0
    system.touch.gestureId = 0

    while True:
        system.battery._update()
        system.touch.update()
        system.handle_swipe()
        system.update_screen()
        # handle long press
        # handle double tap
        system.prevnum = system.touch.fingerNum
        system.display.refresh()

asyncio.run(main())
