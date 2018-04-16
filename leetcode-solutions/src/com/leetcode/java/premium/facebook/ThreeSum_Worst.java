package com.leetcode.java.premium.facebook;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ThreeSum_Worst
{

    static List<List<Integer>> result = new ArrayList<List<Integer>>();

    public static List<List<Integer>> threeSum(int[] nums)
    {
        int length = nums.length;
        for (int i = 0; i < length - 2; i++)
        {
            int k = i;
            int sum = 0;
            for (int j = i; j < k + 3; j++)
            {
                sum += nums[j];
                System.out.print(nums[j] + "Akk");
            }
            System.out.println(sum);
        }
        return null;
    }

    public static void main(String[] args)
    {
        int[] nums = { -1, 0, 1, 2, -1, -4 };
        threeSum(nums);

        int arr[] = { -1, 0, 1, 2, -1, -4 };
        int r = 3;
        int n = arr.length;
        printCombination(arr, n, r);
        System.out.println(result);
        System.out.println(threeSum_leet(nums));
    }

    /**
     * arr[] ---> Input Array data[] ---> Temporary array to store current combination start & end
     * ---> Staring and Ending indexes in arr[] index ---> Current index in data[] r ---> Size of a
     * combination to be printed
     */
    static void combinationUtil(int arr[], int data[], int start, int end, int index, int r)
    {
        if (index == r)
        {
            List<Integer> myList = new ArrayList<>();
            for (int j = 0; j < r; j++)
            {
                myList.add(data[j]);
                System.out.print(data[j] + " ");
            }
            int sum = 0;
            for (int i = 0; i < myList.size(); i++)
            {
                sum += myList.get(i);
            }
            if (sum == 0)
            {
                result.add(myList);
            }
            System.out.println("Akash");
            return;
        }

        for (int i = start; i <= end && end - i + 1 >= r - index; i++)
        {
            data[index] = arr[i];
            combinationUtil(arr, data, i + 1, end, index + 1, r);
        }
    }

    /**
     * The main function that prints all combinations of size r in arr[] of size n. This function
     * mainly uses combinationUtil()
     * 
     * @param arr
     * @param n
     * @param r
     */
    static void printCombination(int arr[], int n, int r)
    {
        // A temporary array to store all combination one by one
        int data[] = new int[r];

        // Print all combination using temprary array 'data[]'
        combinationUtil(arr, data, 0, n - 1, 0, r);
    }

    public static List<List<Integer>> threeSum_leet(int[] nums)
    {
        Arrays.sort(nums);
        List<List<Integer>> list = new ArrayList<List<Integer>>();
        for (int i = 0; i < nums.length - 2; i++)
        {
            if (i > 0 && (nums[i] == nums[i - 1]))
            {
                continue; // avoid duplicates
            }
            for (int j = i + 1, k = nums.length - 1; j < k;)
            {
                if (nums[i] + nums[j] + nums[k] == 0)
                {
                    list.add(Arrays.asList(nums[i], nums[j], nums[k]));
                    j++;
                    k--;
                    while ((j < k) && (nums[j] == nums[j - 1]))
                    {
                        j++;// avoid duplicates
                    }
                    while ((j < k) && (nums[k] == nums[k + 1]))
                    {
                        k--;// avoid duplicates
                    }
                }
                else if (nums[i] + nums[j] + nums[k] > 0)
                {
                    k--;
                }
                else
                {
                    j++;
                }
            }
        }
        return list;
    }

}
