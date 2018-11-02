
# sokobalt

![screenshot](assets/screenshot.png "screenshot")

A kind of Sokoban, a 1981 puzzle game where the player pushes crates in a warehouse

Similar projects 
- [solver in java](https://github.com/jameshong92/sokoban-solver)
- [game in python](http://inventwithpython.com/blog/2011/06/13/new-game-source-code-star-pusher-sokoban-clone/)



# Levels

[Level format](http://sokobano.de/wiki/index.php?title=Level_format)

|symbol|description|
|---|---|
| @ | player starting position |
| $ | box starting position |
| . | goal position |
| + | a goal where the player starts. Can't have @ and + in the same level |
| * | a goal where a box also starts |
| # | wall |
| (space) | empty |

Lines starting with any other character are comments should be ignored.
Levels are separated by at least one empty line or comment. 

Levels:
- [sneezing tiger](http://sneezingtiger.com/sokoban/levels.html)
- [sourcecode.se](http://www.sourcecode.se/sokoban/levels)


# TODO
- ESC to pull menu
- R to reset level
- move history, can undo
- navigate between levels
- store unlocked levels in a local save pickle
- level solver
- use bg and DirtySprite instead of redrawing every tick
