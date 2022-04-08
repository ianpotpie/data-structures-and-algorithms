from collections.abc import Sequence, Iterable
from typing import Union, Any
from math import ceil


class Array(Sequence):
    def __init__(self, size: int) -> None:
        """
        This array implementation uses a python list as the container of the elements. It is not a "real" array, but
        behaves like one. The primary characteristic being that the length is fixed.

        Implements abstract methods from Sequence:
        __getitem__, __setitem__, __delitem__, __len__

        Includes mixin methods from Sequence:
        __contains__, __iter__, __reversed__, index, count

        Overrides methods from object:
        __repr__

        :param size: the size of the array
        """
        self.size: int = size
        self.elements: list = [None for _ in range(size)]

    def __repr__(self) -> str:
        """
        Creates a string representation of the current Array.
        Overrides method in object.

        :return: the string representation
        """
        if self.size == 0:
            return "[]"
        else:
            s = "["
            for element in self.elements:
                s = s + f"{element}, "
            s = s[:-2] + "]"
            return s

    def __len__(self) -> int:
        """
        Counts the number of elements in the current Array.
        Overrides abstract method in Collection.

        :return: the number of elements
        """
        return self.size

    def __getitem__(self, index: Union[int, slice]) -> Union[Any, Sequence]:
        """
        Retrieves the element in an index or the Array of elements in a slice of the current Array.
        Overrides abstract method in Sequence.

        :param index: the index or slice
        :return: the element or Array of elements
        """

        # if the index is an integer, return the element at a single position
        if isinstance(index, int):
            if -self.size <= index < self.size:
                index = index % self.size
                return self.elements[index]
            raise IndexError("array index out of range")

        # if the index is a slice, return a new Array with the elements in the slice
        if isinstance(index, slice):
            start, stop, step = index.indices(self.size)
            slice_size = max(0, ceil((stop - start) / step))
            array_slice = Array(slice_size)
            index = 0
            while index < slice_size:
                array_slice[index] = self.elements[start + (index * step)]
                index += 1
            return array_slice

        # if the index is neither type, return an error
        raise TypeError("index must be an int or a slice")

    def __setitem__(self, index: Union[int, slice], item: Union[Any, Iterable]) -> None:
        """
        Sets the element in an index or the elements in a slice with a value or iterable of values.

        :param index: the index or slice
        :param item: the value or iterable of values
        :return: None
        """

        # if the index is an integer, set the element at a single position
        if isinstance(index, int):
            if -self.size <= index < self.size:
                index = index % self.size
                self.elements[index] = item
                return
            raise IndexError("array index out of range")

        # if the index is a slice, set the elements in a slice of the Array
        if isinstance(index, slice):
            start, stop, step = index.indices(self.size)
            if isinstance(item, Iterable):
                for i, value in enumerate(item):
                    if i >= ((stop - start) / step):
                        break
                    else:
                        self.elements[start + (i * step)] = value
                return
            raise TypeError("can only assign an iterable")

        # if the index is neither type, return an error
        raise TypeError("index must be an int or a slice")
