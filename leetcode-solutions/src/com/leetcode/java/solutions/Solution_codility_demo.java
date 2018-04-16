package com.leetcode.java.solutions;

import java.util.HashMap;
import java.util.Map;

public class Solution_codility_demo
{
    public static int solution(int[] A)
    {
        int max = getMax(A);
        Map<Integer, Integer> myMap = new HashMap<>();
        for (int i = 0; i < A.length; i++)
        {
            myMap.put(A[i], i);
        }
        for (int i = 1; i <= max; i++)
        {
            if (!myMap.containsKey(i))
            {
                return i;
            }
            if (i == max)
            {
                return max + 1;
            }
        }
        return 1;
    }

    public static int getMax(int[] A)
    {
        int max = 0;

        for (int i = 0; i < A.length; i++)
        {
            if (A[i] > max)
            {
                max = A[i];
            }
        }
        return max;
    }

    public static void main(String[] args)
    {
        // int[] arr = { 15, 10, 9, 17, 2, 3, 1, 19 };
        // int[] arr = { 1, 2, 3 };
        int[] arr = { -1, -2, -3 };
        System.out.println(getMax(arr));
        System.out.println(solution(arr));
    }
}
