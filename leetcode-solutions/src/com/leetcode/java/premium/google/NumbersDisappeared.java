package com.leetcode.java.premium.google;

import java.util.ArrayList;
import java.util.List;

public class NumbersDisappeared
{
    public static List<Integer> findDisappearedNumbers(int[] nums)
    {
        int max = nums.length;
        if (max == 0)
        {
            return new ArrayList<>();
        }
        List<Integer> res = new ArrayList<>();
        int n = nums.length;
        for (int i = 0; i < nums.length; i++)
        {
            nums[(nums[i] - 1) % n] += n;
        }
        for (int i = 0; i < nums.length; i++)
        {
            if (nums[i] <= n)
            {
                res.add(i + 1);
            }
        }
        return res;
    }

    public List<Integer> findDisappearedNumbers_withExtraSpace(int[] nums)
    {
        boolean[] marked = new boolean[nums.length];
        for (int i = 0; i < nums.length; ++i)
        {
            int val = nums[i];
            marked[val - 1] = true;
        }
        List<Integer> result = new ArrayList<Integer>();
        for (int i = 0; i < nums.length; ++i)
        {
            if (!marked[i])
            {
                result.add(i + 1);
            }
        }
        return result;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        int[] nums = { 7, 1, 4, 3, 2, 3, 8, 7 };
        System.out.println(findDisappearedNumbers(nums));
    }

}
