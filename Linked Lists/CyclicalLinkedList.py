class Node:
    def __init__(self, value, next_node):
        self.value = value
        self.next_node = next_node


class CyclicalLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, index: int, value: any) -> None:
        """
        Inserts a value at a particular index of the list.
        :param index: the index where the value will be inserted
        :param value: the value of the new list node
        :return: None
        """
        if index < 0:
            raise IndexError("The index cannot be negative")

        if index == 0:
            self.head = Node(value, self.head)

        if index > 0:
            prev_node = None
            curr_node = self.head
            curr_index = 0
            while (curr_node is not None) and (curr_index < index):
                prev_node = curr_node
                curr_node = curr_node.next_node
                curr_index += 1

            if curr_index < index:
                raise IndexError(f"The index exceeds {curr_index}, the maximum possible insertion index")
            else:
                new_node = Node(value, curr_node)
                prev_node.next_node = new_node

    def prepend(self, value: any) -> None:
        """
        Inserts a value at the beginning of the list.
        :param value: the value to be inserted
        :return: None
        """
        self.head = Node(value, self.head)
        if self.head.next_node is None:
            self.head.next_node = self.head
        else:
            curr_node = self.head
            while curr_node.next_node is not self.head.next_node:
                curr_node = curr_node.next_node
            curr_node.next_node = self.head

    def append(self, value: any) -> None:
        """
        Inserts a value at the end of the list.
        :param value: the value to be inserted
        :return: None
        """
        if self.head is None:
            self.head = Node(value, None)
        else:
            curr_node = self.head
            while curr_node.next_node is not self.head:
                curr_node = curr_node.next_node
            curr_node.next_node = Node(value, self.head)

    def get(self, index: int) -> any:
        """
        Gets the value of the node at a particular index of the list.
        :param index: The index of node whose value will be returned.
        :return: None
        """
        if index < 0:
            raise IndexError("The index cannot be negative")
        else:
            curr_node = self.head
            curr_index = 0
            while curr_index < index:
                curr_node = curr_node.next_node
                curr_index += 1

            return curr_node.value

    def index(self, value: any) -> int:
        """
        Returns the index of the first instance of the value in the interval of [start, end)
        :param value: the value of a list node
        :return: the index of the first instance of value, or ValueError if none is found
        """
        if self.head is None:
            raise RuntimeError("Cannot find value in an empty list")

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

        if index < 0:
            raise IndexError("The index cannot be negative")

        if index == 0:
            self.head = self.head.next_node

        if index > 0:
            prev_node = None
            curr_node = self.head
            curr_index = 0
            while (curr_node is not None) and (curr_index < index):
                prev_node = curr_node
                curr_node = curr_node.next_node
                curr_index += 1

            if curr_node is None:
                raise IndexError(f"The index exceeds {curr_index - 1}, the maximum index in the list")
            else:
                prev_node.next_node = curr_node.next_node

    def stringify(self) -> str:
        """
        Create a string representation of the linked list.
        :return: a string representation of the list
        """
        s = "HEAD\n V\n"
        curr_node = self.head
        while curr_node is not None:
            s = s + f"[{curr_node.value}] -> "
            curr_node = curr_node.next_node
        s = s + "None"
        return s


if __name__ == "__main__":
    sll = SinglyLinkedList()
    for i in range(5):
        sll.insert(0, i)
    print(sll.stringify())
