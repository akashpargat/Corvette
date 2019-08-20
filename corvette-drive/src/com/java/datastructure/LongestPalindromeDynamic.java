package com.java.datastructure;

import java.util.HashMap;
import java.util.Map;

public class LongestPalindromeDynamic
{

    public int longestPalindrome(String s)
    {
        Map<Character, Integer> myMap = new HashMap<Character, Integer>();
        for (int i = 0; i < s.length(); i++)
        {
            if (myMap.containsKey(s.charAt(i)))
            {
                myMap.put(s.charAt(i), (myMap.get(s.charAt(i)) + 1));
                continue;
            }
            myMap.put(s.charAt(i), 1);
        }
        int count = 0;
        boolean odd = false;
        for (Integer myVal : myMap.values())
        {
            if (myVal == 1)
            {
                odd = true;
            }
            if (myVal > 1 && myVal % 2 == 0)
            {
                count = myVal + count;
                continue;
            }
            if (myVal > 1 && myVal % 2 != 0)
            {
                count = myVal + count - 1;
                odd = true;
            }
        }
        if (odd)
        {
            return count + 1;
        }
        return count;
    }

    public static void main(String[] args)
    {
        LongestPalindromeDynamic myPal = new LongestPalindromeDynamic();
        System.out.println(myPal.longestPalindrome("bb"));
    }

}
