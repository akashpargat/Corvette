package com.java.datastructure.sorts;

import java.util.Arrays;

public class BubbleSort
{

    public static void main(String[] args)
    {
        bubbleSort(new int[] { 5, 2, 32, 22, 1, 3, 1, 3 });
    }

    public static int[] bubbleSort(int[] lst)
    {
        int n = lst.length;
        boolean swapped;
        do
        {
            swapped = false;
            for (int i = 0; i < n - 1; i++)
            {
                if (lst[i] > lst[i + 1])
                {
                    int temp = lst[i];
                    lst[i] = lst[i + 1];
                    lst[i + 1] = temp;
                    swapped = true;
                }
            }
        }
        while (swapped == true);

        System.out.println(Arrays.toString(lst));
        return lst;
    }
}
