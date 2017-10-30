"""Модуль реализует логику игры «Pacman»"""

from os import path
from copy import deepcopy
from math import sqrt
from enum import Enum

from modules import objects as obj


class Game:
    """Класс уровня игры"""

    TELEPORTATION_COUNT = 3
    LIFE_COUNT = 3

    def __init__(self, filename):
        self.map = obj.Map()
        self.scores = 0
        self.lifes = Game.LIFE_COUNT
        self.teleportations = Game.TELEPORTATION_COUNT
        self.ghosts = {}
        self.actionQueue = obj.Queue()
        self._parse(filename)

    def _parse(self, filename):
        parserTable = {
            ' ': lambda x, y: self.map.objects[x].append(obj.CellState.EMPTY),
            '#': lambda x, y: self.map.objects[x].append(obj.CellState.WALL),
            '.': lambda x, y: self.map.objects[x].append(obj.CellState.POINT),
            '+': lambda x, y: self.map.objects[x].append(obj.CellState.CHERRY),
            '*': lambda x, y: self.map.objects[x].append(obj.CellState.ENERGIZER),
            'G': lambda x, y: self._setPlayerLocation(x, y),
            'B': lambda x, y: self._setGhostLocation(x, y, 'blinky'),
            'P': lambda x, y: self._setGhostLocation(x, y, 'pinky'),
            'I': lambda x, y: self._setGhostLocation(x, y, 'inky'),
            'C': lambda x, y: self._setGhostLocation(x, y, 'clyde'),
        }
        with open(filename, 'r', encoding='UTF-8') as file:
            for string in file:
                if self.map.width == 0:
                    self.map.width = len(string) - 1
                if self.map.objectsCount() == 0:
                    self.map.objects = [[] for i in range(self.map.width)]
                for x in range(self.map.width):
                    symbol = string[x]
                    if symbol in parserTable:
                        parserTable[symbol](x, self.map.height)
                    else:
                        raise SyntaxError("Found invalid symbol in file")
                self.map.height += 1

    def _setPlayerLocation(self, x, y):
        self._playerInitialLocation = obj.Cell(x, y)
        self.player = obj.Entity(obj.Cell(x, y), obj.Direction.LEFT)
        self.map.objects[x].append(obj.CellState.EMPTY)

    def _setGhostLocation(self, x, y, ghostName):
        # Game.GHOST_INITIAL_POSITION.append(obj.Cell(x, y))
        self.ghosts[ghostName] = obj.Ghost(obj.Cell(x, y), obj.Direction.LEFT)
        self.map.objects[x].append(obj.CellState.EMPTY)

    def playerMakeStep(self):
        if not self.actionQueue.empty() and \
        self._canMakeStep(self.actionQueue.peek()):
            self._makeStep(self.actionQueue.dequeue())
        else:
            if self._canMakeStep(self.player.direction):
                self._makeStep(self.player.direction)
            elif not self.actionQueue.empty():
                self.actionQueue.dequeue()

    def _canMakeStep(self, dir):
        location = (self.player.location +
            dir).cycling((self.map.width, self.map.height))
        cellState = self.map[location.X, location.Y]
        return cellState != obj.CellState.WALL

    def _makeStep(self, dir):
        location = (self.player.location +
            dir).cycling((self.map.width, self.map.height))
        cellState = self.map[location.X, location.Y]
        self.player.location = location
        self.player.direction = dir
        if cellState == obj.CellState.POINT:
            self.map[location.X, location.Y] = obj.CellState.EMPTY
            self.scores += 10

    def ghostsMakeStep(self):
        for ghostName in self.ghosts:
            newLocation = Strategy.getNextLocation(
                ghostName,
                self.ghosts,
                self.player,
                self.map
            )
            self.ghosts[ghostName].direction = newLocation - self.ghosts[ghostName].location
            self.ghosts[ghostName].location = newLocation

    def _isEndGame(self):
        for x in range(self.map.width):
            for y in range(self.map.height):
                if self.map[x, y] == obj.CellState.POINT or \
                self.map[x, y] == obj.CellState.ENERGIZER:
                    return False
        return True

    def _isPlayerDied(self):
        for ghost in self.ghosts.values():
            if self.player.location == ghost.location:
                return True
        return False

    def getTickResult(self):
        if self._isPlayerDied():
            self.lifes -= 1
            if self.lifes < 0:
                return TickResult.LEVEL_FAILED
            else:
                self.player.location = self._playerInitialLocation
                return TickResult.PACMAN_DIED
        elif self._isEndGame():
            return TickResult.LEVEL_COMPLETED
        return TickResult.CONTINUE

    def makeTeleportation(self, x, y):
        if 0 <= x < self.map.width and \
           0 <= y < self.map.height and \
           self.map[x, y] != obj.CellState.WALL and\
           self.teleportations > 0:
            self.player.location = obj.Cell(x, y)
            self.teleportations -= 1
            print('TELEPORTED! YOU HAVE ONLY %d TELEPORTATIONS' % self.teleportations)

    def saveResult(self, name, score):
        return Scoreboard.save(name, score)


class Scoreboard:

    SCOREBOARD_FILE = path.join('modules', 'scores.txt')

    def save(name, record):
        scores = []
        scores.append((name, record))
        with open(Scoreboard.SCOREBOARD_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                record = line.split()[1:]
                scores.append((record[0], int(record[1])))
        scores.sort(key=lambda x: -x[1])
        with open(Scoreboard.SCOREBOARD_FILE, 'w', encoding='utf-8') as file:
            index = 1
            for score in scores:
                file.write(str(index) + ' ' + score[0] + ' ' + str(score[1]) + '\n')
                index += 1
        return scores


class Strategy:

    def getNextLocation(name, ghosts, player, map):
        targetPositions = {
            'blinky': lambda: player.location,
            'pinky': lambda: Strategy._getPinkyTargetLocation(player),
            'inky': lambda: Strategy._getInkyTargetLocation(player,
                ghosts['blinky'].location),
            'clyde': lambda: Strategy._getClydeTargetLocation(ghost, player),
        }
        ghost = ghosts[name]
        target = targetPositions[name]()
        directions = [
            direction.value for direction in obj.Direction
                    if direction.value + ghost.direction != obj.Cell(0, 0) and \
                        Strategy._isNotWall(map, (ghost.location +
                            direction.value).cycling((map.width, map.height)))
        ]
        if len(directions) == 0:
            return ghost.location
        minDistanceDir = directions[0]
        minDistance = map.width + map.height
        for direction in directions:
            distance = Strategy._getDistance(ghost.location + direction, target)
            if distance < minDistance:
                minDistance = distance
                minDistanceDir = direction
        return (minDistanceDir + ghost.location).cycling((map.width, map.height))

    def _isNotWall(map, location):
        return map[location.X, location.Y] != obj.CellState.WALL

    def _getDistance(point1, point2):
        return sqrt(pow(point2.X - point1.X, 2) + pow(point2.Y - point1.Y, 2))

    def _getPinkyTargetLocation(player):
        target = player.location + player.direction.value * 4
        if player.direction == obj.Direction.UP:
            target += obj.Direction.LEFT.value * 4
        return target

    def _getInkyTargetLocation(player, blinkyLoc):
        middle = player.location + 2 * player.direction.value
        return 2 * middle - blinkyLoc

    def _getClydeTargetLocation(ghost, player):
        if Strategy._getDistance(ghost.location, player.location) < 9:
            return obj.Cell(0, 0)
        return player.location


class TickResult(Enum):

    CONTINUE = 0
    LEVEL_COMPLETED = 1
    PACMAN_DIED = 2
    LEVEL_FAILED = 3
