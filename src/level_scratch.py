import os

SIZE = 16  # max map width and height
TWAL = '#'
charset = set(['@', '$', '.', '+', '*', TWAL])


class Level:
    """ A Level is a 16x16 map, a player starting position, 
    a list of goal positions, and a list of starting box positions. 
    """

    def __init__(self, tiles, goals, start, boxes):
        """ tiles is list of lists, goals list of 2-tuples, """
        self.tiles = tiles
        self.goals = goals
        self.start = start
        self.boxes = boxes
        

def find_element(e, l):
    """ return the positions of e in l as a list of 2-tuples 
    find_element(1, [[3,2,1],[4],[0,1]]) -> [ (0,2), (2,1) ]
    find_element(1, []) -> []
    """
    return [ (i, ll.index(e)) for i, ll in enumerate(l) if e in ll ]


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
     
    # add walls at the beginning and end of short rows
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
    
    # find player start position, and check if missing or too many
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
            if line and line[0] in charset:  # map line
                level_tiles.append(list(line.rstrip('\r\n')))
            else:  # empty or comment line
                if level_tiles:  # we have lines to build from
                    level = build_level_from_tiles(level_tiles)
                    if level:  # well-formed level
                        levels.append(level)
                level_tiles = []
    
    return levels

################# TESTS ##################


def test_find_element():
    r = find_element(1, [[3, 2, 1], [4], [0, 1]])
    assert len(r) == 2 and r[0] == (0, 2) and r[1] == (2, 1)
    assert find_element(0, []) == []
    

def test_build_level_from_tiles():
    tiles = list(map(lambda x:list(x), ['#####', '#@$.#', '#####']))
    level = build_level_from_tiles(tiles)
    assert level is not None
    assert len(level.goals) == 1 and level.goals[0] == (7, 8)
    assert level.start == (7, 6)
    assert len(level.boxes) == 1 and level.boxes[0] == (7, 7)


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
    test_build_level_from_tiles()
    test_load_level_set()
    load_level_set('../assets/levels_test.txt')
