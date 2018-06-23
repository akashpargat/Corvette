package com.leetcode.java.solutions;

import java.util.HashMap;
import java.util.Map;

import com.leetcode.java.solutions.util.TreeNode;

public class SymmetricTree
{
    @SuppressWarnings("null")
    public static Map<Integer, TreeNode> res = new HashMap<>();

    public static int isSymmetric_helper(TreeNode root)
    {
        if (root == null)
        {
            return 0;
        }
        if (root != null)
        {
            if (res.containsKey(root.val))
            {
                res.remove(root.val);
            }
            else
            {
                res.put(root.val, root);
            }
            isSymmetric_helper(root.left);
            isSymmetric_helper(root.right);
        }
        return 0;
    }

    public static boolean isSymmetric_old(TreeNode root)
    {
        isSymmetric_helper(root);
        if (res.size() <= 1)
        {
            return true;
        }
        return false;

    }

    public static boolean isSymmetric(TreeNode root)
    {
        if (null == root)
            return true;

        return isSym(root.left, root.right);
    }

    private static boolean isSym(TreeNode node1, TreeNode node2)
    {

        if (null == node1 && null == node2)
            return true;
        if (null == node1 && null != node2)
            return false;
        if (null != node1 && null == node2)
            return false;

        if (node1.val != node2.val)
            return false;

        return isSym(node1.left, node2.right) && isSym(node1.right, node2.left);

    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        TreeNode node = new TreeNode(3);
        node.left = new TreeNode(9);
        node.right = new TreeNode(9);
        // node.left.left = new TreeNode(4);
        // node.right.left = new TreeNode(4);
        // node.left.right = new TreeNode(60);
        // node.right.right = new TreeNode(70);
        System.out.println("Pre-Order traversal");
        System.out.println(isSymmetric(node));
    }

}
