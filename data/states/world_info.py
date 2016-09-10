import pygame as pg

import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup


try:
    from pytmx import load_pygame
except ImportError:
    from pytmx.util_pygame import load_pygame

from .. import tools
from ..prepare import GFX, SCREEN_RECT, FONTS, MAP,SCREEN_SIZE,LIVES,MUSIC
from ..components.transition import Transition
from ..components.enemy import Enemy, Fish, Fly, Bat, Enimy, F1sh
from ..components.coin import Coin
from ..components.animation import Animation, Task
from ..components.labels import Blinker, Label


class WorldInfo(tools._State):
    def __init__(self,map,surface,world,music):
        super(WorldInfo, self).__init__()
        tmx_data = load_pygame(map)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, SCREEN_SIZE)
        self.map_layer.zoom = 0.5
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)
        self.animations = pg.sprite.Group()
        self.labels = pg.sprite.Group()
        self.letters = pg.sprite.Group()
        self.surface = surface.convert_alpha()
        self.world = world
        self.music = music

        for object in tmx_data.objects:
            if object.name == 'enemy':
                Enemy(object.x, object.y, self.group)
            elif object.name == 'fish':
                Fish(object.x, object.y, self.group)
            elif object.name == 'fly':
                Fly(object.x, object.y, self.group)
            elif object.name == 'coin':
                Coin(object.x, object.y, self.group)
            elif object.name == 'bat':
                Bat(object.x, object.y, self.group)
            elif object.name == 'enimy':
                Enimy(object.x, object.y, self.group)
            elif object.name == 'f1sh':
                F1sh(object.x, object.y, self.group)


        self.font = FONTS["UbuntuMono-B"]
        timespan = 3000
        midbottom = (SCREEN_RECT.centerx, SCREEN_RECT.bottom - 20)

        self.prompt = Blinker("Press Enter key to continue", {"midbottom": midbottom},
                              500, text_color=(255, 255, 255), font_path=self.font,
                              font_size= 25)

        task = Task(self.labels.add, timespan, args=(self.prompt,))
        self.animations.add(task)


    def startup(self, persist):
        pg.mixer.init()
        song = self.music
        pg.mixer.music.load(song)
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play()

        self.done = False
        self.persist = persist
        self.mask = self.persist['surface']
        self.transition = Transition(self.mask)
        if 'lives' in self.persist:
            self.lives = self.persist['lives']
        else:
            self.lives = LIVES
        if 'coins' in self.persist:
            self.coins = self.persist['coins']
        else:
            self.coins = 0


        font_color = (197, 143, 92)
        text = 'Bottom World' if self.world =='bottom' else 'Upper World'
        Label(text,{"topleft": (10, 10)}, self.labels, font_path=self.font, font_size=20,text_color = font_color)

        self.live_surf = pg.Surface((100,20),pg.SRCALPHA)
        image = pg.transform.scale(GFX['hud_0'],(20,20))
        self.live_surf.blit(image, (30,0))
        labels = pg.sprite.Group()
        Label(' X {}'.format(self.lives), {"topleft": (50, 0)}, labels, font_path= self.font, font_size=20,text_color = font_color)
        labels.draw(self.live_surf)

        self.coin_surf = pg.Surface((100,20),pg.SRCALPHA)
        img = pg.transform.scale(GFX['hud_coins'], (20, 20))
        self.coin_surf.blit(img,(30,0))
        lab = pg.sprite.Group()
        Label(' X {}'.format(self.coins), {"topleft": (50, 0)}, lab, font_path=self.font, font_size=20,
              text_color=font_color)
        lab.draw(self.coin_surf)


    def cleanup(self):
        pg.mixer.quit()
        self.persist['coins'] = self.coins
        self.persist['lives'] = self.lives
        self.persist['surface']= pg.display.get_surface()
        return self.persist

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.type == pg.K_ESCAPE:
                self.quit = True
            elif event.key == pg.K_RETURN:
                self.done = True
                self.next = "LEVELPLAY"

    def update(self, dt):
        self.group.update(dt)
        self.animations.update(dt)
        self.labels.update(dt)

    def draw(self, surface):
        self.group.draw(surface)
        self.group.center((SCREEN_RECT.centerx,SCREEN_RECT.bottom))
        surface.blit(self.surface, (0, 0))
        surface.blit(self.live_surf,(0,40))
        surface.blit(self.coin_surf,(0,80))
        self.letters.draw(surface)
        self.labels.draw(surface)
        self.transition.draw(surface)

bottom_info = WorldInfo(MAP['world_b'],GFX['bottom'],'bottom',MUSIC['bottom'])
bottup_info = WorldInfo(MAP['world_u'],GFX['upper0'],'upper',MUSIC['upper0'])
upper_info = WorldInfo(MAP['world_u'],GFX['upper1'],'upper',MUSIC['upper1'])