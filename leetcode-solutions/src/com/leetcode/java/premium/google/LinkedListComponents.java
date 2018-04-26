package com.leetcode.java.premium.google;

import java.util.HashSet;
import java.util.Set;

import com.leetcode.java.solutions.util.ListNode;

public class LinkedListComponents
{

    public static int numComponents(ListNode head, int[] G)
    {
        Set<Integer> set = new HashSet<>();
        for (int g : G)
            set.add(g);
        int res = 0;
        ListNode pre = head;
        while (pre != null)
        {
            if (set.contains(pre.val))
            {
                ++res;
                ListNode p = pre.next;
                while (p != null && set.contains(p.val))
                {
                    p = p.next;
                }
                pre = p;
                continue;
            }
            pre = pre.next;
        }

        return res;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        ListNode newNode = new ListNode(10);
        newNode.next = new ListNode(20);
        newNode.next.next = new ListNode(30);
        newNode.next.next.next = new ListNode(40);
        newNode.next.next.next.next = new ListNode(50);
        int[] subSet = { 10, 20, 30 };
        System.out.println(numComponents(newNode, subSet));
    }

}
