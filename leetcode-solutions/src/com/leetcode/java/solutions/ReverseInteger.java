package com.leetcode.java.solutions;

public class ReverseInteger
{
    // Fails when the number passed in is really close to the allowed limit of int.
    // 2,147,483,647
    public int reverse_Bad(int x)
    {
        int reversedInt = 0;
        String str = String.valueOf(x);

        for (int i = 0; i < str.length(); i++)
        {
            reversedInt = reversedInt + x % 10;
            reversedInt = reversedInt * 10;
            x = x / 10;
        }
        if (reversedInt < 0)
        {
            reversedInt = reversedInt / 10;
        }
        return reversedInt / 10;
    }

    /**
     * 
     * @param x
     * @return
     */
    public int reverse(int x)
    {
        boolean isLessThanZero = false;
        if (x < 0)
        {
            isLessThanZero = true;
            x = Math.abs(x);
        }
        char temp = 0;
        char[] charArr = Integer.toString(x).toCharArray();
        for (int i = 0; i < charArr.length - 1; i++)
        {
            temp = charArr[i];
            charArr[i] = charArr[charArr.length - i - 1];
            charArr[charArr.length - i - 1] = temp;
        }
        int reverseNumber = Integer.parseInt(String.copyValueOf(charArr));
        if (isLessThanZero)
        {
            return reverseNumber * -1;
        }
        if (reverseNumber > Integer.MAX_VALUE)
        {
            return 0;
        }
        return reverseNumber;
    }

    public boolean palindrome(int number)
    {
        if (number < 0 || (number != 0 && number % 10 == 0))
            return false;
        if (number < 10 && number > 0)
        {
            return true;
        }
        int reverse = 0;// 543212345
        while (number > reverse)
        {
            reverse = reverse * 10 + number % 10;
            if (number == reverse)
                return true;

            number = number / 10;
        }

        return (number == reverse || number / 10 == reverse);
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        ReverseInteger reverse = new ReverseInteger();
        System.out.println(reverse.reverse_Bad(-1234));
        System.out.println(reverse.reverse_Bad(-1));
        System.out.println(reverse.reverse_Bad(0));
        System.out.println(reverse.reverse_Bad(8874653));
        System.out.println(reverse.reverse_Bad(432445345));
        System.out.println(reverse.reverse_Bad(544394357));
        System.out.println(reverse.reverse_Bad(1000000009));
        // Test suite with new reverse
        System.out.println("***********************************");
        System.out.println(reverse.reverse(-1234));
        System.out.println(reverse.reverse(-1));
        System.out.println(reverse.reverse(0));
        System.out.println(reverse.reverse(8874653));
        System.out.println(reverse.reverse(432445345));
        System.out.println(reverse.reverse(544394357));
        // System.out.println(reverse.reverse(1000000009));

        // Test suite for leet code problem number 9 Palindrome Number with no extra space:
        System.out.println("***********************************");
        System.out.println(reverse.palindrome(-1234));
        System.out.println(reverse.palindrome(1));
        System.out.println(reverse.palindrome(0));
        System.out.println(reverse.palindrome(8874653));
        System.out.println(reverse.palindrome(543212345));
        System.out.println(reverse.palindrome(12344321));
    }
}
