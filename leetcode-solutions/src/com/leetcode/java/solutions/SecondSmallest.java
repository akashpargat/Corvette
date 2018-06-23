package com.leetcode.java.solutions;

public class SecondSmallest
{

    private static void secondSmallest(int[] arr)
    {
        int first, second, arr_size = arr.length;

        /* There should be atleast two elements */
        if (arr_size < 2)
        {
            System.out.println(" Invalid Input ");
            return;
        }

        first = second = Integer.MAX_VALUE;
        for (int i = 0; i < arr_size; i++)
        {
            /*
             * If current element is smaller than first then update both first and second
             */
            if (arr[i] < first)
            {
                second = first;
                first = arr[i];
            }

            /*
             * If arr[i] is in between first and second then update second
             */
            else if (arr[i] < second && arr[i] != first)
                second = arr[i];
        }
        if (second == Integer.MAX_VALUE)
            System.out.println("There is no second" + "smallest element");
        else
            System.out.println("The smallest element is " + first + " and second Smallest"
                    + " element is " + second);
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        int[] nums = { 4, 5, 7, 8, 9, 7, 9, 4, 3 };
        secondSmallest(nums);
    }

}
