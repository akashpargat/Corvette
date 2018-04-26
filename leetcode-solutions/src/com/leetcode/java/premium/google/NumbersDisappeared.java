package com.leetcode.java.premium.google;

import java.util.List;

public class NumbersDisappeared
{
    public static List<Integer> findDisappearedNumbers(int[] nums)
    {
        if (nums.length == 0)
        {
            return null;
        }
        int max = 0;
        for (int i = 0; i < nums.length; i++)
        {
            if (nums[i] > max)
            {
                max = nums[i];
            }
        }
        for (int i = 0; i <= max; i++)
        {

        }

        return null;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        int[] nums = { 7, 1, 4, 3, 2, 3, 8, 9 };
        System.out.println(findDisappearedNumbers(nums));
    }

}
