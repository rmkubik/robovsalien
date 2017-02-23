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

    def attack(self):
        print "attack"
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
