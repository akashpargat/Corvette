package com.leetcode.java.solutions;

public class PerfectNumber
{
    public static boolean checkPerfectNumber(int num)
    {
        int sum = 0;
        for (int i = 1; i * i <= num; i++)
        {
            if (num % i == 0)
            {
                sum = sum + i + (num / i);
            }
        }
        return sum - num == num;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        System.out.println(checkPerfectNumber(28));
        System.out.println(checkPerfectNumber(99999996));
    }

}
