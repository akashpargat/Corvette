package com.leetcode.java.solutions;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

/* 
Suppose we have some input in the form of lists of lists. Each list has a length of at least 3.

Each list consists of N elements but contains only 2 different values -- a "default" number that appears N-1 times, and an "outlier" number that only appears once. (For example, in the list [2, 2, 6, 2], the outlier is 6.)

Write a function that, for a given list of lists, returns the outlier from each list. Lists are guaranteed to contain exactly one outlier.


lists = [[1, 2, 1], [2, 2, 2, 2, 2, 6, 2], [3, 1, 1, 1], [9, 9, 4]]


# Expected output: 2, 6, 3, 4

*/

class Solution_Indeed_Karat
{
    public static void main(String[] args)
    {
        List<List<Integer>> inputLists = Arrays.asList(Arrays.asList(1, 2, 1),
                Arrays.asList(2, 2, 2, 2, 2, 6, 2), Arrays.asList(3, 1, 1, 1),
                Arrays.asList(9, 9, 4));

        for (int i : getNumber(inputLists))
        {
            System.out.println(i);
        }
    }

    public static List<Integer> getNumber(List<List<Integer>> input)
    {

        Map<Integer, Integer> result = new HashMap<>();
        List<Integer> finalResult = new ArrayList<>();
        int count = 0;
        for (List<Integer> value : input)
        {
            System.out.println("");
            ;
            for (Integer num : value)
            {
                if (result.containsKey(num))
                {
                    result.put(num, result.get(num) + 1);
                    continue;
                }
                result.put(num, 1);

            }

            Set<Entry<Integer, Integer>> entry = result.entrySet();
            for (Entry<Integer, Integer> entr : entry)
            {
                System.out.println(entr.getKey() + ":" + entr.getValue());
                if (entr.getValue() <= 1)
                {
                    finalResult.add(entr.getKey());
                    // System.out.println(entr.getKey());
                }

            }
            result = new HashMap<>();
        }

        return finalResult;

    }
}
