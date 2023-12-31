import board
import time
import displayio
import digitalio
import traceback
from adafruit_displayio_layout.layouts.page_layout import PageLayout
from adafruit_display_text.bitmap_label import Label
from adafruit_displayio_layout.widgets.flip_input import FlipInput
from vectorio import Circle, Rectangle
from waveshare128 import setup_display, Touch_CST816T, Battery
from adafruit_button import Button
from adafruit_bitmap_font import bitmap_font
from adafruit_bitmapsaver import save_pixels
import analogio
import rtc
import storage
import terminalio
import adafruit_logging as logging
import joshutils
import supervisor

# setup the RTC and time
r = rtc.RTC()
# r.datetime = time.struct_time((2023, 6, 12,   22, 10, -1,   0, -1, -1))

display = setup_display()

SCREEN_OFF_DELAY = 15

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

print("initial displays")
layout = PageLayout(x=0, y=0)
# load our custom font. 10px version of chivo
font = bitmap_font.load_font("chivo10.bdf")
main.append(layout)
display.show(main)

print("battery setup")
battery = Battery()
print("touch setup")
touch = Touch_CST816T()
prevnum = 0

print("logger setup")
logger = logging.getLogger('default')

logger.addHandler(joshutils.JoshLogger('/log.txt','a'))

logger.setLevel(logging.DEBUG)


time_label = None
battery_label = None
hour_setter = None
min_setter = None
save_button = None
start_screen_label = None
start_screen = None


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

def set_start_phase(text):
    start_screen_label.text = text
    display.refresh()

def remove_start_screen():
    main.remove(start_screen)    

setup_start_screen()
set_start_phase('start')

def setup_clock_screen():
    global time_label
    # setup page 1
    view_time_page = displayio.Group()
    rect = Rectangle(pixel_shader=pal, x=0,y=0,width=240,height=240)
    rect.color_index = RED
    view_time_page.append(rect)

    time_label = Label(
        font=font,
        text="The time is here",
        x=120-40,
        y=100,
        scale=1,
    )
    time_label.anchored_position = (120,120)
    time_label.anchor_point = (0.5,1.0)

    view_time_page.append(time_label)
    layout.add_content(view_time_page, page_name='clock')

def update_clock_screen():
    # time_label.text = 'foo time'
    hour = r.datetime.tm_hour
    minute = r.datetime.tm_min

    if hour > 12:
        hour = hour - 12
    h1 = int(hour / 10)
    h2 = hour % 10
    m1 = int(minute / 10)
    m2 = minute % 10
    time_label.text = str(h1)+str(h2)+':'+str(m1)+str(m2)
    # print(r.datetime.tm_sec)
    # secondsText.text = str(h1)+str(h2)+':'+str(m1)+str(m2) + ":" + str(r.datetime.tm_sec)

set_start_phase('clock')
setup_clock_screen()


def setup_settime_screen():
    global hour_setter
    global min_setter
    page2 = displayio.Group()
    page2bg = Rectangle(pixel_shader=pal,x=0,y=0,width=240,height=240)
    page2bg.color_index = BLUE
    page2.append(page2bg)
    hour_setter = FlipInput(
        display,
        value_list=["{0:02d}".format(x) for x in range(1, 12)],
        # use a list of strings from 01 through 31
        # use the {0:02d} format string to always use two digits (e.g. '03')
        font=font,
        horizontal=False,  # use vertical arrows
        # animation_time=0.4,
    )
    hour_setter.x = 50
    hour_setter.y = 80
    page2.append(hour_setter)

    separator_label = Label(
        font=font,
        text=":",
        x=110,
        y=85,
    )
    page2.append(separator_label)

    min_setter = FlipInput(
        display,
        value_list=["{0:02d}".format(x) for x in range(0, 60)],
        # use a list of strings from 01 through 31
        # use the {0:02d} format string to always use two digits (e.g. '03')
        font=font,
        horizontal=False,  # use vertical arrows
        # animation_time=0.4,
    )
    min_setter.x = 130
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
    layout.add_content(page2, page_name='settime')

def update_settime_screen():
    p = (touch.x,touch.y,0)
    # print("set time page")
    if touch.gestureId == 0 and touch.fingerNum == 1 and prevnum == 0:
        # print('touched',p,touch.gestureId, touch.fingerNum)
        if hour_setter.contains(p):
            hour_setter.selected(p)
            time.sleep(0.10)  # add a short delay to reduce accidental press
        if min_setter.contains(p):
            min_setter.selected(p)
            time.sleep(0.10)  # add a short delay to reduce accidental press
        if save_button.contains(p):
            save_button.selected = True
            time.sleep(0.10)
            save_button.selected = False
            print('setting the time to',hour_setter.value,min_setter.value)
            r.datetime = time.struct_time((2023, 1, 1, hour_setter.value+1, min_setter.value, 15, 0, -1, -1))
set_start_phase('settime screen')
setup_settime_screen()

def setup_battery_screen():
    global battery_label
    battery_page = displayio.Group()
    battery_page_bg = Rectangle(pixel_shader=pal,width=240,height=240)
    battery_page_bg.color_index = RED
    battery_page.append(battery_page_bg)
    battery_label = Label(
        font=terminalio.FONT,
        text='battery',
        scale=2,
        x=20,
        y=80,
    )
    battery_page.append(battery_label)
    layout.add_content(battery_page, page_name='battery')

def update_battery_screen():
    avg = sum(battery._samples)/len(battery._samples)
    battery_label.text = "avg value " + str(int(avg)) + "\nvoltage: " + str(battery.voltage) + "\npercentage: " + str(battery.percent)

set_start_phase('battery screen')
setup_battery_screen()


def setup_logger_screen():
    logger_page = displayio.Group()
    sl = joshutils.ScreenLogger(display,logger_page)
    logger.addHandler(sl)
    layout.add_content(logger_page, page_name='logger')

set_start_phase('logger screen')
setup_logger_screen()

def take_screenshot():
    logger.info("taking screenshot")
    try:
        save_pixels('/screenshot.bmp',pixel_source=display)
        logger.info("saved the screenshot")
    except BaseException as e:
        logger.error("couldnt take screenshot")
        logger.error(''.join(traceback.format_exception(e)))
    display.brightness = 0.1
    time.sleep(0.2)
    display.brightness = 1.0

long_happened = False
double_happened = False

count = 0
sleeping = False
display.brightness = 1.0
last_input = time.monotonic()
touch.gestureId = 0
print("setup done")
set_start_phase('done')
remove_start_screen()
while True:
    count += 1
    if (count % 50) == 0:
        logger.info('battery value: %d %f %d %s', battery._pin.value, battery.voltage, battery.percent, battery.charging)
    touch.update()
    battery._update()
    if time.monotonic() - last_input > SCREEN_OFF_DELAY:
        display.brightness = 0
    if layout.showing_page_name == 'clock':
        update_clock_screen()
    if layout.showing_page_index == 'settime':
        update_settime_screen()
    if layout.showing_page_name == 'battery':
        update_battery_screen()
    if touch.gestureId == 0x0c and touch.fingerNum == 1 and not(long_happened):
        logger.info("long touch happened")
        if display.brightness > 0:
            take_screenshot()
        long_happened = True
        display.brightness = 1.0
        last_input = time.monotonic()
    if touch.gestureId == 0x0b and not(double_happened):
        logger.info("double tap happened")
        double_happened = True
        display.brightness = 1.0
        last_input = time.monotonic()
    if touch.fingerNum == 0:
        long_happened = False
    if touch.fingerNum == 0 and prevnum == 1:
        double_happened = False
        last_input = time.monotonic()
        if touch.gestureId == 3:
            if layout.showing_page_index < len(layout.page_content_list)-1:
                layout.showing_page_index += 1
        if touch.gestureId == 4:
            if layout.showing_page_index > 0:
                layout.showing_page_index -= 1
    prevnum = touch.fingerNum
    display.refresh()

