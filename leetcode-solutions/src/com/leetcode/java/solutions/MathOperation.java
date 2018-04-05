package com.leetcode.java.solutions;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MathOperation
{

    public static int divide(int dividend, int divisor)
    {
        if (dividend == Integer.MIN_VALUE && divisor == -1)
            return Integer.MAX_VALUE;
        if (dividend > 0 && divisor > 0)
            return divideHelper(-dividend, -divisor);
        else if (dividend > 0)
            return -divideHelper(-dividend, divisor);
        else if (divisor > 0)
            return -divideHelper(dividend, -divisor);
        else
            return divideHelper(dividend, divisor);
    }

    private static int divideHelper(int dividend, int divisor)
    {
        // base case
        if (divisor < dividend)
            return 0;
        // get highest digit of divisor
        int cur = 0, res = 0;
        while ((divisor << cur) >= dividend && divisor << cur < 0 && cur < 31)
            cur++;
        res = dividend - (divisor << cur - 1);
        if (res > divisor)
            return 1 << cur - 1;
        return (1 << cur - 1) + divide(res, divisor);
    }

    public static void main(String[] args)
    {
        System.out.println("The result is " + divide(7, 3));

        System.out.println(1 / 2);
        subdomainVisits(new String[] { "900 google.mail.com", "50 yahoo.com", "1 intel.mail.com",
                "5 wiki.org" });
    }

    public static List<String> subdomainVisits(String[] cpdomains)
    {
        List<String> ans = new ArrayList<>();
        if (cpdomains == null)
        {
            return ans;
        }
        Map<String, Integer> map = new HashMap<>();
        for (String pair : cpdomains)
        {
            String[] record = pair.split(" ");
            int freq = Integer.parseInt(record[0]);
            String domain = record[1];
            while (domain.indexOf(".") != -1)
            {
                int idx = domain.indexOf(".");
                if (!map.containsKey(domain))
                {
                    map.put(domain, 0);
                }
                map.put(domain, map.get(domain) + freq);
                domain = domain.substring(idx + 1);
            }
            if (!map.containsKey(domain))
            {
                map.put(domain, 0);
            }
            map.put(domain, map.get(domain) + freq);
        }
        for (Map.Entry<String, Integer> entry : map.entrySet())
        {
            ans.add(entry.getValue() + " " + entry.getKey());
        }
        return ans;
    }
}
