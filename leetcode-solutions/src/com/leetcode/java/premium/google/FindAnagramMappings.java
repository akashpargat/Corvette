package com.leetcode.java.premium.google;

import java.util.HashMap;
import java.util.Map;

public class FindAnagramMappings
{
    public static int[] anagramMappings(int[] A, int[] B)
    {
        Map<Integer, Integer> myMap = new HashMap<>();
        for (int i = 0; i < B.length; i++)
        {
            myMap.put(B[i], i);
        }
        int[] res = new int[A.length];
        for (int i = 0; i < A.length; i++)
        {
            if (myMap.containsKey(A[i]))
            {
                res[i] = myMap.get(A[i]);
            }

        }
        return res;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        int[] A = { 12, 28, 46, 32, 50 };
        int[] B = { 50, 12, 32, 46, 28 };
        System.out.println(anagramMappings(A, B));
    }
}
