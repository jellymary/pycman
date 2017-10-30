#!/usr/bin/env python3
"""Модуль тестов для логики игры"""

import unittest

import game
import objects as obj


class TestLogic(unittest.TestCase):

    def initGame(self):
        game = game.Game('test_board.txt')
        game.player.location = obj.Cell(3, 2)
        for name, ghost in game.ghosts:
            if name == 'blinky':
                self.assertEqual(ghost.location, obj.Cell(8, 1))
            elif name == 'pinky':
                self.asserEqual(ghost.location, obj.Cell(5, 3))
            elif name == 'inky':
                self.assertEqual(ghost.location, obj.Cell(4, 6))
            elif name == 'clyde':
                self.assertEqual(ghost.location, obj.Cell(4, 2))
        self.assertEqual(game.map[2, 7], obj.CellState.ENERDGIZER)
        self.assertEqual(game.map[5, 3], obj.CellState.CHERRY)
        self.assertEqual(game.map[0, 0], obj.CellState.WALL)
        self.assertEqual(game.map[1, 1], obj.CellState.EMPTY)
        self.assertEqual(game.map[3, 2], obj.CellState.POINT)



if __name__ == '__main__':
    unittest.main()
