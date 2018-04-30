package com.java.basic.dynamic.programming;

public class LongestCommonPalindromicSubStringDP
{
    public static int countSubstrings_khyade(String s)
    {
        if (s.isEmpty())
        {
            return 0;
        }
        if (s.length() == 1)
        {
            return 1;
        }
        int length = s.length();
        int[][] memo = new int[length + 2][length + 2];
        int count = 0;
        for (int i = 0; i < length + 2; i++)
        {
            memo[i][i] = 1;
        }
        for (int i = 1; i <= length; i++)
        {
            for (int j = 1; j <= i; j++)
            {
                if (s.charAt(i - 1) == s.charAt(j - 1))
                {
                    if (memo[j][i] >= 1)
                    {
                        System.out.print(memo[j][i] + ", ");
                        count++;
                        continue;
                    }
                    memo[j][i] = memo[j + 1][i - 1] + 2;
                    System.out.print(memo[j][i] + ", ");
                    count++;
                }
                else
                {
                    memo[j][i] = 0;
                    System.out.print(memo[j][i] + ", ");
                }
            }
            System.out.println();
        }
        return count;
    }

    public static int countSubstrings(String s)
    {
        if (s.isEmpty())
        {
            return 0;
        }
        if (s.length() == 1)
        {
            return 1;
        }
        int length = s.length();
        boolean[][] memo = new boolean[length + 2][length + 2];
        int count = 0;
        for (int i = 0; i < length; i++)
        {
            memo[i][i] = true;
        }
        for (int i = 0; i <= length; i++)
        {
            for (int j = 0; j <= i; j++)
            {
                if (s.charAt(i) == s.charAt(j))
                {
                    memo[i][j] = true;
                    System.out.print(memo[i][j] + ", ");
                    count++;
                }
                else
                {
                    memo[i][j] = false;
                    System.out.print(memo[i][j] + ", ");
                }
            }
            System.out.println();
        }
        return count;
    }

    public static String longestPalindrome(String s)
    {
        if (s == null || s.length() <= 1)
        {
            return s;
        }

        int len = s.length();
        int maxLen = 1;
        boolean[][] dp = new boolean[len][len];

        String longest = null;
        for (int l = 0; l < len; l++)
        {
            for (int i = 0; i < len - l; i++)
            {
                int j = i + l;
                if (s.charAt(i) == s.charAt(j) && (j - i <= 2 || dp[i + 1][j - 1]))
                {
                    dp[i][j] = true;

                    if (j - i + 1 > maxLen)
                    {
                        maxLen = j - i + 1;
                        longest = s.substring(i, j + 1);
                    }
                }
            }
        }

        return longest;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        // System.out.println(countSubstrings("fdskdf"));
        System.out.println(longestPalindrome("fdskdf"));
    }

}
