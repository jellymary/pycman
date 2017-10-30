#!/usr/bin/env python3
"""Модуль тестов для объектов игры"""

import unittest

# from .. import objects as obj
# from ... import objects
# from ..objects import *
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

    def testNegCell(self):
        self.assertEqual(-obj.Cell(2, 4), obj.Cell(-2, -4))

    def testСyclingCell(self):
        self.assertEqual(obj.Cell(2, 5).cycling((10, 10)), obj.Cell(2, 5))
        self.assertEqual(obj.Cell(7, 12).cycling((5, 5)), obj.Cell(2, 2))


class TestMap(unittest.TestCase):

    def testInitMap(self):
        map = obj.Map()
        self.assertEqual(map._widht, 0)
        self.assertEqual(map.height, 0)

    # def testMapObjects(self):
    #     map = obj.Map()
    #     map.objects = [
    #         [1, 2, 3],
    #         [4, 5, 6]
    #     ]
    #     self.assertEqual(map[0, 1], 2)
    #     self.assertEqual(map._widht(), 3)
    #     self.assertEqual(map.height(), 2)


class TestEntity(unittest.TestCase):

    def testInitEntity(self):
        entity = obj.Entity(obj.Cell(1, 5), obj.Direction.UP)
        self.assertEqual(entity.location, obj.Cell(1, 5))
        self.assertEqual(entity.direction, obj.Direction.UP)


class TestGhost(unittest.TestCase):

    def testInitGhost(self):
        ghost = obj.Ghost(obj.Cell(7, 2), obj.Direction.RIGHT)
        self.assertEqual(ghost.location, obj.Cell(7, 2))
        self.assertEqual(ghost.direction, obj.Direction.RIGHT)
        self.assertEqual(ghost.state, obj.GhostState.CHASE)


class Queue(unittest.TestCase):

    def testQueue(self):
        queue1 = obj.Queue()
        queue2 = obj.Queue(1, 2, 3)
        self.initQueue(queue1, queue2)
        self.emptyQueue(queue1, queue2)
        self.enqueueQueue(queue1, queue2)
        self.dequeueQueue(queue1, queue2)
        self.peekQueue(queue1, queue2)

    def initQueue(self, queue1, queue2):
        self.assertTrue(len(queue1) == 0)
        self.assertEqual(queue2, [1, 2, 3])

    def emptyQueue(self, queue1, queue2):
        self.assertTrue(queue1.empty())
        self.assertFalse(queue2.empty())

    def enqueueQueue(self, queue1, queue2):
        self.assertEqual(queue1.enqueue(5), [5])
        self.assertEqual(queue2.enqueue(5), [1, 2, 3, 5])

    def dequeueQueue(self, queue1, queue2):
        self.assertEqual(queue1.dequeue(), 5)
        self.assertTrue(queue1.empty())
        self.assertEqual(queue2.dequeue(), 1)
        self.assertEqual(queue2, [2, 3, 5])

    def peekQueue(self, queue1, queue2):
        queue1.enqueue(8)
        self.assertEqual(queue1.peek(), 8)
        self.assertFalse(queue1.empty())
        self.assertEqual(queue2.peek(), 2)
        self.assertFalse(queue2.empty())


if __name__ == '__main__':
    unittest.main()
