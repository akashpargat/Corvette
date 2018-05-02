package com.leetcode.java.solutions;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class MajorityElement
{
    public static int majorityElement(int[] nums)
    {
        Map<Integer, Integer> myMap = new HashMap<Integer, Integer>();
        for (int i = 0; i < nums.length; i++)
        {
            if (myMap.containsKey(nums[i]))
            {
                myMap.put(nums[i], myMap.get(nums[i]) + 1);
                continue;
            }
            myMap.put(nums[i], 1);
        }
        return Collections.max(myMap.entrySet(), Map.Entry.comparingByValue()).getKey();
    }

    public int majorityElement_optimized(int[] nums)
    {
        if (nums.length == 1)
        {
            return nums[0];
        }
        Arrays.sort(nums);
        return nums[nums.length / 2];
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        int[] nums = { 2, 2, 1, 1, 1, 2, 2 };
        System.out.println(majorityElement(nums));
    }

}
