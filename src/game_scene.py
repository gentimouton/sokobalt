""" 
If game state is lost, call game over scene.
Can also pause game and go to main menu, passing an option to resume game.
"""

from constants import BTN_DOWN, BTN_UP, BTN_LEFT, BTN_RIGHT
from constants import CMD_NEWG, CMD_RESM
from controls import controller
from level import Level
from pview import T
import pview
import pygame as pg
from scene import Scene


class GameScene(Scene):

    def __init__(self):
        self._build_new_game()
        
    def tick(self, ms):
        """ process player inputs """
        if controller.btn_ispressed(BTN_UP):
            pass
              
        self._draw()
        return None, {}

    def resume(self, **kwargs):
        """ Scene callback. Called from the menu scene via scene manager. """
#         if kwargs['cmd'] == CMD_NEWG:
#             self._build_new_game()
#         elif kwargs['cmd'] == CMD_RESM:
#             pass
        pass

    def _build_new_game(self):
        """ load images and sounds from disk here """
        # build level
        self.level = Level()
        self.bg = self.level.pre_render_map()
        
        
    def _draw(self):
        pview.fill((0, 155, 155))
        # pg.draw.rect(pview.screen, (200, 0, 0), T(20, 20, 100, 200))
        pview.screen.blit(self.bg,(0,0))
        pg.display.flip()
    
    def redraw(self):
        self.bg = self.level.pre_render_map()
        self._draw()
        
if __name__ == "__main__":
    from constants import OUT_QUIT, OUT_FSCR
    pg.init()
    pview.set_mode((800, 600))
    clock = pg.time.Clock()
    scene = GameScene()
    while True:
        ms = clock.tick(60)
        outcome = controller.poll()  # get player input
        if outcome == OUT_QUIT:
            break
        elif outcome == OUT_FSCR:
            pview.toggle_fullscreen()
            scene.redraw()

        next_scene_id, kwargs = scene.tick(ms) 
        pg.display.set_caption('game scene %.1f' % clock.get_fps())
