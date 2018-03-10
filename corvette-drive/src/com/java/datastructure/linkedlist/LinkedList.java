package com.java.datastructure.linkedlist;

import com.java.datastructure.util.Node;

public class LinkedList
{
    public Node head;

    public Node getHead()
    {
        return head;
    }

    public void insertAtEnd(final int data)
    {
        if (head == null)
        {
            head = new Node(data);
            return;
        }
        Node newNode = new Node(data);
        Node last = head;
        while (last.next != null)
        {
            last = last.next;
        }

        last.next = newNode;
        return;
    }

    public void deleteFirst()
    {
        if (head == null)
        {
            System.out.println("LinkedList is Empty.");
            return;
        }
        Node tempHead = head.next;
        head = tempHead;
        return;
    }

    public void deleteAtEnd()
    {
        if (head == null)
        {
            System.out.println("LinkedList is Empty.");
            return;
        }
        Node last = head;
        Node prev = null;
        while (last.next != null)
        {
            prev = last;
            last = last.next;
        }

        prev.next = null;
        return;
    }

    public void insertinFront(final int data)
    {
        if (head == null)
        {
            head = new Node(data);
            return;
        }
        Node newNode = new Node(data);
        newNode.next = head;
        head = newNode;
        return;
    }

    public void insertAfter(final int data, final int addAfterThis)
    {
        if (head == null)
        {
            head = new Node(data);
            return;
        }
        Node newNode = new Node(data);
        Node last = head;
        while (last.next != null)
        {
            if (last.data == addAfterThis)
            {
                Node temp = last.next;
                last.next = newNode;
                newNode.next = temp;
                return;
            }
            last = last.next;
        }

        return;
    }

    public void deleteDataInLinkedList(final int data)
    {
        if (head == null)
        {
            System.out.println("LinkedList is Empty.");
            return;
        }
        Node last = head;
        Node prev = null;
        if (last.data == data)
        {
            head = head.next;
            return;
        }
        while (last.next != null)
        {
            if (last.data == data)
            {
                prev.next = last.next;
                return;
            }
            prev = last;
            last = last.next;
        }

        prev.next = null;
        return;
    }

    /**
     * 
     */
    public void removeDuplicate()
    {
        Node node = head;
        while (node != null)
        {
        	Node runner = node;
            while (runner.next != null)
            {
                if (runner.next.data == node.data)
                {
                	runner.next = runner.next.next;
                }else {
                	runner = runner.next;
                }
            }
            node = node.next;
        }
        System.out.println("Removed Duplicates successfully!!!"); //$NON-NLS-1$
    }

    public static void main(String[] args)
    {
        LinkedList list = new LinkedList();
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
        System.out.println("Now we will delete the last one:");
        // lst.deleteDataInLinkedList(10);
        list.removeDuplicate();
        list.printLinkedList();

    }

    public void printLinkedList()
    {
        Node node = head;
        while (node != null)
        {
            System.out.print(node.data + " ");
            // System.out.println(node.data + " " + node.next);
            node = node.next;
        }
    }
}
