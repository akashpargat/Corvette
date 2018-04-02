package com.leetcode.java.solutions;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * 15. 3Sum <br>
 * Given an array S of n integers, are there elements a, b, c in S such that a + b + c = 0? <br>
 * Find all unique triplets in the array which gives the sum of zero.<br>
 * Note: The solution set must not contain duplicate triplets.<br>
 * For example, given array S = [-1, 0, 1, 2, -1, -4],<br>
 * after sorting [-4, -1, -1, 0, 1, 2] <br>
 * A solution set is:<br>
 * [<br>
 * [-1, 0, 1],<br>
 * [-1, -1, 2]<br>
 * ]
 * 
 * @author Akash pargat
 */
public class ThreeSum
{

    public static List<List<Integer>> threeSum(int[] arr)
    {
        List<List<Integer>> finalResult = new ArrayList<>();
        Arrays.sort(arr);

        for (int i = 0; i < arr.length - 2; i++)
        {
            if (i > 0 && arr[i] == arr[i - 1])
            {
                continue;
            }
            int start = i + 1;
            int end = arr.length - 1;
            while (start < end)
            {
                if (arr[i] + arr[start] + arr[end] == 0)
                {
                    finalResult.add(Arrays.asList(arr[i], arr[start], arr[end]));
                }
                if (arr[i] + arr[start] + arr[end] < 0)
                {
                    int currentStart = start;
                    while (arr[start] == arr[currentStart] && start < end)
                    {
                        start++;
                    }
                }
                else
                {
                    int currentEnd = end;
                    while (arr[end] == arr[currentEnd] && start < end)
                    {
                        end--;
                    }
                }
            }
        }
        return finalResult;
    }

    public static List<List<Integer>> threeSumOptimized(final int[] nums)
    {
        List<List<Integer>> result = new ArrayList<List<Integer>>();
        // sort this nums
        Arrays.sort(nums);
        for (int i = 0; i < nums.length - 2; i++)
        {
            if (i > 0 && nums[i] == nums[i - 1])
            {
                continue;
            }
            int left = i + 1;
            int right = nums.length - 1;
            int target = 0 - nums[i];
            while (left < right)
            {
                if (nums[left] + nums[right] == target)
                {
                    result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    left++;
                    right--;
                    while (left < right && nums[left] == nums[left - 1])
                    {
                        left++;
                    }
                }
                else if (nums[left] + nums[right] < target)
                {
                    left++;
                }
                else
                {
                    right--;
                }
            }
        }
        return result;
    }

    public static void printThreeSum(List<List<Integer>> arrayToPrint)
    {
        for (List<Integer> array : arrayToPrint)
        {
            for (Integer value : array)
            {
                System.out.print(value + " , ");
            }
            System.out.println();
        }
    }

    public static void main(String[] args)
    {
        // Test Suite one
        ThreeSum.printThreeSum(ThreeSum.threeSum(new int[] { -1, 0, 1, 2, -1, -4 }));
        System.out.println("********************************************");
        // Test Suite two
        ThreeSum.printThreeSum(ThreeSum.threeSum(new int[] { -4, -1, -1, -1, 0, 1, 2, 2 }));
        System.out.println("********************************************");
        // Test Suite three
        ThreeSum.printThreeSum(ThreeSum.threeSum(new int[] { -4, -1, -1, 0, 2, 2 }));
        System.out.println("********************************************");
        // Test Suite four
        ThreeSum.printThreeSum(ThreeSum.threeSum(new int[] { -5, -3, -1, 1, 2, 3, 4, 5 }));
        System.out.println("********************************************");
        // Test Suite five
        ThreeSum.printThreeSum(ThreeSum.threeSum(new int[] { 0, 0, 0 }));
        System.out.println("********************************************");
    }
}
