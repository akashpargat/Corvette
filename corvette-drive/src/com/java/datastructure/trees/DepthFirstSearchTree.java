package com.java.datastructure.trees;

import java.util.LinkedList;

import com.java.datastructure.util.TreeNode;
import com.java.datastructure.util.TreePrinter;

public class DepthFirstSearchTree
{
    public void dfs(TreeNode node)
    {
        if (node != null)
        {
            System.out.print(node.value + "->"); //$NON-NLS-1$
            if (node.left != null)
            {
                dfs(node.left);
            }
            if (node.right != null)
            {
                dfs(node.right);
            }
        }
    }

    public void bfs(TreeNode node)
    {
        if (node != null)
        {
            LinkedList<TreeNode> myList = new LinkedList<TreeNode>();
            myList.add(node);
            while (!myList.isEmpty())
            {
                System.out.print(myList.peek().value + "->"); //$NON-NLS-1$
                node = myList.poll();
                if (node.left != null)
                {
                    myList.add(node.left);
                }
                if (node.right != null)
                {
                    myList.add(node.right);
                }
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
        tree.preOrderTraversal(tree.root);
        System.out.println();
        DepthFirstSearchTree dfs = new DepthFirstSearchTree();
        System.out.println("DFS:-"); //$NON-NLS-1$
        dfs.dfs(tree.root);
        System.out.println("\nBFS:-"); //$NON-NLS-1$
        dfs.bfs(tree.root);
    }

}
