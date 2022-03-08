from library.doubly_linked_list import DoublyLinkedList
from random import random, randint, randrange
import unittest


class DoublyLinkedListTest(unittest.TestCase):
    def test_empty_init(self):
        test_dll = DoublyLinkedList([])
        self.assertEqual(len(test_dll), 0)
        self.assertSequenceEqual(test_dll, [])

    def test_collection_init(self):
        for size in range(20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_dll = DoublyLinkedList(test_list)
                self.assertEqual(len(test_list), len(test_dll))
                self.assertSequenceEqual(test_list, test_dll)

    def test_get_empty(self):
        test_dll = DoublyLinkedList([])
        with self.assertRaises(IndexError):
            v = test_dll[0]

    def test_set_empty(self):
        test_dll = DoublyLinkedList([])
        with self.assertRaises(IndexError):
            test_dll[0] = 10

    def test_del_empty(self):
        test_dll = DoublyLinkedList([])
        with self.assertRaises(IndexError):
            del test_dll[0]

    def test_append(self):
        for size in range(20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_dll = DoublyLinkedList([])
                for item in test_list:
                    test_dll.append(item)
                self.assertEqual(len(test_list), len(test_dll))
                self.assertSequenceEqual(test_list, test_dll)

    def test_insert(self):
        for size in range(20):
            for sample in range(50):
                test_list = []
                test_dll = DoublyLinkedList([])
                for s in range(size):
                    i = randint(-s, s)
                    v = random()
                    test_list.insert(i, v)
                    test_dll.insert(i, v)
                self.assertEqual(len(test_list), len(test_dll))
                self.assertSequenceEqual(test_list, test_dll)

    def test_get(self):
        for size in range(1,20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_dll = DoublyLinkedList(test_list)

                # test the out-of-bounds indices
                with self.assertRaises(IndexError):
                    v = test_dll[-(size + 1)]
                with self.assertRaises(IndexError):
                    v = test_dll[size]

                # test the inner indices
                for i in range(-size, size):
                    self.assertEqual(test_list[i], test_dll[i])

    def test_set(self):
        for size in range(1, 20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_dll = DoublyLinkedList(test_list)

                # test the out-of-bounds indices
                with self.assertRaises(IndexError):
                    test_dll[-(size + 1)] = random()
                with self.assertRaises(IndexError):
                    test_dll[size] = random()

                # test the inner indices
                for i in range(-size, size):
                    v = random()
                    test_list[i] = v
                    test_dll[i] = v
                    self.assertSequenceEqual(test_list, test_dll)

    def test_del(self):
        for size in range(1, 20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_dll = DoublyLinkedList(test_list)

                # test the out-of-bounds indices
                with self.assertRaises(IndexError):
                    del test_dll[-(size + 1)]
                with self.assertRaises(IndexError):
                    del test_dll[size]

                # test the inner indices
                for s in range(size, 0, -1):
                    i = randrange(-s, s)
                    del test_list[i]
                    del test_dll[i]
                    self.assertSequenceEqual(test_list, test_dll)

    def test_iter(self):
        for size in range(20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_dll = DoublyLinkedList(test_list)
                for i, v in enumerate(test_dll):
                    self.assertEqual(test_list[i], v)

    def test_index_empty(self):
        test_dll = DoublyLinkedList([])
        with self.assertRaises(ValueError):
            test_dll.index(random())

    def test_index(self):
        test_dll = DoublyLinkedList([1, 5, 5, 2, 7, 9])
        self.assertEqual(test_dll.index(1), 0)
        self.assertEqual(test_dll.index(5), 1)
        self.assertEqual(test_dll.index(5, start=2), 2)
        self.assertEqual(test_dll.index(9), 5)
        with self.assertRaises(ValueError):
            test_dll.index(20)
        with self.assertRaises(ValueError):
            test_dll.index(5, start=3)
        with self.assertRaises(ValueError):
            test_dll.index(9, stop=5)

    def test_clear(self):
        for size in range(20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_dll = DoublyLinkedList(test_list)
                test_list.clear()
                test_dll.clear()
                self.assertSequenceEqual(test_list, [])
                self.assertEqual(len(test_dll), 0)
                self.assertSequenceEqual(test_list, test_dll)

    def test_reverse(self):
        for size in range(20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_dll = DoublyLinkedList(test_list)
                test_list.reverse()
                test_dll.reverse()
                self.assertSequenceEqual(test_list, test_dll)

    def test_extend(self):
        for base_size in range(10):
            for suffix_size in range(10):
                for sample in range(20):
                    base_list = [random() for _ in range(base_size)]
                    suffix_list = [random() for _ in range(suffix_size)]
                    test_dll = DoublyLinkedList(base_list)
                    test_dll.extend(suffix_list)
                    base_list.extend(suffix_list)
                    self.assertSequenceEqual(test_dll, base_list)


if __name__ == '__main__':
    unittest.main()
