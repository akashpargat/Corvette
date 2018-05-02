package com.leetcode.java.premium.facebook;

public class BestTimeBuySellStock
{
    public static int maxProfit(int[] prices)
    {
        if (prices.length == 0)
        {
            return 0;
        }
        int min = prices[0], maxProfit = 0;

        for (int i = 1; i < prices.length; i++)
        {
            int currentProfit = prices[i] - min;
            if (prices[i] < min)
            {
                min = prices[i];
            }
            if (currentProfit > maxProfit)
            {
                maxProfit = currentProfit;
            }
        }

        return maxProfit;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        int[] prices = { 7, 1, 5, 3, 6, 4 };
        int[] prices1 = { 7 };
        int[] prices2 = {};
        int[] prices3 = { 2, 4, 1 };
        System.out.println(maxProfit(prices3));
    }

}
