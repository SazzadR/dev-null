import unittest

from app import Solution


class TestApp(unittest.TestCase):
    def test_find_max_average(self):
        solution = Solution()
        cases = (
            ([1, 12, -5, -6, 50, 3], 4, 12.75),
            ([5], 1, 5.0),
            ([1, 12, -5, -6, 50, 3], 1, 50.0),
            ([1, 2, 3, 4], 4, 2.5),
            ([-5, -2, -3, -4], 2, -2.5),
            ([9, 7, 1, 2], 2, 8.0),
            ([1, 2, 7, 9], 2, 8.0),
            ([4, 4, 4, 4], 2, 4.0),
            ([0, 0, 0], 2, 0.0),
            ([1, 0, 0, 0, 2], 3, 2 / 3),
        )
        for nums, k, expected in cases:
            with self.subTest(nums=nums, k=k):
                self.assertAlmostEqual(solution.findMaxAverage(nums, k), expected)
