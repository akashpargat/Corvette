package com.leetcode.java.premium.facebook;

public class ValidPalindrome
{
    public static boolean isPalindrome(String instring)
    {

        // String words = instring.replaceAll("[^a-zA-Z ]", "").toLowerCase().replaceAll("\\s",
        // "");// .split("\\s+"); //$NON-NLS-1$ //$NON-NLS-2$ //$NON-NLS-3$ //$NON-NLS-4$
        String words = instring.replaceAll("\\W", "").toLowerCase();
        char[] ch = words.toCharArray();
        System.out.println(words);
        int j = ch.length - 1;
        for (int i = 0; i < j; i++)
        {
            if (ch[i] != ch[j])
            {
                return false;
            }
            j--;
        }
        return true;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        System.out.println(isPalindrome("A man, a plan, a canal: Panama")); //$NON-NLS-1$
        System.out.println(isPalindrome("race a car")); //$NON-NLS-1$
        System.out.println(isPalindrome("0P")); //$NON-NLS-1$
        System.out.println("**********Opti************");
        System.out.println(isPalindrome_optimized("A man, a plan, a canal: Panama")); //$NON-NLS-1$
        System.out.println(isPalindrome_optimized("race a car")); //$NON-NLS-1$
        System.out.println(isPalindrome_optimized("0P")); //$NON-NLS-1$
    }

    public static boolean isPalindrome_optimized(String s)
    {
        int l = 0;
        int r = s.length() - 1;
        while (l < r)
        {

            if (!isAlpNum(s.charAt(l)))
            {
                l++;
                continue;
            }

            if (!isAlpNum(s.charAt(r)))
            {
                r--;
                continue;
            }

            if (isUpperAndConvertLower(s.charAt(l)) != isUpperAndConvertLower(s.charAt(r)))
            {
                return false;
            }

            l++;
            r--;
        }

        return true;
    }

    private static char isUpperAndConvertLower(char c)
    {
        if (c >= 'A' && c <= 'Z')
        {
            return (char) (c + 'a' - 'A');
        }
        return c;

    }

    private static boolean isAlpNum(char c)
    {
        if (c >= 'A' && c <= 'Z')
        {
            return true;
        }
        if (c >= 'a' && c <= 'z')
        {
            return true;
        }
        if (c >= '0' && c <= '9')
        {
            return true;
        }
        return false;
    }
}
