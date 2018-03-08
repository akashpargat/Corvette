package com.java.datastructure;

public class MergeSort
{
    static int sortedArr[] = new int[25];

    public static int[] split(final int[] number)
    {
        int length = number.length;
        int[] left;
        int[] right;
        if (length % 2 == 0)
        {
            left = new int[length / 2];
            right = new int[length / 2];
        }
        else
        {
            left = new int[length / 2];
            right = new int[length / 2 + 1];
        }

        for (int i = 0; i < length; i++)
        {
            if (i < length / 2)
            {
                left[i] = number[i];
            }
            else
            {
                right[i - length / 2] = number[i];
            }
        }
        if (left.length > 1)
        {
            left = split(left);
        }
        if (right.length > 1)
        {
            right = split(right);
        }
        return mergeSort(left, right);
    }

    public static int[] mergeSort(final int left[], final int[] right)
    {

        if (left[0] > right[0])
        {
            System.out.println("Hello");
        }
        else
        {
            System.out.println("Hello Ass");
        }
        return sortedArr;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        System.out.println(split(new int[] { 5, 2, 32, 22, 1, 3, 1, 3 }));
    }

}
