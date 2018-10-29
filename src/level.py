import os
from copy import deepcopy
from constants import DIRN, DIRS, DIRE, DIRW

# sokoban file format: characters and their meaning
TWAL, TFLR, TGOL = '#', ' ', '.'
TPLR, TBOX, TPGL, TBGL = '@', '$', '+', '*'
TILESET = set([TWAL, TFLR, TGOL, TPLR, TBOX, TPGL, TBGL])

DIRMAP = {  # coords are (y,x)
    DIRN: (-1, 0),
    DIRS: (1, 0),
    DIRE: (0, 1),
    DIRW: (0, -1)
    }


class Level:
    """ A Level is a 16x16 map, a player starting position, 
    a list of goal positions, and a list of starting box positions. 
    """
    
    def __init__(self, tiles, goals, player, boxes):
        """ tiles is list of lists, with all possible tiles eg TWAL and TPGL. 
        positions are 2-tuples. 
        goals and boxes are lists of 2-tuples, player a 2-tuple.
        """
        self.base_tiles = tiles  #  use these to reset level
        self.base_goals = goals
        self.base_player = player
        self.base_boxes = boxes
        self.reset()
            
    def __repr__(self):
        tiles = [
            [
                TPGL if (tile == self.player and tile in self.goals) 
                    else TBGL if tile in self.boxes and tile in self.goals
                    else TBOX if tile in self.boxes 
                    else TPLR if tile == self.player
                    else tile  # wall, empty floor, or empty goal
                for tile in row
                ]
            for row in self.tiles
            ]
        return '\n'.join([''.join(row) for row in tiles]) 
    
    def is_complete(self):
        """ true if each goal has a box, false otherwise """
        free = sum([0 if goal in self.boxes else 1 for goal in self.goals])
        return free == 0
    
    def reset(self):
        """ prepare mutable game state """
        self.tiles = deepcopy(self.base_tiles)
        self.goals = deepcopy(self.base_goals)
        self.player = deepcopy(self.base_player)
        self.boxes = deepcopy(self.base_boxes)
        
    def move(self, d):
        """ execute move in direction d if possible. 
        return true if player moved, false otherwise. 
        does not check for victory condition.
        """
        tiles = self.tiles
        dy, dx = DIRMAP[d]
        y, x = self.player
        src = tiles[y][x]
        d1y, d1x = y + dy, x + dx
        dest1 = tiles[d1y][d1x]  # walls around. Should be in bounds
        
        if tiles[d1y][d1x] == TWAL:  # wall: cant move 
            return False
        elif (d1y, d1x) in self.boxes:  # box: check if can push 
            d2y, d2x = y + 2 * dy, x + 2 * dx
            dest2 = tiles[d2y][d2x]  # beyond the box, should be in bounds
            if (d2y, d2x) in self.boxes or dest2 == TWAL:  # other box or wall
                return False
            else:  # can push box: move the box 
                tiles[d2y][d2x] = TBGL if dest2 == TGOL else TBOX 
                tiles[d1y][d1x] = TGOL if dest1 == TBGL else TFLR
                i = self.boxes.index((d1y, d1x))
                self.boxes[i] = (d2y, d2x)
                
        # whether pushing box or not, move player 
        tiles[y][x] = TGOL if src == TPGL else TFLR
        tiles[d1y][d1x] = TPGL if dest1 in (TGOL, TBGL) else TPLR
        self.player = d1y, d1x 
        return True
    

def find_element(e, l):
    """ return the positions of e in l as a list of 2-tuples
    l must be a list of sublists.
    e is an element potentially present in the sublists. 
    find_element(1, [[3,2,1],[4],[0,1]]) -> [ (0,2), (2,1) ]
    find_element(1, []) -> []
    find_element(1, [ [1,1], [1] ]) -> [ (0,0), (0,1), (1,0) ] 
    """
    return [(i, j) for i, ll in enumerate(l) for j, ee in enumerate(ll) if e == ee]


def flood_fill(tiles, pos, from_values, to_value):
    """ recursive flood fill https://en.wikipedia.org/wiki/Flood_fill
    tiles must be a rectangular list of lists, tiles[j][i] is row j column i. 
    pos is a position in tiles to start flooding from.
    from_values must be a list or set, not a single value.
    """
    y, x = pos
    if y < 0 or y >= len(tiles) or x < 0 or x >= len(tiles[0]):  
        return  # out of bounds
    if tiles[y][x] == to_value or tiles[y][x] not in from_values:
        return  # already filled
    tiles[y][x] = to_value
    flood_fill(tiles, (y, x + 1), from_values, to_value)
    flood_fill(tiles, (y, x - 1), from_values, to_value)
    flood_fill(tiles, (y - 1, x), from_values, to_value)
    flood_fill(tiles, (y + 1, x), from_values, to_value)


def build_level_from_tiles(tiles, maxs=16):
    """ tiles is a list of lists of characters. 
    maxs is max size of level output. 
    return a square Level if tiles are well-formed, None otherwise.
    Well-formed tiles means: 
    - widest row and tallest column are less than max size, 
    - enough room to support walls all around the periphery,
    - the number of boxes is at least the number of goals,
    - must have 1+ box, 1+ empty goal, and exactly 1 player,
    - each tile must be in the supported tileset '@.#*$ '
    """
    w = max(map(lambda x:len(x), tiles))
    h = len(tiles)
    if w > maxs or h > maxs:  # too wide or too tall
        print('Level is too wide or too tall: %d,%d' % (w, h))
        return None
    
    # check that all characters are supported 
    n_wrong = sum([0 if e in '@.#*$+ ' else 1 for row in tiles for e in row]) 
    if n_wrong >= 1:
        print('Level has %d tiles with unrecognized character(s)' % n_wrong)
        return None
    
    # add walls at the end of short rows
    tiles = [ line + [TWAL] * (w - len(line)) for line in tiles ]
    # widen map: add walls evenly on left and right sides to reach max width 
    for i, line in enumerate(tiles):
        left_hole = (maxs - len(line)) // 2
        right_hole = maxs - len(line) - left_hole 
        tiles[i] = [TWAL] * left_hole + tiles[i] + [TWAL] * right_hole
    # add rows of walls above and below, if necessary
    tiles = [[TWAL] * maxs] * ((maxs - h) // 2) + tiles
    tiles = tiles + [[TWAL] * maxs] * (maxs - len(tiles))  # remaining missing 
    
    # check that there are walls all around the periphery
    n_walls = sum([1 if e == TWAL else 0 for e in tiles[0]])
    n_walls += sum([1 if row[0] == TWAL else 0 for row in tiles[1:-1]])
    n_walls += sum([1 if row[-1] == TWAL else 0 for row in tiles[1:-1]])
    n_walls += sum([1 if e == TWAL else 0 for e in tiles[-1]])
    if n_walls != 4 * (maxs - 1):
        print('Level has %d peripheral walls, need %d' 
              % (n_walls, 4 * (maxs - 1)))
        print(tiles)
        return None
    
    # find player position, and check if missing or too many
    start = find_element('@', tiles) + find_element('+', tiles) 
    if len(start) != 1:
        print('Level has 0 or >1 player starting positions: %s' % str(start))
        print(tiles)
        return None    
    start = start[0]
    
    # find goal positions, and check at least one of them has no box on it
    goals = find_element('.', tiles) + find_element('+', tiles)
    if not goals:
        print('Level has all its goals fulfilled already')
        print(tiles)
        return None 
    goals = goals + find_element('*', tiles)  # add goals with boxes on them 
    
    # find boxes starting positions. Check 1+ box, and n_boxes >= n_goals.
    boxes = find_element('$', tiles) + find_element('*', tiles)
    if not boxes:
        print('Level has no box to move')
        print(tiles)
        return None
    if len(boxes) < len(goals):
        print('Level has fewer boxes than goals')
        print(tiles)
        return None
    
    # replace unreachable tiles by walls via flood filling algo
    reach = [ [0 if tile == TWAL else 1 for tile in row] for row in tiles ]
    flood_fill(reach, start, [1], 2)  # fill reachable 1s to 2s, 0s stay walls
    tiles = [ 
        [tile if reach[j][i] == 2 else TWAL for i, tile in enumerate(row)]
        for j, row in enumerate(tiles)
        ]
         
    return Level(tiles, goals, start, boxes)
    
    
def load_level_set(filepath, maxs=16):
    """ return list of levels, or None if cant load the file """
    if not os.path.isfile(filepath):
        print('could not find file %s' % filepath)
        return None
    
    with open(filepath, 'r') as f:
        levels = []
        level_tiles = [] 
        for line in list(f) + ['\n']:  # extra line break for last level
            if line and line[0] in TILESET:
                level_tiles.append(list(line.rstrip('\r\n')))
            else:  # empty or comment line
                if level_tiles:  # we have lines to build from
                    level = build_level_from_tiles(level_tiles, maxs)
                    if level:  # well-formed level
                        levels.append(level)
                    level_tiles = []
    
    return levels

################# TESTS ##################


def test_flood_fill():
    a = [ 
        [1, 1, 2],
        [1, 2, 1],
        [3, 1, 2]
        ]
    flood_fill(a, (0, 0), [1, 3], 2)
    r = [ 
        [2, 2, 2],
        [2, 2, 1],
        [2, 2, 2]
        ]
    assert a == r

    
def test_find_element():
    assert find_element(0, []) == []
    assert find_element(1, [[3,2,1],[4],[0,1]]) == [ (0,2), (2,1) ]
    assert find_element(1, [ [1,1], [1] ]) == [ (0,0), (0,1), (1,0) ] 
    
    
def test_build_level_from_tiles():
    """ test basic level building """
    tiles = list(map(lambda x:list(x), ['#####', '#+$ #', '#####']))
    level = build_level_from_tiles(tiles, 16)
    assert level is not None
    assert len(level.goals) == 1 
    assert level.goals[0] == (7, 6)
    assert level.player == (7, 6)
    assert len(level.boxes) == 1 
    assert level.boxes[0] == (7, 7)

    
def test_build_level_from_tiles2():
    """ In the level below, test that padding does not shift row 2 to the right.
    padding should add 4 walls top right and 2 walls bottom right.
    padding should also add 4 rows of walls at the top, 5 bot, 5 left, 5 right.
    """
    level_str = (
        "####\n"
        "# .#\n"
        "#  ###\n"
        "#*@  #\n"
        "#  $ #\n"
        "#  ###\n"
        "####\n"
        )
    tiles = list(map(lambda x:list(x), level_str.split(sep='\n')))
    level = build_level_from_tiles(tiles, 16)
    assert level
    assert level.tiles[4][9] == TWAL  # added wall just right of row 1 above
    assert level.tiles[10][10] == TWAL  # added wall 2 times right of row 7
    assert level.tiles[5][6] == TFLR  # row 2's empty floor
    assert level.tiles[5][7] == TGOL  # row 2's goal
    

def test_build_level_from_tiles3():
    """ Test that short lines dont shift right, and middle holes get filled. """
    level_str = (
        "###\n"
        "#.#\n"  
        "# # ###\n"   
        "#$###*#\n"
        "#     #\n"
        " ##@ ##\n"  
        "  ####\n"  
        )
    tiles = list(map(lambda x:list(x), level_str.split(sep='\n')))
    level = build_level_from_tiles(tiles, 16)
    assert level
    assert level.tiles[5][5] == TGOL  # short lines dont shift right
    assert level.tiles[6][7] == TWAL  # test that middle hole gets filled
    assert level.tiles[9][4] == TWAL  # before-last row's first hole gets filled 
    assert level.tiles[10][4] == TWAL  # last row's first 2 holes get filled 


def test_build_level_from_tiles4():
    level_str = (
        "  ####\n"
        "###  ####\n"
        "#     $ #\n"
        "# #  #$ #\n"
        "# . .#@ #\n"
        "#########\n"
        )
    tiles = list(map(lambda x:list(x), level_str.split(sep='\n')))
    level = build_level_from_tiles(tiles, 16)
    assert level
    
    
def test_load_level_set():
    """ create a levelset file, load set, test set, delete file """
    filename = 'levelset.txt.test'
    # create levelset file
    with open(filename, 'w') as f:
        level1 = '\n'.join(['#####', '#@$.#', '#####'])
        level2 = '\n'.join(['#####', '#+ $#', '#$.*#', '#####'])
        f.write('level 1\n' + level1 + '\r\n')
        f.write('level 2\n' + level2)
    # load and test set
    maxs = 16
    levels = load_level_set(filename, maxs)
    assert len(levels) == 2  # detected 2 well-formed levels
    assert levels[0] and len(levels[0].tiles) == maxs
    assert levels[1] and len(levels[1].tiles) == maxs
    # delete file
    try:
        os.remove(filename)
    except OSError:
        pass
    

def test_moves():
    """ build a level, make 4 moves, check game is over """ 
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
    level.move(DIRN)
    level.move(DIRE)
    level.move(DIRE)
    level.move(DIRE)
    level.move(DIRE)  # bump into wall
    level.move(DIRS)
    level.move(DIRS)  # bump into box blocked by wall
    level.move(DIRW)
    assert level.goals == level.boxes
    assert level.player == (3, 4)
    

if __name__ == "__main__":
    test_find_element()
    test_flood_fill()
    test_build_level_from_tiles()
    test_build_level_from_tiles2()
    test_build_level_from_tiles3()
    test_build_level_from_tiles4()
    test_load_level_set()
    
    test_moves()
#     levels = load_level_set('../assets/levels_test.txt', 8)
    
