class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.length = 1

    def append(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
        else:
            current_node = self.head
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = new_node
        self.length += 1

    def print_list(self):
        if self.head is None:
            print("empty list")
        else:
            temp = self.head
            values = []
            while temp is not None:
                values.append(str(temp.value))
                temp = temp.next
            print(" -> ".join(values))

    def make_empty(self):
        self.head = None
        self.tail = None
        self.length = 0

    def partition_list(self, x):
        left_dummy = LinkedList("LEFT_DUMMY")
        left_current = left_dummy.head

        right_dummy = LinkedList("RIGHT_DUMMY")
        right_current = right_dummy.head

        current = self.head
        while current:
            new_node = Node(current.value)
            if current.value < x:
                left_current.next = new_node
                left_current = left_current.next
            else:
                right_current.next = new_node
                right_current = right_current.next

            current = current.next

        left_current.next = right_dummy.head.next
        left_dummy.head = left_dummy.head.next

        self.head = left_dummy.head
