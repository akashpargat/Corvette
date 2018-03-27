package com.leetcode.java.solutions;

import com.java.datastructure.util.TreeNode;
import com.java.datastructure.util.TreePrinter;

/**
 * 1. Two Sum</br>
 * Given an array of integers, return indices of the two numbers such that they add up to a specific
 * target. You may assume that each input would have exactly one solution, and you may not use the
 * same element twice. Example: Given nums = [2, 7, 11, 15], target = 9, Because nums[0] + nums[1] =
 * 2 + 7 = 9, return [0, 1].
 * 
 * @author Akash Pargat
 */
public class TwoSum
{
    private static TreeNode root;

    public int[] twoSum(int[] nums, int target)
    {
        int[] array = new int[2];
        if (nums == null)
        {
            return null;
        }
        if (nums.length <= 1)
        {
            return array;
        }
        int j = 0;
        for (int i = 0; i < nums.length; i++)
        {
            if (isInTheBinaryTree(root, target - nums[i]))
            {
                array[j] = i;
                System.out.println(i + "th index with value :-->" + nums[i]); //$NON-NLS-1$
                j++;
            }
        }
        return array;
    }

    public TreeNode createTree(final TreeNode node, final int value)
    {
        TreeNode current = node;

        if (current == null)
        {
            current = new TreeNode(String.valueOf(value));
        }
        if (Integer.parseInt(current.value) < value)
        {
            current.right = createTree(current.right, value);
        }
        else if (Integer.parseInt(current.value) > value)
        {
            current.left = createTree(current.left, value);
        }
        else
        {
            return current;
        }

        return current;
    }

    public boolean isInTheBinaryTree(final TreeNode node, int value)
    {
        if (node == null)
        {
            return false;
        }
        if (Integer.parseInt(node.value) == value)
        {
            return true;
        }
        if (Integer.parseInt(node.value) < value)
        {
            return isInTheBinaryTree(node.right, value);
        }

        return isInTheBinaryTree(node.left, value);
    }

    public static void main(String[] args)
    {// Test Suite One
        TwoSum ts = new TwoSum();
        int[] myArray = { 12, 11, 5, 7, 13, 18, 3 };
        int target = 8;
        for (int i = 0; i < myArray.length; i++)
        {
            root = ts.createTree(root, myArray[i]);
        }
        TreePrinter.print(root);
        int arr[] = ts.twoSum(myArray, target);
        System.out.println("The sum of value with index " + arr[0] + " and index " + arr[1] //$NON-NLS-1$ //$NON-NLS-2$
                + " is the total value of target."); //$NON-NLS-1$

        // Test Suite two
        TwoSum ts1 = new TwoSum();
        int[] myArray1 = { 12, 11, 7, 6, 13, 10, 4 };
        int target1 = 10;
        root = null;
        for (int i = 0; i < myArray1.length; i++)
        {
            root = ts1.createTree(root, myArray1[i]);
        }
        TreePrinter.print(root);
        int arr1[] = ts1.twoSum(myArray1, target1);
        System.out.println("The sum of value with index " + arr1[0] + " and index " + arr1[1] //$NON-NLS-1$ //$NON-NLS-2$
                + " is the total value of target."); //$NON-NLS-1$
    }

}
