import array
import unittest

from linked_list import LinkedList


class TestLinkedList(unittest.TestCase):
    def test_append(self):
        ll = LinkedList(0)
        ll.append(1)
        ll.append(2)
        tail = ll.head.next.next
        self.assertEqual(tail.value, 2)
        self.assertEqual(ll.length, 3)

    def test_prepend(self):
        ll = LinkedList(1)
        ll.append(2)
        ll.append(3)
        ll.prepend(0)
        self.assertEqual(ll.head.value, 0)
        self.assertEqual(ll.length, 4)

    def test_pop(self):
        ll = LinkedList(1)
        node = ll.pop()
        self.assertEqual(node.value, 1)
        self.assertEqual(ll.length, 0)
        node = ll.pop()
        self.assertEqual(node, None)
        self.assertEqual(ll.length, 0)

        ll = LinkedList(1)
        ll.append(2)
        ll.append(3)
        node = ll.pop()
        self.assertEqual(node.value, 3)
        self.assertEqual(ll.length, 2)

    def test_pop_first(self):
        ll = LinkedList(0)
        self.assertEqual(ll.length, 1)
        node = ll.pop_first()
        self.assertEqual(node.value, 0)
        self.assertEqual(ll.length, 0)
        node = ll.pop_first()
        self.assertEqual(node, None)

        ll = LinkedList(3)
        ll.append(2)
        ll.append(1)
        node = ll.pop_first()
        self.assertTrue(node.value, 3)
        self.assertEqual(ll.length, 2)

    def test_get(self):
        ll = LinkedList(0)
        ll.append(1)
        ll.append(2)
        node = ll.get(1)
        self.assertEqual(node.value, 1)
        node = ll.get(5)
        self.assertEqual(node, None)

    def test_set_value(self):
        ll = LinkedList(0)
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.set_value(2, "abc")
        self.assertEqual(ll.head.next.next.value, "abc")

    def test_insert(self):
        ll = LinkedList(0)
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.append(4)
        ll.insert(3, "xyz")
        self.assertEqual(ll.head.next.next.next.value, "xyz")
        self.assertEqual(ll.length, 6)

        ll = LinkedList(0)
        ll.insert(2, "xyz")
        self.assertEqual(ll.length, 1)

    def test_remove(self):
        ll = LinkedList("a")
        ll.append("b")
        ll.append("c")
        ll.append("d")
        ll.append("e")
        self.assertEqual(ll.head.next.next.value, "c")
        self.assertEqual(ll.length, 5)
        node = ll.remove(2)
        self.assertEqual(ll.head.next.next.value, "d")
        self.assertEqual(ll.length, 4)
        self.assertEqual(node.value, "c")

    def test_reverse(self):
        ll = LinkedList("a")
        ll.append("b")
        ll.append("c")
        ll.reverse()
        values_in_reverse_order = []
        current = ll.head
        for _ in range(3):
            values_in_reverse_order.append(current.value)
            current = current.next
        self.assertEqual(values_in_reverse_order, ["c", "b", "a"])

    def test_representation(self):
        ll = LinkedList(0)
        ll.append(1)
        ll.append(2)
        self.assertEqual(ll.__repr__(), "[0]->[1]->[2]")
        ll.reverse()
        self.assertEqual(ll.__repr__(), "[2]->[1]->[0]")
