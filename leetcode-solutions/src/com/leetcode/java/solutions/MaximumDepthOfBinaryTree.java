package com.leetcode.java.solutions;

import com.java.datastructure.util.TreeNode;
import com.java.datastructure.util.TreePrinter;

public class MaximumDepthOfBinaryTree
{
    static int sumL = 0;
    static int sumR = 0;

    public static int maxDepth(TreeNode root)
    {
        if (root == null)
        {
            return 0;
        }

        return Math.max(maxDepth(root.left), maxDepth(root.right)) + 1;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        TreeNode node = new TreeNode("3");
        node.left = new TreeNode("9");
        node.right = new TreeNode("20");
        // node.left.left = new TreeNode("4");
        node.right.left = new TreeNode("50");
        // node.left.right = new TreeNode("60");
        System.out.println("Pre-Order traversal");
        TreePrinter.print(node);
        System.out.println();
        System.out.println(maxDepth(node));
    }

}
