from library.array_list import ArrayList
from random import random, randint
import unittest


class ArrayListTest(unittest.TestCase):
    def test_empty_init(self):
        test_arraylist = ArrayList()
        self.assertEqual(len(test_arraylist), 0)
        self.assertSequenceEqual(test_arraylist, [])

    def test_collection_init(self):

        # test with an empty list
        test_list = []
        test_arraylist = ArrayList(test_list)
        self.assertEqual(len(test_arraylist), 0)
        self.assertSequenceEqual(test_arraylist, test_list)

        # test with a nonempty list
        test_list = [1, 2, 3]
        test_arraylist = ArrayList(test_list)
        self.assertEqual(len(test_arraylist), 3)
        self.assertSequenceEqual(test_arraylist, test_list)

        # model test
        for size in range(10):
            for sample in range(10):
                self.assertEqual(len(test_arraylist), 3)
                self.assertSequenceEqual(test_arraylist, test_list)

    def test_getitem(self):

        # test index out of range
        for size in range(10):
            test_arraylist = ArrayList([random() for _ in range(size)])
            with self.assertRaises(IndexError):
                v = test_arraylist[size]
            with self.assertRaises(IndexError):
                v = test_arraylist[-size - 1]

        # model test index
        for size in range(10):
            for sample in range(10):
                test_list = [random() for _ in range(size)]
                test_arraylist = ArrayList(test_list)
                for index in range(size):
                    self.assertEqual(test_list[index], test_arraylist[index])

        # model test slice
        for size in range(5):
            for sample in range(5):
                test_list = [random() for _ in range(size)]
                test_arraylist = ArrayList(test_list)
                for start in range(size):
                    for stop in range(size):
                        for step in [-3, -2, -1, 1, 2, 3]:
                            self.assertSequenceEqual(test_list[start:stop:step], test_arraylist[start:stop:step])

    def test_setitem(self):

        # test index out of range
        for size in range(10):
            test_arraylist = ArrayList([i for i in range(size)])
            with self.assertRaises(IndexError):
                test_arraylist[size] = random()
            with self.assertRaises(IndexError):
                test_arraylist[-size - 1] = random()

        # model test index
        for size in range(10):
            for sample in range(10):
                test_list = [random() for _ in range(size)]
                test_arraylist = ArrayList(test_list)
                for index in range(size):
                    r = random()
                    test_list[index] = r
                    test_arraylist[index] = r
                    self.assertSequenceEqual(test_list, test_arraylist)

        # model test slice
        count = 1
        for size in range(5):
            for start in range(size):
                for stop in range(size):
                    for sample in range(5):
                        for step in [-3, -2, -1, 1, 2, 3]:
                            test_list = [random() for _ in range(size)]
                            test_arraylist = ArrayList(test_list)
                            if step != 1:
                                insertion = [random() for _ in range(start, stop, step)]
                            else:
                                insertion = [random() for _ in range(sample)]
                            test_list[start:stop:step] = insertion
                            test_arraylist[start:stop:step] = insertion
                            self.assertSequenceEqual(test_list, test_arraylist)

    def test_delitem(self):

        # test index out of range
        for size in range(10):
            test_arraylist = ArrayList([i for i in range(size)])
            with self.assertRaises(IndexError):
                del test_arraylist[size]
            with self.assertRaises(IndexError):
                del test_arraylist[-size - 1]

        # model test index
        for size in range(10):
            for sample in range(10):
                test_list = [random() for _ in range(size)]
                test_arraylist = ArrayList(test_list)
                for del_size in range(size, 0, -1):
                    i = randint(0, del_size - 1)
                    del test_list[i]
                    del test_arraylist[i]
                    self.assertSequenceEqual(test_list, test_arraylist)

        # model test slice
        for size in range(5):
            for start in range(size):
                for stop in range(size):
                    for step in [-3, -2, -1, 1, 2, 3]:
                        test_list = [random() for _ in range(size)]
                        test_arraylist = ArrayList(test_list)
                        for sample in range(5):
                            del test_list[start:stop:step]
                            del test_arraylist[start:stop:step]
                            self.assertSequenceEqual(test_list, test_arraylist)

    def test_append(self):
        for size in range(20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_arraylist = ArrayList()
                for item in test_list:
                    test_arraylist.append(item)
                self.assertEqual(len(test_list), len(test_arraylist))
                self.assertSequenceEqual(test_list, test_arraylist)

    def test_insert(self):
        for size in range(20):
            for sample in range(50):
                test_list = []
                test_arraylist = ArrayList()
                for s in range(size):
                    i = randint(-s, s)
                    v = random()
                    test_list.insert(i, v)
                    test_arraylist.insert(i, v)
                self.assertEqual(len(test_list), len(test_arraylist))
                self.assertSequenceEqual(test_list, test_arraylist)

    def test_clear(self):
        for size in range(0, 20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_arraylist = ArrayList(test_list)
                test_list.clear()
                test_arraylist.clear()
                self.assertSequenceEqual(test_list, [])
                self.assertSequenceEqual(test_list, test_arraylist)

    def test_copy(self):
        for size in range(20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_arraylist = ArrayList(test_list)
                test_copy = test_arraylist.copy()
                self.assertSequenceEqual(test_list, test_copy)
                self.assertSequenceEqual(test_list, test_copy)

    def test_sort(self):
        for size in range(20):
            for sample in range(50):
                test_list = [random() for _ in range(size)]
                test_arraylist = ArrayList(test_list)
                test_list.sort()
                test_arraylist.sort()
                self.assertSequenceEqual(test_list, test_arraylist)


if __name__ == '__main__':
    unittest.main()
