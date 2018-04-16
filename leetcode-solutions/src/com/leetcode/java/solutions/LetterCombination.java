package com.leetcode.java.solutions;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

public class LetterCombination
{
    private static final String[] LETTERS = { " ", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", //$NON-NLS-1$ //$NON-NLS-2$ //$NON-NLS-3$ //$NON-NLS-4$ //$NON-NLS-5$ //$NON-NLS-6$ //$NON-NLS-7$ //$NON-NLS-8$
            "tuv", "wxyz" }; //$NON-NLS-1$ //$NON-NLS-2$

    public static List<String> letterCombinations(String digits)
    {
        return (digits.length() == 0) ? Arrays.asList()
                : permute(digits, new StringBuilder(), new ArrayList<>(), 0);
    }

    private static List<String> permute(String digits, StringBuilder result, List<String> results,
            int i)
    {
        if (i == digits.length())
        {
            results.add(result.toString());
        }
        else
        {
            for (char c : LETTERS[Character.digit(digits.charAt(i), 10)].toCharArray())
            {
                result.append(c);
                permute(digits, result, results, i + 1);
                result.deleteCharAt(result.length() - 1);
            }
        }
        return results;
    }

    public static ArrayList<String> letterCombinationsMyWay(String digits)
    {
        ArrayList<String> res = new ArrayList<String>();
        ArrayList<String> preres = new ArrayList<String>();
        res.add("");

        for (int i = 0; i < digits.length(); i++)
        {
            String letters = map.get(digits.charAt(i));
            if (letters.length() == 0)
            {
                continue;
            }
            for (String str : res)
            {
                for (int j = 0; j < letters.length(); j++)
                {
                    preres.add(str + letters.charAt(j));
                }
            }
            res = preres;
            preres = new ArrayList<String>();
        }
        return res;
    }

    static final HashMap<Character, String> map = new HashMap<Character, String>()
    {
        {
            put('1', "");
            put('2', "abc");
            put('3', "def");
            put('4', "ghi");
            put('5', "jkl");
            put('6', "mno");
            put('7', "pqrs");
            put('8', "tuv");
            put('9', "wxyz");
            put('0', "");
        }
    };

    public static void main(String[] args)
    {
        LetterCombination.printCombo(letterCombinations("234"));
        System.out.println("**********");
        LetterCombination.printCombo(letterCombinationsMyWay("234"));
    }

    private static void printCombo(List<String> stringToPrint)
    {
        for (String value : stringToPrint)
        {
            System.out.println(value + " ");
        }
    }
}
