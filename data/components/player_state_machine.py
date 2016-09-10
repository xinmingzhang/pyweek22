import pygame as pg
from itertools import cycle

from ..prepare import GFX, SCREEN_RECT,SPEED_X,SPEED_Y,GRAVITY
from ..tools import strip_from_sheet as strip




class State(object):
    def __init__(self, name, reverse, player):
        self.name = name
        self.reverse = reverse
        self.player = player
        self.next = None

    def do_actions(self):
        pass

    def get_event(self,event):
        pass

    def check_conditions(self):
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass


class StateMachine(object):
    def __init__(self):

        self.states = {}
        self.active_state = None

    def add_state(self, state):

        self.states[state.name] = state

    def get_event(self, event):
        self.active_state.get_event(event)

    def check(self):

        if self.active_state is None:
            return

        self.active_state.do_actions()

        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)

    def set_state(self, new_state_name):

        if self.active_state is not None:
            self.active_state.exit_actions()

        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()

class PlayerStanding(State):
    def __init__(self, reverse, player):
        super(PlayerStanding,self).__init__('standing',reverse,player)




    def get_event(self,event):
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_LEFT, pg.K_a):
                self.next =  'walk_left'
            elif event.key in (pg.K_RIGHT, pg.K_d):
                self.next = 'walk_right'
            elif event.key in (pg.K_DOWN, pg.K_s):
                self.next = 'crouch'
            elif event.key in (pg.K_UP,pg.K_w):
                self.next = 'jump'


    def check_conditions(self):
        key = pg.key.get_pressed()
        if key[pg.K_LEFT] or key[pg.K_a]:
            self.next = 'walk_left'
        elif key[pg.K_RIGHT] or key[pg.K_d]:
            self.next = 'walk_right'
        elif key[pg.K_DOWN] or key[pg.K_s]:
            self.next = 'crouch'
        if self.next != None:
            return self.next


    def entry_actions(self):
        self.next = None
        self.player.speed = [0,0]
        if self.reverse == False:
            self.player.images = cycle([GFX['p_stand']])
        elif self.reverse == True:
            self.player.images = cycle([pg.transform.flip(GFX['p_stand'],True,True)])

class PlayerCrouch(State):
    def __init__(self,reverse, player):
        super(PlayerCrouch, self).__init__('crouch',reverse,player)


    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_LEFT, pg.K_a):
               self.next = 'crouch_left'
            elif event.key in (pg.K_RIGHT, pg.K_d):
                self.next = 'crouch_right'
            elif event.key in (pg.K_UP, pg.K_w):
                self.next = 'standing'
        elif event.type == pg.KEYUP:
            if event.key in (pg.K_DOWN,pg.K_s):
                self.next = 'standing'

    def check_conditions(self):
        key = pg.key.get_pressed()
        if not (key[pg.K_s] or key[pg.K_DOWN]):
            self.next = 'standing'
        if self.next != None:
            return self.next


    def entry_actions(self):
        self.next = None
        self.player.speed = [0,0]
        if self.reverse == False:
            self.player.images = cycle([GFX['p_crouch']])
        elif self.reverse == True:
            self.player.images = cycle([pg.transform.flip(GFX['p_crouch'],True,True)])


class PlayerCrouchLeft(State):
    def __init__(self,reverse,player):
        super(PlayerCrouchLeft,self).__init__('crouch_left',reverse,player)


    def get_event(self,event):
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_LEFT, pg.K_a):
                self.next = None
            elif event.key in (pg.K_RIGHT, pg.K_d):
                self.next = 'crouch_right'

        elif event.type == pg.KEYUP:
            if event.key in (pg.K_LEFT, pg.K_a):
                self.next = 'crouch'
            if event.key in (pg.K_DOWN,pg.K_s):
                self.next = 'walk_left'

    def check_conditions(self):
        if self.next != None:
            return self.next

    def entry_actions(self):
        self.next = None
        if self.reverse == False:
            self.player.speed = [-SPEED_X/2,0]
            self.player.images = cycle(strip(GFX['p_crouch0'],(0,0),(23,24),2))
        elif self.reverse == True:
            self.player.speed = [SPEED_X/2,0]
            self.player.images = cycle(strip(pg.transform.flip(GFX['p_crouch0'],True,True),(0,0),(23,24),2))



class PlayerCrouchRight(State):
    def __init__(self, reverse,player):
        super(PlayerCrouchRight, self).__init__('crouch_right',reverse,player)


    def check_conditions(self):
        if self.next != None:
            return self.next
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_LEFT, pg.K_a):
                self.next=  'crouch_left'
            elif event.key in (pg.K_RIGHT, pg.K_d):
                self.next = None
        elif event.type == pg.KEYUP:
            if event.key in (pg.K_RIGHT, pg.K_d):
                self.next = 'crouch'
            elif event.key in (pg.K_DOWN,pg.K_s):
                self.next = 'walk_right'

    def entry_actions(self):
        self.next = None
        if self.reverse == False:
            self.player.speed = [SPEED_X / 2,0]
            self.player.images = cycle(strip(GFX['p_crouch1'],(0,0),(23,24),2))
        elif self.reverse == True:
            self.player.speed = [-SPEED_X / 2,0]
            self.player.images = cycle(strip(pg.transform.flip(GFX['p_crouch1'],True,True),(0,0),(23,24),2))


class PlayerWalkLeft(State):
    def __init__(self,reverse,player):
        super(PlayerWalkLeft, self).__init__('walk_left',reverse,player)



    def check_conditions(self):
        key = pg.key.get_pressed()
        if not (key[pg.K_a] or key[pg.K_LEFT]):
            self.next = 'standing'
        if self.next != None:
            return self.next

    def get_event(self,event):
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_LEFT, pg.K_a):
                self.next = None
            elif event.key in (pg.K_RIGHT, pg.K_d):
                self.next = 'walk_right'
            elif event.key in (pg.K_DOWN, pg.K_s):
                self.next = 'crouch_left'
            elif event.key in (pg.K_UP,pg.K_w):
                self.next = 'jump_left'

        elif event.type == pg.KEYUP:
            if event.key in (pg.K_LEFT, pg.K_a):
                self.next = 'standing'

    def entry_actions(self):
        self.next = None
        if self.reverse == False:
            self.player.speed = [-SPEED_X, 0]
            self.player.images = cycle(strip(GFX['p_walk0'],(0,0),(24,31),11))
        if self.reverse == True:
            self.player.speed = [SPEED_X, 0]
            self.player.images = cycle(strip(pg.transform.flip(GFX['p_walk0'],True,True),(0,0),(24,31),11))


class PlayerWalkRight(State):
    def __init__(self,reverse,player):
        super(PlayerWalkRight, self).__init__('walk_right',reverse,player)

    def check_conditions(self):
        key = pg.key.get_pressed()
        if not (key[pg.K_d] or key[pg.K_RIGHT]):
            self.next = 'standing'
        if self.next != None:
            return self.next

    def get_event(self,event):
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_RIGHT, pg.K_d):
                self.next = None
            elif event.key in (pg.K_LEFT, pg.K_a):
                self.next = 'walk_left'
            elif event.key in (pg.K_DOWN, pg.K_s):
                self.next ='crouch_right'
            elif event.key in (pg.K_UP, pg.K_w):
                self.next = 'jump_right'
        elif event.type == pg.KEYUP:
            if event.key in (pg.K_RIGHT, pg.K_d):
                self.next = 'standing'

    def entry_actions(self):
        self.next = None
        if self.reverse == False:
            self.player.speed = [SPEED_X, 0]
            self.player.images = cycle(strip(GFX['p_walk1'], (0, 0), (24, 31), 11))
        elif self.reverse == True:
            self.player.speed = [-SPEED_X, 0]
            self.player.images = cycle(strip(pg.transform.flip(GFX['p_walk1'],True,True), (0, 0), (24, 31), 11))

class PlayerJump(State):
    def __init__(self,reverse,player):
        super(PlayerJump, self).__init__('jump',reverse,player)

    def check_conditions(self):
        if self.player.on_ground == True:
            return 'standing'
        elif self.next != None:
            return self.next


    def get_event(self,event):
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_RIGHT, pg.K_d):
                self.next =  'jump_right'
            elif event.key in (pg.K_LEFT, pg.K_a):
                self.next =  'jump_left'



    def entry_actions(self):
        self.next = None
        self.player.on_ground = False
        if self.reverse == False:
            self.player.speed[1] = - SPEED_Y
            self.player.images = cycle([GFX['p1_jump']])
        elif self.reverse == True:
            self.player.speed[1] = SPEED_Y
            self.player.images = cycle([pg.transform.flip(GFX['p1_jump'],True,True)])

class PlayerJumpLeft(State):
    def __init__(self,reverse,player):
        super(PlayerJumpLeft, self).__init__('jump_left',reverse,player)

    def check_conditions(self):
        if self.player.on_ground == True:
            self.next =  'walk_left'
        if self.next != None:
            return self.next


    def get_event(self,event):
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_LEFT, pg.K_a):
                self.next = 'walk_left'


    def entry_actions(self):
        self.next = None
        if self.reverse == False:
            self.player.speed[0] = - SPEED_X
            self.player.images = cycle([GFX['p_jump0']])
            if self.player.on_ground:
                self.player.speed[1] = - SPEED_Y
        elif self.reverse == True:
            self.player.speed[0] = SPEED_X
            self.player.images = cycle([pg.transform.flip(GFX['p_jump0'], True, True)])
            if self.player.on_ground:
                self.player.speed[1] = SPEED_Y

        self.player.on_ground = False



class PlayerJumpRight(State):
    def __init__(self,reverse,player):
        super(PlayerJumpRight, self).__init__('jump_right',reverse,player)

    def check_conditions(self):
        if self.player.on_ground == True:
            self.next = 'walk_right'
        if self.next != None:
            return self.next


    def get_event(self,event):
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_RIGHT, pg.K_d):
                self.next = 'walk_right'


    def entry_actions(self):
        self.next = None
        if self.reverse == False:
            self.player.speed[0] = SPEED_X
            self.player.images = cycle([GFX['p_jump1']])
            if self.player.on_ground:
                self.player.speed[1] = - SPEED_Y
        elif self.reverse == True:
            self.player.speed[0] = - SPEED_X
            self.player.images = cycle([pg.transform.flip(GFX['p_jump1'],True,True)])
            if self.player.on_ground:
                self.player.speed[1] = SPEED_Y

        self.player.on_ground = False


player_dict = {
    'standing':PlayerStanding,
    'crouch':PlayerCrouch,
    'crouch_left':PlayerCrouchLeft,
    'crouch_right':PlayerCrouchRight,
    'walk_left':PlayerWalkLeft,
    'walk_right':PlayerWalkRight,
    'jump':PlayerJump,
    'jump_left':PlayerJumpLeft,
    'jump_right':PlayerJumpRight
}
