package com.java.basic.dynamic.programming;

/**
 * Step to generate the memorization matrix: 1. We have to move diagonally 2.
 * 
 * @author Akash
 *
 */
public class LongestCommonSubSequenceDynamicProgramming
{
    static int max = Integer.MIN_VALUE;
    static int row = 0;
    static int column = 0;

    private static int[][] getLongestCommonSubSequenceMemo(final String firstString,
            final String secondString)
    {
        int firstLength = firstString.length();
        int secondLength = secondString.length();
        char[] firstStringArr = firstString.toCharArray();
        char[] secondStringArr = secondString.toCharArray();
        int[][] arr = new int[firstLength + 1][secondLength + 1];
        for (int i = 1; i <= firstLength; i++)
        {
            for (int j = 1; j <= secondLength; j++)
            {
                if (firstStringArr[i - 1] == secondStringArr[j - 1])
                {
                    arr[i][j] = arr[i - 1][j - 1] + 1;
                    if (arr[i][j] > max)
                    {
                        max = arr[i][j];
                        row = i;
                        column = j;
                    }
                    System.out.print(arr[i][j] + ", ");
                }
                else
                {
                    arr[i][j] = Math.max(arr[i][j - 1], arr[i - 1][j]);
                    System.out.print(arr[i][j] + ", ");
                }
            }
            System.out.println();
        }
        return arr;
    }

    private static void getLongestSubSequenceLength(final int[][] arr, String firstString)
    {

    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        getLongestSubSequenceLength(getLongestCommonSubSequenceMemo("kdmadamns", "aksmadamwde"),
                "kdmadamns");
        System.out.println(max + "*************************************");
        flush();
        getLongestSubSequenceLength(getLongestCommonSubSequenceMemo("abbcsddsdd", "jdsbcswewew"),
                "abbcsddsdd");
        System.out.println(max + "*************************************");
        flush();
        getLongestSubSequenceLength(getLongestCommonSubSequenceMemo("akash", "cash"), "cash");
        System.out.println(max + "*************************************");
        flush();
        getLongestSubSequenceLength(getLongestCommonSubSequenceMemo("bqdrcvefgh", "abcvdefgh"),
                "bqdrcvefgh");
        System.out.println(max + "*************************************");
    }

    private static void flush()
    {
        max = 0;
        row = 0;
        column = 0;
    }

}
