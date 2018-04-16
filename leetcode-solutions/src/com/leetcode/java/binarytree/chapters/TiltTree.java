package com.leetcode.java.binarytree.chapters;

import com.leetcode.java.solutions.util.TreeNode;

public class TiltTree
{
    static int result = 0;

    public static int findTilt(TreeNode root)
    {
        postOrder(root);
        return result;
    }

    private static int postOrder(TreeNode root)
    {
        if (root == null)
            return 0;

        int left = postOrder(root.left);
        int right = postOrder(root.right);

        result += Math.abs(left - right);

        return left + right + root.val;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub

        TreeNode node = new TreeNode(10);
        node.left = new TreeNode(20);
        node.right = new TreeNode(30);
        node.left.left = new TreeNode(40);
        node.right.left = new TreeNode(50);

        System.out.println(findTilt(node));
    }

}
