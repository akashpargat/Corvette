package com.leetcode.java.solutions;

public class MaximumSizeSubarraySum_K
{

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        // int[] arr = { -1, 5, 1, -2, -3, 8 };
        int[] arr = { -2, -1, 2, 1 };
        int k = 1;
        System.out.println(maxSubArrayLen(arr, k));
    }

    public static int maxSubArrayLen_NonWorking(int[] nums, int k)
    {
        int sum = 0;
        int psuedoCount = 0;
        int prevCount = 0;
        for (int i = 0; i < nums.length; i++)
        {
            psuedoCount++;
            sum += nums[i];
            if (sum == k)
            {
                if (prevCount < psuedoCount)
                {
                    prevCount = psuedoCount;
                }
                sum = 0;
                psuedoCount = 0;
            }
        }
        return prevCount;
    }

    public static int maxSubArrayLen(int[] nums, int k)
    {
        int sum = 0;
        int psuedoCount = 0;
        int prevCount = 0;
        for (int i = 0; i < nums.length; i++)
        {
            sum += nums[i];
            if (sum == k)
            {
                if (prevCount < psuedoCount)
                {
                    prevCount = psuedoCount;
                }
                sum = 0;
                psuedoCount = 0;
                i--;
            }
            if (i == nums.length - 1)
            {
                i = nums.length - i - 1;
            }
        }
        return prevCount;
    }

}
