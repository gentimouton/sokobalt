from constants import BSLC, BDWN, BUPP, BLFT, BRGT, BMNU
from controls import controller
import ptext
from pview import T
import pview
import pygame as pg
from scene import Scene, SCN_GAME, SCN_QUIT


class MenuScene(Scene):
    """ Main menu.
    Show list of levels, player can select one and start playing.
    """

    def __init__(self, levels):
        self.w = 5  # UI constant for this scene
        self._choice = 0  # TODO: should init at latest unlocked level
        self._choices = [
            ('L%d' % i, SCN_GAME, {'level': i})
            for i in range(len(levels))
        ]
        blanks = self.w - ((len(levels) + 1) % self.w)  # +1 for quit button
        self._choices += [('--', None, {})] * blanks
        self._choices += [('Quit', SCN_QUIT, {})]
        # current level in game scene, used if player wants to resume level
        self.cur_level = None

    def tick(self, ms):
        # process inputs
        cur = self._choice
        w = self.w
        n = len(self._choices)
        if controller.btn_event(BSLC):
            c = self._choices[self._choice]
            if c[2]['level'] == self.cur_level:
                return SCN_GAME, {'resume_level': True}  # key matters, not value
            else:
                return c[1], c[2]
        if controller.btn_event(BMNU):  # press menu button when in menu: exit
            return SCN_QUIT, {}
        elif controller.btn_event(BDWN):
            self._choice = (cur + w) % n
        elif controller.btn_event(BUPP):
            self._choice = (cur - w) % n
        elif controller.btn_event(BLFT):
            if cur % w == 0:  # beginning of row
                self._choice += w - 1  # go to end
            else:
                self._choice -= 1
        elif controller.btn_event(BRGT):
            if cur % w == w - 1:  # end of row
                self._choice -= w - 1  # back to beginning
            else:
                self._choice += 1

        # draw the whole screen
        pview.fill('black')
        for i, choice in enumerate(self._choices):
            x = 150 + (i % self.w) * 100
            y = 200 + (i // self.w) * 100
            ptext.draw(choice[0], T(x, y), fontsize=T(50))
        x = 115 + (self._choice % self.w) * 100
        y = 190 + (self._choice // self.w) * 100
        ptext.draw('>', T(x, y), fontsize=T(70))
        ptext.draw('F11: toggle fullscreen\nEsc: quit', T(10, 10), fontsize=T(20))
        pg.display.flip()
        return None, {}  # no next scene to return

    def resume(self, **kwargs):
        """ called by scene manager from the game scene, passing kwargs. """
        self._choice = 0
        if kwargs.get('current_level'):
            level = kwargs['current_level']
            self._choice = level
            self.cur_level = level


if __name__ == "__main__":
    def main():
        from settings import FPS, BASE_RES

        pg.init()
        pview.set_mode(BASE_RES)
        clock = pg.time.Clock()
        levels = [1, 2, 3, 4, 5, 6]
        scene = MenuScene(levels)
        while not pg.event.peek([pg.QUIT, pg.KEYDOWN]):
            ms = clock.tick(FPS)
            scene_id, kwargs = scene.tick(ms)


    main()
