import unittest

from app import LinkedList


class TestApp(unittest.TestCase):
    def test_reverse_linked_list(self):
        ll = LinkedList(1)
        ll.append(2)
        ll.append(3)
        ll.reverse()
        self.assertEqual(self.linkedlist_to_list(ll.head), [3, 2, 1])

        ll = LinkedList(1)
        ll.reverse()
        self.assertEqual(self.linkedlist_to_list(ll.head), [1])

    @staticmethod
    def linkedlist_to_list(head):
        result = []
        current = head
        while current:
            result.append(current.value)
            current = current.next
        return result
