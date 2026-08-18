import unittest

from app import LinkedList, find_kth_from_end


class TestApp(unittest.TestCase):
    def test_find_kth_from_end(self):
        ll = LinkedList(1)
        ll.append(2)
        ll.append(3)
        ll.append(4)
        ll.append(5)
        node = find_kth_from_end(ll, 2)
        self.assertEqual(node.value, 4)

        ll = LinkedList(1)
        node = find_kth_from_end(ll, 2)
        self.assertEqual(node, None)

        ll = LinkedList(1)
        node = find_kth_from_end(ll, 1)
        self.assertEqual(node.value, 1)
