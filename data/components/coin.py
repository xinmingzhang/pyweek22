import pygame as pg
from itertools import cycle


from ..prepare import GFX
from ..tools import strip_from_sheet as strip

class Coin(pg.sprite.Sprite):
    def __init__(self,x,y,*group):
        super(Coin,self).__init__(*group)
        self.x = x
        self.y = y
        self.pos = self.x,self.y
        self.images = cycle(strip(GFX['gold'], (0, 0), (20, 20), 6))
        self.image = next(self.images)
        self.rect = self.image.get_rect(topleft = self.pos)
        self.direction = 'right'

        self.frame_time = 200
        self.frame_timer = 0

    def update(self, dt):
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.image = next(self.images)
        self.frame_timer += dt
