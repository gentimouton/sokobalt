import pygame as pg

from constants import TILE_WALL, TILE_FLOR
from settings import BASE_RES

from pview import T

DIR_N = 'N'
DIR_S = 'S'
DIR_E = 'E'
DIR_W = 'W'
dir_vectors = {DIR_N: (0, -1), DIR_S: (0, 1), DIR_E: (1, 0), DIR_W: (-1, 0)}

N_TILES = 16  # square levels of 16x16 tiles
tile_size = BASE_RES // N_TILES


def load_map():
    """ Take a filename, return list of lists """
    # TODO: read from file instead
    return [
        [TILE_WALL, TILE_WALL, TILE_WALL, TILE_WALL],
        [TILE_WALL, TILE_FLOR, TILE_FLOR, TILE_WALL],
        [TILE_WALL, TILE_FLOR, TILE_FLOR, TILE_WALL],
        [TILE_WALL, TILE_WALL, TILE_WALL, TILE_WALL]
        ]

        
class Level():

    def __init__(self):
        # self.tiles, self.tile_types = load_map('assets/level.map') # TODO
        self.tiles = load_map() 
        self.w, self.h = len(self.tiles[0]), len(self.tiles)
        self.characters = {}
        self.occupancy = [[None for _ in range(self.h)] for _ in range(self.w)]
        
    def pre_render_map(self):
        # tileset = load_spritesheet_flat('assets/tileset.png') # TODO
        tile_s = T(tile_size)
        s = self.w * tile_s, self.h * tile_s
        bg = pg.Surface(s)
        for map_y, line in enumerate(self.tiles):
            for map_x, tile_type in enumerate(line):
                # tileset_id = int(self.tile_types[tile_type]['tileset_id'])
                # tile_img = tileset[tileset_id]
                color = (99, 99, 99) if tile_type == TILE_WALL else (0, 222, 0)
                tile_img = pg.Surface((tile_s, tile_s))
                tile_img.fill(color)
                bg.blit(tile_img, (map_x * tile_s, map_y * tile_s))
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
        
