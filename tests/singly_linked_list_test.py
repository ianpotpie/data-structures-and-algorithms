from library.singly_linked_list import SinglyLinkedList
from random import random, randint, randrange
import unittest


class SinglyLinkedListTests(unittest.TestCase):
    def test_empty_init(self):
        test_sll = SinglyLinkedList([])
        self.assertEqual(len(test_sll), 0)
        self.assertSequenceEqual(test_sll, [])

    def test_collection_init(self):
        for size in range(20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_sll = SinglyLinkedList(test_list)
                self.assertEqual(len(test_list), len(test_sll))
                self.assertSequenceEqual(test_list, test_sll)

    def test_get_empty(self):
        test_sll = SinglyLinkedList([])
        with self.assertRaises(IndexError):
            v = test_sll[0]

    def test_set_empty(self):
        test_sll = SinglyLinkedList([])
        with self.assertRaises(IndexError):
            test_sll[0] = 10

    def test_del_empty(self):
        test_sll = SinglyLinkedList([])
        with self.assertRaises(IndexError):
            del test_sll[0]

    def test_append(self):
        for size in range(20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_sll = SinglyLinkedList([])
                for item in test_list:
                    test_sll.append(item)
                self.assertEqual(len(test_list), len(test_sll))
                self.assertSequenceEqual(test_list, test_sll)

    def test_insert(self):
        for size in range(20):
            for sample in range(50):
                test_list = []
                test_sll = SinglyLinkedList([])
                for s in range(size):
                    i = randint(-s, s)
                    v = random()
                    test_list.insert(i, v)
                    test_sll.insert(i, v)
                self.assertEqual(len(test_list), len(test_sll))
                self.assertSequenceEqual(test_list, test_sll)

    def test_get(self):
        for size in range(1,20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_sll = SinglyLinkedList(test_list)

                # test the out-of-bounds indices
                with self.assertRaises(IndexError):
                    v = test_sll[-(size + 1)]
                with self.assertRaises(IndexError):
                    v = test_sll[size]

                # test the inner indices
                for i in range(-size, size):
                    self.assertEqual(test_list[i], test_sll[i])

    def test_set(self):
        for size in range(1, 20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_sll = SinglyLinkedList(test_list)

                # test the out-of-bounds indices
                with self.assertRaises(IndexError):
                    test_sll[-(size + 1)] = random()
                with self.assertRaises(IndexError):
                    test_sll[size] = random()

                # test the inner indices
                for i in range(-size, size):
                    v = random()
                    test_list[i] = v
                    test_sll[i] = v
                    self.assertSequenceEqual(test_list, test_sll)

    def test_del(self):
        for size in range(1, 20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_sll = SinglyLinkedList(test_list)

                # test the out-of-bounds indices
                with self.assertRaises(IndexError):
                    del test_sll[-(size + 1)]
                with self.assertRaises(IndexError):
                    del test_sll[size]

                # test the inner indices
                for s in range(size, 0, -1):
                    i = randrange(-s, s)
                    del test_list[i]
                    del test_sll[i]
                    self.assertSequenceEqual(test_list, test_sll)

    def test_iter(self):
        for size in range(20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_sll = SinglyLinkedList(test_list)
                for i, v in enumerate(test_sll):
                    self.assertEqual(test_list[i], v)

    def test_index_empty(self):
        test_sll = SinglyLinkedList([])
        with self.assertRaises(ValueError):
            test_sll.index(random())

    def test_index(self):
        test_sll = SinglyLinkedList([1, 5, 5, 2, 7, 9])
        self.assertEqual(test_sll.index(1), 0)
        self.assertEqual(test_sll.index(5), 1)
        self.assertEqual(test_sll.index(5, start=2), 2)
        self.assertEqual(test_sll.index(9), 5)
        with self.assertRaises(ValueError):
            test_sll.index(20)
        with self.assertRaises(ValueError):
            test_sll.index(5, start=3)
        with self.assertRaises(ValueError):
            test_sll.index(9, stop=5)

    def test_clear(self):
        for size in range(20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_sll = SinglyLinkedList(test_list)
                test_list.clear()
                test_sll.clear()
                self.assertSequenceEqual(test_list, [])
                self.assertEqual(len(test_sll), 0)
                self.assertSequenceEqual(test_list, test_sll)

    def test_reverse(self):
        for size in range(20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_sll = SinglyLinkedList(test_list)
                test_list.reverse()
                test_sll.reverse()
                self.assertSequenceEqual(test_list, test_sll)

    def test_extend(self):
        for base_size in range(10):
            for suffix_size in range(10):
                for sample in range(20):
                    base_list = [random() for _ in range(base_size)]
                    suffix_list = [random() for _ in range(suffix_size)]
                    test_sll = SinglyLinkedList(base_list)
                    test_sll.extend(suffix_list)
                    base_list.extend(suffix_list)
                    self.assertSequenceEqual(test_sll, base_list)


if __name__ == '__main__':
    unittest.main()
