package com.leetcode.java.solutions;

import com.java.datastructure.linkedlist.LinkedList;
import com.java.datastructure.util.LinkedListNode;

/**
 * 2. Add Two Numbers<br>
 * You are given two non-empty linked lists representing two non-negative integers. The digits are
 * stored in reverse order and each of their nodes contain a single digit. Add the two numbers and
 * return it as a linked list. You may assume the two numbers do not contain any leading zero,
 * except the number 0 itself.<br>
 * Example Input: (2 -> 4 -> 3) + (5 -> 6 -> 4) Output: 7 -> 0 -> 8 Explanation: 342 + 465 = 807.
 * NOTE: Assumption is that both the list have same amount of nodes. In Above example we have 3 in
 * both.
 * 
 * @author Akash Pargat
 */
public class AddTwoNumbers
{
    public static void main(String[] args)
    {
        // First Testing Suite
        LinkedList list = new LinkedList();
        list.insertAtEnd(2);
        list.insertAtEnd(4);
        list.insertAtEnd(3);
        LinkedList list1 = new LinkedList();
        list1.insertAtEnd(5);
        list1.insertAtEnd(6);
        list1.insertAtEnd(4);
        printLinkedList(addLinkedList(list.getHead(), list1.getHead()));

        // Second Testing Suite
        LinkedList list2 = new LinkedList();
        list2.insertAtEnd(9);
        list2.insertAtEnd(9);
        list2.insertAtEnd(9);
        LinkedList list3 = new LinkedList();
        list3.insertAtEnd(9);
        list3.insertAtEnd(9);
        list3.insertAtEnd(9);
        printLinkedList(addLinkedList(list2.getHead(), list3.getHead()));

        // Third Testing Suite
        LinkedList list4 = new LinkedList();
        list4.insertAtEnd(1);
        list4.insertAtEnd(1);
        list4.insertAtEnd(1);
        LinkedList list5 = new LinkedList();
        list5.insertAtEnd(1);
        list5.insertAtEnd(1);
        list5.insertAtEnd(1);
        printLinkedList(addLinkedList(list4.getHead(), list5.getHead()));
    }

    /**
     * Method to add the two linked list in a reverse order.
     * 
     * @param firstNumberNode
     *            First Node to be added.
     * @param secondNumberNode
     *            Second node to be added.
     * @return Sum of the provided list in a reverse order.
     */
    private static LinkedList addLinkedList(LinkedListNode firstNumberNode,
            LinkedListNode secondNumberNode)
    {
        int buffer = 0;
        boolean carry = false;
        LinkedList newLinkedList = new LinkedList();
        if (firstNumberNode == null || secondNumberNode == null)
        {
            return null;
        }
        while (firstNumberNode != null && secondNumberNode != null)
        {
            buffer = firstNumberNode.data + secondNumberNode.data;
            if (buffer >= 10 && carry)
            {
                carry = true;
                newLinkedList.insertAtEnd(buffer % 10 + 1);
            }
            else if (buffer >= 10)
            {
                carry = true;
                newLinkedList.insertAtEnd(buffer % 10);
            }
            else if (carry && buffer < 10)
            {
                newLinkedList.insertAtEnd(buffer + 1);
                carry = false;
            }
            else
            {
                newLinkedList.insertAtEnd(buffer);
            }
            firstNumberNode = firstNumberNode.next;
            secondNumberNode = secondNumberNode.next;
        }
        if (carry)
        {
            newLinkedList.insertAtEnd(1);
        }
        return newLinkedList;
    }

    private static void printLinkedList(LinkedList linkedList)
    {
        LinkedListNode node = linkedList.getHead();
        System.out.println("The addition of the given linked list in a reverse order is: "); //$NON-NLS-1$
        while (node != null)
        {
            System.out.print(node.data + " ->"); //$NON-NLS-1$
            node = node.next;
        }
    }
}
