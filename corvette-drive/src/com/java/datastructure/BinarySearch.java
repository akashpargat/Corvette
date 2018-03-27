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
