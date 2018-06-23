package com.leetcode.java.solutions.util;

import com.java.datastructure.util.PrintableNode;

public class TreeNode implements PrintableNode
{
    public int val;
    public TreeNode left;
    public TreeNode right;

    public TreeNode(int x)
    {
        val = x;
    }

    @Override
    public PrintableNode getLeft()
    {
        // TODO Auto-generated method stub
        return left;
    }

    @Override
    public PrintableNode getRight()
    {
        // TODO Auto-generated method stub
        return right;
    }

    @Override
    public String getText()
    {
        // TODO Auto-generated method stub
        return Integer.toString(val);
    }
}
