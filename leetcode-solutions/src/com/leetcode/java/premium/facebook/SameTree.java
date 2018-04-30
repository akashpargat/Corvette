package com.leetcode.java.premium.facebook;

import com.leetcode.java.solutions.util.TreeNode;

/**
 * @author A
 */
public class SameTree
{
    /**
     * @param p
     *            s
     * @param q
     *            s
     * @return s
     */
    public static boolean isSameTree(TreeNode p, TreeNode q)
    {
        if (p == null && q == null)
        {
            return true;
        }
        if (p == null || q == null)
        {
            return false;
        }
        return p.val == q.val && isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
    }

    public boolean isSameTree_easy(TreeNode p, TreeNode q)
    {
        if (p == null && q == null)
        {
            return true;
        }
        if (p == null || q == null)
        {
            return false;
        }
        if (p.val == q.val)
        {
            return isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
        }
        return false;
    }

    public static void main(String[] args)
    {

        TreeNode tree1 = new TreeNode(10);
        tree1.left = new TreeNode(20);
        tree1.right = new TreeNode(30);
        TreeNode tree2 = new TreeNode(10);
        tree2.left = new TreeNode(20);
        tree2.right = new TreeNode(30);
        System.out.println(isSameTree(tree1, tree2));
    }
}
