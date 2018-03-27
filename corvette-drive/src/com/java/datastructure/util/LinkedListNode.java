package com.java.datastructure.util;

/**
 * 
 * Utility class for linked list node.
 * 
 * @author Akash Pargat
 */
public class LinkedListNode
{
    public int data;
    public LinkedListNode next;

    /**
     * @param data
     *            Data to be entered for the linked list node.
     */
    public LinkedListNode(final int data)
    {
        this.data = data;
        next = null;
    }
}
