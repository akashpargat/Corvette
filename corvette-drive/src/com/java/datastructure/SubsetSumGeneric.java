package com.java.datastructure;

import java.util.ArrayList;
import java.util.List;

public class SubsetSumGeneric
{
    static List<List<Integer>> some = new ArrayList<List<Integer>>();

    /**
     * arr[] ---> Input Array <br>
     * data[] ---> Temporary array to store current combination <br>
     * start & end ---> Staring and Ending indexes in arr[] <br>
     * index ---> Current index in data[] <br>
     * r ---> Size of a combination to be printed
     */
    static void combinationUtil(int array[], int arrayLength, int subSetSize, int index,
            int tempArray[], int i)
    {
        if (index == subSetSize)
        {
            List<Integer> myList = new ArrayList<>();
            int sum = 0;
            for (int j = 0; j < subSetSize; j++)
            {
                System.out.print(tempArray[j] + " ");
                sum += tempArray[j];
                myList.add(tempArray[j]);
            }
            if (sum == 0)
            {
                some.add(myList);
            }
            System.out.print("-->" + sum);
            System.out.println("");
            return;
        }

        if (i >= arrayLength)
        {
            return;
        }

        tempArray[index] = array[i];
        combinationUtil(array, arrayLength, subSetSize, index + 1, tempArray, i + 1);
        combinationUtil(array, arrayLength, subSetSize, index, tempArray, i + 1);
    }

    static void printCombination(int array[], int arrayLength, int subSetSize)
    {
        int tempArray[] = new int[subSetSize];
        combinationUtil(array, arrayLength, subSetSize, 0, tempArray, 0);
    }

    public List<List<Integer>> threeSum(int[] nums)
    {
        printCombination(nums, nums.length, 3);
        return some;
    }

    public static void main(String[] args)
    {
        // int arr[] = { 1, 2, 3, 4, 5 };
        // int subSetSize = 3;
        // int arrayLength = arr.length;
        // printCombination(arr, arrayLength, subSetSize);
        int arr1[] = { -1, 0, 1, 2, -1, -4 };
        printCombination(arr1, arr1.length, 3);
    }
}
