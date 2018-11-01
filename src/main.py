from constants import OUT_FSCR, OUT_QUIT
from controls import controller
from game_scene import GameScene
import pview
import pygame as pg

from menu_scene import MenuScene
from scene import SCN_QUIT, SCN_GAME, SCN_MENU
from settings import BASE_RES, FPS


def main():
    pg.init()
    pg.display.set_caption('Sokobalt')
    pview.set_mode(BASE_RES)
    clock = pg.time.Clock()
    scenes = {
        SCN_MENU: MenuScene(),
        SCN_GAME: GameScene()
    }
    cur_scene = scenes[SCN_GAME]

    while True:
        ms = clock.tick(FPS)  # throttle

        # poll controls
        outcome = controller.poll()  # get player input
        if outcome == OUT_QUIT:
            break
        elif outcome == OUT_FSCR:
            pview.toggle_fullscreen()
            cur_scene.redraw()

        # tick scene
        next_scene_id, kwargs = cur_scene.tick(ms)
        if next_scene_id == SCN_QUIT:  # quit via dummy scene constant
            break
        elif next_scene_id is not None:  # change scene
            cur_scene.pause()
            cur_scene = scenes[next_scene_id]
            cur_scene.resume(**kwargs)


if __name__ == "__main__":
    main()
