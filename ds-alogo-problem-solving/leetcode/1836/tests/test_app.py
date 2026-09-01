import unittest

from app import LinkedList


class TestApp(unittest.TestCase):
    def test_remove_duplicates(self):
        # Test 1: List with no duplicates
        ll = LinkedList(1)
        ll.append(2)
        ll.append(3)
        self.assertEqual(self.assertion_helper(ll, [1, 2, 3]), "Test PASS")

        # Test 2: List with some duplicates
        ll = LinkedList(1)
        ll.append(2)
        ll.append(1)
        ll.append(3)
        ll.append(2)
        self.assertEqual(self.assertion_helper(ll, [1, 2, 3]), "Test PASS")

        # Test 3: List with all duplicates
        ll = LinkedList(1)
        ll.append(1)
        ll.append(1)
        self.assertEqual(self.assertion_helper(ll, [1]), "Test PASS")

        # Test 4: List with consecutive duplicates
        ll = LinkedList(1)
        ll.append(1)
        ll.append(2)
        ll.append(2)
        ll.append(3)
        self.assertEqual(self.assertion_helper(ll, [1, 2, 3]), "Test PASS")

        # Test 5: List with non-consecutive duplicates
        ll = LinkedList(1)
        ll.append(2)
        ll.append(1)
        ll.append(3)
        ll.append(2)
        ll.append(4)
        self.assertEqual(self.assertion_helper(ll, [1, 2, 3, 4]), "Test PASS")

        # Test 6: List with duplicates at the end
        ll = LinkedList(1)
        ll.append(2)
        ll.append(3)
        ll.append(3)
        self.assertEqual(self.assertion_helper(ll, [1, 2, 3]), "Test PASS")

        # Test 7: Empty list
        ll = LinkedList(None)
        ll.head = None  # Directly setting the head to None
        ll.length = 0   # Adjusting the length to reflect an empty list
        self.assertEqual(self.assertion_helper(ll, []), "Test PASS")

    @staticmethod
    def assertion_helper(linked_list, expected_values):
        print("Before: ", end="")
        linked_list.print_list()
        linked_list.remove_duplicates()
        print("After:  ", end="")
        linked_list.print_list()

        # Collect values from linked list after removal
        result_values = []
        node = linked_list.head
        while node:
            result_values.append(node.value)
            node = node.next

        # Determine if the test passes
        if result_values == expected_values:
            return "Test PASS"
        else:
            return "Test FAIL"
