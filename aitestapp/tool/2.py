def find_max(nums):
    
    max_num = nums[0]
    for i in nums:
        if i > max_num:
            max_num = i
    return max_num

if __name__ == "__main__":
    nums = [1, 4, 5, 6, 7, 8, 9, 0, 2, 3]
    print(find_max(nums))      