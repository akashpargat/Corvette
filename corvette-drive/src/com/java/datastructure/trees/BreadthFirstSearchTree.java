package com.java.datastructure.trees;

import java.util.LinkedList;

import com.java.datastructure.linkedlist.Queue;
import com.java.datastructure.util.TreeNode;
import com.java.datastructure.util.TreePrinter;

public class BreadthFirstSearchTree
{

    public BinarySearchTree tree = new BinarySearchTree();
    public TreeNode node;
    public LinkedList<Integer> ints = new LinkedList<>();

    public Queue<TreeNode> queue = new Queue<>();

    private void enQueue(TreeNode data)
    {
        if (queue != null)
        {
            queue.add(data);
        }
    }

    private TreeNode deQueue()
    {
        TreeNode queueTopElement = null;
        if (queue != null)
        {
            queueTopElement = queue.peek();
            queue.remove();
        }

        return queueTopElement;
    }

    private void breadthFirstSearch(BinarySearchTree treeToSearch)
    {
        enQueue(treeToSearch.getRoot());
        while (!queue.isEmpty())
        {
            TreeNode newNode = deQueue();
            System.out.println(newNode.value);
            if (newNode.left != null)
            {
                enQueue(newNode.left);
            }
            if (newNode.right != null)
            {
                enQueue(newNode.right);
            }
        }
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        BinarySearchTree tree = new BinarySearchTree();
        tree.createBinarySearchTree("5");
        tree.createBinarySearchTree("1");
        tree.createBinarySearchTree("3");
        tree.createBinarySearchTree("4");
        tree.createBinarySearchTree("7");
        tree.createBinarySearchTree("6");
        tree.createBinarySearchTree("10");
        tree.createBinarySearchTree("2");
        tree.createBinarySearchTree("13");
        tree.createBinarySearchTree("9");
        tree.createBinarySearchTree("0");
        TreePrinter.print(tree.root);
        tree.preOrderTraversal(tree.root);
        System.out.println();
        BreadthFirstSearchTree bfs = new BreadthFirstSearchTree();
        bfs.breadthFirstSearch(tree);
    }

}
