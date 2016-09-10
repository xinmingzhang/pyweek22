import pygame as pg
import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

try:
    from pytmx import load_pygame
except ImportError:
    from pytmx.util_pygame import load_pygame


from .. import tools
from ..prepare import MAP, SCREEN_SIZE, SCREEN_RECT,GFX,TIME,SFX,MUSIC
from ..components.animation import Animation
from ..components.hud import Hud
from ..components.transition import Transition
from ..components.player import Player
from ..components.enemy import Enemy, Fish, Fly, Bat, Enimy, F1sh
from ..components.coin import Coin
from ..components.angles import get_distance





class LevelPlay(tools._State):
    def __init__(self):
        super(LevelPlay, self).__init__()

        tmx_data = load_pygame(MAP['map0'])

        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_rect = pg.Rect(0, 0, map_data.map_size[0]*map_data.tile_size[0],map_data.map_size[1]*map_data.tile_size[1])
        self.map_layer = pyscroll.BufferedRenderer(map_data, SCREEN_SIZE)
        self.map_layer.zoom = 1
        self.group = PyscrollGroup(map_layer = self.map_layer, default_layer = 2)
        self.animations = pg.sprite.Group()
        self.labels = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.pos_x = None
        self.pos_y = None
        self.pos_x_r = None
        self.pos_y_r = None
        self.upper_world = False

        self.time = 0
        self.timer = TIME
        self.coin_num = 0
        self.player_lives = 0
        self.hud = Hud()

        self.walls = list()
        for object in tmx_data.objects:
            if object.name == 'collide':
                self.walls.append(pg.Rect(
                    object.x, object.y,
                    object.width, object.height))
            elif object.name == 'playerpos':
                self.pos_x = object.x
                self.pos_y = object.y
                self.player = Player(self.pos_x,self.pos_y,False,self.group)
            elif object.name == 'playerpos_r':
                self.pos_x_r = object.x
                self.pos_y_r = object.y
            elif object.name == 'enemy':
                Enemy(object.x,object.y,self.enemies)
            elif object.name == 'fish':
                Fish(object.x,object.y,self.enemies)
            elif object.name == 'fly':
                Fly(object.x,object.y,self.enemies)
            elif object.name == 'coin':
                Coin(object.x,object.y,self.coins)
            elif object.name == 'bat':
                Bat(object.x,object.y,self.enemies)
            elif object.name == 'enimy':
                Enimy(object.x,object.y,self.enemies)
            elif object.name == 'f1sh':
                F1sh(object.x,object.y,self.enemies)
            elif object.name == 'over_event':
                self.over_rect = pg.Rect(object.x, object.y, object.width, object.height)
            elif object.name == 'over_event_r':
                self.over_rect_r = pg.Rect(object.x, object.y, object.width, object.height)

        self.player.platform = self.walls

        



    def get_event(self, event):

        self.player.get_event(event)
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.map_layer.zoom = 0.5
        elif event.type == pg.KEYUP:
            if event.type == pg.K_ESCAPE:
                self.quit = True
            elif event.key == pg.K_SPACE:
                self.map_layer.zoom = 1
            else:
                pass

    def startup(self, persist):
        pg.mixer.init()

        song = MUSIC['bg']
        pg.mixer.music.load(song)
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play()

        self.done = False
        self.persist = persist
        self.mask = self.persist['surface']
        self.transition = Transition(self.mask)
        self.player_lives = self.persist['lives']
        self.coin_num = self.persist['coins']



        if self.player.reverse == True:
            self.fog = pg.Surface(SCREEN_RECT.size, pg.SRCALPHA)
            self.fog_color = (0, 0, 0, 200)
            self.fog.fill(self.fog_color)




    def player_dead(self):
        sound = SFX['dead0']
        sound.play()

        self.player_lives -= 1
        if self.player_lives < 1:
            self.done = True
            self.next = 'LOSE'
        buffer = pg.display.get_surface()
        self.switch_screen = Transition(buffer)
        if self.player.reverse == False:
            self.player.rect.x, self.player.rect.y = self.pos_x, self.pos_y
        elif self.player.reverse == True:
            self.player.rect.x, self.player.rect.y = self.pos_x_r,self.pos_y_r




    def update(self, dt):
        self.offset_x, self.offset_y = self.group._map_layer.get_center_offset()

        self.time += dt
        if self.time > self.timer:
            self.time -= self.timer
            self.player_dead()

        self.group.update(dt)
        self.enemies.update(dt)
        self.coins.update(dt)
        self.hud.update(self,dt)
        self.animations.update(dt)

        if self.player.rect.colliderect(self.over_rect_r):
            if self.player.reverse == True:
                self.done = True
                self.next = 'WIN'


        if self.player.rect.colliderect(self.over_rect):
            self.player.rect.x, self.player.rect.y = self.pos_x_r, self.pos_y_r
            if self.coin_num >= 30:
                self.player.kill()
                self.player = Player(self.pos_x_r, self.pos_y_r,True,self.group)
                self.player.platform = self.walls
                self.done = True
                self.next = 'UPPER'
            elif self.coin_num < 30:
                self.player.reverse = False
                self.done = True
                self.next = 'BOTUP'


        if pg.sprite.spritecollide(self.player, self.coins, True):
            self.coin_num += 1
            sound = SFX['coin']
            sound.play()
            self.labels.empty()
            self.animations.empty()
            coin_sprite = pg.sprite.Sprite(self.labels)
            coin_sprite.image = GFX['hud_coins']
            x = self.offset_x + self.player.rect.x
            y = self.offset_y + self.player.rect.y
            coin_sprite.rect = pg.Rect((x,y),coin_sprite.image.get_size())
            ani = Animation(x = 50, y = 10, duration= 100, transition="out_bounce")
            ani.start(coin_sprite.rect)
            self.animations.add(ani)

        if not self.map_rect.contains(self.player.rect):
            self.player_dead()

        if pg.sprite.spritecollide(self.player,self.enemies,False):
            self.player_dead()

        self.labels.update(dt)


    def cleanup(self):
        pg.mixer.quit()
        self.persist = {}
        self.persist['coins'] = self.coin_num
        self.persist['lives'] = self.player_lives
        self.persist['surface']= pg.display.get_surface()
        return self.persist

    def draw(self, surface):
        self.group.empty()
        if self.player.reverse == True:
            close = (enemy for enemy in self.enemies if get_distance(enemy.rect.center, self.player.rect.center) <= 100)
            close_enemies = pg.sprite.Group(close)
            self.group.add(self.player,self.coins,close_enemies)
        elif self.player.reverse == False:
            close = (enemy for enemy in self.enemies if get_distance(enemy.rect.center, self.player.rect.center) <= SCREEN_SIZE[0])
            close_enemies = pg.sprite.Group(close)
            self.group.add(self.player,self.coins,close_enemies)


        self.group.draw(surface)
        self.group.center(self.player.rect.center)



        if hasattr(self,'fog') and self.map_layer.zoom == 1:
            self.fog.fill(self.fog_color)
            for i in range(200):
                pg.draw.circle(self.fog, pg.Color(0,0,0,200-i), (self.player.rect.centerx+self.offset_x,self.player.rect.centery+self.offset_y), int(100-i*0.5))
            surface.blit(self.fog,(0,0))
        elif hasattr(self,'fog') and self.map_layer.zoom == 0.5:
            self.fog.fill(self.fog_color)
            surface.blit(self.fog,(0,0))

        self.hud.draw(surface)
        self.transition.draw(surface)
        self.labels.draw(surface)

        if hasattr(self,'switch_screen'):
            self.switch_screen.draw(surface)






