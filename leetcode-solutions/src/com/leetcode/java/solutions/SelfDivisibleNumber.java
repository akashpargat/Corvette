package com.leetcode.java.solutions;

import java.util.ArrayList;
import java.util.List;

public class SelfDivisibleNumber
{
    public static List<Integer> selfDividingNumbers(int left, int right)
    {
        List<Integer> result = new ArrayList<>();
        for (int l = left; l <= right; l++)
        {
            boolean flag = false;
            int dum = l;
            while (dum > 0)
            {
                int var = dum % 10;
                if (var == 0)
                {
                    break;
                }
                if (l % var != 0)
                {
                    break;
                }
                dum /= 10;
                if (dum == 0 && flag == false)
                {
                    result.add(l);
                }
            }
        }
        return result;
    }

    public static void main(String[] args)
    {
        System.out.println(selfDividingNumbers(1, 22));
    }
}
