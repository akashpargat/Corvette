package com.leetcode.java.premium.facebook;

public class DecodeWays
{
    public static int numDecodings(String s)
    {
        if (s.isEmpty())
        {
            return 0;
        }
        int n = s.length();
        if (n == 0)
            return 0;

        int[] memo = new int[n + 1];
        memo[n] = 1;
        memo[n - 1] = s.charAt(n - 1) != '0' ? 1 : 0;

        for (int i = n - 2; i >= 0; i--)
            if (s.charAt(i) == '0')
                continue;
            else
                memo[i] = (Integer.parseInt(s.substring(i, i + 2)) <= 26)
                        ? memo[i + 1] + memo[i + 2]
                        : memo[i + 1];

        return memo[0];
    }

    public static int decodeDp(String message)
    {
        int msgLen = message.length();
        int[] decodeCount = new int[msgLen + 1];

        decodeCount[0] = 1;
        decodeCount[1] = 1;

        for (int i = 2; i < msgLen + 1; i++)
        {
            if (message.charAt(i - 1) > '0')
                decodeCount[i] = decodeCount[i - 1];

            if ((message.charAt(i - 2) < '2')
                    || (message.charAt(i - 2) == '2' && message.charAt(i - 1) < '7'))
                decodeCount[i] = decodeCount[i] + decodeCount[i - 2];
        }

        return decodeCount[msgLen];
    }

    private static int myDecode(String stringToDecode)
    {
        int length = stringToDecode.length();
        int[] memo = new int[length + 1];

        memo[0] = 1;
        memo[1] = 1;
        for (int i = 2; i < length + 1; i++)
        {
            if (stringToDecode.charAt(i - 1) > '0')
            {
                memo[i] = memo[i - 1];
            }
            if (stringToDecode.charAt(i - 2) < '2'
                    || (stringToDecode.charAt(i - 2) == '2' && stringToDecode.charAt(i - 1) < '7'))
            {
                memo[i] = memo[i - 1] + memo[i - 2];
            }
        }

        return memo[length];
    }

    public static void main(String[] args)
    {
        System.out.println(myDecode("2321"));
    }

}
