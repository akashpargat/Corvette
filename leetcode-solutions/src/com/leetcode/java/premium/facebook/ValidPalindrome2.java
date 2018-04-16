package com.leetcode.java.premium.facebook;

public class ValidPalindrome2
{
    public static boolean isPalindrome(String words)
    {

        // String words = instring.replaceAll("[^a-zA-Z ]", "").toLowerCase().replaceAll("\\s",
        // "");// .split("\\s+"); //$NON-NLS-1$ //$NON-NLS-2$ //$NON-NLS-3$ //$NON-NLS-4$
        // char[] ch = words.toCharArray();
        System.out.println(words);
        int j = words.length() - 1;
        int count = 0;
        StringBuilder sb1 = new StringBuilder(words);
        StringBuilder sb2 = new StringBuilder(words);
        for (int i = 0; i <= j; i++)
        {
            if (words.charAt(i) != words.charAt(j))
            {
                if (ValidPalindrome.isPalindrome_optimized(sb1.deleteCharAt(i).toString()))
                {
                    return true;
                }
                else if (ValidPalindrome.isPalindrome_optimized(sb2.deleteCharAt(j).toString()))
                {
                    j--;
                    return true;
                }
                else
                {
                    return false;
                }
            }
            j--;
        }
        return true;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        System.out.println(isPalindrome("amanaplanacanalpanama")); //$NON-NLS-1$
        System.out.println(isPalindrome("raceacar")); //$NON-NLS-1$
        System.out.println(isPalindrome("ak")); //$NON-NLS-1$
        System.out.println(isPalindrome("abca")); //$NON-NLS-1$
        System.out.println(isPalindrome("abc")); //$NON-NLS-1$
        System.out.println(isPalindrome("deeee")); //$NON-NLS-1$
        System.out.println(isPalindrome("abbbac")); //$NON-NLS-1$
        System.out.println("**********Opti************"); //$NON-NLS-1$
    }

    private boolean isPalindromeInRange(char[] schars, int i, int j)
    {
        int start = i, end = j;
        while (start <= end)
        {
            if (schars[start] != schars[end])
            {
                return false;
            }
            start++;
            end--;
        }
        return true;
    }

    public boolean validPalindrome_optimized(String s)
    {
        char[] schars = s.toCharArray();
        int start = 0, end = schars.length - 1;
        while (start <= end)
        {
            if (schars[start] != schars[end])
            {
                return isPalindromeInRange(schars, start + 1, end)
                        || isPalindromeInRange(schars, start, end - 1);
            }
            start++;
            end--;
        }
        return true;
    }
}
