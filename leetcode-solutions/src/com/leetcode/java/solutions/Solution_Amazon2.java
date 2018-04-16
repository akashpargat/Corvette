package com.leetcode.java.solutions;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

public class Solution_Amazon2
{
    public static List<String> retrieveMostFrequentlyUsedWords(String literatureText,
            List<String> wordsToExclude)
    {
        Map<String, Integer> freq = new HashMap<>();
        List<String> finalResult = new ArrayList<>();
        if (literatureText.isEmpty())
        {
            return finalResult;
        }
        String alphaNumericStr = literatureText.replaceAll("[^a-zA-Z0-9]", " ");
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

        for (int i = 0; i < wordsToExclude.size(); i++)
        {
            if (freq.containsKey(wordsToExclude.get(i)))
            {
                freq.remove(wordsToExclude.get(i));
            }
        }

        Entry<String, Integer> maxEntry = null;

        for (Entry<String, Integer> entry : freq.entrySet())
        {
            if (maxEntry == null || entry.getValue().compareTo(maxEntry.getValue()) > 0)
            {
                maxEntry = entry;
            }
        }

        Set<Entry<String, Integer>> entry = freq.entrySet();
        for (Entry<String, Integer> entr : entry)
        {
            System.out.println(entr.getKey() + ":" + entr.getValue());
            if (entr.getValue() == maxEntry.getValue())
            {
                finalResult.add(entr.getKey());
                // System.out.println(entr.getKey());
            }

        }
        return finalResult;
    }
    // METHOD SIGNATURE ENDS

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        List<String> toRemove = new ArrayList<>();
        // toRemove.add("is");
        // toRemove.add("and");
        // toRemove.add("this");

        retrieveMostFrequentlyUsedWords(
                "Yo this is Akash with akash and his friend friend akash nice akash akash Akash hey friend friend",
                toRemove);
    }

}
