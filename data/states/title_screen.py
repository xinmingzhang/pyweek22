import pygame as pg

import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

try:
    from pytmx import load_pygame
except ImportError:
    from pytmx.util_pygame import load_pygame





from .. import tools
from ..prepare import GFX, SCREEN_RECT, FONTS, MAP,SCREEN_SIZE,MUSIC
from ..components.animation import Animation, Task
from ..components.labels import Blinker



class Icon(pg.sprite.Sprite):
    def __init__(self, image, topleft, reverse, *groups):
        super(Icon, self).__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=topleft)
        if reverse:
            self.image = pg.transform.flip(self.image,True,True)


class TitleScreen(tools._State):
    def __init__(self):
        super(TitleScreen, self).__init__()

        pg.mixer.init()

        song = MUSIC['bg']
        pg.mixer.music.load(song)
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play()

        tmx_data = load_pygame(MAP['title0'])

        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, SCREEN_SIZE)
        self.map_layer.zoom = 1
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        self.animations = pg.sprite.Group()
        self.labels = pg.sprite.Group()
        self.letters = pg.sprite.Group()

        imgs0 = [GFX["letter_{}".format(letter)] for letter in "UPSIDE"]
        delays0 = [x * 250 for x in (1, 2, 3, 4, 5, 6)]
        w, h = imgs0[0].get_size()
        space = 10
        left0 = 70
        top0 = SCREEN_RECT.centery - 90
        timespan = 1500
        for img, delay in zip(imgs0, delays0):
            icon = Icon(img, (left0, -100), False,self.letters)
            left0 += w + space
            ani = Animation(top=top0, duration=timespan, delay=delay, transition="out_bounce", round_values=True)
            ani.start(icon.rect)
            self.animations.add(ani)

        imgs1 = [GFX["letter_{}".format(letter)] for letter in "DOWN"]
        delays1 = [x * 250 for x in (3, 4, 5, 6)]

        space = 10
        left1 = 280
        top1 = SCREEN_RECT.centery

        for img, delay in zip(imgs1, delays1):
            icon = Icon(img, (left1, 580), True,self.letters)
            left1 += w + space
            ani = Animation(top=top1, duration=timespan, delay=delay, transition="out_bounce", round_values=True)
            ani.start(icon.rect)
            self.animations.add(ani)
        midbottom = (SCREEN_RECT.centerx, SCREEN_RECT.bottom - 120)
        font = FONTS["UbuntuMono-B"]
        self.prompt = Blinker("Press any key to continue", {"midbottom": midbottom},
                              500, text_color=(255, 255, 255), font_path=font,
                              font_size=30)
        task = Task(self.labels.add, max(delays1) + timespan, args=(self.prompt,))
        self.animations.add(task)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.type == pg.K_ESCAPE:
                self.quit = True
            else:
                self.done = True
                self.next = "INTRO"

    def cleanup(self):
        pg.mixer.quit()
        self.persist['surface']= pg.display.get_surface()
        return self.persist

    def update(self, dt):

        self.animations.update(dt)
        self.labels.update(dt)

    def draw(self, surface):
        self.group.draw(surface)
        self.letters.draw(surface)
        self.labels.draw(surface)

