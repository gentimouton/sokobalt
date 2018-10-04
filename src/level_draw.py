import pview
import pygame as pg
from level_scratch import SIZE, TWAL


def draw_level(level, surf):
    """ draw level onto surf. 
    surf is a pygame surface of any size.
    """
    surf.fill((0, 0, 0))  # prefill for non-square surf or fullscreen edges
    w, h = surf.get_size()
    s = min(w // SIZE, h // SIZE)  # this way, no need to use pview.T
    rect = (s, s, 2 * s, 3 * s)
    pg.draw.rect(surf, (155, 211, 155), rect)

    for y, row in enumerate(level.tiles):
        for x, tile in enumerate(row):
            color = (111, 11, 11) if tile == TWAL else (211, 155, 155)
            rect = [x * s, y * s, s, s]
            pg.draw.rect(surf, color, rect)

    # TODO: draw rest of level

################# TESTS ################## 


def test_draw_level():
    # make a dummy level
    from level_scratch import build_level_from_tiles
    tiles = list(map(lambda x:list(x), ['#####', '#@$.#', '#####']))
    level = build_level_from_tiles(tiles)
    # draw with pygame
    pg.init()
    BASE_RES = (512, 600) # should be square, but rectangular here to test
    pview.set_mode(BASE_RES)
    
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                done = True
            if event.type == pg.KEYDOWN and event.key == pg.K_F11:
                pview.toggle_fullscreen()
        # draw every loop, kinda wasteful
        draw_level(level, pview.screen)
        pg.display.flip()


if __name__ == "__main__":
    test_draw_level()  # press ESC or F11
    
