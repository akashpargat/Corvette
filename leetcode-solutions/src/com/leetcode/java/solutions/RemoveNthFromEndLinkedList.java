package com.leetcode.java.solutions;

public class RemoveNthFromEndLinkedList
{

    public static ListNode removeNthFromEnd(ListNode head, int n)
    {
        ListNode slowPointer = head;
        ListNode fastPointer = head;
        int count = 0;
        while (fastPointer != null && fastPointer.next != null && fastPointer.next.next != null)
        {
            count++;
            fastPointer = fastPointer.next.next;
        }
        count++;
        int val = 2 * count - n - 1;
        for (int i = 0; i <= val; i++)
        {
            slowPointer = slowPointer.next;
        }
        System.out.println(slowPointer.val);
        slowPointer = slowPointer.next;
        return head;
    }

    public static void main(String[] args)
    {
        ListNode myNode = new ListNode(10);
        myNode.next = new ListNode(20);
        myNode.next.next = new ListNode(30);
        myNode.next.next.next = new ListNode(40);
        myNode.next.next.next.next = new ListNode(50);
        myNode.next.next.next.next.next = new ListNode(60);
        myNode.next.next.next.next.next.next = new ListNode(70);
        RemoveNthFromEndLinkedList.removeNthFromEnd(myNode, 3);
        System.out.println(""); //$NON-NLS-1$
    }

    public static class ListNode
    {
        int val;
        ListNode next;

        ListNode(int x)
        {
            val = x;
        }
    }
}
