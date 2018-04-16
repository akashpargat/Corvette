package com.leetcode.java.premium.facebook;

public class MoveZeroes
{
    @SuppressWarnings("nls")
    public static void moveZeroes(int[] nums)
    {
        int length = nums.length;
        for (int i = 0; i < length; i++)
        {
            if (nums[i] != 0)
            {
                continue;
            }
            for (int j = i; j < length; j++)
            {
                if (nums[i] == 0 && nums[j] != 0)
                {
                    nums[i] = nums[j];
                    nums[j] = 0;
                    break;
                }
            }
        }
        for (int k = 0; k < length; k++)
        {
            System.out.print(nums[k] + ", ");
        }
    }

    public static void moveZeroes_optimized(int[] nums)
    {

        if (nums == null || nums.length == 0)
        {
            return;
        }

        int insertPos = 0;
        for (int num : nums)
        {
            if (num != 0)
            {
                nums[insertPos++] = num;
            }
        }

        while (insertPos < nums.length)
        {
            nums[insertPos++] = 0;
        }

    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        int[] nums = { 8, 0, 5, 3, 0, 5, 0, 7, 0, 0, 0, 2, 1 };
        moveZeroes(nums);
    }
}
