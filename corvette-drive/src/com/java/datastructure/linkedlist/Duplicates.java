package com.java.datastructure.linkedlist;

import com.java.datastructure.util.Node;

/**
 * Class which checks for duplicates and removes them from a linked list.
 */
public class Duplicates
{
    /**
     */
    public Duplicates(LinkedList list)
    {
        list.insertAtEnd(10);
        list.insertAtEnd(20);
        list.insertAtEnd(30);
        list.insertAtEnd(40);
        list.insertAtEnd(20);
        list.insertAtEnd(60);
        list.insertAtEnd(40);
        list.insertAtEnd(80);
        list.insertAtEnd(80);
        list.insertAtEnd(100);
        list.printLinkedList();
    }

    /**
     * 
     */
    public void removeDuplicate(Node node)
    {
        Node fast = node;
        Node prev = node;
        while (node.next != null)
        {
            while (fast.next != null)
            {
                if (node.data == fast.data)
                {
                    prev.next = fast.next;
                }
                prev = fast;
                fast = fast.next;
            }
            node = node.next;
        }
        System.out.println("Yo this is my thing!!!"); //$NON-NLS-1$
    }

    public static void main(String[] args)
    {
        LinkedList list = new LinkedList();
        Duplicates dup = new Duplicates(list);
        dup.removeDuplicate(list.getHead());
        list.printLinkedList();
    }
}
