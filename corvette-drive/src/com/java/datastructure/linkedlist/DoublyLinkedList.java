package com.java.datastructure.linkedlist;

import com.java.datastructure.util.DoublyLinkedListNode;

public class DoublyLinkedList
{
    private DoublyLinkedListNode head;

    public DoublyLinkedListNode getHead()
    {
        return head;
    }

    public DoublyLinkedList()
    {
        // TODO Auto-generated constructor stub
    }

    public void printLinkedList(DoublyLinkedListNode node)
    {
        while (node != null)
        {
            System.out.print(node.data + " ");
            node = node.next;
        }
    }

    public void insertAtEnd(final int data)
    {
        if (head == null)
        {
            head = new DoublyLinkedListNode(data);
            return;
        }
        DoublyLinkedListNode newNode = new DoublyLinkedListNode(data);
        DoublyLinkedListNode last = head;
        while (last.next != null)
        {
            last = last.next;
        }

        last.next = newNode;
        newNode.prev = last;
        return;
    }

    public DoublyLinkedListNode reverse(DoublyLinkedListNode node)
    {
        DoublyLinkedListNode current = node;
        DoublyLinkedListNode temp = null;

        while (current != null)
        {
            temp = current.prev;
            current.prev = current.next;
            current.next = temp;
            current = current.prev;
        }
        if (temp != null)
        {
            node = temp.prev;
        }

        return node;
    }

    public static void main(String[] args)
    {
        DoublyLinkedList doublyLinkedList = new DoublyLinkedList();
        doublyLinkedList.insertAtEnd(10);
        doublyLinkedList.insertAtEnd(20);
        doublyLinkedList.insertAtEnd(30);
        doublyLinkedList.insertAtEnd(40);
        doublyLinkedList.insertAtEnd(50);
        doublyLinkedList.insertAtEnd(60);
        doublyLinkedList.insertAtEnd(70);
        doublyLinkedList.insertAtEnd(80);
        doublyLinkedList.printLinkedList(doublyLinkedList.getHead());
        doublyLinkedList.printLinkedList(doublyLinkedList.reverse(doublyLinkedList.getHead()));
    }
}
