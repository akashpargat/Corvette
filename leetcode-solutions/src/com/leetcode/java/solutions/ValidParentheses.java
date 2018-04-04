package com.leetcode.java.solutions;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.Map;

public class ValidParentheses
{

    public boolean isValid_misLeading(String s)
    {
        char[] stringArray = s.toCharArray();
        Map<Character, Integer> myMap = new HashMap<>();
        for (int i = 0; i < stringArray.length; i++)
        {
            if (!myMap.containsKey(stringArray[i]))
            {
                myMap.put(stringArray[i], 1);
            }
            else
            {
                myMap.put(stringArray[i], myMap.get(stringArray[i]) + 1);
            }

        }
        char[] validData = { '(', ')', '{', '}', '[', ']' };
        for (int i = 0; i < validData.length - 1; i++)
        {
            if (myMap.get(validData[i]) == myMap.get(validData[i + 1])
                    && myMap.get(validData[i]) != null && myMap.get(validData[i + 1]) != null)
            {
                return true;
            }
            i++;
        }
        return false;
    }

    public boolean isValid(String s)
    {
        if ((s.length() & 1) == 1)
            return false;
        else
        {
            Deque<Character> p = new ArrayDeque<>(s.length());
            for (int i = 0; i < s.length(); i++)
                switch (s.charAt(i))
                {
                    case '(':
                        p.push(')');
                        break;
                    case '{':
                        p.push('}');
                        break;
                    case '[':
                        p.push(']');
                        break;
                    case ')':
                    case '}':
                    case ']':
                        if (p.isEmpty() || p.pop() != s.charAt(i))
                            return false;
                }
            return p.isEmpty();
        }
    }

    public static void main(String[] args)
    {
        new ValidParentheses().isValid("()");
    }

}
