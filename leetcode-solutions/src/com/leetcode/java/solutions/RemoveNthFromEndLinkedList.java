package com.leetcode.java.solutions;

import com.leetcode.java.solutions.util.ListNode;

public class RemoveNthFromEndLinkedList
{
    ListNode headNode;

    public ListNode removeNthFromEnd_Scrap(ListNode head, int n)
    {
        headNode = head;
        ListNode fastPointer = head;
        int count = 0;
        if (head.next == null)
        {
            return head;
        }
        while (fastPointer != null && fastPointer.next != null && fastPointer.next.next != null)
        {
            count++;
            fastPointer = fastPointer.next.next;
        }
        count++;
        int totalElement = count % 2 == 0 ? (count * 2) - 1 : count * 2;
        int val = totalElement - n - 1;
        ListNode last = headNode;
        ListNode prev = null;
        for (int i = 0; i <= val; i++)
        {
            prev = last;
            last = last.next;
        }
        System.out.println(prev.val);
        prev.next = prev.next.next;
        return headNode;
    }

    public static void main(String[] args)
    {
        ListNode myNode = new ListNode(1);
        myNode.next = new ListNode(2);
        myNode.next.next = new ListNode(3);
        myNode.next.next.next = new ListNode(4);
        myNode.next.next.next.next = new ListNode(5);
        myNode.next.next.next.next.next = new ListNode(6);
        myNode.next.next.next.next.next.next = new ListNode(7);
        myNode.next.next.next.next.next.next.next = new ListNode(8);
        RemoveNthFromEndLinkedList rs = new RemoveNthFromEndLinkedList();
        rs.removeNthFromEnd(myNode, 2);
        System.out.println(""); //$NON-NLS-1$
    }

    public ListNode removeNthFromEnd(ListNode head, int n)
    {
        ListNode dummy = new ListNode(0);
        dummy.next = head;
        ListNode fast = dummy;
        ListNode slow = dummy;
        int temp = n;
        for (; fast.next != null; temp--)
        {
            if (temp <= 0)
            { // control
                slow = slow.next;
            }
            fast = fast.next;
        }
        slow.next = slow.next.next;// delete Nth
        return dummy.next;
    }

    public ListNode removeNthFromEnd_Efficient(ListNode head, int n)
    {
        ListNode dummy = new ListNode(0);
        dummy.next = head;
        ListNode node = dummy;
        ListNode runner = dummy;

        while (n > 0)
        {
            runner = runner.next;
            n--;
        }
        while (runner.next != null)
        {
            runner = runner.next;
            node = node.next;
        }

        node.next = node.next.next;
        return dummy.next;
    }

}
