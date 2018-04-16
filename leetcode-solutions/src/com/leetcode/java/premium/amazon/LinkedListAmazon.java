package com.leetcode.java.premium.amazon;

import com.leetcode.java.solutions.util.ListNode;

public class LinkedListAmazon
{

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        ListNode firstNode = new ListNode(10);
        firstNode.next = new ListNode(20);
        // firstNode.next.next = new ListNode(30);
        // firstNode.next.next.next = new ListNode(40);
        // firstNode.next.next.next.next = new ListNode(50);
        // firstNode.next.next.next.next.next = new ListNode(60);
        // firstNode.next.next.next.next.next.next = new ListNode(70);
        // firstNode.next.next.next.next.next.next.next = new ListNode(80);
        // firstNode.next.next.next.next.next.next.next.next = new ListNode(90);

        ListNode secondNode = firstNode.next;
        // secondNode.next = new ListNode(43);
        // secondNode.next.next = new ListNode(55);
        // secondNode.next.next.next = firstNode.next.next.next.next.next;
        ListNode result = getIntersectionNode(firstNode, secondNode);
        System.out.println(result.val);

        System.out.println("This is the XOR: ");
    }

    public static ListNode getIntersectionNode(ListNode firstNode, ListNode secondNode)
    {
        if (firstNode == null || secondNode == null)
        {
            return null;
        }
        if (firstNode == secondNode)
        {
            return firstNode;
        }
        ListNode headA = firstNode;
        ListNode headB = secondNode;
        int firstLength = getLenght(headA);
        int secondLenght = getLenght(headB);
        int dif = Math.abs(firstLength - secondLenght);
        int greatest = firstLength > secondLenght ? firstLength : secondLenght;
        if (greatest == firstLength)
        {
            while (dif != 0)
            {
                headA = headA.next;
                dif--;
            }
        }
        else
        {
            while (dif != 0)
            {
                headB = headB.next;
                dif--;
            }
        }
        while (headA != null)
        {
            if (headA == headB)
            {
                return headA;
            }

            headA = headA.next;
            headB = headB.next;
        }

        return null;
    }

    public static int getLenght(ListNode node)
    {
        int count = 0;

        while (node != null)
        {
            count++;
            node = node.next;
        }

        return count;
    }
}
