#!/usr/bin/env python3
"""Модуль тестов для объектов игры"""

import unittest

import objects as obj


class TestObjects(unittest.TestCase):

    def testEqualCell(self):
        self.assertTrue(obj.Cell(1, 0) == obj.Cell(1, 0))

    def testCellAdd(self):
        self.assertEqual(obj.Cell(5, -3) + obj.Cell(-7, 2), obj.Cell(-2, -1))
        self.assertEqual(obj.Cell(-2, 1) + obj.Direction.UP, obj.Cell(-2, 0))
        with self.assertRaises(TypeError):
            obj.Cell(1, 0) + 5

    def testInverseAdd(self):
        self.assertEqual(obj.Cell(1, -2) + obj.Cell(-3, 1), obj.Cell(-3, 1) + obj.Cell(1, -2))

    def testCellMul(self):
        with self.assertRaises(TypeError):
            obj.Cell(2, 3) * [1, 2, 3]
        self.assertTrue(obj.Cell(2, 3) * 5 == obj.Cell(10, 15))

    def testInverseMul(self):
        self.assertEqual(obj.Cell(4, -3) * 2, 2 * obj.Cell(4, -3))

    def testSubCell(self):
        self.assertEqual(obj.Cell(1, 2) - obj.Cell(2, 1), obj.Cell(-1, 1))

    def testCellToStr(self):
        self.assertEqual(str(obj.Cell(1, 2)), "Cell(1, 2)")

    def testCellSumAndMul(self):
        self.assertTrue(obj.Cell(3, -2) * 2 + obj.Cell(1, 4) == obj.Cell(7, 0))


if __name__ == '__main__':
    unittest.main()
