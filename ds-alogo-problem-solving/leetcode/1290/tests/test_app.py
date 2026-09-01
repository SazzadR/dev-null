import unittest

from app import LinkedList


class TestApp(unittest.TestCase):
    def test_binary_to_decimal(self):
        # Test case 1: Binary number 110 = Decimal number 6
        linked_list = LinkedList(1)
        linked_list.append(1)
        linked_list.append(0)
        print("Test case 1 linked list:")
        linked_list.print_list()
        result = linked_list.binary_to_decimal()
        self.assertEqual(result, 6)


        # Test case 2: Binary number 1000 = Decimal number 8
        linked_list = LinkedList(1)
        linked_list.append(0)
        linked_list.append(0)
        linked_list.append(0)
        print("Test case 2 linked list:")
        linked_list.print_list()
        result = linked_list.binary_to_decimal()
        self.assertEqual(result, 8)

        # Test case 3: Binary number 0 = Decimal number 0
        linked_list = LinkedList(0)
        print("Test case 3 linked list:")
        linked_list.print_list()
        result = linked_list.binary_to_decimal()
        self.assertEqual(result, 0)

        # Test case 4: Binary number 1 = Decimal number 1
        linked_list = LinkedList(1)
        print("Test case 4 linked list:")
        linked_list.print_list()
        result = linked_list.binary_to_decimal()
        self.assertEqual(result, 1)

        # Test case 5: Binary number 1101 = Decimal number 13
        linked_list = LinkedList(1)
        linked_list.append(1)
        linked_list.append(0)
        linked_list.append(1)
        print("Test case 5 linked list:")
        linked_list.print_list()
        result = linked_list.binary_to_decimal()
        self.assertEqual(result, 13)
