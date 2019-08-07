package com.java.dynamic.programming.tabulation;

import java.util.Arrays;

public class MinimumStepsToReachOne
{

    public static int minSteps(int N)
    {

        int dp[] = new int[N + 1];
        Arrays.fill(dp, Integer.MAX_VALUE);
        dp[1] = 0;
        for (int i = 2; i <= N; i++)
        {
            if (i % 2 == 0 && i >= 1)
            {
                dp[i] = Math.min(dp[i / 2] + 1, dp[i - 1] + 1);
            }
            if (i % 3 == 0 && i >= 1)
            {
                dp[i] = Math.min(dp[i / 3] + 1, dp[i]);
            }
            dp[i] = Math.min(dp[i - 1] + 1, dp[i]);
        }
        return dp[N];
    }

    public static void main(String[] args)
    {
        System.out.println(minSteps(949415));
    }

}
