package com.leetcode.java.solutions;

import org.apache.commons.lang3.StringUtils;

/**
 * Given a string, find the length of the longest substring without repeating characters.
 * Examples:Given "abcabcbb", the answer is "abc", which the length is 3. Given "bbbbb", the answer
 * is "b", with the length of 1. Given "pwwkew", the answer is "wke", with the length of 3.<br>
 * Note that the answer must be a substring, "pwke" is a subsequence and not a substring.
 * 
 * @author Akash Pargat
 */
public class LongestSubstringWithoutRepeatingCharacters
{

    /**
     * Gets the longest sub string length.
     * 
     * @param word
     * @return
     */
    private static int getLongestSubstringLength(final String word)
    {
        int result = 0;
        int[] cache = new int[256];
        if (word == StringUtils.EMPTY)
        {
            return 0;
        }
        if (word.length() == 1)
        {
            return 1;
        }
        for (int i = 0, j = 0; i < word.length(); i++)
        {
            j = (cache[word.charAt(i)] > 0) ? Math.max(j, cache[word.charAt(i)]) : j;
            cache[word.charAt(i)] = i + 1;
            result = Math.max(result, i - j + 1);
        }
        return result;
    }

    public static void main(String[] args)
    {
        // Test suite one
        System.out.println(getLongestSubstringLength("kddcadeypzday"));
        // Test suite two
        System.out.println(getLongestSubstringLength("aaaaaaa"));
        // Test suite three
        System.out.println(getLongestSubstringLength(""));
    }

}
