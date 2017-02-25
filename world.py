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
        return self.row == other.row & self.col == other.col

    def move(self, world, newMap, enemies, allies):
        target = None
        targetDist = sys.maxint
        for enemy in enemies:
            if distance(self.row, self.col, enemy.row, enemy.col) < targetDist:
                targetDist = distance(self.row, self.col, enemy.row, enemy.col)
                target = enemy
        if target != None:
            rowDiff = self.row - target.row
            colDiff = self.col - target.col
            if abs(rowDiff) >= abs(colDiff):
                if rowDiff > 0:
                    if world["map"][self.row - 1][self.col] == Tiles.Empty \
                    or world["map"][self.row - 1][self.col] == Tiles.Burned:
                        newMap[self.row][self.col] = Tiles.Empty
                        newMap[self.row - 1][self.col] = self.team
                        self.row -= 1
                    elif world["map"][self.row - 1][self.col] == Tiles.Explosion:
                        newMap[self.row][self.col] = Tiles.Empty
                        allies.remove(self)
                elif rowDiff < 0:
                    if world["map"][self.row + 1][self.col] == Tiles.Empty \
                    or world["map"][self.row + 1][self.col] == Tiles.Burned:
                        newMap[self.row][self.col] = Tiles.Empty
                        newMap[self.row + 1][self.col] = self.team
                        self.row += 1
                    elif world["map"][self.row + 1][self.col] == Tiles.Explosion:
                        newMap[self.row][self.col] = Tiles.Empty
                        allies.remove(self)
            else:
                if colDiff > 0:
                    if world["map"][self.row][self.col - 1] == Tiles.Empty \
                    or world["map"][self.row][self.col - 1] == Tiles.Burned:
                        newMap[self.row][self.col] = Tiles.Empty
                        newMap[self.row][self.col - 1] = self.team
                        self.col -= 1
                    elif world["map"][self.row][self.col - 1] == Tiles.Explosion:
                        newMap[self.row][self.col] = Tiles.Empty
                elif colDiff < 0:
                    if world["map"][self.row][self.col + 1] == Tiles.Empty \
                    or world["map"][self.row][self.col + 1] == Tiles.Burned:
                        newMap[self.row][self.col] = Tiles.Empty
                        newMap[self.row][self.col + 1] = self.team
                        self.col += 1
                    elif world["map"][self.row][self.col + 1] == Tiles.Explosion:
                        newMap[self.row][self.col] = Tiles.Empty
            if self in allies:
                allies[allies.index(self)].row = self.row
                allies[allies.index(self)].col = self.col

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
