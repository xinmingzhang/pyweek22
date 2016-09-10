import os
import pygame as pg
from . import tools

pg.init()
pg.mixer.pre_init(44100, -16, 1, 512)


SCREEN_SIZE = (640, 480)

ORIGINAL_CAPTION = "Upside_down"



os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)

SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


SPEED_X = 0.2
SPEED_Y = 0.47
GRAVITY = 0.001


LIVES = 3
CHEAT_LIVES = 30
TIME = 120000


GFX = tools.load_all_gfx(os.path.join("resources", "graphics"))
FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
SFX = tools.load_all_sfx(os.path.join("resources", "sound"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
MAP = tools.load_all_maps(os.path.join("resources", "maps"))

ICON = GFX['icon']

