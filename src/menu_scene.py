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
        # selection logic and rendering constants and variables
        self._choice = 0  # TODO: should init at latest unlocked level
        self._choices = [
            ('L%d' % i, SCN_GAME, {'level': i})
            for i in range(len(levels))
        ]
        self._page_w = 5  # number of levels per row
        self._page_h = 4  # number of rows per screen
        blanks = self._page_w - (len(levels) % self._page_w)
        self._choices += [('--', None, {})] * blanks  # pad last row with blanks

        self._page_start_row = self._choice // self._page_w  # for pagination

        self._ongoing_level = None  # if player wants to resume current level

    def tick(self, ms):
        # process inputs: play selected level or quit
        if controller.btn_event(BSLC):
            c = self._choices[self._choice]
            if c[1] and c[2]['level'] == self._ongoing_level:
                return SCN_GAME, {'resume_level': True}  # key matters, not value
            else:
                return c[1], c[2]
        if controller.btn_event(BMNU):  # press menu button when in menu: exit
            return SCN_QUIT, {}

        # process inputs: move level cursor
        cursor_row = self._choice // self._page_w
        max_row = len(self._choices) // self._page_w - 1
        if controller.btn_event(BDWN) and cursor_row < max_row:
            self._choice += self._page_w
        elif controller.btn_event(BUPP) and cursor_row > 0:
            self._choice -= self._page_w
        elif controller.btn_event(BLFT) and self._choice > 0:
            self._choice -= 1
        elif controller.btn_event(BRGT) and self._choice < len(self._choices)-1:
            self._choice += 1

        # draw bg
        pview.fill((86, 55, 35))

        # adjust page start if needed
        cursor_row = self._choice // self._page_w
        cursor_col = self._choice % self._page_w
        if cursor_row > self._page_start_row + self._page_h - 1:
            self._page_start_row += 1
        if cursor_row < self._page_start_row:
            self._page_start_row -= 1

        # draw level numbers
        start_choice = self._page_start_row * self._page_w
        end_choice = start_choice + self._page_h * self._page_w
        visible_choices = self._choices[start_choice:end_choice]
        for i, choice in enumerate(visible_choices):
            x = 150 + (i % self._page_w) * 100
            y = 150 + (i // self._page_w) * 100
            ptext.draw(choice[0], T(x, y), fontsize=T(50), color=(185, 122, 87))

        # draw pointer
        x = 115 + cursor_col * 100
        y = 140 + (cursor_row - self._page_start_row) * 100
        ptext.draw('>', T(x, y), fontsize=T(70), color=(0, 162, 232))

        # draw command tips
        ptext.draw('F11: toggle fullscreen\nEsc: quit', T(10, 10),
                   fontsize=T(20), color=(185, 122, 87))

        pg.display.flip()
        return None, {}  # no next scene to return

    def resume(self, **kwargs):
        """ called by scene manager from the game scene, passing kwargs. """
        self._choice = 0
        if kwargs.get('current_level'):
            level = kwargs['current_level']
            self._choice = level
            self._ongoing_level = level


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
