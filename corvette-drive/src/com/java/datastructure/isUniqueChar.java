package com.java.datastructure;

public class isUniqueChar
{
    public static String isUniqueChars(String str)
    {
        if (str.length() > 128)
        {
            return "Come on man this ain't happening"; //$NON-NLS-1$
        }

        boolean[] value = new boolean[128];
        for (int i = 0; i < str.length(); i++)
        {
            int uniCode = str.charAt(i);
            if (value[uniCode])
            {
                return "Sorry Boss the string provided is not unique."; //$NON-NLS-1$
            }
            value[uniCode] = true;
        }

        return "The given string is unique."; //$NON-NLS-1$
    }

    public static void main(String[] args)
    {
        System.out.println(isUniqueChars("AKASH")); //$NON-NLS-1$
        System.out.println(isUniqueChars("JATIN")); //$NON-NLS-1$

        int x = -4;
        System.out.println(x >> 1);
        int y = 4;
        System.out.println(y >> 1);

        int a[] = { 1, 2, 3, 5 };
        int b[] = { 1, 1, 2, 2, 3, 3, 4 };
        int xor = 0;
        for (int i = 0; i < b.length; i++)
        {
            xor = xor ^ b[i];
        }
        System.out.println(xor);
        // Missing element in range
        int xorr = 0;
        int xorr1 = 0;
        for (int i = 0; i < a.length; i++)
        {
            xorr = xorr ^ a[i];
        }
        for (int i = 1; i < 6; i++)
        {
            xorr1 = xorr1 ^ i;
        }

        System.out.println("The missing element is : " + (xorr ^ xorr1)); //$NON-NLS-1$

        int ones = 0, twos = 0;
        int common_bit_mask;
        int arr[] = { 3, 3, 3, 5, 2, 4, 2, 5, 2, 5 };
        for (int i = 0; i < arr.length; i++)
        {
            twos = twos | (ones & arr[i]);

            ones = ones ^ arr[i];

            common_bit_mask = ~(ones & twos);

            ones &= common_bit_mask;

            twos &= common_bit_mask;
        }
        System.out.println("Yo_____" + ones);
        System.out.println(5 & 4);
    }
}
