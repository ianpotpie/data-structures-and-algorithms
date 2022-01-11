class Node:
    def __init__(self, value, prev_node, next_node):
        self.value = value
        self.prev_node = prev_node
        self.next_node = next_node


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, index: int, value: any) -> None:
        """
        Inserts a value at a particular index of the list.
        :param index: the index where the value will be inserted
        :param value: the value of the new list node
        :return: None
        """
        if index == 0:
            self.head = Node(value, None, self.head)
            if self.head.next_node is None:
                self.tail = self.head
            else:
                self.head.next_node.prev_node = self.head

        if index > 0:
            curr_node = self.head
            curr_index = 0
            while (curr_node is not None) and (curr_index < index):
                curr_node = curr_node.next_node
                curr_index += 1

            if curr_index < index:
                raise IndexError(f"The index exceeds {curr_index}, the maximum possible insertion index")
            else:
                new_node = Node(value, curr_node.prev_node, curr_node)
                new_node.prev_node.next_node = new_node
                if curr_node is None:
                    self.tail = new_node
                else:
                    curr_node.prev_node = new_node

        if index == -1:
            self.tail = Node(value, self.tail.prev_node, None)
            if self.tail.prev_node is None:
                self.head = self.tail
            else:
                self.tail.prev_node.next_node = self.tail

        if index < -1:
            curr_node = self.tail
            curr_index = -1
            while (curr_node is not None) and (curr_index > index):
                curr_node = curr_node.prev_node
                curr_index -= 1

            if curr_index > index:
                raise IndexError(f"The index exceeds {curr_index}, the minimum possible insertion index")
            else:
                new_node = Node(value, curr_node, curr_node.next_node)
                new_node.next_node.prev_node = new_node
                if curr_node is None:
                    self.head = new_node
                else:
                    curr_node.next_node = new_node

    def prepend(self, value: any) -> None:
        """
        Inserts a value at the beginning of the list.
        :param value: the value to be inserted
        :return: None
        """
        self.head = Node(value, None, self.head)
        if self.head.next_node is None:
            self.tail = self.head
        else:
            self.head.next_node.prev_node = self.head

    def append(self, value: any) -> None:
        """
        Inserts a value at the end of the list.
        :param value: the value to be inserted
        :return: None
        """
        self.tail = Node(value, self.tail, None)
        if self.tail.prev_node is None:
            self.head = self.tail
        else:
            self.tail.prev_node.next_node = self.tail

    def get(self, index: int) -> any:
        """
        Gets the value of the node at a particular index of the list.
        :param index: The index of node whose value will be returned.
        :return: None
        """

        if self.head is None:
            raise RuntimeError("Cannot get value from an empty list")

        if index < 0:
            curr_node = self.tail
            curr_index = -1
            while (curr_node is not None) and (curr_index > index):
                curr_node = curr_node.prev_node
                curr_index -= 1

            if curr_node is None:
                raise IndexError(f"The index exceeds {curr_index + 1}, the minimum index in the list")
            else:
                return curr_node.value

        if self.tail is None:
            raise RuntimeError("Cannot get value from an empty list")

        if index >= 0:
            curr_node = self.head
            curr_index = 0
            while (curr_node is not None) and (curr_index < index):
                curr_node = curr_node.next_node
                curr_index += 1

            if curr_node is None:
                raise IndexError(f"The index exceeds {curr_index - 1}, the maximum index in the list")
            else:
                return curr_node.value

    def index(self, value: any) -> int:
        """
        Returns the index of the first instance of the value in the interval of [start, end)
        :param value: the value of a list node
        :return: the index of the first instance of value, or ValueError if none is found
        """
        curr_node = self.head
        curr_index = 0
        while curr_node is not None:
            if curr_node.value == value:
                return curr_index
            else:
                curr_node = curr_node.next_node
                curr_index += 1

        raise ValueError(f"{value} is not in the list")

    def remove(self, index) -> None:
        """
        Removes the node at a particular index of the list and returns its value.
        :param index: The index of the node to be removes.
        :return: None
        """
        if self.head is None:
            raise RuntimeError("Cannot remove from an empty list")

        if index == 0:
            self.head = self.head.next_node
            if self.head is None:
                self.tail = None
            else:
                self.head.prev_node = None

        if index > 0:
            curr_node = self.head
            curr_index = 0
            while (curr_node is not None) and (curr_index < index):
                curr_node = curr_node.next_node
                curr_index += 1

            if curr_node is None:
                raise IndexError(f"The index exceeds {curr_index - 1}, the maximum index in the list")
            else:
                if curr_node.prev_node is None:
                    self.head = curr_node.next_node
                    self.head.prev_node = None
                else:
                    curr_node.prev_node.next_node = curr_node.next_node

                if curr_node.next_node is None:
                    self.tail = curr_node.prev_node
                    self.tail.next_node = None
                else:
                    curr_node.next_node.prev_node = curr_node.prev_node

        if self.tail is None:
            raise RuntimeError("Cannot remove from an empty list")

        if index == -1:
            self.tail = self.tail.prev_node
            if self.tail is None:
                self.head = None
            else:
                self.tail.next_node = None

        if index < -1:
            curr_node = self.tail
            curr_index = 0
            while (curr_node is not None) and (curr_index > index):
                curr_node = curr_node.prev_node
                curr_index -= 1

            if curr_node is None:
                raise IndexError(f"The index exceeds {curr_index + 1}, the minimum index in the list")
            else:
                if curr_node.prev_node is None:
                    self.head = curr_node.next_node
                    self.head.prev_node = None
                else:
                    curr_node.prev_node.next_node = curr_node.next_node

                if curr_node.next_node is None:
                    self.tail = curr_node.prev_node
                    self.tail.next_node = None
                else:
                    curr_node.next_node.prev_node = curr_node.prev_node

    def print_list(self) -> None:
        """
        Create a string representation of the linked list.
        :return: a string representation of the list
        """
        if self.head is None:
            print("HEAD -> None <- Tail")
        else:
            print("\t\tHEAD")
            print("\t\t V")
            s = "None <- "
            curr_node = self.head
            while curr_node is not None:
                if curr_node.next_node is None:
                    s = s + f"[{curr_node.value}]"
                else:
                    s = s + f"[{curr_node.value}] <=> "
                curr_node = curr_node.next_node
            s = s + " -> None"
            list_len = len(s)
            print(s)
            print((" " * (list_len - 10)) + "^")
            print((" " * (list_len - 11)) + "TAIL")


if __name__ == "__main__":
    dll = DoublyLinkedList()
    for i in range(2):
        dll.insert(0, i)
    dll.print_list()
