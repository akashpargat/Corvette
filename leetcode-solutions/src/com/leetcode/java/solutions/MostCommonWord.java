package com.leetcode.java.solutions;

import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

public class MostCommonWord
{

    public static String mostCommonWord(String paragraph, String[] banned)
    {
        Map<String, Integer> freq = new HashMap<>();
        if (paragraph.isEmpty())
        {
            return "";
        }
        String alphaNumericStr = paragraph.replaceAll("[^a-zA-Z0-9]", " ").toLowerCase();
        String[] arr = alphaNumericStr.split(" ");
        for (String ss : arr)
        {
            if (freq.containsKey(ss))
            {
                freq.put(ss, freq.get(ss) + 1);
                continue;
            }
            freq.put(ss, 1);
        }

        for (int i = 0; i < banned.length; i++)
        {
            if (freq.containsKey(banned[i]))
            {
                freq.remove(banned[i]);
            }
        }

        Entry<String, Integer> maxEntry = null;

        for (Entry<String, Integer> entry : freq.entrySet())
        {
            if (entry.getKey().isEmpty())
            {
                continue;
            }
            if (maxEntry == null || entry.getValue().compareTo(maxEntry.getValue()) > 0)
            {
                maxEntry = entry;
            }
        }

        Set<Entry<String, Integer>> entry = freq.entrySet();
        for (Entry<String, Integer> entr : entry)
        {
            if (entr.getKey().isEmpty())
            {
                continue;
            }
            // System.out.println(entr.getKey() + ":" + entr.getValue());
            if (entr.getValue() == maxEntry.getValue())
            {
                // finalResult.add(entr.getKey());
                System.out.println(entr.getKey());
                return entr.getKey();
            }

        }
        return null;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        String[] toRemove = { "abc", "abcd", "jeff" };
        mostCommonWord("abc abc? abcd the jeff!", toRemove);
    }

}
