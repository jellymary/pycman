#!/usr/bin/env python3
"""Графическая версия игры «Pacman»"""

import sys

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QFrame, QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer

from modules import game
from modules.game import TickResult
from modules import objects as obj


class PacmanGame(QWidget):

    LEVEL_NAMES = ['1.txt', '2.txt']
    DELAY = 10
    PACMAN_DELAY = 7
    GHOST_DELAY = 9
    SCORES = 0

    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)
        self.timer = QTimer()
        self.timer.start(PacmanGame.DELAY)
        self.timer.timeout.connect(self.update)
        self.board = None
        self.levelIndex = 0
        self.loadLevel()
        self.initWindow()

    def loadLevel(self):
        name = self.LEVEL_NAMES[self.levelIndex]
        self.gameLevel = game.Game(name)
        if not self.board:
            self.board = Board(self)
        self.board.level = self.gameLevel
        self.playerTimeCount = 0
        self.ghostTimeCount = 0
        PacmanGame.SCORES += self.gameLevel.scores

    def initWindow(self):
        self.resize(Board.CELL_WIDTH * self.gameLevel.map.width, 600)
        self.moveToCenter()
        self.setWindowTitle('Pacman')
        self.show()

    def moveToCenter(self):
        screen = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        self.move((screen.width() - widget.width()) / 2,
            (screen.height() - widget.height()) / 2)

    def keyPressEvent(self, event):
        self.key_events = {
            Qt.Key_Escape: self.close,
            Qt.Key_W: lambda: self.gameLevel.actionQueue.enqueue(obj.Direction.UP),
            Qt.Key_A: lambda: self.gameLevel.actionQueue.enqueue(obj.Direction.LEFT),
            Qt.Key_S: lambda: self.gameLevel.actionQueue.enqueue(obj.Direction.DOWN),
            Qt.Key_D: lambda: self.gameLevel.actionQueue.enqueue(obj.Direction.RIGHT)
            }

        if event.key() in self.key_events:
            self.key_events[event.key()]()

    def update(self):
        self.playerTimeCount += 1
        self.ghostTimeCount += 1
        if self.playerTimeCount == PacmanGame.PACMAN_DELAY:
            self.gameLevel.playerMakeStep()
            self.playerTimeCount = 0
        if self.ghostTimeCount == PacmanGame.GHOST_DELAY:
            self.gameLevel.ghostsMakeStep()
            self.ghostTimeCount = 0
        self.board.update()
        result = self.gameLevel.getTickResult()
        self._processTickResult(result)

    def mousePressEvent(self, event):
        rect = self.getRectangle(event.x() - self.board.frameRect().left(),
            event.y() - self.board.frameRect().top())
        if self.gameLevel.TELEPORTATION_COUNT > 0 and event.button() == Qt.LeftButton and rect:
            self.gameLevel.TELEPORTATION_COUNT -= 1
            self.gameLevel.player.location = rect
            self.board.update()

    def getRectangle(self, x, y):
        rect = obj.Cell(x // Board.CELL_WIDTH, y // Board.CELL_HEIGHT)
        if rect.X < 0 or rect.X > self.gameLevel.map.width - 1 or \
        rect.Y < 0 or rect.Y > self.gameLevel.map.height - 1 or \
        self.gameLevel.map[rect.X, rect.Y] == obj.CellState.WALL:
            return None
        return rect

    def _processTickResult(self, result):
        if result == TickResult.LEVEL_FAILED:
            if self.levelIndex == 0:
                self.close()
            else:
                self.levelIndex -= 1
                self.loadLevel()
        elif result == TickResult.LEVEL_COMPLETED:
            self.levelIndex += 1
            if self.levelIndex >= len(self.LEVEL_NAMES):
                self.close()
            else:
                self.loadLevel()
        elif result == TickResult.PACMAN_DIED:
            self._displayFailMessage()

    def _displayFailMessage(self):
        print('RIP! YOU HAVE ONLY %d LIFES' % self.gameLevel.lifes)


class Board(QFrame):

    CELL_WIDTH = 25
    CELL_HEIGHT = 25

    def __init__(self, parent):
        super().__init__(parent)
        self.level = parent.gameLevel
        self.resize(self.level.map.width * Board.CELL_WIDTH, self.level.map.height * Board.CELL_HEIGHT)
        # self.moveCenter()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawBoard(painter)
        self.drawCell(painter, self.level.player.location.X * Board.CELL_WIDTH,
                       self.level.player.location.Y * Board.CELL_HEIGHT, 'player')
        for name, ghost in self.level.ghosts.items():
            self.drawCell(painter, ghost.location.X * Board.CELL_WIDTH,
                ghost.location.Y * Board.CELL_HEIGHT, name)

    def drawBoard(self, painter):
        for y in range(self.level.map.height):
            for x in range(self.level.map.width):
                fieldObject = self.level.map[x, y]
                if fieldObject != obj.CellState.EMPTY:
                    self.drawCell(painter, x * Board.CELL_WIDTH, y* Board.CELL_HEIGHT, fieldObject)

    def drawCell(self, painter, x, y, cell):
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        painter.setPen(col)
        colorTable = {
            obj.CellState.EMPTY: QColor(211, 250, 211),
            obj.CellState.WALL: QColor(47, 79, 79),
            obj.CellState.POINT: QColor(255, 200, 250),
            obj.CellState.CHERRY: QColor(220, 20, 60),
            obj.CellState.ENERGIZER: QColor(139, 0, 0),
            'player': QColor(255, 215, 0),
            'blinky': QColor(255, 0, 0),
            'pinky': QColor(255, 20, 147),
            'inky': QColor(51, 51, 255),
            'clyde': QColor(255, 153, 0)
        }
        rectangle = self.contentsRect()
        color = colorTable[cell]
        painter.setBrush(color)
        painter.drawRect(rectangle.left() + x, y, Board.CELL_WIDTH, rectangle.top() + Board.CELL_HEIGHT)


if __name__ == '__main__':
    app = QApplication([])
    pacman = PacmanGame()
    sys.exit(app.exec_())
