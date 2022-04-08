from collections.abc import MutableSequence, Iterator, Iterable
from typing import Any, Union


class SinglyLinkedListNode:
    def __init__(self, val, nxt):
        self.val = val
        self.nxt = nxt


class SinglyLinkedList(MutableSequence):
    def __init__(self, elements=()) -> None:
        """
        The singly-linked list stores elements in a sequence of linked nodes. The head of the list is kept as the starting
        point of all operations.

        Implements abstract methods from MutableSequence:
        __getitem__, __setitem__, __delitem__, __len__, insert

        Includes mixin methods from MutableSequence:
        __contains__, __iter__, __reversed__, index, count, append, reverse, extend, pop, remove, __iadd__

        Overrides mixin methods from MutableSequence:
        clear, __iter__, __reversed__

        Implements methods from list:
        copy, sort

        Overrides methods from object:
        __repr__

        :param elements: the initial elements of the ArrayList
        """
        self.size = 0
        self.head = None

        # initialize the list
        prev_node = None
        for element in elements:
            self.size += 1
            if self.head is None:
                self.head = SinglyLinkedListNode(element, None)
                prev_node = self.head
            else:
                prev_node.nxt = SinglyLinkedListNode(element, None)
                prev_node = prev_node.nxt

    def __repr__(self) -> str:
        """
        Creates a string representation of the list.
        :return: a string of the list
        """
        if self.size == 0:
            return "[]"
        else:
            s = "["
            curr_node = self.head
            while curr_node is not None:
                s = s + f"{curr_node.val}, "
                curr_node = curr_node.nxt
            s = s[:-2] + "]"
            return s

    def __len__(self) -> int:
        """
        Counts the number of elements in the LinkedList.
        Overrides the abstract method from the Collection class.

        :return: the number of elements
        """
        return self.size

    def __getitem__(self, index: Union[int, slice]) -> Union[Any, MutableSequence]:
        """
        Retrieves the element in an index or elements in a slice of the LinkedList.
        Overrides abstract method in MutableSequence.

        :param index: the index or slice
        :return: the value or values
        """

        # if the index is an integer, return the element at a single position
        if isinstance(index, int):
            if -self.size <= index < self.size:
                index = index % self.size
                curr_node = self.head
                curr_index = 0
                while curr_index < index:
                    curr_node = curr_node.nxt
                    curr_index += 1
                return curr_node.val
            else:
                raise IndexError("list index out of range")

        # if the index is a slice, return a new LinkedList with the elements in that slice
        if isinstance(index, slice):
            start, stop, step = index.indices(self.size)
            new_list = SinglyLinkedList()
            prev_node = None
            for i, element in enumerate(self):
                if (i == start) and

        # if the index is neither type, return an error
        raise TypeError("index must be an int or a slice")

    # Implements MutableSequence abstract method
    def __setitem__(self, index: int, value: any) -> None:
        """
        Sets the element in an index or elements in a slice of the ArrayList with a value or iterable of values.
        Overrides abstract method in MutableSequence.

        :param index: the index or slice
        :param value: the value or values
        :return: None
        """

        if -self.size <= index < self.size:
            index = index % self.size
            curr_node = self.head
            curr_index = 0
            while curr_index < index:
                curr_node = curr_node.nxt
                curr_index += 1
            curr_node.val = value
        else:
            raise IndexError

    # Implements MutableSequence abstract method
    def __delitem__(self, index: int) -> None:
        if -self.size <= index < self.size:
            index = index % self.size
            prev_node = None
            curr_node = self.head
            curr_index = 0
            while curr_index < index:
                prev_node = curr_node
                curr_node = curr_node.nxt
                curr_index += 1
            self.size -= 1
            if prev_node is None:
                self.head = self.head.nxt
            else:
                prev_node.nxt = curr_node.nxt
        else:
            raise IndexError

    # Implements MutableSequence abstract method
    def insert(self, index: int, value: any) -> None:
        """
        Inserts a new item into the list at a given index.
        :param index: the index of the new item
        :param value: the value of the new item
        :return: None
        """
        if -self.size <= index <= self.size:
            index = (index + self.size) if index < 0 else index
            prev_node = None
            curr_node = self.head
            curr_index = 0
            while curr_index < index:
                prev_node = curr_node
                curr_node = curr_node.nxt
                curr_index += 1
            if prev_node is None:
                self.head = SinglyLinkedListNode(value, self.head)
            else:
                prev_node.nxt = SinglyLinkedListNode(value, curr_node)
            self.size += 1
        else:
            raise IndexError

    # Overrides MutableSequence mixin method for efficiency:
    # The mixin implementation of __iter__() used a while loop and a stored
    # index. It used the built-in get() method in order to retrieve sequential
    # values. With a linked list, the iterator instead stores the current node
    # in the list, and iterates by traversing the pointer of the node. This
    # allows the iterator to avoid re-traversing segments of the list
    def __iter__(self) -> Iterator:
        """
        Creates an iterator for the list. This iterator works by storing the
        current node and then traversing along the node pointer at each
        iteration. The default method increments a stored index which would
        cause the iterator to traverse large portions of the list at each
        iteration.
        :return: an iterator for the list
        """
        return SinglyLinkedListIterator(self)

    # Overrides MutableSequence mixin method for efficiency:
    # The mixin implementation of index() used a while loop and a stored index
    # rather than the built-in iterator. The built-in iterator is more
    # efficient since it does not require re-traversal of any segments of the
    # list.
    def index(self, value: any, start=0, stop=None) -> int:
        """
        Finds and returns the index of the first instance of a given value.
        :param value: the value to be found
        :param start: the start (inclusive) bound of the search interval
        :param stop: the end (exclusive) bound of the search interval
        :return: the index of the first instance of the value
        """
        stop = len(self) if stop is None else stop
        for i, item in enumerate(self):
            if stop <= i:
                raise ValueError
            if (item == value) and (start <= i):
                return i
        raise ValueError

    # Overrides MutableSequence mixin method for efficiency:
    # The mixin method implements the clear() method by repeatedly removing
    # single values. A more efficient method is to reset the list all at once.
    def clear(self) -> None:
        self.size = 0
        self.head = None

    # Overrides MutableSequence mixin method for efficiency:
    # The mixin implementation of reverse() iterates through the indices of the
    # list and swaps complementary index value. However, this method requires
    # re-traversing the list which every change of indices. Instead, we can
    # change the direction of the links in the list in order to reverse it.
    def reverse(self) -> None:
        """
        Reverses the list IN PLACE.
        :return: None
        """
        prev_node = None
        curr_node = self.head
        while curr_node is not None:
            next_node = curr_node.nxt
            curr_node.nxt = prev_node
            prev_node = curr_node
            curr_node = next_node
        self.head = prev_node

    # Overrides MutableSequence mixin method for efficiency:
    # The mixin implementation of extend works by repeatedly appending values.
    # However, each call to append traverses the entire list. It is more
    # efficient to reverse the list, insert the values at the front, and then
    # reverse the list a final time.
    def extend(self, values: Iterable) -> None:
        self.reverse()
        for value in values:
            self.insert(0, value)
        self.reverse()


class SinglyLinkedListIterator:
    def __init__(self, singly_linked_list):
        self.curr_node = singly_linked_list.head

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_node is None:
            raise StopIteration
        else:
            curr_node = self.curr_node
            self.curr_node = curr_node.nxt
            return curr_node.val
