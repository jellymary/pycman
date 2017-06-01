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

    def testNegCell(self):
        self.assertEqual(-obj.Cell(2, 4), obj.Cell(-2, -4))


class TestMap(unittest.TestCase):

    def testInitMap(self):
        map = obj.Map()
        self.assertEqual(map.width, 0)
        self.assertEqual(map.height, 0)

    def testMapObjects(self):
        pass


class TestCharacter(unittest.TestCase):

    pass


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
