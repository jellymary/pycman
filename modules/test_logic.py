#!/usr/bin/env python3
"""Модуль тестов для логики игры"""

import unittest

import objects as obj


class TestLogic(unittest.TestCase):

    def initGame(self):
        self.assertTrue(obj.Cell(1, 0) == obj.Cell(1, 0))


if __name__ == '__main__':
    unittest.main()
