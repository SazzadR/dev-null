import unittest

from app import Solution


class TestApp(unittest.TestCase):
    def test_contains_duplicate(self):
        solution = Solution()
        for nums in ([1, 2, 3, 1], [1, 1, 1, 3, 3, 4, 3, 2, 4, 2], [0, 0], [-1, 2, -1]):
            with self.subTest(nums=nums):
                self.assertTrue(solution.containsDuplicate(nums))

    def test_no_duplicates(self):
        solution = Solution()
        for nums in ([1, 2, 3, 4], [1], [], [-1, 0, 1]):
            with self.subTest(nums=nums):
                self.assertFalse(solution.containsDuplicate(nums))
