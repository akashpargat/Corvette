package com.leetcode.java.premium.facebook;

import com.java.datastructure.trees.BinarySearchTree;
import com.java.datastructure.util.TreeNode;
import com.java.datastructure.util.TreePrinter;

public class FlattenBinaryTreeToLinkedList
{
    public static void flatten(TreeNode root)
    {
        if (root != null)
        {
            System.out.print(root.value + "->"); //$NON-NLS-1$
            if (root.left != null)
            {
                TreeNode newNode = root.left;
                flatten(root.left);
            }
            if (root.right != null)
            {
                flatten(root.right);
            }
        }
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
    }

}
