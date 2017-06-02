#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Графическая версия игры «Pacman»"""

import sys
import os
import math

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QFrame, QGridLayout, QLabel, QInputDialog
from PyQt5.QtGui import QPainter, QColor, QImage, QIcon
from PyQt5.QtCore import Qt, QTimer, QRect

from modules import game
from modules.game import TickResult
from modules import objects as obj


class PacmanGame(QWidget):

    LEVEL_NAMES = ['1.txt', '2.txt']
    DELAY = 10
    PACMAN_DELAY = 7
    GHOST_DELAY = 9

    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)
        self.timer = QTimer()
        self.timer.start(PacmanGame.DELAY)
        self.timer.timeout.connect(self.update)
        self.board = None
        self.levelIndex = 0
        self.globalScores = 0
        self.loadLevel()
        self.initWindow()

    def initWindow(self):
        self.resize(Board.CELL_WIDTH * self.gameLevel.map.width,
            Board.CELL_HEIGHT * self.gameLevel.map.height + 50)
        self.moveToCenter()
        self.setWindowTitle('Pacman')
        self.setWindowIcon(QIcon(os.path.join('images', 'pacman.png')))
        self.show()

    def moveToCenter(self):
        screen = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        self.move((screen.width() - widget.width()) / 2,
            (screen.height() - widget.height()) / 2)

    def loadLevel(self):
        name = os.path.join('levels', self.LEVEL_NAMES[self.levelIndex])
        self.gameLevel = game.Game(name)
        if not self.board:
            self.board = Board(self)
        self.board.level = self.gameLevel
        self.playerTimeCount = 0
        self.ghostTimeCount = 0

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
            print(self.gameLevel.scores)
            self.playerTimeCount = 0
        if self.ghostTimeCount == PacmanGame.GHOST_DELAY:
            self.gameLevel.ghostsMakeStep()
            self.ghostTimeCount = 0
        result = self.gameLevel.getTickResult()
        self._processTickResult(result)
        self.board.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = (event.x() - self.board.frameRect().left()) // Board.CELL_WIDTH
            y = (event.y() - self.board.frameRect().top()) // Board.CELL_HEIGHT
            self.gameLevel.makeTeleportation(x, y)
        self.board.update()

    def _processTickResult(self, result):
        if result == TickResult.LEVEL_FAILED:
            if self.levelIndex == 0:
                self.globalScores += self.gameLevel.scores
                self.timer.stop()
                self.ExitDialog()
                self.close()
            else:
                self.levelIndex -= 1
                self.loadLevel()
        elif result == TickResult.LEVEL_COMPLETED:
            self.globalScores += self.gameLevel.scores
            self.levelIndex += 1
            if self.levelIndex >= len(self.LEVEL_NAMES):
                self.close()
            else:
                self.loadLevel()
        elif result == TickResult.PACMAN_DIED:
            self._displayFailMessage()

    def _displayFailMessage(self):
        print('RIP! YOU HAVE ONLY %d LIFES' % self.gameLevel.lifes)

    def ExitDialog(self):
        dialog = QInputDialog()
        name, ok = dialog.getText(self, 'Сохранение результата', 'Введите своё имя:')
        if (ok and len(name) != 0):
            self.gameLevel.saveResult(name, self.globalScores)
        os.startfile(r'C:\Users\maryk\OneDrive\Python\task\Pacman2\modules\scores.txt')


class Board(QFrame):

    CELL_WIDTH = 25
    CELL_HEIGHT = 25

    CELL_COLORS = {
        obj.CellState.EMPTY: QColor(230, 230, 230),
        obj.CellState.WALL: QColor(47, 79, 79),
        obj.CellState.POINT: QColor(250, 200, 255),
        obj.CellState.CHERRY: QColor(220, 20, 60),
        obj.CellState.ENERGIZER: QColor(139, 0, 0)
    }

    ENTITIES = {
        'player': lambda self, painter, x, y: self.drawPacman(painter, x, y),
        'blinky': lambda self, painter, x, y: self.drawGhost(painter, x, y,
            QImage(Board.BLINKY_IMAGE)),
        'pinky': lambda self, painter, x, y: self.drawGhost(painter, x, y,
            QImage(Board.PINKY_IMAGE)),
        'inky': lambda self, painter, x, y: self.drawGhost(painter, x, y,
            QImage(Board.INKY_IMAGE)),
        'clyde': lambda self, painter, x, y: self.drawGhost(painter, x, y,
            QImage(Board.CLYDE_IMAGE))
    }

    PACMAN_HOLE_SIZE = 90 * 16
    ANIMATION_DELAY = 30
    BLINKY_IMAGE = os.path.join('images', 'ghost1.png')
    PINKY_IMAGE = os.path.join('images', 'ghost2.png')
    INKY_IMAGE = os.path.join('images', 'ghost3.png')
    CLYDE_IMAGE = os.path.join('images', 'ghost4.png')

    def __init__(self, parent):
        super().__init__(parent)
        self.level = parent.gameLevel
        self.animationCounter = Board.ANIMATION_DELAY
        self.resize(self.level.map.width * Board.CELL_WIDTH,
            self.level.map.height * Board.CELL_HEIGHT)
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
                self.drawCell(painter, x * Board.CELL_WIDTH,
                    y * Board.CELL_HEIGHT, fieldObject)

    def drawCell(self, painter, x, y, cell):
        col = QColor(212, 212, 212)
        painter.setPen(col)
        rectangle = self.contentsRect()
        if cell in obj.CellState:
            color = Board.CELL_COLORS[cell]
            painter.setBrush(color)
            painter.drawRect(rectangle.left() + x, y,
                Board.CELL_WIDTH, rectangle.top() + Board.CELL_HEIGHT)
        else:
            color = Board.ENTITIES[cell](self, painter, rectangle.left() + x, y)

    def drawPacman(self, painter, x, y):
        pacmanColor = QColor(255, 215, 0)
        ellipseData = (x + 2, y + 2, Board.CELL_WIDTH - 4, Board.CELL_HEIGHT - 4)
        backColor = Board.CELL_COLORS[obj.CellState.EMPTY]
        painter.setPen(backColor)
        painter.setBrush(pacmanColor)
        direction = self.level.player.direction.value
        angle = math.atan2(-direction.Y, direction.X) * 180 / math.pi * 16
        self.animationCounter = (self.animationCounter - 1) % Board.ANIMATION_DELAY
        holeSize = Board.PACMAN_HOLE_SIZE * abs(self.animationCounter -
            Board.ANIMATION_DELAY / 2) * 2 / Board.ANIMATION_DELAY
        painter.drawEllipse(*ellipseData)
        painter.setBrush(backColor)
        painter.drawPie(*ellipseData, angle - holeSize / 2, holeSize)
        painter.setPen(pacmanColor)
        painter.drawArc(*ellipseData, angle + holeSize / 2, 360 * 16 - holeSize - 16)

    def drawGhost(self, painter, x, y, image):
        painter.drawImage(QRect(x, y, Board.CELL_WIDTH, Board.CELL_HEIGHT), image)


if __name__ == '__main__':
    app = QApplication([])
    pacman = PacmanGame()
    sys.exit(app.exec_())
