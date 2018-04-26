package com.java.datastructure.linkedlist;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.TreeMap;

public class Dummy
{
    /*
     * Complete the oddNumbers function below.
     */
    static int[] oddNumbers(int l, int r)
    {
        /*
         * Write your code here.
         */
        int[] myArr = new int[r];
        int count = 0;
        for (int i = l; i <= r; i++)
        {
            if (i % 2 != 0)
            {
                myArr[count] = i;
            }
            count++;

            List<Integer> myList = new ArrayList<>();

        }
        return myArr;
    }

    static String[] sortWordsByScore(String[] words)
    {

        Map<Integer, String> myMap = new TreeMap<Integer, String>();
        /*
         * Write your code here.
         */
        for (int i = 0; i < words.length; i++)
        {
            String str = words[i];
            int num = getNumeric(str);
            if (myMap.containsKey(num))
            {

            }
            myMap.put(num, str);
        }
        String[] result = new String[myMap.size()];
        Set<Entry<Integer, String>> entry = myMap.entrySet();
        int count = 0;
        for (Entry<Integer, String> entr : entry)
        {
            result[count] = entr.getValue();
            count++;
        }
        return result;
    }

    private static int getNumeric(String str)
    {
        // TODO Auto-generated method stub
        char[] strChar = str.toCharArray();
        int sum = 0;
        for (int i = 0; i < strChar.length; i++)
        {
            if (strChar[i] == 'a' || strChar[i] == 'A')
            {
                sum += 2;
                continue;
            }
            if (strChar[i] == 'b' || strChar[i] == 'B')
            {
                sum += 2;
                continue;
            }
            if (strChar[i] == 'c' || strChar[i] == 'C')
            {
                sum += 3;
                continue;
            }
            if (strChar[i] == 'd' || strChar[i] == 'D')
            {
                sum += 4;
                continue;
            }
            if (strChar[i] == 'e' || strChar[i] == 'E')
            {
                sum += 10;
                continue;
            }
            if (strChar[i] == 'f' || strChar[i] == 'F')
            {
                sum += 6;
                continue;
            }
            if (strChar[i] == 'g' || strChar[i] == 'G')
            {
                sum += 7;
                continue;
            }
            if (strChar[i] == 'h' || strChar[i] == 'H')
            {
                sum += 8;
                continue;
            }
            if (strChar[i] == 'i' || strChar[i] == 'I')
            {
                sum += 18;
                continue;
            }
            if (strChar[i] == 'j' || strChar[i] == 'J')
            {
                sum += 10;
                continue;
            }
            if (strChar[i] == 'k' || strChar[i] == 'K')
            {
                sum += 11;
                continue;
            }
            if (strChar[i] == 'l' || strChar[i] == 'L')
            {
                sum += 12;
                continue;
            }
            if (strChar[i] == 'm' || strChar[i] == 'M')
            {
                sum += 13;
                continue;
            }
            if (strChar[i] == 'n' || strChar[i] == 'N')
            {
                sum += 14;
                continue;
            }
            if (strChar[i] == 'o' || strChar[i] == 'O')
            {
                sum += 30;
                continue;
            }
            if (strChar[i] == 'p' || strChar[i] == 'P')
            {
                sum += 16;
                continue;
            }
            if (strChar[i] == 'q' || strChar[i] == 'Q')
            {
                sum += 17;
                continue;
            }
            if (strChar[i] == 'r' || strChar[i] == 'R')
            {
                sum += 18;
                continue;
            }
            if (strChar[i] == 's' || strChar[i] == 'S')
            {
                sum += 19;
                continue;
            }
            if (strChar[i] == 't' || strChar[i] == 'T')
            {
                sum += 20;
                continue;
            }
            if (strChar[i] == 'u' || strChar[i] == 'U')
            {
                sum += 42;
                continue;
            }
            if (strChar[i] == 'v' || strChar[i] == 'V')
            {
                sum += 22;
                continue;
            }
            if (strChar[i] == 'w' || strChar[i] == 'W')
            {
                sum += 23;
                continue;
            }
            if (strChar[i] == 'x' || strChar[i] == 'X')
            {
                sum += 24;
                continue;
            }
            if (strChar[i] == 'y' || strChar[i] == 'Y')
            {
                sum += 25;
                continue;
            }
            if (strChar[i] == 'z' || strChar[i] == 'Z')
            {
                sum += 26;
                continue;
            }
        }
        return sum;
    }

    public static void main(String[] args)
    {
        oddNumbers(2, 9);
        String[] sd = { "a", "b" };
        System.out.println(sortWordsByScore(sd));
    }
}
