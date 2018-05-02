package com.leetcode.java.solutions;

import com.java.datastructure.util.TreeNode;
import com.java.datastructure.util.TreePrinter;

public class SymmetricTree
{
    @SuppressWarnings("null")
    public static int isSymmetric(TreeNode root)
    {
        if (root == null)
        {
            return 0;
        }
        if (root != null)
        {
            String leftVal = root.value;
            System.out.print(leftVal + ", ");
            int left = isSymmetric(root.left);
            int right = isSymmetric(root.right);
            String rightVal = root.value;
            System.out.print(rightVal + ", ");
            if (leftVal.equals(rightVal))
            {
                System.out.println("Biatchhhh");
            }
        }
        return 0;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        TreeNode node = new TreeNode("3");
        node.left = new TreeNode("9");
        node.right = new TreeNode("9");
        node.left.left = new TreeNode("4");
        node.right.left = new TreeNode("4");
        node.left.right = new TreeNode("60");
        node.right.right = new TreeNode("70");
        System.out.println("Pre-Order traversal");
        TreePrinter.print(node);
        isSymmetric(node);
    }

}
