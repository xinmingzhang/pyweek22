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
from ..components.transition import Transition




class EndScreen(tools._State):
    def __init__(self,surface,img,choice,music):
        super(EndScreen, self).__init__()

        '''tmx_data = load_pygame(MAP['title0'])

        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, SCREEN_SIZE)
        self.map_layer.zoom = 1
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)'''


        self.animations = pg.sprite.Group()
        self.labels = pg.sprite.Group()
        self.letters = pg.sprite.Group()
        self.surface = surface
        self.img = img
        self.choice = choice
        self.music = music

    def startup(self,persist):
        pg.mixer.init()
        song =self.music
        pg.mixer.music.load(song)
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play()

        self.persist = persist
        self.mask = self.persist['surface']
        self.transition = Transition(self.mask)

        img_sprite = pg.sprite.Sprite(self.labels)
        img_sprite.image = self.img
        if self.choice == 1:
            img_sprite.rect = self.img.get_rect(center =(SCREEN_SIZE[0]/2, - SCREEN_SIZE[1]/4))
            ani = Animation(x = SCREEN_SIZE[0]/2 , y = SCREEN_SIZE[1]/4, duration=1000, delay = 2000, transition="out_bounce")
        elif self.choice == 0:
            h = img_sprite.image.get_height()
            w = img_sprite.image.get_width()
            img_sprite.rect = self.img.get_rect(center =(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]+ h))
            ani = Animation(x = SCREEN_SIZE[0]/2 - w / 2, y = SCREEN_SIZE[1]/2- h, duration=1000, delay = 2000, transition="out_bounce")

        ani.start(img_sprite.rect)
        self.animations.add(ani)




        midbottom = (SCREEN_RECT.centerx, SCREEN_RECT.bottom - 20)
        font = FONTS["UbuntuMono-B"]
        self.prompt = Blinker("Press Enter key to exit", {"midbottom": midbottom},
                              500, text_color=(255, 255, 255), font_path=font,
                              font_size = 20)
        task = Task(self.labels.add, 1000, args=(self.prompt,))
        self.animations.add(task)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_RETURN:
                self.quit = True





    def update(self, dt):

        self.animations.update(dt)
        self.labels.update(dt)

    def draw(self, surface):
        #self.group.draw(surface)
        surface.blit(self.surface,(0,0))

        self.labels.draw(surface)
        self.transition.draw(surface)

win = EndScreen(GFX['game_over0'],GFX['choice0'],0,MUSIC['game_over0'])
lose = EndScreen(GFX['game_over1'],GFX['choice1'],1,MUSIC['game_over1'])
