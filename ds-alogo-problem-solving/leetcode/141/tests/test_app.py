import unittest

from app import LinkedList


class TestApp(unittest.TestCase):
    def test_has_loop(self):
        my_linked_list_1 = LinkedList(1)
        my_linked_list_1.append(2)
        my_linked_list_1.append(3)
        my_linked_list_1.append(4)
        my_linked_list_1.tail.next = my_linked_list_1.head
        self.assertTrue(my_linked_list_1.has_loop())


        my_linked_list_2 = LinkedList(1)
        my_linked_list_2.append(2)
        my_linked_list_2.append(3)
        my_linked_list_2.append(4)
        self.assertFalse(my_linked_list_2.has_loop())
