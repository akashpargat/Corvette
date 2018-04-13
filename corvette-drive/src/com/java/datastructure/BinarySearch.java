package com.java.datastructure;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

public class BinarySearch
{
    public static void main(String[] args)
    {
        // int[] arr = BubbleSort.bubbleSort(new int[] { 5, 7, 3, 2, 1, 4, 6 });
        // System.out.println(binarySearch(arr, 1, 0, arr.length - 1));
        // System.out.println(19 / 10);
        // for(int i =0; i<=20; i++) {
        // System.out.println("Mod of number : "+ i + " = " +i%10);
        // }
        removeDuplicates(new int[] { 1, 3, 1, 2, 1, 2, 3, 1, 2, 3, 1, 2, 3, 2, 1, 1, 2, 2, 3, 1, 2,
                1, 2, 1, 3, 2, 1, 2, 2, 3, 2 });
    }

    int binarySearch_template1(int[] nums, int target)
    {
        if (nums == null || nums.length == 0)
        {
            return -1;
        }

        int left = 0, right = nums.length - 1;
        while (left <= right)
        {
            // Prevent (left + right) overflow
            int mid = left + (right - left) / 2;
            if (nums[mid] == target)
            {
                return mid;
            }
            else if (nums[mid] < target)
            {
                left = mid + 1;
            }
            else
            {
                right = mid - 1;
            }
        }

        // End Condition: left > right
        return -1;
    }

    int binarySearch_template2(int[] nums, int target)
    {
        if (nums == null || nums.length == 0)
        {
            return -1;
        }

        int left = 0, right = nums.length;
        while (left < right)
        {
            // Prevent (left + right) overflow
            int mid = left + (right - left) / 2;
            if (nums[mid] == target)
            {
                return mid;
            }
            else if (nums[mid] < target)
            {
                left = mid + 1;
            }
            else
            {
                right = mid;
            }
        }

        // Post-processing:
        // End Condition: left == right
        if (left != nums.length && nums[left] == target)
        {
            return left;
        }
        return -1;
    }

    int binarySearch_template3(int[] nums, int target)
    {
        if (nums == null || nums.length == 0)
        {
            return -1;
        }

        int start = 0, end = nums.length - 1;
        while (start + 1 < end)
        {
            // Prevent (left + right) overflow
            int mid = start + (end - start) / 2;
            if (nums[mid] == target)
            {
                return mid;
            }
            else if (nums[mid] < target)
            {
                start = mid;
            }
            else
            {
                end = mid;
            }
        }

        // Post-processing:
        // End Condition: start + 1 == end
        if (nums[start] == target)
        {
            return start;
        }
        if (nums[end] == target)
        {
            return end;
        }
        return -1;
    }

    private static String binarySearch(int[] bubbleSortArray, int numberTofind, int firstIndex,
            int lastIndex)
    {
        if (lastIndex >= firstIndex)
        {
            int mid = firstIndex + (lastIndex - firstIndex) / 2;
            int middleElement = bubbleSortArray[mid];

            if (middleElement == numberTofind)
            {
                return "Found the number and it is " + middleElement;
            }

            if (middleElement > numberTofind)
            {
                binarySearch(bubbleSortArray, numberTofind, firstIndex, mid - 1);
            }

            return binarySearch(bubbleSortArray, numberTofind, mid + 1, lastIndex);
        }

        return "Sorry the number was not found in the given array.";
    }

    private static void removeDuplicates(final int[] array)
    {
        Map<Integer, Integer> withoutDuplicates = new LinkedHashMap<>();
        for (int arr : array)
        {
            if (!withoutDuplicates.containsKey(arr))
            {
                withoutDuplicates.put(arr, 1);
            }
            else
            {
                withoutDuplicates.put(arr, withoutDuplicates.get(arr) + 1);
            }
        }
        Set<Entry<Integer, Integer>> entry = withoutDuplicates.entrySet();
        for (Entry<Integer, Integer> entr : entry)
        {
            System.out.println(entr.getKey());
        }
    }
}
