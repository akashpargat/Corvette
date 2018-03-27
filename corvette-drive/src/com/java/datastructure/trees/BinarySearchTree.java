package com.java.datastructure.trees;

import com.java.datastructure.util.TreeNode;
import com.java.datastructure.util.TreePrinter;

@SuppressWarnings("nls")
public class BinarySearchTree
{
    public TreeNode root;

    private TreeNode addBinarySearchTreeRecursive(TreeNode current, String value)
    {
        if (current == null)
        {
            return new TreeNode(value);
        }

        if (Integer.parseInt(value) < Integer.parseInt((current.value)))
        {
            current.left = addBinarySearchTreeRecursive(current.left, value);
        }
        else if (Integer.parseInt(value) > Integer.parseInt((current.value)))
        {
            current.right = addBinarySearchTreeRecursive(current.right, value);
        }
        else
        {
            // value already exists
            return current;
        }

        return current;
    }

    public void createBinarySearchTree(String value)
    {
        root = addBinarySearchTreeRecursive(root, value);
    }

    public void inOrderTraversal(TreeNode node)
    {
        if (node != null)
        {
            inOrderTraversal(node.left);
            printElement(node.value);
            inOrderTraversal(node.right);
        }
    }

    public void postOrderTraversal(TreeNode node)
    {
        if (node != null)
        {
            postOrderTraversal(node.left);
            postOrderTraversal(node.right);
            printElement(node.value);
        }
    }

    public void preOrderTraversal(TreeNode node)
    {
        if (node != null)
        {
            printElement(node.value);
            preOrderTraversal(node.left);
            preOrderTraversal(node.right);
        }
    }

    public boolean isBalanced(TreeNode node)
    {
        if (node == null)
        {
            return true;
        }
        if (Math.abs(getHeight(node.left) - getHeight(node.right)) <= 1 && isBalanced(node.left)
                && isBalanced(node.right))
        {
            return true;
        }
        return false;
    }

    public boolean isValidBST(TreeNode root)
    {
        if (root == null)
        {
            return true;
        }

        return helper(root, Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY);
    }

    public boolean helper(TreeNode root, double low, double high)
    {

        if (Integer.parseInt(root.value) <= low || Integer.parseInt(root.value) >= high)
        {
            return false;
        }

        if (root.left != null && !helper(root.left, low, Integer.parseInt(root.value)))
        {
            return false;
        }

        if (root.right != null && !helper(root.right, Integer.parseInt(root.value), high))
        {
            return false;
        }

        return true;
    }

    private int getHeight(TreeNode node)
    {
        if (node == null)
        {
            return 0;
        }
        int l = getHeight(node.left);
        int r = getHeight(node.right);
        return 1 + (l >= r ? l : r);
    }

    private void printElement(String value)
    {
        // TODO Auto-generated method stub
        System.out.print(value + "->");
    }

    public static void main(String[] args)
    {
        BinarySearchTree tree = new BinarySearchTree();
        // String[] treeArray = { "8", "7", "9", "10", "3", "4", "1", "12", "6", "5" };
        String[] treeArray = { "1", "2", "3", "4", "5", "6", "7", "8", "9", "10" };
        for (int i = 0; i < treeArray.length; i++)
        {
            tree.createBinarySearchTree(treeArray[i]);
        }
        TreeNode nodeToPrint = tree.root;
        // tree.createMinimalBST(treeArray);
        TreePrinter.print(tree.createMinimalBST(treeArray));
        // TreePrinter.print(tree.root);
        System.out.println("In Order Traversal: ");
        tree.inOrderTraversal(nodeToPrint);
        nodeToPrint = tree.root;
        System.out.println("\nPre Order Traversal: ");
        tree.preOrderTraversal(nodeToPrint);
        nodeToPrint = tree.root;
        System.out.println("\nPost Order Traversal: ");
        tree.postOrderTraversal(nodeToPrint);
        System.out.println(tree.isBalanced(nodeToPrint));
        System.out.println(tree.isValidBST(nodeToPrint));
        System.out.println(Math.sqrt(4));
        Double d = Double.MAX_VALUE;
    }

    private TreeNode createMinimalBST(String[] tree)
    {
        return createMinimalBST(tree, 0, tree.length - 1);
    }

    private TreeNode createMinimalBST(String[] tree, int start, int end)
    {
        if (end < start)
        {
            return null;
        }

        int mid = (start + end) / 2;
        TreeNode newNode = new TreeNode(tree[mid]);
        newNode.left = createMinimalBST(tree, start, mid - 1);
        newNode.right = createMinimalBST(tree, mid + 1, end);
        return newNode;
    }

    public TreeNode mergeTrees(TreeNode t1, TreeNode t2)
    {
        if (t1 == null && t2 == null)
        {
            return null;
        }

        int val = (t1 == null ? 0 : Integer.parseInt(t1.value))
                + (t2 == null ? 0 : Integer.parseInt(t2.value));
        TreeNode newNode = new TreeNode(String.valueOf(val));

        newNode.left = mergeTrees(t1 == null ? null : t1.left, t2 == null ? null : t2.left);
        newNode.right = mergeTrees(t1 == null ? null : t1.right, t2 == null ? null : t2.right);

        return newNode;
    }

    public TreeNode getRoot()
    {
        // TODO Auto-generated method stub
        return root;
    }
}
