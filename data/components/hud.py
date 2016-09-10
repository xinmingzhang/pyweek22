import pygame as pg




from ..prepare import MAP, SCREEN_SIZE, SCREEN_RECT,FONTS,GFX
from ..components.animation import Animation, Task
from ..components.labels import Label,Blinker

class Hud(object):
    def __init__(self):
        pass

    def update(self,game,dt):
        self.coin = game.coin_num
        self.time = game.timer - game.time
        self.lives = game.player_lives
        self.labels = pg.sprite.Group()
        w, h = SCREEN_SIZE[0], 60
        self.img= pg.Surface((w, h), pg.SRCALPHA)
        self.img.blit(GFX['hud_coins'], (50, 10))
        self.img.blit(GFX['hud_0'], (490, 10))
        self.font = FONTS["UbuntuMono-B"]
        self.minute = int(self.time // 60000)
        self.second_10 = int(self.time % 60000 // 1000 // 10)
        self.second = int(self.time % 60000 // 1000 % 10)
        text_color0 = (255, 0, 0) if self.coin < 30 else(255, 255, 255)
        text_color1 = (255, 0, 0) if (self.second_10 == 0 and self.minute == 0)else (255, 255, 255)
        text_color2 = (255, 0, 0) if self.lives == 1 else (255, 255, 255)
        Label('X {}'.format(self.coin), {"topleft": (100, 10)}, self.labels, font_path=self.font, font_size=40,text_color=text_color0)
        Label('{}:{}{}'.format(self.minute, self.second_10, self.second), {"topleft": (290, 10)}, self.labels, font_path=self.font, font_size=40,
              text_color=text_color1)
        Label('X {}'.format(self.lives), {"topleft": (540, 10)}, self.labels, font_path=self.font, font_size=40,text_color=text_color2)
        self.labels.draw(self.img)


    def draw(self,surface):
        surface.blit(self.img,(0,0))


