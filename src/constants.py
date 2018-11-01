
# outcomes of controller and scene manager
OUT_NONE, OUT_QUIT, OUT_FSCR = 'none', 'quit', 'fullscreen'

# buttons
BSLC, BUPP, BDWN, BLFT, BRGT = 'select', 'up', 'down', 'left', 'right'

# colorkey of sprites 
TRANSPARENT = (255, 0, 255)

# spritesheet constants
SWAL, SFLR, SGOL = 'wall', 'floor', 'goal'
SBOX, SPLR, SNON = 'box', 'player', 'none'
SPLE, SPLW, SPLS, SPLN = 'face east', 'face west', 'face south', 'face north'
SDNC, SDNS = 'dance1', 'dance2'
# sprites must be in this order in the spritesheet
SPR_ORDER = [
    SWAL, SFLR, SGOL, SBOX, SPLR, SNON,
    SPLE, SPLW, SPLS, SPLN, SDNC, SDNS
    ]

# all possible directions
DIRN, DIRS, DIRE, DIRW = 'N', 'S', 'E', 'W'
