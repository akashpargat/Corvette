package com.leetcode.java.premium.google;

public class JudgeRouteCircle
{
    public static boolean judgeCircle(String moves)
    {
        int length = moves.length();
        char[] move = moves.toCharArray();
        if (length % 2 != 0)
        {
            return false;
        }
        int lCount = 0;
        int rCount = 0;
        int dCount = 0;
        int uCount = 0;
        for (int i = 0; i < length; i++)
        {
            if (move[i] == 'L')
            {
                lCount++;
            }
            if (move[i] == 'R')
            {
                rCount++;
            }
            if (move[i] == 'U')
            {
                uCount++;
            }
            if (move[i] == 'D')
            {
                dCount++;
            }
        }
        if (lCount == rCount && dCount == uCount)
        {
            return true;
        }

        return false;
    }

    public static boolean judgeCircle_optimized(String moves)
    {
        int[] result = new int[128];

        for (char c : moves.toCharArray())
        {
            result[c]++;
        }
        return result['U'] == result['D'] && result['L'] == result['R'];
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        System.out.println(judgeCircle("DURDLDRRLL"));
    }

}
