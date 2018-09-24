from constants import BTN_SLCT, BTN_DOWN, BTN_UP
import pygame as pg

FPS = 30
DEBUG = True
BASE_RES = 640 # ideally a multiple of 8

# map button to keys
bmap = {
    BTN_SLCT: [pg.K_SPACE, pg.K_RETURN],
    BTN_UP: [pg.K_w, pg.K_UP],
    BTN_DOWN: [pg.K_s, pg.K_DOWN],
    }

# map keys to button, eg K_d -> 'right'
kmap = {e: btn for (btn, v) in bmap.items() for e in v}
