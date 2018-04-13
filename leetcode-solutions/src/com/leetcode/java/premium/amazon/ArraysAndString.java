package com.leetcode.java.premium.amazon;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

public class ArraysAndString
{
    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        // leectode:
        // Answer: t

        System.out.println(firstUniqChar(
                "yekbsxznylrwamcaugrqrurvpqybkpfzwbqiysrdnrsnbftvrnszfjbkbmrctjizkjqoxqzddyfnavnhqeblfmzqgsjflghaulbadwqsyuetdelujphmlgtmkoaoijypvcajctbaumeromgejtewbwqptotrorephegyobbstvywljboeihdliknluqdpgampjyjpinxhhqexoctysfdciqjbzilnodzoihihusxluqoayenluziobxiodrfdkinkzzozmxfezfvllpdvogqqtquwcsijwachefspywdgsohqtlquhnoecccgbkrzqcprzmwvygqwddnehhi"));

        System.out.println(reverseString("Akash is my friend?"));
        char[] rotate = "Akash is my friend?".toCharArray();
        reverseWords(rotate);
    }

    public static int firstUniqChar(String s)
    {
        char unique = getUniqueChar(s);
        if (unique == 'f')
        {
            return -1;
        }
        for (int i = 0; i < s.length(); i++)
        {
            if (s.charAt(i) == unique)
            {
                return i;
            }
        }
        return -1;
    }

    private static char getUniqueChar(String s)
    {
        Map<Character, Integer> myMap = new LinkedHashMap<>();
        for (int i = 0; i < s.length(); i++)
        {
            if (myMap.containsKey(s.charAt(i)))
            {
                myMap.put(s.charAt(i), myMap.get(s.charAt(i)) + 1);
                continue;
            }
            myMap.put(s.charAt(i), 1);
        }
        Set<Entry<Character, Integer>> set = myMap.entrySet();
        int count = 0;
        for (Entry<Character, Integer> ch : set)
        {
            count = count + ch.getValue();
            if (ch.getValue() == 1)
            {
                return ch.getKey();
            }
        }
        return 'f';
    }

    public static String reverseString(String s)
    {
        char[] sChar = s.toCharArray();
        int start = 0;
        int end = s.length() - 1;
        char temp;
        while (start < end)
        {
            temp = sChar[end];
            sChar[end] = sChar[start];
            sChar[start] = temp;
            start++;
            end--;
        }

        return String.valueOf(sChar);
    }

    public static void reverseChar(char[] sChar, int start, int end)
    {
        // int start = 0;
        // int end = s.length() - 1;
        char temp;
        while (start < end)
        {
            temp = sChar[end];
            sChar[end] = sChar[start];
            sChar[start] = temp;
            start++;
            end--;
        }
    }

    public static void reverseWords(char[] str)
    {
        reverseChar(str, 0, str.length - 1);
        int i = 0;
        while (true)
        {

        }
    }

}
