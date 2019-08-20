package com.java.datastructure;

import com.java.datastructure.util.LinkedListNode;

public class SwapNodesInPair
{
    public LinkedListNode swapPair(LinkedListNode head)
    {
        if (head == null)
        {
            return null;
        }
        LinkedListNode tempHead = new LinkedListNode(0);
        tempHead.next = head;
        LinkedListNode tempBase = tempHead;
        LinkedListNode tempPr = tempHead.next;
        LinkedListNode tempNx = tempHead.next.next;
        while (tempNx != null)
        {
            tempBase.next = tempNx;
            tempPr.next = tempNx.next;
            tempNx.next = tempPr;

            if (tempNx.next == null || tempNx.next.next == null)
            {
                return tempHead.next;
            }
            tempPr = tempPr.next;
            tempBase = tempBase.next.next;
            tempNx = tempNx.next.next.next;
        }
        return tempHead.next;
        // LinkedListNode tempHead = new LinkedListNode(0);
        //
        // tempHead.next = head;
        //
        // LinkedListNode tempBase = head;
        //
        // while (head != null && head.next != null)
        // {
        //
        // LinkedListNode tempPr = head.next;
        //
        // tempHead.next = tempPr;
        //
        // head.next = tempPr.next;
        //
        // tempPr.next = head;
        //
        // head = head.next;
        //
        // tempBase = tempBase.next.next;
        //
        // }
        //
        // return tempBase.next;
    }

    public LinkedListNode swapPairsRecurssion(LinkedListNode head)
    {
        if ((head == null) || (head.next == null))
        {
            return head;
        }
        LinkedListNode headNode = head.next;
        head.next = swapPairsRecurssion(head.next.next);
        headNode.next = head;
        return headNode;
    }

    public static void main(String[] args)
    {
        LinkedListNode head = new LinkedListNode(1);
        head.next = new LinkedListNode(2);
        head.next.next = new LinkedListNode(3);
        head.next.next.next = new LinkedListNode(4);
        head.next.next.next.next = new LinkedListNode(5);
        head.next.next.next.next.next = new LinkedListNode(6);
        head.next.next.next.next.next.next = new LinkedListNode(7);
        LinkedListNode printFirst = head;
        System.out.println("Before Swap:");
        while (printFirst != null)
        {
            System.out.print(printFirst.data + " -> ");
            printFirst = printFirst.next;
        }
        SwapNodesInPair swap = new SwapNodesInPair();
        LinkedListNode print = swap.swapPair(head);
        // LinkedListNode print = swap.swapPairsRecurssion(head);
        System.out.println("\nAfter Swap:");
        while (print != null)
        {
            System.out.print(print.data + " -> ");
            print = print.next;
        }
    }

}
