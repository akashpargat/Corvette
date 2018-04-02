package com.leetcode.java.solutions;

import java.util.ArrayList;

import org.apache.commons.lang3.StringUtils;

/**
 * 6. ZigZag Conversion<br>
 * The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this:
 * (you may want to display this pattern in a fixed font for better legibility)<br>
 * P A H N<br>
 * A P L S I I G<br>
 * Y I R <br>
 * And then read line by line: "PAHNAPLSIIGYIR"<br>
 * Write the code that will take a string and make this conversion given a number of rows: string
 * convert(string text, int nRows); convert("PAYPALISHIRING", 3) should return "PAHNAPLSIIGYIR".
 * 
 * @author Akash Pargat
 */
public class ZigZagConversion
{
    public String convert(String zigZagString, int numRows)
    {
        if (numRows <= 0)
        {
            return StringUtils.EMPTY;
        }
        @SuppressWarnings("unchecked")
        ArrayList<Character>[] rows = new ArrayList[numRows];
        for (int i = 0; i < numRows; i++)
        {
            rows[i] = new ArrayList<Character>();
        }
        for (int i = 0, n = zigZagString.length(); i < zigZagString.length();)
        {
            for (int j = 0; i < n && j < numRows; j++, i++)
            {
                rows[j].add(zigZagString.charAt(i));
            }
            for (int j = numRows - 2; i < n && j > 0; j--, i++)
            {
                rows[j].add(zigZagString.charAt(i));
            }
        }
        StringBuilder stringBuilder = new StringBuilder(zigZagString.length());
        for (int row = 0; row < numRows; row++)
        {
            for (int j = 0, rowLen = rows[row].size(); j < rowLen; j++)
            {
                stringBuilder.append(rows[row].get(j));
            }
        }
        return stringBuilder.toString();
    }

    public static void main(String[] args)
    {
        // Test case Suite one
        ZigZagConversion zigZag = new ZigZagConversion();
        System.out.println(zigZag.convert("OurTeamIsHiring", 4));
        // Test case Suite two
        System.out.println(zigZag.convert("HI", 4));
        // Test case Suite Three
        System.out.println(zigZag.convert("H", 0));
        // Test case Suite Four
        System.out.println(zigZag.convert(StringUtils.EMPTY, 0));
        // Test case Suite Four
        System.out.println(zigZag.convert("HeyCanYouBringMeTheSoda....Please!!!!", 1));
        // Test case Suite Five
        System.out.println(zigZag.convert("Hey Can You Bring Me The Soda....Please!!!!", 10));
    }
}
