class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        unique_numbers = set()

        for num in nums:
            if num in unique_numbers:
                return True
            unique_numbers.add(num)

        return False
