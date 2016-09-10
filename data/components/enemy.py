import pygame as pg
from itertools import cycle


from ..prepare import GFX, SPEED_Y,SPEED_X,GRAVITY
from ..tools import strip_from_sheet as strip

class Enemy(pg.sprite.Sprite):
    def __init__(self,x,y,*group):
        super(Enemy,self).__init__(*group)
        self.x = x
        self.y = y
        self.pos = self.x,self.y
        self.images = cycle(strip(GFX['e_walk1'], (0, 0), (24, 31), 11))
        self.image = next(self.images)
        self.rect = self.image.get_rect(bottomleft = self.pos)
        self.direction = 'right'

        self.frame_time = 60
        self.frame_timer = 0

    def update(self, dt):
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.image = next(self.images)
        if self.direction == 'right':
            self.rect.x += 1
            if self.rect.x - self.x >=180:
                self.images = cycle(strip(GFX['e_walk0'], (0, 0), (24, 31), 11))
                self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= 1
            if self.rect.x < self.x:
                self.images = cycle(strip(GFX['e_walk1'], (0, 0), (24, 31), 11))
                self.direction = 'right'
        self.frame_timer += dt

class Fish(pg.sprite.Sprite):
    def __init__(self, x, y, *group):
        super(Fish,self).__init__(*group)
        self.x = x
        self.y = y
        self.pos = self.x, self.y
        self.speed = SPEED_Y/3
        self.image = GFX['piranha']
        self.rect = self.image.get_rect(topleft=self.pos)
        self.direction = 'up'

    def update(self, dt):
        if self.direction == 'up':
            self.rect.y -= self.speed * dt - 0.5 * GRAVITY * dt * dt
            if self.y - self.rect.y >= 270:
                self.direction = 'down'
                self.image = GFX['piranha_down']
        if self.direction == 'down':
            self.rect.y += self.speed * dt - 0.5 * GRAVITY * dt * dt
            if self.rect.y > self.y:
                self.direction = 'up'
                self.image = GFX['piranha']

class Fly(pg.sprite.Sprite):
    def __init__(self,x,y,*group):
        super(Fly,self).__init__(*group)
        self.x = x
        self.y = y
        self.pos = self.x,self.y
        self.speed = SPEED_X/2
        self.images = cycle(strip(GFX['flyFly2'], (0, 0), (36, 18), 2))
        self.image = next(self.images)
        self.rect = self.image.get_rect(topleft = self.pos)
        self.direction = 'right'

        self.frame_time = 160
        self.frame_timer = 0

    def update(self, dt):
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.image = next(self.images)
        if self.direction == 'right':
            self.rect.x += self.speed * dt
            if self.rect.x - self.x >=280:
                self.images = cycle(strip(GFX['flyFly1'], (0, 0), (36, 18), 2))
                self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed * dt
            if self.rect.x < self.x:
                self.images = cycle(strip(GFX['flyFly2'], (0, 0), (36, 18), 2))
                self.direction = 'right'
        self.frame_timer += dt

class Bat(pg.sprite.Sprite):
    def __init__(self,x,y,*group):
        super(Bat,self).__init__(*group)
        self.x = x
        self.y = y
        self.pos = self.x,self.y
        self.speed = SPEED_X/2
        self.org_images = GFX['bat']
        self.r_images = pg.transform.flip(self.org_images, True, True)
        self.l_images = pg.transform.flip(self.org_images, False, True)
        self.images = cycle(strip(self.r_images, (0, 0), (37, 20), 2))

        self.image = next(self.images)
        self.rect = self.image.get_rect(topleft = self.pos)
        self.direction = 'right'

        self.frame_time = 160
        self.frame_timer = 0

    def update(self, dt):
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.image = next(self.images)
        if self.direction == 'right':
            self.rect.x += self.speed * dt
            if self.rect.x - self.x >=380:
                self.images = cycle(strip(self.l_images, (0, 0), (37, 20), 2))
                self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed * dt
            if self.rect.x < self.x:
                self.images = cycle(strip(self.r_images, (0, 0), (37, 20), 2))
                self.direction = 'right'
        self.frame_timer += dt

class Enimy(pg.sprite.Sprite):
    def __init__(self,x,y,*group):
        super(Enimy,self).__init__(*group)
        self.x = x
        self.y = y
        self.pos = self.x,self.y
        self.org_img = GFX['e0_walk0']
        self.org_img_r = pg.transform.flip(self.org_img,True,False)
        self.images = cycle(strip(self.org_img_r, (0, 0), (24, 31), 11))
        self.image = next(self.images)
        self.rect = self.image.get_rect(topleft = self.pos)
        self.direction = 'right'

        self.frame_time = 60
        self.frame_timer = 0

    def update(self, dt):
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.image = next(self.images)
        if self.direction == 'right':
            self.rect.x += 1
            if self.rect.x - self.x >=200:
                self.images = cycle(strip(self.org_img, (0, 0), (24, 31), 11))
                self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= 1
            if self.rect.x < self.x:
                self.images = cycle(strip(self.org_img_r, (0, 0), (24, 31), 11))
                self.direction = 'right'
        self.frame_timer += dt

class F1sh(pg.sprite.Sprite):
    def __init__(self, x, y, *group):
        super(F1sh,self).__init__(*group)
        self.x = x
        self.y = y
        self.pos = self.x, self.y
        self.speed = SPEED_Y/3
        self.image = GFX['piranha0']
        self.rect = self.image.get_rect(topleft=self.pos)
        self.direction = 'up'

    def update(self, dt):
        if self.direction == 'up':
            self.rect.y -= self.speed * dt - 0.5 * GRAVITY * dt * dt
            if self.y - self.rect.y >= 320:
                self.direction = 'down'
                self.image = pg.transform.flip(GFX['piranha0'],False,True)
        if self.direction == 'down':
            self.rect.y += self.speed * dt - 0.5 * GRAVITY * dt * dt
            if self.rect.y > self.y:
                self.direction = 'up'
                self.image = GFX['piranha0']