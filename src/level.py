from constants import TWAL, TFLR, TGOL
from pview import T
import pygame as pg
from settings import BASE_RES, SPRITESHEET


DIR_N = 'N'
DIR_S = 'S'
DIR_E = 'E'
DIR_W = 'W'
dir_vectors = {DIR_N: (0, -1), DIR_S: (0, 1), DIR_E: (1, 0), DIR_W: (-1, 0)}

N_TILES = 16  # square levels of 16x16 tiles


def load_spritesheet(filename):
    """ Load spritesheet from file. 
    Returned img size is that of original file, not scaled to game window. 
    return [wall, floor, goal, box, player]
    """
    sheet = pg.image.load(filename).convert()
    sheet.set_colorkey((255, 0, 255), pg.RLEACCEL)
    w = 8  # width of sprite in pixels. Sprites are square.
    images = [sheet.subsurface((x * w, 0, w, w)) for x in range(5)]
#     if resize_to:
#         images = list(
#             map(
#                 lambda img: pg.transform.scale(img, (resize_to, resize_to))
#                 ))
    return images

    
def load_map():
    """ Take a filename, return list of lists """
    # TODO: read from file instead
    # TODO: return coords where player and box(es) start. 
    return [
        [TWAL, TWAL, TWAL, TWAL, TWAL, TWAL, TWAL, TWAL, TWAL, TWAL],
        [TWAL, TFLR, TWAL, TFLR, TFLR, TFLR, TFLR, TFLR, TFLR, TWAL],
        [TWAL, TFLR, TWAL, TFLR, TFLR, TWAL, TWAL, TWAL, TFLR, TWAL],
        [TWAL, TFLR, TWAL, TWAL, TFLR, TFLR, TFLR, TWAL, TFLR, TWAL],
        [TWAL, TFLR, TFLR, TFLR, TFLR, TFLR, TFLR, TWAL, TFLR, TWAL],
        [TWAL, TFLR, TFLR, TFLR, TFLR, TFLR, TFLR, TFLR, TFLR, TWAL],
        [TWAL, TFLR, TFLR, TFLR, TGOL, TWAL, TFLR, TGOL, TFLR, TWAL],
        [TWAL, TFLR, TFLR, TFLR, TFLR, TWAL, TFLR, TFLR, TFLR, TWAL],
        [TWAL, TFLR, TFLR, TWAL, TWAL, TWAL, TWAL, TFLR, TFLR, TWAL],
        [TWAL, TWAL, TWAL, TWAL, TWAL, TWAL, TWAL, TWAL, TWAL, TWAL]
        ]

        
class Level():

    def __init__(self):
        """ Load spritesheet and map only once. Rescale in pre_render_map. """
        # self.tiles, self.tile_types = load_map('assets/level.map') # TODO
        self.sheet = load_spritesheet(SPRITESHEET)
        self.tiles = load_map() 
        self.w, self.h = len(self.tiles[0]), len(self.tiles)
        self.characters = {}
        self.occupancy = [[None for _ in range(self.h)] for _ in range(self.w)]
        # TODO: add player and boxes from map
        
    def pre_render_map(self):
        tsize = T(BASE_RES // N_TILES)
        bg = pg.Surface((self.w * tsize, self.h * tsize))
        timgs = dict(zip([TWAL, TFLR, TGOL], self.sheet[:3])) 
        for map_y, line in enumerate(self.tiles):
            for map_x, tile_type in enumerate(line):
                
#                 color = (99, 99, 99) if tile_type == TWAL else (0, 222, 0)
#                 tile_img = pg.Surface((tsize, tsize))
#                 tile_img.fill(color)
                tile_img = pg.transform.scale(timgs[tile_type], (tsize, tsize))
                bg.blit(tile_img, (map_x * tsize, map_y * tsize))
        return bg
    
    def get_destination(self, cur_pos, direction):
        # return new position, delta to get there
        dx, dy = dir_vectors[direction]
        x, y = cur_pos
        newx, newy = x + dx, y + dy
        if newy < 0 or newy >= self.w or newx < 0 or newx >= self.h:
            return None, None
        else:
            return (newx, newy), (dx, dy)
    
    def get_occupancy(self, pos):
        x, y = pos
        return self.occupancy[x][y]

    def move_character_to(self, char, pos):
        x, y = pos
        if char in self.characters.keys():
            oldx, oldy = self.characters[char]
            self.occupancy[oldx][oldy] = None
        self.occupancy[x][y] = char
        self.characters[char] = pos
        
