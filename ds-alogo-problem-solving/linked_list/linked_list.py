from multiprocessing import current_process
from platform import node
from queue import LifoQueue, Queue
import queue


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __repr__(self):
        return f"<Node value={self.value!r}>"


class LinkedList:
    def __init__(self, value):
        new_node = Node(value=value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def __repr__(self):
        output = ""
        if self.length == 0:
            return output

        current_node = self.head
        while current_node.next != None:
            output += f"[{current_node.value}]->"
            current_node = current_node.next
        output += f"[{current_node.value}]"

        return output

    def append(self, value) -> None:
        new_node = Node(value=value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            current_tail = self.tail
            current_tail.next = new_node
            self.tail = new_node
        self.length += 1

    def prepend(self, value) -> None:
        new_node = Node(value=value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            current_head = self.head
            new_node.next = current_head
            self.head = new_node
        self.length += 1

    def pop(self) -> Node | None:
        if self.length == 0:
            return None
        else:
            if self.length == 1:
                tail_to_be_removed = self.head
                self.head = None
                self.tail = None
            else:
                tail_to_be_removed = self.tail
                current_node = self.head

                while current_node.next != tail_to_be_removed:
                    current_node = current_node.next

                self.tail = current_node
                self.tail.next = None

            self.length -= 1

            return tail_to_be_removed

    def pop_first(self) -> Node | None:
        if self.length == 0:
            return None
        else:
            head_to_be_removed = self.head
            if self.length == 1:
                self.head = None
                self.tail = None
            else:
                self.head = self.head.next
            head_to_be_removed.next = None
            self.length -= 1

            return head_to_be_removed

    def get(self, index: int) -> Node | None:
        if index < 0 or index >= self.length:
            return None

        i = 0
        current_node = self.head
        while current_node.next:
            if i == index:
                break
            current_node = current_node.next
            i += 1

        return current_node

    def set_value(self, index: int, value) -> None:
        node = self.get(index)
        if node:
            node.value = value

    def insert(self, index: int, value) -> None:
        if index < 0 or index >= self.length:
            return None

        if index == 0:
            self.prepend(value=value)
        else:
            new_node = Node(value=value)

            previous_node = self.get(index - 1)
            current_node = previous_node.next

            previous_node.next = new_node
            new_node.next = current_node

            self.length += 1

    def remove(self, index) -> Node | None:
        if index < 0 or index >= self.length:
            return None

        if index == 0:
            return self.pop_first()
        if index + 1 == self.length:
            return self.pop()
        else:
            previous_node = self.get(index - 1)
            node_to_be_removed = previous_node.next
            next_node = node_to_be_removed.next

            previous_node.next = next_node
            node_to_be_removed.next = None
            self.length -= 1

            return node_to_be_removed

    def reverse(self):
        old_head = self.head

        current = self.head
        previous = None

        while current:
            temp = current.next
            current.next = previous

            previous = current
            current = temp

        self.head = previous
        self.tail = old_head
