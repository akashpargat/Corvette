package com.java.basic.dynamic.programming;

/**
 * 
 * Steps to generate the matrix: 1. If the value at i, j is not same then put 0 at the location. 2.
 * If the value matches then add i-1,j-1 (diagonal) + 1
 * 
 * To get the value look for the max in the matrix and then see where that value came from until
 * reached zero(Tricky but lets see....)
 * 
 * @author Akash
 *
 */
public class LongestCommonSubStringDynamicProgramming
{
    static int max = Integer.MIN_VALUE;
    static int row = 0;
    static int column = 0;

    private static int[][] getLongestCommonSubStringMemo(final String firstString,
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
                    arr[i][j] = 0;
                    System.out.print(arr[i][j] + ", ");
                }
            }

            System.out.println();
        }

        return arr;
    }

    private static void getLongestSubstringLength(final int[][] arr, String firstString)
    {

        char[] myStr = firstString.toCharArray();
        System.out.println("The longest common substring is: ");

        for (int i = max; i > 0; i--)
        {
            column--;
            System.out.println(myStr[column]);
        }
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        getLongestSubstringLength(getLongestCommonSubStringMemo("kdmadamns", "aksmadamwde"),
                "kdmadamns");
        System.out.println(max + "*************************************");
        flush();
        getLongestSubstringLength(getLongestCommonSubStringMemo("abbcsddsdd", "jdsbcswewew"),
                "abbcsddsdd");
        System.out.println(max + "*************************************");
        flush();
        getLongestSubstringLength(getLongestCommonSubStringMemo("akash", "cash"), "cash");
        System.out.println(max + "*************************************");
    }

    private static void flush()
    {
        max = 0;
        row = 0;
        column = 0;
    }
}
