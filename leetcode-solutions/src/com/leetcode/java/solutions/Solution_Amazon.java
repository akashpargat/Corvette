package com.leetcode.java.solutions;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class Solution_Amazon
{
    public static List<String> integerString = new ArrayList<>();
    public static Map<String, String> myStr = new HashMap<>();
    static LinkedHashMap<String, String> sort = new LinkedHashMap<>();

    public static List<String> reorderLines(int logFileSize, List<String> logLines)
    {
        for (String str : logLines)
        {
            String[] val = str.split(" ");
            String[] yourArray = Arrays.copyOfRange(val, 1, val.length);
            String secondString = convertStringArrayToString(yourArray, "");
            System.out.println(secondString);
            if (isNumeric(String.valueOf(val[1])))
            {
                integerString.add(str);
                continue;
            }

            myStr.put(val[0], secondString);

            sort = sortHashMapByValues(myStr);
            System.out.println(sort);
            for (int i = 0; i < val.length; i++)
            {

            }

        }
        sort.putAll(myStr);
        return logLines;
        // WRITE YOUR CODE HERE
    }

    private static String convertStringArrayToString(Object[] arr, String delimiter)
    {
        StringBuilder sb = new StringBuilder();
        for (Object obj : arr)
            sb.append(obj.toString()).append(delimiter);
        return sb.substring(0, sb.length());

    }

    public static boolean isNumeric(String str)
    {
        try
        {
            double d = Double.parseDouble(str);
        }
        catch (NumberFormatException nfe)
        {
            return false;
        }
        return true;
    }

    public static LinkedHashMap<String, String> sortHashMapByValues(Map<String, String> myStr2)
    {
        List<String> mapKeys = new ArrayList<>(myStr2.keySet());
        List<String> mapValues = new ArrayList<>(myStr2.values());
        Collections.sort(mapValues);
        Collections.sort(mapKeys);

        LinkedHashMap<String, String> sortedMap = new LinkedHashMap<>();

        Iterator<String> valueIt = mapValues.iterator();
        while (valueIt.hasNext())
        {
            String val = valueIt.next();
            Iterator<String> keyIt = mapKeys.iterator();

            while (keyIt.hasNext())
            {
                String key = keyIt.next();
                String comp1 = myStr2.get(key);
                String comp2 = val;

                if (comp1.equals(comp2))
                {
                    keyIt.remove();
                    sortedMap.put(key, val);
                    break;
                }
            }
        }
        return sortedMap;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        List<String> myString = new ArrayList<>();
        myString.add("z0 akas bah cas");
        myString.add("ds34 erwer43 bah cas");
        myString.add("rt2 uyju bah cas");
        myString.add("123ds 10 12 1");
        myString.add("d0 9 7 8");

        reorderLines(5, myString);
    }

}
