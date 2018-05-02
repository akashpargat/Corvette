package com.leetcode.java.premium.amazon;

import com.leetcode.java.solutions.util.ListNode;

public class MergeSortedLinkedList
{
    public static ListNode mergeTwoLists(ListNode l1, ListNode l2)
    {
        ListNode dummyNode = new ListNode(0);
        ListNode buffer = dummyNode;
        while (l1 != null && l2 != null)
        {
            if (l1.val <= l2.val)
            {
                ListNode newNode = new ListNode(l1.val);
                l1 = l1.next;
                buffer.next = newNode;
                buffer = buffer.next;
            }
            else if (l1.val > l2.val)
            {
                ListNode newNode = new ListNode(l2.val);
                l2 = l2.next;
                buffer.next = newNode;
                buffer = buffer.next;
            }

        }
        if (l1 != null)
        {
            buffer.next = l1;
        }
        if (l2 != null)
        {
            buffer.next = l2;
        }
        return dummyNode.next;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        ListNode firstNode = new ListNode(10);
        firstNode.next = new ListNode(20);
        firstNode.next.next = new ListNode(30);
        firstNode.next.next.next = new ListNode(40);
        ListNode secondNode = new ListNode(10);
        secondNode.next = new ListNode(25);
        secondNode.next.next = new ListNode(30);
        secondNode.next.next.next = new ListNode(40);
        ListNode newNode = mergeTwoLists(firstNode, secondNode);
        while (newNode != null)
        {
            System.out.println(newNode.val + ", ");
            newNode = newNode.next;
        }
    }
}
