package com.leetcode.java.premium.amazon;

import com.java.datastructure.util.TreePrinter;
import com.leetcode.java.solutions.util.TreeNode;

public class MergeBinaryTree
{

    public static TreeNode mergeTrees(TreeNode t1, TreeNode t2)
    {
        if (t1 == null)
        {
            return t2;
        }
        if (t2 == null)
        {
            return t1;
        }
        t1.val += t2.val;
        t1.left = mergeTrees(t1.left, t2.left);
        t1.right = mergeTrees(t1.right, t2.right);

        return t1;
    }

    public static TreeNode mergeTrees_extraSpace(TreeNode t1, TreeNode t2)
    {
        if (t1 == null)
        {
            return t2;
        }
        if (t2 == null)
        {
            return t1;
        }

        TreeNode root = new TreeNode(t1.val + t2.val);
        root.left = mergeTrees(t1.left, t2.left);
        root.right = mergeTrees(t1.right, t2.right);

        return root;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        TreeNode node1 = new TreeNode(10);
        node1.left = new TreeNode(30);
        node1.left.left = new TreeNode(50);
        node1.right = new TreeNode(20);
        TreeNode node2 = new TreeNode(20);
        node2.left = new TreeNode(10);
        node2.left.right = new TreeNode(40);
        node2.right = new TreeNode(30);
        node2.right.right = new TreeNode(70);
        TreePrinter.print(mergeTrees(node1, node2));
        TreePrinter.print(mergeTrees_extraSpace(node1, node2));
    }

}
