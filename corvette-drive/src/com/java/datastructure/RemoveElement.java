package com.java.datastructure;

public class RemoveElement
{
    public int removeElement(int[] nums, int val)
    {
        int len = nums.length - 1;
        int i = 0;
        while (i != len)
        {
            if (nums[i] == val && nums[len] == val)
            {
                len--;
                continue;
            }
            if (nums[i] == val && nums[len] != val)
            {
                nums[i] = nums[len];
                nums[len] = val;
                len--;
            }
            i++;
        }
        return len;
    }

    public static void main(String[] args)
    {
        RemoveElement rem = new RemoveElement();
        int abc[] = { 2, 1, 2, 3, 4, 7, 43, 54543, 543, 654, 65, 2, 9, 2, 6, 2 };
        System.out.println(rem.removeElement(abc, 2));
        for (int i = 0; i < abc.length; i++)
        {
            System.out.print(abc[i] + ", ");
        }
    }

}
