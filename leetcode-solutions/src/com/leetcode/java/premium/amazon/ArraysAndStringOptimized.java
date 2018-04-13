package com.leetcode.java.premium.amazon;

public class ArraysAndStringOptimized
{

    public static void main(String[] args)
    {
        System.out.println(firstUniqChar_optimized(
                "yekbsxznylrwamcaugrqrurvpqybkpfzwbqiysrdnrsnbftvrnszfjbkbmrctjizkjqoxqzddyfnavnhqeblfmzqgsjflghaulbadwqsyuetdelujphmlgtmkoaoijypvcajctbaumeromgejtewbwqptotrorephegyobbstvywljboeihdliknluqdpgampjyjpinxhhqexoctysfdciqjbzilnodzoihihusxluqoayenluziobxiodrfdkinkzzozmxfezfvllpdvogqqtquwcsijwachefspywdgsohqtlquhnoecccgbkrzqcprzmwvygqwddnehhi"));

    }

    public static int firstUniqChar_optimized(String s)
    {

        int resIndex = s.length();

        if (resIndex == 0)
            return -1;

        for (char c = 'a'; c <= 'z'; c++)
        {

            int index = s.indexOf(c);

            if (index != -1 && index == s.lastIndexOf(c))
            {
                resIndex = Math.min(resIndex, index);
            }

        }

        return resIndex == s.length() ? -1 : resIndex;
    }

    public String reverseString_optimized(String s)
    {
        char[] c = s.toCharArray();
        int l = c.length - 1;
        int mid = (l + 1) / 2;
        char t;
        for (int i = 0; i < mid; i++)
        {
            t = c[i];
            c[i] = c[l - i];
            c[l - i] = t;
        }
        return String.valueOf(c);
    }

}
