package com.leetcode.java.premium.amazon;

public class JewelsAndStones
{

    public static int numJewelsInStones(String J, String S)
    {
        boolean[] bit = new boolean[128];
        int lenghtJ = J.length();
        int lenghtS = S.length();
        for (int i = 0; i < lenghtJ; i++)
        {
            bit[J.charAt(i)] = true;
        }
        int count = 0;
        for (int i = 0; i < lenghtS; i++)
        {
            if (bit[S.charAt(i)] == true)
            {
                count++;
            }
        }
        return count;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        System.out.println(numJewelsInStones("aA", "aAAbbbb"));
    }

}
