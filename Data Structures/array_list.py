from collections.abc import MutableSequence, Iterable
from math import ceil
from typing import Union, Any
from library.array import Array

DEFAULT_CAPACITY: int = 8
EXPAND_FACTOR: float = 2
SHRINK_FACTOR: float = 4


class ArrayList(MutableSequence):
    def __init__(self, elements: Iterable = ()) -> None:
        """
        The ArrayList uses an array in order to store the values of the list. During insertion, all elements in front
        of the inserted element will be shifted forward. When the size of the list reaches the size of the array, a new
        and larger array is created and the elements are copied over. If the number of elements becomes small enough in
        the process of deletion, then a new smaller array is created and the elements are copied over.

        Implements abstract methods from MutableSequence:
        __getitem__, __setitem__, __delitem__, __len__, insert

        Includes mixin methods from MutableSequence:
        __contains__, __iter__, __reversed__, index, count, append, reverse, extend, pop, remove, __iadd__

        Overrides mixin methods from MutableSequence:
        clear

        Implements methods from list:
        copy, sort

        Overrides methods from object:
        __repr__

        :param elements: the initial elements of the ArrayList
        """
        self.size: int = 0
        self.array: Array = Array(DEFAULT_CAPACITY)

        # initialize the ArrayList
        for element in elements:
            if len(self.array) == self.size:
                new_size = max(self.size + 1, int(self.size * EXPAND_FACTOR))
                new_array = Array(new_size)
                new_array[0:self.size] = self.array
                self.array = new_array
            self.array[self.size] = element
            self.size += 1

    def __repr__(self) -> str:
        """
        Creates a string representation of the ArrayList.
        Overrides method in object.

        :return: the string representation
        """
        if self.size == 0:
            return "[]"
        else:
            s = "["
            for i in range(self.size):
                s = s + f"{self.array[i]}, "
            s = s[:-2] + "]"
            return s

    def __len__(self) -> int:
        """
        Counts the number of elements in the ArrayList.
        Overrides abstract method in Collection.

        :return: the number of elements
        """
        return self.size

    def __getitem__(self, index: Union[int, slice]) -> Union[Any, MutableSequence]:
        """
        Retrieves the element in an index or elements in a slice of the ArrayList.
        Overrides abstract method in MutableSequence.

        :param index: the index or slice
        :return: the value or values
        """

        # if the index is an integer, return the element at a single position
        if isinstance(index, int):
            if -self.size <= index < self.size:
                index = index % self.size
                return self.array[index]
            raise IndexError("list index out of range")

        # if the index is a slice, return a new ArrayList with the elements in the slice
        if isinstance(index, slice):
            start, stop, step = index.indices(self.size)
            slice_size = max(0, ceil((stop - start) / step))
            slice_array = Array(max(DEFAULT_CAPACITY, slice_size))
            index = 0
            while index < slice_size:
                slice_array[index] = self.array[start + (index * step)]
                index += 1
            list_slice = ArrayList()
            list_slice.array = slice_array
            list_slice.size = slice_size
            return list_slice

        # if the index is neither type, return an error
        raise TypeError("index must be an int or a slice")

    def __setitem__(self, index: Union[int, slice], value: Union[Any, Iterable]) -> None:
        """
        Sets the element in an index or elements in a slice of the ArrayList with a value or iterable of values.
        Overrides abstract method in MutableSequence.

        :param index: the index or slice
        :param value: the value or values
        :return: None
        """

        # if the index is an integer, set the element at a single position
        if isinstance(index, int):
            if -self.size <= index < self.size:
                index = index % self.size
                self.array[index] = value
                return
            raise IndexError("array index out of range")

        # if the index is a slice, set the elements in a slice of the Array
        if isinstance(index, slice):
            start, stop, step = index.indices(self.size)
            if isinstance(value, Iterable):
                insertion = ArrayList(value)

                slice_size = max(0, ceil((stop - start) / step))

                # if the step size is 1, then the insertion can have a different length from the slice
                if step == 1:
                    new_list = ArrayList()
                    for i in range(0, start):
                        new_list.append(self.array[i])
                    for element in value:
                        new_list.append(element)
                    for i in range(max(start, stop), self.size):
                        new_list.append(self.array[i])
                    self.array = new_list.array
                    self.size = new_list.size
                else:
                    if len(insertion) != slice_size:
                        ValueError(
                            f"attempt to assign sequence of size {len(insertion)} to extended slice of size {slice_size}")
                    for i, element in enumerate(insertion):
                        self.array[start + (i * step)] = element
                return
            raise TypeError("can only assign an iterable")

        # if the index is neither type, return an error
        raise TypeError("index must be an int or a slice")

    def __delitem__(self, index: Union[int, slice]) -> None:
        """
        Deletes the element in an index or elements in a slice of the ArrayList.
        Overrides abstract method in MutableSequence.

        :param index: the index or slice
        :return: None
        """

        # if the index is an integer, delete the element at a single position
        if isinstance(index, int):
            if -self.size <= index < self.size:
                index = index % self.size
                for i in range(index, self.size - 1):
                    self.array[i] = self.array[i + 1]
                self.size -= 1
                if self.size <= int(len(self.array) / SHRINK_FACTOR):
                    new_capacity = max(self.size, DEFAULT_CAPACITY, int(len(self.array) / SHRINK_FACTOR))
                    new_array = Array(new_capacity)
                    for i, element in enumerate(self):
                        new_array[i] = element
                    self.array = new_array
                return
            raise IndexError("list index out of range")

        # if the index is a slice, delete the elements in the slice of the ArrayList
        if isinstance(index, slice):
            start, stop, step = index.indices(self.size)
            slice_size = max(0, ceil((stop - start) / step))
            new_size = self.size - slice_size
            new_array = Array(max(DEFAULT_CAPACITY, new_size))
            if step > 0:
                index = 0
                for i, element in enumerate(self):
                    if (i == start) and (i < stop):
                        start = start + step
                    else:
                        new_array[index] = element
                        index += 1
            else:
                index = new_size - 1
                for i, element in enumerate(reversed(self)):
                    i = (self.size - 1) - i
                    if (i == start) and (i > stop):
                        start = start + step
                    else:
                        new_array[index] = element
                        index -= 1
            self.array = new_array
            self.size = new_size
            return

        # if the index is neither type, return an error
        raise TypeError("index must be an int or a slice")

    def insert(self, index: int, value: Any) -> None:
        """
        Inserts a new value into the ArrayList at a given index.
        Overrides abstract method in MutableSequence.

        :param index: the index
        :param value: the new value
        :return: None
        """
        if -self.size <= index <= self.size:
            index = (index + self.size) if index < 0 else index
            if self.size == len(self.array):
                new_size = max(self.size + 1, int(self.size * EXPAND_FACTOR))
                new_array = Array(new_size)
                new_array[:self.size] = self.array[:self.size]
                self.array = new_array
            for i in range(self.size, index, -1):
                self.array[i] = self.array[i - 1]
            self.array[index] = value
            self.size += 1
            return
        raise IndexError("index out of range")

    # Overrides MutableSequence mixin method for efficiency:
    # The mixin method implements the clear() method by repeatedly removing
    # single values. A more efficient method is to reset the list all at once.
    def clear(self) -> None:
        """
        Removes all the elements in the ArrayList.
        Overrides mixin method in MutableSequence.

        :return:
        """
        self.size = 0
        self.array = Array(DEFAULT_CAPACITY)

    def copy(self) -> MutableSequence:
        """
        Creates a shallow copy of the ArrayList.
        Implements copy to fulfill the list interface.

        :return: a copy of the ArrayList
        """
        new_list = ArrayList()
        for element in self:
            new_list.append(element)
        return new_list

    def sort(self) -> None:
        """
        Sorts the ArrayList with mergesort.
        Implements sort to fulfill the list interface.

        :return: None
        """

        list_size = 1
        while list_size < self.size:
            for start in range(0, self.size, 2 * list_size):
                list1 = self[start:start + list_size]
                iter1 = iter(list1)

                try:
                    val1 = next(iter1)
                except StopIteration:
                    iter1, val1 = None, None

                list2 = self[start + list_size: start + (2 * list_size)]
                iter2 = iter(list2)

                try:
                    val2 = next(iter2)
                except StopIteration:
                    iter2, val2 = None, None

                index = start
                while (iter1 is not None) or (iter2 is not None):
                    if iter1 is None:
                        self.array[index] = val2
                        try:
                            val2 = next(iter2)
                        except StopIteration:
                            iter2, val2 = None, None
                    elif iter2 is None:
                        self.array[index] = val1
                        try:
                            val1 = next(iter1)
                        except StopIteration:
                            iter1, val1 = None, None
                    elif val2 < val1:
                        self.array[index] = val2
                        try:
                            val2 = next(iter2)
                        except StopIteration:
                            iter2, val2 = None, None
                    else:
                        self.array[index] = val1
                        try:
                            val1 = next(iter1)
                        except StopIteration:
                            iter1, val1 = None, None
                    index += 1
            list_size *= 2
