package com.leetcode.java.solutions;

import java.util.HashMap;
import java.util.Map;

public class DecodeWays
{
    static int numberOfWays = 0;

    public static int numDecodings(String s)
    {
        if (s.isEmpty())
        {
            return 0;
        }
        if (s.equals("0"))
        {
            return 0;
        }
        char[] val = s.toCharArray();
        Map<Character, Integer> occurence = new HashMap<>();
        for (int i = 0; i < val.length; i++)
        {
            occurence.put(val[i], 1);
        }
        numberOfWays = 1;

        for (int j = 0; j < val.length - 1; j++)
        {
            if (val[j] != '0' || val[j + 1] != '0')
            {
                String ss = Character.toString(val[j]) + Character.toString(val[j + 1]);
                if (Integer.parseInt(ss) <= 26 && Integer.parseInt(ss) > 0)
                {
                    numberOfWays += 1;
                }
            }
        }
        return 0;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        numDecodings("100002");
        System.out.println(numberOfWays);
    }

}
