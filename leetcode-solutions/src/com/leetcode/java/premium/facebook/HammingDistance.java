package com.leetcode.java.premium.facebook;

public class HammingDistance
{
    public static int hammingDistance(int x, int y)
    {
        return Integer.bitCount(x ^ y);
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        System.out.println(hammingDistance(1, 4));
    }

}
