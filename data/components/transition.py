import pygame as pg
from ..prepare import GFX, SCREEN_RECT, FONTS, MAP,SCREEN_SIZE

COLOR_KEY = (0, 255, 0)
HEIGHT = 40
SPEED = 40



class Rain(pg.sprite.Sprite):
    def __init__(self, x, y, direction,*group):
        super(Rain,self).__init__(*group)
        self.direction = direction
        self.rect = pg.Rect((x, y), (SCREEN_SIZE[0],HEIGHT))
        self.image = pg.Surface(self.rect.size)
        self.image.fill(COLOR_KEY)
        self.d = direction


    def update(self, surface):
        surface.blit(self.image, self.rect)
        self.rect.x += self.d * SPEED
        if self.direction > 0:
            if self.rect.x >0 and self.d == 1:
                self.rect.x = SCREEN_SIZE[0]
                self.rect.y += HEIGHT
                self.d= -1
            elif self.rect.x <0 and self.d ==-1:
                self.rect.x = -SCREEN_SIZE[0]
                self.rect.y += HEIGHT
                self.d = 1
            elif self.rect.y >=SCREEN_SIZE[1]:
                self.kill()
        elif self.direction < 0:
            if self.rect.x < 0 and self.d == -1:
                self.rect.x = -SCREEN_SIZE[0]
                self.rect.y -= HEIGHT
                self.d = 1
            elif self.rect.x >0 and self.d ==1:
                self.rect.x = SCREEN_SIZE[0]
                self.rect.y -= HEIGHT
                self.d = -1
            elif self.rect.y <= 0:
                self.kill()


class Transition:
    def __init__(self,surface):
        self.surface = pg.Surface(SCREEN_SIZE).convert()
        self.surface.set_colorkey(COLOR_KEY)
        img = pg.transform.rotozoom(surface,180,0.5)
        self.surface.blit(img,(SCREEN_SIZE[0]/4,SCREEN_SIZE[1]/4))
        self.rain = pg.sprite.Group()
        Rain(-SCREEN_SIZE[0], 0, 1, self.rain)
        Rain(SCREEN_SIZE[0], SCREEN_SIZE[1]-HEIGHT, -1, self.rain)
        self.group = self.rain.copy()

    def draw(self,surface):
        surface.blit(self.surface,(0,0))
        self.rain.update(self.surface)
        surface.blit(self.surface,(0,0))


