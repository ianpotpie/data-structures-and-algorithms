from collections.abc import MutableSequence, Iterator, Iterable, Collection
from typing import Optional


class DoublyLinkedListNode:
    def __init__(self, val: any, prv: Optional[object], nxt: Optional[object]):
        self.val = val
        self.prv = prv
        self.nxt = nxt


class DoublyLinkedList(MutableSequence):
    def __init__(self, items=()) -> None:
        self.size = len(items)
        self.head = None
        self.tail = None
        for item in items:
            self.append(item)

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

    # Implements MutableSequence abstract method
    def __getitem__(self, index: int) -> any:
        if -self.size <= index < self.size:
            index = index % self.size
            curr_node = self.tail if (2 * index >= self.size) else self.head
            curr_index = (self.size - 1) if (2 * index >= self.size) else 0
            step = -1 if (2 * index >= self.size) else 1
            while curr_index != index:
                curr_node = curr_node.nxt if step == 1 else curr_node.prv
                curr_index += step
            return curr_node.val
        else:
            raise IndexError

    # Implements MutableSequence abstract method
    def __setitem__(self, index: int, value: any) -> None:
        if -self.size <= index < self.size:
            index = index % self.size
            curr_node = self.tail if (2 * index >= self.size) else self.head
            curr_index = (self.size - 1) if (2 * index >= self.size) else 0
            step = -1 if (2 * index >= self.size) else 1
            while curr_index != index:
                curr_node = curr_node.nxt if step == 1 else curr_node.prv
                curr_index += step
            curr_node.val = value
        else:
            raise IndexError

    # Implements MutableSequence abstract method
    def __delitem__(self, index: int) -> None:
        if -self.size <= index < self.size:
            index = index % self.size
            curr_node = self.tail if (2 * index >= self.size) else self.head
            curr_index = (self.size - 1) if (2 * index >= self.size) else 0
            step = -1 if (2 * index >= self.size) else 1
            while curr_index != index:
                curr_node = curr_node.nxt if step == 1 else curr_node.prv
                curr_index += step
            if curr_node.nxt is None:
                self.tail = curr_node.prv
                if self.tail is not None:
                    self.tail.nxt = None
            else:
                curr_node.nxt.prv = curr_node.prv
            if curr_node.prv is None:
                self.head = curr_node.nxt
                if self.head is not None:
                    self.head.prv = None
            else:
                curr_node.prv.nxt = curr_node.nxt
            self.size -= 1
        else:
            raise IndexError

    # Implements MutableSequence abstract method
    def __len__(self) -> int:
        return self.size

    # Implements MutableSequence abstract method
    def insert(self, index: int, value: any) -> None:
        """
        Inserts a new item into the list at a given index.
        :param index: the index of the new item
        :param value: the value of the new item
        :return: None
        """
        if -self.size <= index <= self.size:
            if index == self.size:
                new_node = DoublyLinkedListNode(value, self.tail, None)
                self.tail = new_node
                if new_node.prv is None:
                    self.head = new_node
                else:
                    new_node.prv.nxt = new_node
            else:
                index = (index + self.size) if index < 0 else index
                curr_node = self.tail if (2 * index >= self.size) else self.head
                curr_index = (self.size - 1) if (2 * index >= self.size) else 0
                step = -1 if (2 * index >= self.size) else 1
                while curr_index != index:
                    curr_node = curr_node.nxt if step == 1 else curr_node.prv
                    curr_index += step
                new_node = DoublyLinkedListNode(value, curr_node.prv, curr_node)
                curr_node.prv = new_node
                if new_node.prv is None:
                    self.head = new_node
                else:
                    new_node.prv.nxt = new_node
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
        return DoublyLinkedListIterator(self, reverse=False)

    # Overrides MutableSequence mixin method for efficiency:
    # The mixin implementation of __reversed__() used a while loop and a stored
    # index. It used the built-in get() method in order to retrieve sequential
    # values. With a linked list, the iterator instead stores the current node
    # in the list, and iterates by traversing the pointer of the node. This
    # allows the iterator to avoid re-traversing segments of the list
    def __reversed__(self) -> Iterator:
        """
        Creates an iterator for the list. This iterator works by storing the
        current node and then traversing along the node pointer at each
        iteration. The default method increments a stored index which would
        cause the iterator to traverse large portions of the list at each
        iteration.
        :return: an iterator for the list
        """
        return DoublyLinkedListIterator(self, reverse=True)

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
        self.tail = None

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
        curr_node = self.head
        while curr_node is not None:
            prev_node = curr_node.prv
            curr_node.prv = curr_node.nxt
            curr_node.nxt = prev_node
            curr_node = curr_node.prv
        tail = self.tail
        self.tail = self.head
        self.head = tail


class DoublyLinkedListIterator:
    def __init__(self, singly_linked_list, reverse):
        self.curr_node = singly_linked_list.tail if reverse else singly_linked_list.head
        self.step = -1 if reverse else 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_node is None:
            raise StopIteration
        else:
            curr_node = self.curr_node
            self.curr_node = curr_node.nxt if self.step == 1 else curr_node.prv
            return curr_node.val
