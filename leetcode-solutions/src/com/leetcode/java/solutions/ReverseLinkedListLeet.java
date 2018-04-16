package com.leetcode.java.solutions;

import com.leetcode.java.solutions.util.ListNode;

public class ReverseLinkedListLeet
{
    public static ListNode reverseList(ListNode head)
    {
        if (head == null || head.next == null)
            return head;
        ListNode nextNode = head.next;
        ListNode newHead = reverseList(nextNode);
        nextNode.next = head;
        head.next = null;
        return newHead;
    }

    public ListNode reverseList_iterative(ListNode head)
    {
        ListNode prev = null;
        while (head != null)
        {
            ListNode temp = head.next;
            head.next = prev;
            prev = head;
            head = temp;
        }

        return prev;
    }

    public static ListNode reverseBetween(ListNode head, int m, int n)
    {
        ListNode newNode = head;
        if (head == null || head.next == null)
        {
            return head;
        }
        for (int i = 1; i < m; i++)
        {
            newNode = newNode.next;
        }
        ListNode prevNode = newNode;
        for (int j = 1; j < n && newNode != null; j++)
        {
            ListNode tempNode = newNode.next;
            newNode.next = prevNode;
            prevNode = newNode;
            newNode = tempNode;
        }
        return newNode;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        ListNode myNode = new ListNode(10);
        myNode.next = new ListNode(20);
        myNode.next.next = new ListNode(30);
        myNode.next.next.next = new ListNode(40);
        myNode.next.next.next.next = new ListNode(50);
        myNode.next.next.next.next.next = new ListNode(60);

        // ListNode newNode = reverseList(myNode);
        // while (newNode != null)
        // {
        // System.out.print(newNode.val + ", ");
        // newNode = newNode.next;
        // }
        System.out.println();
        ListNode newNodeSpecial = reverseBetween(myNode, 2, 5);
        while (newNodeSpecial != null)
        {
            System.out.print(newNodeSpecial.val + ", ");
            newNodeSpecial = newNodeSpecial.next;
        }
    }

}
