package com.leetcode.java.solutions;

import java.util.Arrays;
import java.util.List;

public class KeyboardRow
{
    private static final List<Character> TOP = Arrays.asList('Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I',
            'O', 'P');
    private static final List<Character> MIDDLE = Arrays.asList('A', 'S', 'D', 'F', 'G', 'H', 'J',
            'K', 'L');
    private static final List<Character> BOTTOM = Arrays.asList('Z', 'X', 'C', 'V', 'B', 'N', 'M');

    public static String[] findWords(String[] words)
    {
        for (int i = 0; i < words.length; i++)
        {
            char[] val = words[i].toCharArray();
            boolean top = false;
            boolean middle = false;
            boolean bottom = false;
            for (int j = 0; j < val.length; j++)
            {
                if (TOP.contains(val[j]) && !middle && !bottom)
                {
                    System.out.println(words[i]);
                }
                if (MIDDLE.contains(val[j]) && !top && !bottom)
                {
                    System.out.println(words[i]);
                }
                if (BOTTOM.contains(val[j]) && !middle && !top)
                {
                    System.out.println(words[i]);
                }
            }
        }
        return null;
    }

    public static void main(String[] args)
    {
        String[] words = { "Hello", "Alaska", "Dad", "Peace" };
        String[] result = findWords(words);
        // TODO Auto-generated method stub
        for (int i = 0; i < result.length; i++)
        {
            System.out.println(result[i]);
        }
    }
}
