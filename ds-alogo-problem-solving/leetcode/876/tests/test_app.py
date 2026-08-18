import unittest

from app import LinkedList


class TestApp(unittest.TestCase):
    def test_find_middle_node_odd(self):
        ll = LinkedList(1)
        ll.append(2)
        ll.append(3)
        ll.append(4)
        ll.append(5)
        ll.append(6)
        ll.append(7)
        ll.append(8)
        ll.append(9)
        middle_node = ll.find_middle_node()
        self.assertEqual(middle_node.value, 5)

    def test_find_middle_node_even(self):
        ll = LinkedList(1)
        ll.append(2)
        ll.append(3)
        ll.append(4)
        ll.append(5)
        ll.append(6)
        ll.append(7)
        ll.append(8)
        ll.append(9)
        ll.append(9)
        middle_node = ll.find_middle_node()
        self.assertEqual(middle_node.value, 6)
