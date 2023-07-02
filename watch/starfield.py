import displayio
from random import randint
from vectorio import Circle, Rectangle

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

    
class StarfieldScreen:
    def __init__(self, system) -> None:

        self.stars = []
        self.page = displayio.Group()
        self.pal = displayio.Palette(2)
        self.pal[0] = 0x000000
        self.pal[1] = 0xffffff
        self.bitmap = displayio.Bitmap(240,240,len(self.pal))
        self.tilegrid = displayio.TileGrid(self.bitmap, pixel_shader=self.pal)
        self.page.append(self.tilegrid)
        system.layout.add_content(self.page, page_name='starfield')

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