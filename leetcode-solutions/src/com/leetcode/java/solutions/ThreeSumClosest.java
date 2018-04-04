package com.leetcode.java.solutions;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ThreeSumClosest
{
    static List<List<Integer>> some = new ArrayList<List<Integer>>();
    static int[] sums = new int[15];

    public static void subset(int[] A, int k, int start, int currLen, boolean[] used, int target)
    {
        if (currLen == k)
        {
            List<Integer> myList = new ArrayList<>();
            int sum = 0;
            for (int i = 0; i < A.length; i++)
            {
                if (used[i] == true)
                {
                    // System.out.print(A[i] + " ");
                    sum += A[i];
                    myList.add(A[i]);
                }
            }
            // sums.add(sum);
            some.add(myList);
            // System.out.print("-->" + sum);
            // System.out.println();
            return;
        }
        if (start == A.length)
        {
            return;
        }
        // For every index we have two options,
        // 1.. Either we select it, means put true in used[] and make currLen+1
        used[start] = true;
        subset(A, k, start + 1, currLen + 1, used, target);
        // 2.. OR we dont select it, means put false in used[] and dont increase
        // currLen
        used[start] = false;
        subset(A, k, start + 1, currLen, used, target);
    }

    public static int threeSumClosest(int[] nums, int target)
    {
        boolean[] B = new boolean[nums.length];
        subset(nums, 3, 0, 0, B, target);
        Arrays.sort(sums);
        return 0;
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
        int A[] = { -1, 0, 1, 2, -1, -4 };
        // boolean[] B = new boolean[A.length];
        // subset(A, 4, 0, 0, B);

        ThreeSumClosest.threeSumClosest(A, 0);
        System.out.println("Akash");

    }
}
