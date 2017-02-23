class Entity:
    def __init__(self, _row, _col, _team):
        row = _row
        col = _col
        team = _team
        self.row = _row
        self.col = _col
        self.team = _team

    def __eq__(self, other):
        return self.row == other.row & self.col == other.col

    def move(self):
        print "move"
    def attack(self, world, newMap, enemies):
        target = None
        targetDist = sys.maxint
        for enemy in enemies:
            if distance(self.row, self.col, enemy.row, enemy.col) < targetDist:
                targetDist = distance(self.row, self.col, enemy.row, enemy.col)
                target = enemy
        if target != None:
            atkRow = target.row + random.randint(-1, 1)
            atkCol = target.col + random.randint(-1, 1)

            if (atkRow < 0):
                atkRow = 0
            if (atkRow >= world["height"]):
                atkRow = world["height"] - 1
            if (atkCol < 0):
                atkCol = 0
            if (atkCol >= world["width"]):
                atkCol = world["width"] - 1

            if atkRow == target.row & atkCol == target.col:
                enemies.remove(target)

            newMap[atkRow][atkCol] = Tiles.Explosion


class Tiles:
    Explosion = u'\U0001F4A5'
    Fire = u'\U0001F525'
    Tree_Pine = u'\U0001F332'
    Tree_Oak = u'\U0001F333'
    Tree_Holiday = u'\U0001F384'
    Empty = u'\u25AB'u'\uFE0F'
    Burned = u'\u25AA'u'\uFE0F'
    Robot = u'\U0001F916'
    Alien = u'\U0001F47D'
