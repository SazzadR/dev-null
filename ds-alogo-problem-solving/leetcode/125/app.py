class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1

        result = True

        while left <= right:
            while left < right and not s[left].isalnum():
                left += 1
            while right > left and not s[right].isalnum():
                right -= 1


            if s[left].lower() !=  s[right].lower():
                result = False
                break

            left += 1
            right -= 1

        return result
