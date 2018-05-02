package com.leetcode.java.solutions;

public class SingleNumber
{

    public static int singleNumber(int[] nums)
    {
        int result = 0;
        for (int num : nums)
        {
            result = result ^ num;
        }
        return result;
    }

    public static void main(String[] args)
    {
        int nums[] = { 27677, 1, 3, 1, 2, 3, 5, 2, 27677 };
        // TODO Auto-generated method stub
        System.out.println(singleNumber(nums));
    }

}
