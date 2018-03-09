package com.java.datastructure;

import java.util.HashMap;

public class PalindromePErmutation
{
    public static String isPalindrome(String str)
    {
        char[] strArray = str.toCharArray();
        int index = str.length() - 1;
        for (int i = 0; i < str.length(); i++)
        {
            if (strArray[i] == ' ')
            {
                i++;
            }
            if (strArray[index] == ' ')
            {
                index--;
            }
            if (strArray[i] != strArray[index])
            {
                return "The give string is not a palindrome.";
            }
            index--;
        }
        return "The given string is a palindrome.";
    }

    public static void main(String[] args)
    {
        System.out.println(isPalindrome("?eva, can i stab bats in a c,ave?"));

        System.out.println(canPermutePalindrome("?eva, can i stab bats in a c,ave?"));
    }

    public static boolean canPermutePalindrome(String s)
    {
        HashMap<Character, Integer> map = new HashMap<>();
        for (int i = 0; i < s.length(); i++)
        {
            map.put(s.charAt(i), map.getOrDefault(s.charAt(i), 0) + 1);
        }
        int count = 0;
        for (char key : map.keySet())
        {
            count += map.get(key) % 2;
        }
        return count <= 1;
    }
}
