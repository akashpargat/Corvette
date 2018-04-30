package com.leetcode.java.premium.facebook;

import com.java.datastructure.trees.BinarySearchTree;
import com.java.datastructure.util.TreeNode;
import com.java.datastructure.util.TreePrinter;

public class FlattenBinaryTreeToLinkedList
{
    public static void flatten(TreeNode root)
    {
        flatten(root, null);
    }

    private static TreeNode flatten(TreeNode root, TreeNode pre)
    {
        if (root == null)
        {
            return pre;
        }
        pre = flatten(root.right, pre);
        pre = flatten(root.left, pre);
        root.right = pre;
        root.left = null;
        pre = root;
        return pre;
    }

    public static void main(String[] args)
    {
        BinarySearchTree tree = new BinarySearchTree();
        tree.createBinarySearchTree("5"); //$NON-NLS-1$
        tree.createBinarySearchTree("1"); //$NON-NLS-1$
        tree.createBinarySearchTree("3"); //$NON-NLS-1$
        tree.createBinarySearchTree("4"); //$NON-NLS-1$
        tree.createBinarySearchTree("7"); //$NON-NLS-1$
        tree.createBinarySearchTree("6"); //$NON-NLS-1$
        tree.createBinarySearchTree("10"); //$NON-NLS-1$
        tree.createBinarySearchTree("2"); //$NON-NLS-1$
        tree.createBinarySearchTree("13"); //$NON-NLS-1$
        tree.createBinarySearchTree("9"); //$NON-NLS-1$
        tree.createBinarySearchTree("0"); //$NON-NLS-1$
        TreePrinter.print(tree.root);
        System.out.println("Pre-Order traversal");
        tree.preOrderTraversal(tree.root);
        System.out.println("\nFlatten");
        flatten(tree.root);
        TreePrinter.print(tree.root);
    }

}
