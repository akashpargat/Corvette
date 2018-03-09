package com.java.datastructure;

/**
 * Input: aaabbbbbbccccccdddaaaaaccccbbbb Output: a3b6c6d3a5c4b4
 * 
 * @author AP027887
 */
public class StringCompression
{

    private String compare(final String stringToCompare)
    {
        int count = 0;
        StringBuffer newString = new StringBuffer();
        for (int i = 0; i < stringToCompare.length(); i++)
        {
            if (stringToCompare.charAt(i) != stringToCompare.charAt(i + 1))
            {
                newString.append(stringToCompare.charAt(i));
                newString.append(count);
                count = 0;
            }
            count++;
        }
        return stringToCompare;
    }

    public static void main(String[] args)
    {

    }
}
