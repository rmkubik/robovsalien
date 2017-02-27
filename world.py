# -*- coding: utf-8 -*-
import random
import sys

def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + (y1 - y2)

class Entity:
    def __init__(self, _row, _col, _team):
        self.row = _row
        self.col = _col
        self.team = _team

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __str__(self):
        return self.team.encode('utf-8') + "[" + str(self.row) + ", " + str(self.col) + "]"

    def move(self, world, newMap, enemies, allies):
        moveRow = self.row + random.randint(-1, 1)
        moveCol = self.col + random.randint(-1, 1)

        if (moveRow < 0):
            moveRow = 0
        if (moveRow >= world["height"]):
            moveRow = world["height"] - 1
        if (moveCol < 0):
            moveCol = 0
        if (moveCol >= world["width"]):
            moveCol = world["width"] - 1

        if newMap[moveRow][moveCol] == Tiles.Empty \
        or newMap[moveRow][moveCol] == Tiles.Burned:
            newMap[self.row][self.col] = Tiles.Empty
            newMap[moveRow][moveCol] = self.team
            self.row = moveRow
            self.col = moveCol

        elif newMap[moveRow][moveCol] == Tiles.Explosion:
            newMap[self.row][self.col] = Tiles.Empty
            allies.remove(self)

    def attack(self, world, newMap, enemies, allies):
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

            for enemy in enemies:
                if atkRow == enemy.row and atkCol == enemy.col:
                    enemies.remove(enemy)

            for ally in allies:
                if atkRow == ally.row and atkCol == ally.col:
                    allies.remove(ally)

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
