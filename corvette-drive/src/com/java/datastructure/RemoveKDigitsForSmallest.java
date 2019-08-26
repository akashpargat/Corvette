package com.java.datastructure;

public class RemoveKDigitsForSmallest
{
    public String removeKdigits(String num, int k)
    {
        int len = num.length();
        int outLen = len - k - 1;
        char out[] = new char[len];
        int min = Integer.MAX_VALUE;
        for (int i = 0; i < len; i++)
        {
            while (i <= outLen)
            {
                if (Integer.parseInt(String.valueOf(num.charAt(i))) <= min)
                {
                    out[i] = num.charAt(i);
                    min = Integer.parseInt(String.valueOf(num.charAt(i + 1)));
                    break;
                }
                i++;
            }
        }

        return String.valueOf(out);
    }

    public static void main(String[] args)
    {
        RemoveKDigitsForSmallest val = new RemoveKDigitsForSmallest();
        System.out.println(val.removeKdigits("10121341", 3));
    }

}
