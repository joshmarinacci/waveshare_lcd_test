import displayio
import terminalio
from random import randint
from vectorio import Circle, Rectangle
import math
from adafruit_datetime import datetime
from adafruit_display_text.bitmap_label import Label



def reset_star(star):
    star[0] = 120
    star[1] = 120
    star[2] = randint(-2,2)
    star[3] = randint(-2,2)
    if star[2] == 0 and star[3] == 0:
        return reset_star(star)
    return star

def check_star(star):
    if(star[0] <= 0):
        return reset_star(star)
    if(star[0] >= 239):
        return reset_star(star)
    if star[1]  <= 0:
        return reset_star(star)
    if star[1] >= 239:
        return reset_star(star)
    return star

def position(now=None): 
    if now is None: 
        now = datetime.now()

    diff = now - datetime(2001, 1, 1)
    days = diff.days + diff.seconds / 86400
    lunations = 0.20439731 + (days * 0.03386319269)
    return lunations % 1

def phase(pos): 
   index = (pos * 8) + 0.5
   index = math.floor(index)
   return {
      0: "New Moon", 
      1: "Waxing Crescent", 
      2: "First Quarter", 
      3: "Waxing Gibbous", 
      4: "Full Moon", 
      5: "Waning Gibbous", 
      6: "Last Quarter", 
      7: "Waning Crescent"
   }[int(index) & 7]

    
class StarfieldScreen:
    def __init__(self, system) -> None:
        self.name = 'starfield'
        pos = position()
        phasename = phase(pos)
        roundedpos = round(float(pos), 3)
        print('moon', phasename, roundedpos)
        self.stars = []
        self.view = displayio.Group()
        self.pal = displayio.Palette(2)
        self.pal[0] = 0x000000
        self.pal[1] = 0xffffff
        self.bitmap = displayio.Bitmap(240,240,len(self.pal))
        self.tilegrid = displayio.TileGrid(self.bitmap, pixel_shader=self.pal)
        self.view.append(self.tilegrid)
        self.label = Label(
            font=terminalio.FONT,
            text=":",
            anchor_point=(0.5,0.5),
            anchored_position=(120,120),
        )
        self.label.text = phasename
        self.view.append(self.label)

    def update(self, system):
        if len(self.stars) < 50:
            star = reset_star([0,0,0,0])
            self.stars.append(star)
        for s in self.stars:
            self.bitmap[s[0],s[1]] = 0
            s[0] += int(s[2])
            s[1] += int(s[3])
            s[2] *= 1.1
            s[3] *= 1.1
            check_star(s)
            self.bitmap[s[0],s[1]] = 1
            system.display.refresh()