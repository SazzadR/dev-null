class Solution:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        average = 0
        max_average = 0

        max_sliding_window_index = len(nums) - k
        for i in range(0, max_sliding_window_index + 1):
            if i == 0:
                sum = 0
                for j in range(0, k):
                    sum += nums[j]
                average = sum/k
                max_average = average
            else:
                average = ((average * k) - nums[i - 1] + nums[i+k-1]) / k
                if average > max_average:
                    max_average = average

        return max_average
