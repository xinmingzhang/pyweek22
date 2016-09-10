import pygame as pg

import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup


try:
    from pytmx import load_pygame
except ImportError:
    from pytmx.util_pygame import load_pygame

from .. import tools
from ..prepare import GFX, SCREEN_RECT, FONTS, MAP,SCREEN_SIZE,CHEAT_LIVES,SFX,MUSIC
from ..components.transition import Transition
from ..components.animation import Task
from ..components.labels import Blinker,Label





class Intro(tools._State):
    def __init__(self):
        super(Intro, self).__init__()

        tmx_data = load_pygame(MAP['intro'])

        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, SCREEN_SIZE)
        self.map_layer.zoom = 0.5

        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        self.animations = pg.sprite.Group()
        self.labels = pg.sprite.Group()
        self.letters = pg.sprite.Group()
        self.surface = GFX['intro'].convert_alpha()
        self.cheat = False


        timespan = 3000
        midbottom = (SCREEN_RECT.centerx, SCREEN_RECT.bottom - 20)
        font = FONTS["UbuntuMono-B"]
        self.prompt = Blinker("Press Enter key to continue", {"midbottom": midbottom},
                              500, text_color=(255, 255, 255), font_path=font,
                              font_size= 25)
        Label('UP-UP-DOWN-DOWN-LEFT-RIGHT-LEFT-RIGHT-B-A',{"topleft": (50, 0)},self.labels,font_path=font,font_size = 7)
        task = Task(self.labels.add, timespan, args=(self.prompt,))
        self.animations.add(task)


    def startup(self, persist):
        pg.mixer.init()
        song = MUSIC['intro']
        pg.mixer.music.load(song)
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play()

        self.persist = persist
        self.mask = self.persist['surface']
        self.transition = Transition(self.mask)
        self.code = ''



    def cleanup(self):

        pg.mixer.quit()
        self.persist['surface']= pg.display.get_surface()
        return self.persist

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            elif event.key == pg.K_RETURN:


                self.done = True
                self.next = 'BOTTOM'
            elif event.key == pg.K_UP:
                self.code += 'u'
            elif event.key == pg.K_DOWN:
                self.code += 'd'
            elif event.key == pg.K_LEFT:
                self.code += 'l'
            elif event.key == pg.K_RIGHT:
                self.code += 'r'
            elif event.key == pg.K_a:
                self.code += 'a'
            elif event.key == pg.K_b:
                self.code += 'b'
            else:
                pass


    def update(self, dt):
        if self.code.endswith('uuddlrlrba'):
            self.cheat = True
            self.persist['lives'] = CHEAT_LIVES
            self.code += 'a'
        if self.cheat == True:
            sound = SFX['cheat']
            sound.play()
            self.cheat = False
        self.animations.update(dt)
        self.labels.update(dt)

    def draw(self, surface):

        self.group.draw(surface)
        self.group.center((SCREEN_RECT.centerx,SCREEN_RECT.bottom))
        surface.blit(self.surface, (0, 0))
        self.transition.draw(surface)
        self.letters.draw(surface)
        self.labels.draw(surface)

