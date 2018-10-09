from level import TWAL, TFLR, TGOL, TBGL, TPGL
import pview
import pygame as pg


# colorkey of sprites 
TRANSPARENT = (255, 0, 255)

# spritesheet constants
SWAL, SFLR, SGOL = 'wall', 'floor', 'goal'
SBOX, SPLR, SNON = 'box', 'player', 'none'
SPLE, SPLW = 'player east', 'player west'
SPLS, SPLN = 'player south', 'player north' 
SDNC, SDNS = 'player dance1', 'player dance2'


def load_spritesheet(filename, spr_order, s):
    """ Generic spritesheet loader. 
    File should have square sprites of size s.
    spr_order is the order of sprites in the file, flattened. 
    Use SNON to in spr_order to skip slots with no sprite. 
    returns a mapping of spr_constant to img
    """
    img = pg.image.load(filename).convert()
    img.set_colorkey(TRANSPARENT, pg.RLEACCEL)
    ntiles_w, ntiles_h = img.get_width() // s, img.get_height() // s
    sheet = [img.subsurface((x * s, y * s, s, s)) 
             for y in range(ntiles_h) for x in range(ntiles_w)]
    d = dict(zip(spr_order, sheet[:len(spr_order)]))
    return d
    
    
def draw_level(level, surf, sprites):
    """ draw level onto surf. 
    level is a Level.
    surf is a pygame surface of any size.
    sprites is a dict mapping sprite name to sprite img
    """
    surf.fill((0, 0, 0))  # prefill for non-square surf or fullscreen edges
    w, h = surf.get_size()
    maxs = len(level.tiles)  # assumes level is always square
    s = min(w // maxs, h // maxs)  # this way, no need to use pview.T
    rect = (s, s, 2 * s, 3 * s)
    pg.draw.rect(surf, (155, 211, 155), rect)
    scaled_sprites = {n: pg.transform.scale(img, (s, s)) 
                      for n, img in sprites.items()}
    # draw background
    for y, row in enumerate(level.tiles):
        for x, tile in enumerate(row):
            rect = [x * s, y * s, s, s]
            if tile == TWAL:
                surf.blit(scaled_sprites[SWAL], rect)
            elif tile in (TGOL, TBGL, TPGL):
                surf.blit(scaled_sprites[SGOL], rect)
            else:
                surf.blit(scaled_sprites[SFLR], rect)
    # draw player and boxes
    y, x = level.player
    rect = [s * x, s * y, s, s]
    surf.blit(scaled_sprites[SPLR], rect)
    for (y, x) in level.boxes:
        rect = [s * x, s * y, s, s]
        surf.blit(scaled_sprites[SBOX], rect)
    
################# TESTS ################## 


def test_load_spritesheet():
    import os
    s = 20
    filename = 'tmp_img.test'
    # make a dummy spritesheet file
    surf = pg.surface.Surface((s * 2, s))
    surf.fill((255, 0, 0), (0, 0, s, s))  # first spr is red square
    surf.fill((0, 255, 0), (s, 0, s, s))  # second is green square
    pg.image.save(surf, filename)
    # read file as spritesheet
    # TODO: 
    # test sprite sizes and colors
    # TODO:    
    # delete file
    try:
        os.remove(filename)
    except OSError:
        pass


def test_draw_level():
    # make a dummy level
    from level import Level
    tiles = [
        "########",
        "########",
        "##    ##",
        "##@.$ ##",
        "##   *##",
        "########",
        "########",
        "########"
        ]
    tiles = list(map(lambda r: list(r), tiles))
    level = Level(tiles, [(3, 3), (4, 5)], (3, 2), [(3, 4), (4, 5)])
    
    # load sprites and canvas with pygame
    pg.init()
    BASE_RES = (512, 600)  # should be square, but rectangular here to test
    pview.set_mode(BASE_RES)
    
    # sheet and expected order of images, flattened
    spr_order = [SWAL, SFLR, SGOL, SBOX, SPLR, SNON,
                 SPLE, SPLW, SPLS, SPLN, SDNC, SDNS]
    sprites = load_spritesheet('../assets/sokobalt_tilesheet_8px.png',
                             spr_order, 8)
    
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
        draw_level(level, pview.screen, sprites)
        pg.display.flip()


if __name__ == "__main__":
    test_draw_level()  # press ESC or F11
    # test_load_spritesheet() # TODO: 
