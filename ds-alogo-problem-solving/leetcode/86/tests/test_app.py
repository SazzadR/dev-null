import unittest

from app import LinkedList


class TestApp(unittest.TestCase):
    def test_partition(self):
        print("-----------------------")

        # Test 1: Partition in Middle
        print("Test 1: Partition in Middle")
        x = 5
        print(f"x = {x}")
        ll = LinkedList(5)
        for i in [8, 3, 10, 2, 4]:
            ll.append(i)
        print("Before:", self.linkedlist_to_list(ll.head))
        ll.partition_list(x)
        print("After:", self.linkedlist_to_list(ll.head))
        self.assertEqual(self.linkedlist_to_list(ll.head), [3, 2, 4, 5, 8, 10])

        print("-----------------------")

        # Test 2: Partition at Start
        print("Test 2: Partition at Start")
        x = 3
        print(f"x = {x}")
        ll = LinkedList(5)
        for i in [8, 3, 10, 2, 4]:
            ll.append(i)
        print("Before:", self.linkedlist_to_list(ll.head))
        ll.partition_list(x)
        print("After:", self.linkedlist_to_list(ll.head))
        self.assertEqual(self.linkedlist_to_list(ll.head), [2, 5, 8, 3, 10, 4])

        print("-----------------------")

        # Test 3: Partition at End
        print("Test 3: Partition at End")
        x = 11
        print(f"x = {x}")
        ll = LinkedList(5)
        for i in [8, 3, 10, 2, 4]:
            ll.append(i)
        print("Before:", self.linkedlist_to_list(ll.head))
        ll.partition_list(x)
        print("After:", self.linkedlist_to_list(ll.head))
        self.assertEqual(self.linkedlist_to_list(ll.head), [5, 8, 3, 10, 2, 4])

        print("-----------------------")

        # Test 4: Empty List
        print("Test 4: Empty List")
        x = 5
        print(f"x = {x}")
        ll = LinkedList(1)
        ll.make_empty()
        print("Before:", self.linkedlist_to_list(ll.head))
        ll.partition_list(x)
        print("After:", self.linkedlist_to_list(ll.head))
        self.assertIsNone(ll.head)

        print("-----------------------")

        # Test 5: All Greater or Equal
        print("Test 5: All Greater or Equal")
        x = 3
        print(f"x = {x}")
        ll = LinkedList(5)
        for i in [6, 7, 8]:
            ll.append(i)
        print("Before:", self.linkedlist_to_list(ll.head))
        ll.partition_list(x)
        print("After:", self.linkedlist_to_list(ll.head))
        self.assertEqual(self.linkedlist_to_list(ll.head), [5, 6, 7, 8])

        print("-----------------------")

        # Test 6: Single Element
        print("Test 6: Single Element")
        x = 5
        print(f"x = {x}")
        ll = LinkedList(4)
        print("Before:", self.linkedlist_to_list(ll.head))
        ll.partition_list(x)
        print("After:", self.linkedlist_to_list(ll.head))
        self.assertEqual(self.linkedlist_to_list(ll.head), [4])

        print("-----------------------")

        # Test 7: Duplicates Equal to x
        print("Test 7: Duplicates Equal to x")
        x = 3
        print(f"x = {x}")
        ll = LinkedList(3)
        for i in [1, 3, 2, 3]:
            ll.append(i)
        print("Before:", self.linkedlist_to_list(ll.head))
        ll.partition_list(x)
        print("After:", self.linkedlist_to_list(ll.head))
        self.assertEqual(self.linkedlist_to_list(ll.head), [1, 2, 3, 3, 3])

        print("-----------------------")

        # Test 8: Already Partitioned
        print("Test 8: Already Partitioned")
        x = 5
        print(f"x = {x}")
        ll = LinkedList(1)
        for i in [2, 5, 8, 10]:
            ll.append(i)
        print("Before:", self.linkedlist_to_list(ll.head))
        ll.partition_list(x)
        print("After:", self.linkedlist_to_list(ll.head))
        self.assertEqual(self.linkedlist_to_list(ll.head), [1, 2, 5, 8, 10])

        print("-----------------------")

    @staticmethod
    def linkedlist_to_list(head):
        result = []
        current = head
        while current:
            result.append(current.value)
            current = current.next
        return result
