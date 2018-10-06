import os

SIZE = 16  # max map width and height
TWAL, TFLR, TGOL = '#', ' ', '.'
TPLR, TBOX, TPGL, TBGL = '@', '$', '+', '*'
TILESET = set([TWAL, TFLR, TGOL, TPLR, TBOX, TPGL, TBGL])


class Level:
    """ A Level is a 16x16 map, a player starting position, 
    a list of goal positions, and a list of starting box positions. 
    """
    
    def __init__(self, tiles, goals, player, boxes):
        """ tiles is list of lists, with all possible tiles eg TWAL and TPGL. 
        positions are 2-tuples. 
        goals and boxes are lists of 2-tuples, player a 2-tuple.
        """
        self.tiles = tiles  #  original tiles from level file, used to reset
        self.goals = goals
        self.player = player
        self.boxes = boxes
            
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
        

def find_element(e, l):
    """ return the positions of e in l as a list of 2-tuples 
    find_element(1, [[3,2,1],[4],[0,1]]) -> [ (0,2), (2,1) ]
    find_element(1, []) -> []
    """
    return [ (i, ll.index(e)) for i, ll in enumerate(l) if e in ll ]


def flood_fill(tiles, pos, from_values, to_value):
    """ recursive flood fill https://en.wikipedia.org/wiki/Flood_fill
    tiles is a square list of lists, tiles[j][i] is row j column i. 
    pos is a position in tiles to start flooding from.
    from_values must be a list or set, not a single value.
    """
    x, y = pos
    if y < 0 or y >= len(tiles) or x < 0 or x >= len(tiles[0]):  
        return  # out of bounds
    if tiles[y][x] == to_value or tiles[y][x] not in from_values:
        return  # already filled
    tiles[y][x] = to_value
    flood_fill(tiles, (x + 1, y), from_values, to_value)
    flood_fill(tiles, (x - 1, y), from_values, to_value)
    flood_fill(tiles, (x, y - 1), from_values, to_value)
    flood_fill(tiles, (x, y + 1), from_values, to_value)

    
def build_level_from_tiles(tiles):
    """ tiles is a list of lists of characters. 
    return a Level if tiles are well-formed, None otherwise.
    Well-formed tiles means: 
    - max width and height of 16, supporting walls all around the periphery,
    - the number of boxes is at least the number of goals,
    - must have 1+ box, 1+ empty goal, and exactly 1 player,
    - each tile must be in the supported tileset '@.#*$ '
    """
    w = max(map(lambda x:len(x), tiles))
    h = len(tiles)
    if w > SIZE or h > SIZE:  # too wide or too tall
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
        left_hole = (SIZE - len(line)) // 2
        right_hole = SIZE - len(line) - left_hole 
        tiles[i] = [TWAL] * left_hole + tiles[i] + [TWAL] * right_hole
    # add rows of walls above and below, if necessary
    tiles = [[TWAL] * SIZE] * ((SIZE - h) // 2) + tiles
    tiles = tiles + [[TWAL] * SIZE] * (SIZE - len(tiles))  # remaining missing 
    
    # check that there are walls all around the periphery
    n_walls = sum([1 if e == TWAL else 0 for e in tiles[0]])
    n_walls += sum([1 if row[0] == TWAL else 0 for row in tiles[1:-1]])
    n_walls += sum([1 if row[-1] == TWAL else 0 for row in tiles[1:-1]])
    n_walls += sum([1 if e == TWAL else 0 for e in tiles[-1]])
    if n_walls != 4 * (SIZE - 1):
        print('Level has %d peripheral walls, need %d' 
              % (n_walls, 4 * (SIZE - 1)))
        return None
    
    # find player position, and check if missing or too many
    start = find_element('@', tiles) + find_element('+', tiles) 
    if len(start) != 1:
        print('Level has 0 or >1 player starting positions: %s' % str(start))
        return None    
    start = start[0]
    
    # find goal positions, and check at least one of them has no box on it
    goals = find_element('.', tiles) + find_element('+', tiles)
    if not goals:
        print('Level has all its goals fulfilled already')
        return None 
    goals = goals + find_element('*', tiles)  # add goals with boxes on them 
    
    # find boxes starting positions. Check 1+ box, and n_boxes >= n_goals.
    boxes = find_element('$', tiles) + find_element('*', tiles)
    if not boxes:
        print('Level has no box to move')
        return None
    if len(boxes) < len(goals):
        print('Level has fewer boxes than goals')
        return None
    
    # replace unreachable tiles by walls via flood filling algo
    reach = [ [0 if tile == TWAL else 1 for tile in row] for row in tiles ]
    flood_fill(reach, start, [1], 2)  # fill reachable 1s to 2s, 0s stay walls
    tiles = [ 
        [tile if reach[j][i] == 2 else TWAL for i, tile in enumerate(row)]
        for j, row in enumerate(tiles)
        ]
         
    return Level(tiles, goals, start, boxes)
    
    
def load_level_set(filepath):
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
                    level = build_level_from_tiles(level_tiles)
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
    assert a[0][0] == 2
    assert a[2][0] == 2
    assert a[2][1] == 2
    assert a[1][2] == 1  # enclaved 1, should stay 

    
def test_find_element():
    r = find_element(1, [[3, 2, 1], [4], [0, 1]])
    assert len(r) == 2 and r[0] == (0, 2) and r[1] == (2, 1)
    assert find_element(0, []) == []
    

def test_build_level_from_tiles():
    """ test basic level building """
    tiles = list(map(lambda x:list(x), ['#####', '#+$ #', '#####']))
    level = build_level_from_tiles(tiles)
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
    level = build_level_from_tiles(tiles)
    assert level
    assert level.tiles[4][9] == TWAL  # added wall just right of row 1 above
    assert level.tiles[10][10] == TWAL  # added wall 2 times right of row 7
    assert level.tiles[5][6] == TFLR  # row 2's empty floor
    assert level.tiles[5][7] == TGOL  # row 2's goal
    

def test_build_level_from_tiles3():
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
    level = build_level_from_tiles(tiles)
    assert level
    assert level.tiles[5][5] == TGOL  # short lines dont shift right
    assert level.tiles[6][7] == TWAL  # test that middle hole gets filled
    assert level.tiles[9][4] == TWAL  # before-last row's first hole gets filled 
    assert level.tiles[10][4] == TWAL  # last row's first 2 holes get filled 


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
    levels = load_level_set(filename)
    assert len(levels) == 2  # detected 2 well-formed levels
    assert levels[0] and len(levels[0].tiles) == SIZE
    assert levels[1] and len(levels[1].tiles) == SIZE
    # delete file
    try:
        os.remove(filename)
    except OSError:
        pass
    
    
if __name__ == "__main__":
    test_find_element()
    test_flood_fill()
    test_build_level_from_tiles()
    test_build_level_from_tiles2()
    test_build_level_from_tiles3()
    test_load_level_set()
    load_level_set('../assets/levels_test.txt')
