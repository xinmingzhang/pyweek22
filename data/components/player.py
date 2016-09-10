import pygame as pg
from itertools import cycle


from ..prepare import GFX, SCREEN_RECT,GRAVITY
from ..tools import strip_from_sheet as strip

from .player_state_machine import StateMachine, player_dict


class Player(pg.sprite.Sprite):
    def __init__(self,x,y,reverse,*groups):
        super(Player,self).__init__(*groups)
        self.x = x
        self.y = y
        self.pos = self.x,self.y
        self.speed = [0,0]
        self.images = cycle(strip(GFX['p_walk0'],(0,0),(24,31),1))
        self.image = next(self.images)
        self.rect = self.image.get_rect(bottomleft = self.pos)
        self.reverse = reverse
        self.on_ground = True

        
        self.x_acc = 0
        self.y_acc = GRAVITY if self.reverse == False else -GRAVITY*3/4

        stand_state = player_dict['standing'](self.reverse,self)
        walk_left_state = player_dict['walk_left'](self.reverse,self)
        walk_right_state = player_dict['walk_right'](self.reverse,self)
        crouch_state = player_dict['crouch'](self.reverse,self)
        crouch_left_state = player_dict['crouch_left'](self.reverse,self)
        crouch_right_state = player_dict['crouch_right'](self.reverse,self)
        jump_state = player_dict['jump'](self.reverse,self)
        jump_left_state = player_dict['jump_left'](self.reverse,self)
        jump_right_state = player_dict['jump_right'](self.reverse,self)


        self.brain = StateMachine()
        self.brain.add_state(walk_left_state)
        self.brain.add_state(walk_right_state)
        self.brain.add_state(crouch_state)
        self.brain.add_state(crouch_left_state)
        self.brain.add_state(crouch_right_state)
        self.brain.add_state(stand_state)
        self.brain.add_state(jump_state)
        self.brain.add_state(jump_left_state)
        self.brain.add_state(jump_right_state)
        self.brain.set_state('standing')

        self.frame_time = 60
        self.frame_timer = 0


    def get_event(self, event):
        self.brain.get_event(event)


    def update(self, dt):
        self.brain.check()
        if not self.check_fall_down(self.platform):
            self.on_ground = False
        if self.on_ground == False:
            self.speed[1] += self.y_acc * dt
            self.rect.y += self.speed[1] * dt - 0.5 * self.y_acc * dt * dt
        self.frame_timer += dt
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.image = next(self.images)
        self.rect.x += self.speed[0] * dt + 0.5 * self.x_acc * dt * dt
        bottomright = self.rect.bottomright
        self.rect = self.image.get_rect(bottomright = bottomright)
        self.check_platerform_collide(self.platform)


    def check_fall_down(self,platform):
        if self.reverse == False:
            self.rect.move_ip(0,1)
            if self.rect.collidelist(platform) >-1:
                collide = True
            elif self.rect.collidelist(platform) == -1:
                collide = False
            self.rect.move_ip(0,-1)
        elif self.reverse == True:
            self.rect.move_ip(0,-1)
            if self.rect.collidelist(platform) >-1:
                collide = True
            elif self.rect.collidelist(platform) == -1:
                collide = False
            self.rect.move_ip(0,1)
        return collide

    def check_platerform_collide(self, platform):
        delta_pos = 15
        index = self.rect.collidelist(platform)
        if index > -1:
            if delta_pos > self.rect.right - platform[index].left > 0:
                self.rect.right = platform[index].left
            if delta_pos > platform[index].right - self.rect.left > 0:
                self.rect.left = platform[index].right
            if delta_pos > self.rect.bottom - platform[index].top > 0:
                self.rect.bottom = platform[index].top
                if self.reverse == False:
                    self.on_ground = True
                    self.speed[1] = 0
                elif self.reverse == True:
                    self.speed[1] = 0
            if delta_pos > platform[index].bottom - self.rect.top > 0:
                self.rect.top = platform[index].bottom
                if self.reverse == False:
                    self.speed[1] = 0
                elif self.reverse == True:
                    self.on_ground = True
                    self.speed[1] = 0


    def draw(self, surface):
        surface.blit(self.image, self.rect)







