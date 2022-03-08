import unittest
from math import ceil

from library.array import Array
from random import random


class ArrayTest(unittest.TestCase):
    def test_init(self):

        # empty init
        test_array = Array()
        self.assertEqual(len(test_array), 0)
        self.assertSequenceEqual(test_array, [])

        # nonempty init
        for size in range(10):
            test_array = Array(size)
            self.assertEqual(len(test_array), size)

    def test_getitem(self):

        # test index out of range
        for size in range(10):
            test_array = Array(size)
            with self.assertRaises(IndexError):
                v = test_array[size]
            with self.assertRaises(IndexError):
                v = test_array[-size - 1]

        # model test index
        for size in range(10):
            for sample in range(10):
                test_list = [random() for _ in range(size)]
                test_array = Array(size)
                for i, element in enumerate(test_list):
                    test_array[i] = element
                for index in range(size):
                    self.assertEqual(test_list[index], test_array[index])

        # model test slice
        for size in range(5):
            for sample in range(5):
                test_list = [random() for _ in range(size)]
                test_array = Array(size)
                for i, element in enumerate(test_list):
                    test_array[i] = element
                for start in range(-(size + 1), size + 2):
                    for stop in range(-(size + 1), size + 2):
                        for step in range(-(size + 1), size + 2):
                            if step == 0:
                                with self.assertRaises(ValueError):
                                    v = test_array[start:stop:step]
                            else:
                                self.assertSequenceEqual(test_list[start:stop:step], test_array[start:stop:step])

    def test_setitem(self):

        # test index out of range
        for size in range(10):
            test_array = Array(size)
            with self.assertRaises(IndexError):
                test_array[size] = random()
            with self.assertRaises(IndexError):
                test_array[-size - 1] = random()

        # model test index
        for size in range(10):
            for sample in range(10):
                test_list = [random() for _ in range(size)]
                test_array = Array(size)
                for i, element in enumerate(test_list):
                    test_array[i] = element
                for index in range(size):
                    r = random()
                    test_list[index] = r
                    test_array[index] = r
                    self.assertSequenceEqual(test_list, test_array)

        # model test slice
        for size in range(5):
            for insert_size in range(0, size + 2):
                for start in range(-(size + 1), size + 2):
                    for stop in range(-(size + 1), size + 2):
                        for step in range(-(size + 1), size + 2):
                            for sample in range(5):
                                test_list = [random() for _ in range(size)]
                                test_array = Array(size)
                                for i, element in enumerate(test_list):
                                    test_array[i] = element
                                insertion = [random() for _ in range(insert_size)]
                                if step == 0:
                                    with self.assertRaises(ValueError):
                                        test_array[start:stop:step] = insertion
                                else:
                                    s = slice(start, stop, step).indices(size)
                                    slice_size = max(0, ceil((s[1] - s[0]) / s[2]))
                                    if slice_size != insert_size:
                                        with self.assertRaises(ValueError):
                                            test_array[start:stop:step] = insertion
                                    else:
                                        test_list[start:stop:step] = insertion
                                        test_array[start:stop:step] = insertion
                                        self.assertSequenceEqual(test_list, test_array)


if __name__ == '__main__':
    unittest.main()
