""" 
If game state is lost, call game over scene.
Can also pause game and go to main menu, passing an option to resume game.
"""

from constants import BTN_DOWN, BTN_UP, BTN_LEFT, BTN_RIGHT
from controls import controller
from level import Level
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
        pass

    def _build_new_game(self):
        """ load images and sounds from disk here """
#         self.level = Level()
#         self.bg = self.level.pre_render_map()
        self.bg = pg.surface.Surface((200, 200)) # TODO: tie level here
        
    def _draw(self):
        pview.fill((0, 155, 155))
        # pg.draw.rect(pview.screen, (200, 0, 0), T(20, 20, 100, 200))
        pview.screen.blit(self.bg, (0, 0))
        pg.display.flip()
    
    def redraw(self):
        # TODO: scale level bg
        self._draw()
        
        
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
