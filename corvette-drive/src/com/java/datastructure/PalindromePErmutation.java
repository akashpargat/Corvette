package com.java.datastructure;

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
    }
}
