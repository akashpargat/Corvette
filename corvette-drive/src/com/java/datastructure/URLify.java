package com.java.datastructure;

import java.util.HashMap;
import java.util.Map;

public class URLify
{
    public static int countBlankSpace(String str)
    {
        int count = 0;
        char[] actualString = str.toCharArray();
        for (int i = 0; i < actualString.length; i++)
        {
            if (actualString[i] == ' ')
            {
                count++;
            }
        }
        return count;
    }

    public static char[] urlIfy(String str)
    {
        int newStringLength = str.length() + countBlankSpace(str) * 2;
        char[] oldString = str.toCharArray();
        char[] newString = new char[newStringLength];

        for (int i = oldString.length - 1; i >= 0; i--)
        {
            if (oldString[i] == ' ')
            {
                newString[newStringLength - 1] = '0';
                newString[newStringLength - 2] = '2';
                newString[newStringLength - 3] = '%';
                newStringLength = newStringLength - 3;
            }
            else
            {
                newString[newStringLength - 1] = oldString[i];
                newStringLength--;
            }
        }

        return newString;
    }

    Map<Integer, String> map = new HashMap();
    String host = "http://tinyurl.com/";

    public String encode(String longUrl)
    {
        int key = longUrl.hashCode();
        map.put(key, longUrl);
        return host + key;
    }

    public String decode(String shortUrl)
    {
        int key = Integer.parseInt(shortUrl.replace(host, ""));
        return map.get(key);
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        System.out.println(urlIfy("Yo Mr. Diggle how is it going?"));
    }
}
