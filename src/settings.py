from constants import BSLC, BDWN, BUPP, BLFT, BRGT
import pygame as pg


FPS = 30
DEBUG = True
BASE_RES = 800, 600  # height should ideally be a multiple of 8

SHEET_FILENAME = '../assets/sokobalt_tilesheet_8px.png'
SPR_SIZE = 8 # size of sprites, in pixels. Sprites must be square.

LEVELS_FILENAME = '../assets/levels_test.txt'
# LEVELS_FILENAME = '../assets/levels_microban.txt'
LEVELS_MAXSIZE = 12 # maximum width and height of a level

# map button to keys
bmap = {
    BSLC: [pg.K_SPACE, pg.K_RETURN],
    BUPP: [pg.K_w, pg.K_UP],
    BDWN: [pg.K_s, pg.K_DOWN],
    BLFT: [pg.K_a, pg.K_LEFT],
    BRGT: [pg.K_d, pg.K_RIGHT],
    }

# map keys to button, eg K_d -> 'right'
kmap = {e: btn for (btn, v) in bmap.items() for e in v}
