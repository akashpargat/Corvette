package com.java.basic.programs;

public class Factorial
{
    int result = 1;

    private int getFactorial(final int number)
    {
        if (number < 0)
        {
            return 0;
        }
        if (number == 0)
        {
            return 1;
        }

        result = number * getFactorial(number - 1);
        return result;
    }

    public static int increasingSequence(int a[], int b[])
    {
        int count = 0;
        for (int i = 0; i < a.length - 1; i++)
        {
            if (a[i] > a[i + 1] || b[i] > b[i + 1])
            {
                if (a[i] < b[i + 1] && b[i] < a[i + 1])
                {
                    int temp = a[i];
                    a[i] = b[i];
                    b[i] = temp;
                    count++;
                }
                else
                {
                    return -1;
                }
            }

        }

        return count;
    }

    public static void main(String[] args)
    {
        // Test Cases
        System.out.println(new Factorial().getFactorial(-1));
        System.out.println(new Factorial().getFactorial(0));
        System.out.println(new Factorial().getFactorial(1));
        System.out.println(new Factorial().getFactorial(2));
        System.out.println(new Factorial().getFactorial(3));
        System.out.println(new Factorial().getFactorial(5));
        //
        System.out.println("***********************************"); //$NON-NLS-1$
        int a[] = { 5, 3, 7, 7, 10 };
        int b[] = { 1, 6, 6, 9, 9 };
        System.out.println(increasingSequence(a, b));
    }
}
