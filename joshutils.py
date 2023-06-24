import board
import time
import sys
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
import supervisor

class ScreenLogger(logging.Handler):
    def __init__(self, display:displayio.Display, group:displayio.Group) -> None:
        print("making josh print handler")
        super().__init__()
        fontx, fonty = terminalio.FONT.get_bounding_box()
        term_palette = displayio.Palette(2)
        term_palette[0] = 0x000000
        term_palette[1] = 0xffffff
        self.logbox = displayio.TileGrid(terminalio.FONT.bitmap,
                                    x=0,
                                    y=0,
                                    width=display.width // fontx,
                                    height=display.height // fonty,
                                    tile_width=fontx,
                                    tile_height=fonty,
                                    pixel_shader=term_palette)
        group.append(self.logbox)
        self.logterm = terminalio.Terminal(self.logbox, terminalio.FONT)
    def emit(self, record: logging.LogRecord) -> None:
        txt = f"\r\n{record.levelname} - {record.msg}"
        self.logterm.write(txt)
        # self.logterm.write(b'\n')


class JoshLogger(logging.Handler):
    terminator = "\n"
    def __init__(self, filename: str, mode: str = "a") -> None:
        super().__init__()
        if supervisor.runtime.usb_connected:
            print("JoshLogger -> STDERR")
            self.enabled = False
            self.stream = sys.stderr

        else:
            storage.remount("/", False)
            self.enabled = True
            self.stream = open(filename, mode=mode)

    def close(self) -> None:
        """Closes the file"""
        if self.enabled:
            self.stream.flush()
            self.stream.close()

    def emit(self, record: logging.LogRecord) -> None:
        self.stream.write(self.format(record) + self.terminator)
        if self.enabled:
            self.stream.flush()

