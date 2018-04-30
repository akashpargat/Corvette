package com.leetcode.java.premium.contest;

import java.util.ArrayList;
import java.util.List;

public class ShortestDistanceToChar
{
    public static int[] shortestToChar(String S, char C)
    {
        int length = S.length();
        int[] result = new int[length + 10];
        List<Integer> myList = new ArrayList<>();
        for (int i = 0; i < length; i++)
        {
            if (S.charAt(i) == C)
            {
                myList.add(i);
            }
        }
        System.out.println(myList);
        int count = 0;
        int prev = 0;
        for (Integer val : myList)
        {
            int move = val - prev;
            prev = val + 1;

            for (int i = move; i >= 0; i--)
            {
                result[count] = i;
                System.out.print(result[count] + ", ");
                count++;
            }
        }
        return null;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        shortestToChar("loveleetcode", 'e');
    }

}
