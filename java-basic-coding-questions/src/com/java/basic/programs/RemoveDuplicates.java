package com.java.basic.programs;

public class RemoveDuplicates
{

    public static void main(String[] args)
    {
        int nums[] = { 1, 2, 3, 3, 4, 4, 4, 5, 6, 6 };
        System.out.println(removeDuplicates(nums));
        System.out.println(removeDuplicates_leet(nums));
        System.out.println(removeElement_leet(new int[] { 3, 2, 2, 3 }, 3));
    }

    public static int removeDuplicates(int[] nums)
    {
        int count = 0;
        for (int i = 0; i < nums.length - 1; i++)
        {
            if (nums[i] == nums[i + 1])
            {
                // i++;
            }
            else
            {
                count++;
            }
        }
        count++;
        return count;
    }

    public static int removeDuplicates_leet(int[] nums)
    {
        int dupes = 0;

        for (int i = 1; i < nums.length; i++)
        {
            if (nums[i] == nums[i - 1])
            {
                dupes++;
            }

            nums[i - dupes] = nums[i];
        }

        return nums.length - dupes;
    }

    public static int removeElement_leet(int[] nums, int val)
    {
        return 0;
    }
}
