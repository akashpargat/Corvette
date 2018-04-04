package com.leetcode.java.solutions;

import java.util.ArrayList;

public class SwapNodesInPairs
{

    public ListNode swapPairs(ListNode head)
    {
        if (head == null)
        {
            return null;
        }
        ListNode newhead = new ListNode(-1);// dummy
        newhead.next = head;
        ListNode temp = newhead;

        ListNode one = null;
        ListNode two = null;

        // {dummy->1->2->3->4->null}
        // explanation for one loop rest are same.

        while (temp.next != null && temp.next.next != null)
        {
            // temp points to dummy in the beginning.
            // one -> 1
            one = temp.next;
            // two -> 2
            two = temp.next.next;
            // 1-> = 2.next = 3;
            one.next = two.next;
            // 2-> = 1
            two.next = one;
            // now dummy should point to 2
            // if the below is not done dummy->1;
            temp.next = two;
            // temp was pointing to dummy
            // temp->1
            temp = one;

            // now { dummy->2->1->3->4 }

        }
        return newhead.next;
    }

    public static void main(String[] args)
    {
        ListNode myNode = new ListNode(10);
        myNode.next = new ListNode(20);
        myNode.next.next = new ListNode(30);
        myNode.next.next.next = new ListNode(40);
        myNode.next.next.next.next = new ListNode(50);
        // myNode.next.next.next.next.next = new ListNode(60);
        // myNode.next.next.next.next.next.next = new ListNode(70);
        SwapNodesInPairs sn = new SwapNodesInPairs();
        // sn.swapPairs_recursion(myNode);
        sn.reverseKGroup(myNode, 3);
    }

    public ListNode swapPairs_recursion(ListNode head)
    {
        if (head == null || head.next == null)
        {
            return head;
        }
        ListNode n = head.next;
        head.next = swapPairs(head.next.next);
        n.next = head;
        return n;
    }

    /**
     * Leetcode #25 Reverse Nodes in k-Group
     * 
     * @param node
     * @param k
     * @return
     */
    public ListNode reverseKGroup(ListNode node, int k)
    {
        ArrayList<ListNode> myNodes = new ArrayList<ListNode>();
        if (k == 1 || node.next == null)
        {
            return node;
        }
        ListNode prev = null;
        ListNode current = node;
        ListNode next = null;
        while (current != null)
        {
            int count = 0;
            for (int i = 0; i < k && current != null; i++)
            {
                next = current.next;
                current.next = prev;
                prev = current;
                current = next;
                count++;
            }
            if (count == k)
            {
                myNodes.add(prev);
            }
            else
            {
                myNodes.add(reverse(prev));
            }

            prev = null;
        }
        // Adds to the end of reversed node
        ListNode tempNode = prev;
        while (tempNode.next != null)
        {
            tempNode = tempNode.next;
        }
        tempNode.next = current;
        return prev;
    }

    public ListNode reverseKGroup_Leet(ListNode head, int k)
    {
        ListNode curr = head;
        int count = 0;
        while (curr != null && count != k)
        { // find the k+1 node
            curr = curr.next;
            count++;
        }
        if (count == k)
        { // if k+1 node is found
            curr = reverseKGroup(curr, k); // reverse list with k+1 node as head
            // head - head-pointer to direct part,
            // curr - head-pointer to reversed part;
            while (count-- > 0)
            { // reverse current k-group:
                ListNode tmp = head.next; // tmp - next head in direct part
                head.next = curr; // preappending "direct" head to the reversed list
                curr = head; // move head of reversed part to a new node
                head = tmp; // move "direct" head to the next node in direct part
            }
            head = curr;
        }
        return head;
    }

    private ListNode reverse(ListNode prev)
    {
        ListNode prevBuffer = null;
        ListNode current = prev;
        ListNode nextBuffer = null;
        while (current != null)
        {
            nextBuffer = current.next;
            current.next = prevBuffer;
            prevBuffer = current;
            current = nextBuffer;
        }
        return prevBuffer;
    }

    private static class ListNode
    {
        int val;
        ListNode next;

        ListNode(int x)
        {
            val = x;
        }
    }
}