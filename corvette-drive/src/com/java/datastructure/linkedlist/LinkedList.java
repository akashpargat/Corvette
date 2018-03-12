package com.java.datastructure.linkedlist;

import java.util.HashSet;

import com.java.datastructure.util.LinkedListNode;

public class LinkedList
{
    private  LinkedListNode head;

    public LinkedListNode getHead()
    {
        return head;
    }

    public void insertAtEnd(final int data)
    {
        if (head == null)
        {
            head = new LinkedListNode(data);
            return;
        }
        LinkedListNode newNode = new LinkedListNode(data);
        LinkedListNode last = head;
        while (last.next != null)
        {
            last = last.next;
        }

        last.next = newNode;
        return;
    }

    public void deleteFirst()
    {
        if (head == null)
        {
            System.out.println("LinkedList is Empty.");
            return;
        }
        LinkedListNode tempHead = head.next;
        head = tempHead;
        return;
    }

    public void deleteAtEnd()
    {
        if (head == null)
        {
            System.out.println("LinkedList is Empty.");
            return;
        }
        LinkedListNode last = head;
        LinkedListNode prev = null;
        while (last.next != null)
        {
            prev = last;
            last = last.next;
        }

        prev.next = null;
        return;
    }

    public void insertinFront(final int data)
    {
        if (head == null)
        {
            head = new LinkedListNode(data);
            return;
        }
        LinkedListNode newNode = new LinkedListNode(data);
        newNode.next = head;
        head = newNode;
        return;
    }

    public void insertAfter(final int data, final int addAfterThis)
    {
        if (head == null)
        {
            head = new LinkedListNode(data);
            return;
        }
        LinkedListNode newNode = new LinkedListNode(data);
        LinkedListNode last = head;
        while (last.next != null)
        {
            if (last.data == addAfterThis)
            {
                LinkedListNode temp = last.next;
                last.next = newNode;
                newNode.next = temp;
                return;
            }
            last = last.next;
        }

        return;
    }

    public void deleteDataInLinkedList(final int data)
    {
        if (head == null)
        {
            System.out.println("LinkedList is Empty.");
            return;
        }
        LinkedListNode last = head;
        LinkedListNode prev = null;
        if (last.data == data)
        {
            head = head.next;
            return;
        }
        while (last.next != null)
        {
            if (last.data == data)
            {
                prev.next = last.next;
                return;
            }
            prev = last;
            last = last.next;
        }

        prev.next = null;
        return;
    }

    /**
     * 
     */
    public void removeDuplicate()
    {
        LinkedListNode node = head;
        while (node != null)
        {
        	LinkedListNode runner = node;
            while (runner.next != null)
            {
                if (runner.next.data == node.data)
                {
                	runner.next = runner.next.next;
                }else {
                	runner = runner.next;
                }
            }
            node = node.next;
        }
        System.out.println("Removed Duplicates successfully!!!"); //$NON-NLS-1$
    }
    

    /**
     * 
     */
//    public void removeDuplicate_usingHashSet()
//    {
//    	HashSet<Integer> hash = new HashSet<>();
//        Node node = head;
//        LinkedList newList = new LinkedList();
//        while (node.next != null)
//        {
//        		hash.add(node.data);
//        		node = node.next;
//        }
//        while (hash.iterator().hasNext())
//        {
//        		newList.insertAtEnd(hash.iterator().next().intValue());
//        }
//        head = newList.head;
//        System.out.println("Removed Duplicates successfully!!!"); //$NON-NLS-1$
//    }

    public static void main(String[] args)
    {
        LinkedList list = new LinkedList();
        list.insertAtEnd(10);
        list.insertAtEnd(20);
        list.insertAtEnd(30);
        list.insertAtEnd(40);
        list.insertAtEnd(20);
        list.insertAtEnd(60);
        list.insertAtEnd(40);
        list.insertAtEnd(80);
        list.insertAtEnd(80);
        list.insertAtEnd(100);
        list.printLinkedList(list.getHead());
        System.out.println("Now we will delete the last one:");
        // lst.deleteDataInLinkedList(10);
        list.removeDuplicate();
//        list.removeDuplicate_usingHashSet();
        list.printLinkedList(list.getHead());
        //list.printKthLinkedList(6);
    }
    
    public void printKthLinkedList(int k)
    {
    	if(head == null) {
    		return;
    	}
        LinkedListNode node = head;
        LinkedListNode toIgnore = head;
        int count=0;
        while (node != null)
        {
            node = node.next;
            count++;
        }
        if(count < k) {
        	return;
        }
        int toPrint = count -k;
        for(int i=0 ; i< toPrint; i++) {
        	toIgnore = toIgnore.next;
        }
        while(toIgnore!=null) {
        	System.out.println(toIgnore.data);
        	toIgnore = toIgnore.next;
        }
    }
    /* Function to reverse the linked list */
   public LinkedListNode reverse(LinkedListNode node) {
        LinkedListNode prev = null;
        LinkedListNode current = node;
        LinkedListNode next = null;
        while (current != null) {
            next = current.next;
            current.next = prev;
            prev = current;
            current = next;
        }
        node = prev;
        return node;
    }
    
    public void addCircularLinkedList() {
    	LinkedListNode node = head;
    	while(node.next!= null) {
    		node = node.next;
    	}
    	node.next = head.next.next.next.next.next;
    }
    public void printLinkedList(LinkedListNode node)
    {
        while (node != null)
        {
            System.out.print(node.data + " ");
            node = node.next;
        }
    }
}
