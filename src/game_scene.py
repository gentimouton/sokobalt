""" 
If game state is lost, call game over scene.
Can also pause game and go to main menu, passing an option to resume game.
"""

from constants import BDWN, BUPP, BLFT, BRGT, BSLC
from constants import SPR_ORDER, DIRN, DIRS, DIRE, DIRW
from controls import controller
from level import load_level_set
from level_draw import load_spritesheet, draw_level
import pview
import pygame as pg
from scene import Scene
from settings import SHEET_FILENAME, LEVELS_FILENAME, LEVELS_MAXSIZE, SPR_SIZE


class GameScene(Scene):

    def __init__(self):
        # load spritesheet
        self.sprites = load_spritesheet(SHEET_FILENAME, SPR_ORDER, SPR_SIZE)
        # load level set  
        self.levels = load_level_set(LEVELS_FILENAME, LEVELS_MAXSIZE)  # list
        self.cur_level = 0
        self.start_level()
        
    def start_level(self):
        self.level = self.levels[self.cur_level]
        self.level.reset()
        
    def tick(self, ms):
        """ process player inputs and draw """
        if controller.btn_event(BUPP):
            self.level.move(DIRN)
        if controller.btn_event(BDWN):
            self.level.move(DIRS)
        if controller.btn_event(BLFT):
            self.level.move(DIRW)
        if controller.btn_event(BRGT):
            self.level.move(DIRE)
        if controller.btn_event(BSLC):
            self.start_level()
        
        if self.level.is_complete():
            # TODO: dance
            # load next level
            self.cur_level = (self.cur_level + 1) % len(self.levels)
            self.start_level()
        
        self._draw()
        return None, {}

    def resume(self, **kwargs):
        """ Scene callback. Called from the menu scene via scene manager. """
        pass

    def _draw(self):
        # TODO: DirtySprite for player and fixed surf for bg
        pview.fill((0, 155, 155))  # unnecessary?
        draw_level(self.level, pview.screen, self.sprites)
#         pview.screen.blit(self.bg, (0, 0))
        pg.display.flip()
        # TODO: right-side HUD tracking steps and current level number
        # TODO: level navigator menu (can replay any unlocked one)
    
    def redraw(self):
        # TODO: recompute/redraw bg
#         self._draw()
        pass
        
        
if __name__ == "__main__":
    from constants import OUT_QUIT, OUT_FSCR
    from settings import BASE_RES
    pg.init()
    pview.set_mode((BASE_RES, BASE_RES))
    clock = pg.time.Clock()
    scene = GameScene()
    while True:
        ms = clock.tick(30)
        outcome = controller.poll()  # get player input
        if outcome == OUT_QUIT:
            break
        elif outcome == OUT_FSCR:
            pview.toggle_fullscreen()
            scene.redraw()

        next_scene_id, kwargs = scene.tick(ms) 
        pg.display.set_caption('game scene %.1f' % clock.get_fps())
