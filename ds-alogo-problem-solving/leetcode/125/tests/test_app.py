import unittest

from app import Solution


class TestApp(unittest.TestCase):
    def test_is_palindrome(self):
        solution = Solution()
        for s in ("A man, a plan, a canal: Panama", " ", "", "a", "Aa", "12321", "a(bcb_ a", ".,!"):
            with self.subTest(s=s):
                self.assertTrue(solution.isPalindrome(s))

    def test_is_not_palindrome(self):
        solution = Solution()
        for s in ("race a car", "0P", "ab", "1231", "a.,b"):
            with self.subTest(s=s):
                self.assertFalse(solution.isPalindrome(s))
