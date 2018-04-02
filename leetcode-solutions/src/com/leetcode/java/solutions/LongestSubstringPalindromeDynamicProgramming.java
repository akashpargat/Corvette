package com.leetcode.java.solutions;

public class LongestSubstringPalindromeDynamicProgramming
{
    public static String longestPalindrome(String s)
    {
        int length = s.length();
        int palindromeLength = 0;
        char palindrome[] = new char[s.length()];
        boolean memo[][] = new boolean[length][length];
        if (length == 1)
        {
            return s;
        }
        for (int i = 0; i < length; i++)
        {
            for (int j = 0; j < length; j++)
            {
                memo[i][j] = false;
            }
        }
        for (int i = 0; i < length; i++)
        {
            memo[i][i] = true;
            if (s.substring(i, i).length() > palindromeLength)
            {
                palindrome = s.substring(i, i).toCharArray();
                palindromeLength = palindrome.length;
            }
        }
        for (int i = 0; i < length - 1; i++)
        {
            if (s.charAt(i) == s.charAt(i + 1))
            {
                memo[i][i + 1] = true;
                if (s.substring(i, i + 1).length() > palindromeLength)
                {
                    palindrome = s.substring(i, i + 1 + 1).toCharArray();
                    palindromeLength = palindrome.length;
                }
            }
        }
        int j;
        for (int k = 2; k < length; k++)
        {
            for (int i = 0; i < length - k; i++)
            {
                j = i + k;
                if (s.charAt(i) == s.charAt(j) && memo[i + 1][j - 1] == true)
                {
                    if (s.substring(i, j + 1).length() > palindromeLength)
                    {
                        palindrome = s.substring(i, j + 1).toCharArray();
                        palindromeLength = palindrome.length;
                    }
                    memo[i][j] = true;
                }
            }
        }

        if (palindromeLength == 0)
        {
            return String.valueOf(s.charAt(0));
        }
        return String.valueOf(palindrome);
    }

    public static String longestPalindromeSubStringOptimized(String s)
    {
        int start = 0, end = 0;
        for (int i = 0; i < s.length(); i++)
        {
            int len1 = expand(s, i, i);
            int len2 = expand(s, i, i + 1);
            int len = Math.max(len1, len2);
            if (len > end - start)
            {
                start = i - (len - 1) / 2;
                end = i + len / 2;
            }
        }
        return s.substring(start, end + 1);
    }

    private static int expand(String givenString, int startIndex, int endIndex)
    {
        while (startIndex >= 0 && endIndex < givenString.length()
                && givenString.charAt(startIndex) == givenString.charAt(endIndex))
        {
            startIndex--;
            endIndex++;
        }
        return endIndex - startIndex - 1;
    }

    public static void main(String[] args)
    {
        System.out.println(LongestSubstringPalindromeDynamicProgramming.longestPalindrome("abcda")); //$NON-NLS-1$
        System.out.println(LongestSubstringPalindromeDynamicProgramming
                .longestPalindromeSubStringOptimized("baac")); //$NON-NLS-1$
    }

}
