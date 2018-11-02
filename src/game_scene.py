""" 
If game state is lost, call game over scene.
Can also pause game and go to main menu, passing an option to resume game.
"""
import ptext
from pview import T
from constants import BDWN, BUPP, BLFT, BRGT, BRST
from constants import SPR_ORDER, DIRN, DIRS, DIRE, DIRW
from controls import controller
from level_draw import load_spritesheet, draw_level
import pview
import pygame as pg
from scene import Scene, SCN_GAME
from settings import SHEET_FILENAME, SPR_SIZE, BASE_RES


class GameScene(Scene):

    def __init__(self, levels):
        # load spritesheet
        self.sprites = load_spritesheet(SHEET_FILENAME, SPR_ORDER, SPR_SIZE)
        self.levels = levels
        self.level = levels[0]

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
        if controller.btn_event(BRST):
            self.level.reset()

        if self.level.is_complete():
            # TODO: dance
            return SCN_GAME, {'level': self.level.level_num + 1}

        self._draw()
        return None, {}

    def resume(self, **kwargs):
        """ Scene callback. Called from the menu scene via scene manager. """
        self.level = self.levels[kwargs['level'] % len(self.levels)]
        self.level.reset()

    def _draw(self):
        # TODO: DirtySprite for player and fixed surf for bg
        pview.fill((0, 155, 155))  # unnecessary?
        draw_level(self.level, pview.screen, self.sprites)
        # pview.screen.blit(self.bg, (0, 0))
        # TODO: right-side HUD tracking steps and current level number
        x = BASE_RES[1] + 10
        y = 10
        ptext.draw('Level %d' % self.level.level_num, T(x, y), fontsize=T(40))
        w, h = BASE_RES
        txt = 'R: rest level\nF11: toggle fullscreen\nEsc: menu'
        ptext.draw(txt, T(h+20, h-80), fontsize=T(20))

        pg.display.flip()

        # TODO: level navigator menu (can replay any unlocked one)

    def redraw(self):
        # TODO: recompute/redraw bg
        # self._draw()
        pass


if __name__ == "__main__":
    from constants import OUT_QUIT, OUT_FSCR
    from settings import LEVELS_FILENAME, LEVELS_MAXSIZE
    from level import load_level_set

    pg.init()
    pview.set_mode(BASE_RES)
    clock = pg.time.Clock()
    levels = load_level_set(LEVELS_FILENAME, LEVELS_MAXSIZE)  # list
    scene = GameScene(levels)
    while True:
        ms = clock.tick(30)
        outcome = controller.poll()  # get player input
        if outcome == OUT_QUIT:
            break
        elif outcome == OUT_FSCR:
            pview.toggle_fullscreen()
            scene.redraw()

        next_scene_id, kwargs = scene.tick(ms)
        if next_scene_id == SCN_GAME:  # level completed, switch to game scene
            scene.resume(**kwargs)
        pg.display.set_caption('game scene -- %.1f fps' % clock.get_fps())
