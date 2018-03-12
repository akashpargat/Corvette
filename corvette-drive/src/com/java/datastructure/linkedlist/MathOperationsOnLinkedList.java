package com.java.datastructure.linkedlist;

import com.java.datastructure.util.LinkedListNode;

public class MathOperationsOnLinkedList {

public MathOperationsOnLinkedList(LinkedListNode first, LinkedListNode second) {
	// TODO Auto-generated constructor stub
	printLinkedList(addLinkedList( first,  second));
}

private LinkedListNode addLinkedList(LinkedListNode first, LinkedListNode second) {
	int firstCount = getCount(first);
	int secondCount = getCount(second);
	LinkedListNode firstNode = first;
	LinkedListNode secondNode = second;
	LinkedList secondLinkedListToAdd = new LinkedList();
	LinkedList firstLinkedListToAdd = new LinkedList();
	LinkedList newAddedLinkedList = new LinkedList();
	if(firstCount > secondCount) {
		for(int i=0; i< firstCount; i++) {
			if(secondNode!=null) {
				secondLinkedListToAdd.insertAtEnd(secondNode.data);
				secondNode =secondNode.next;
				continue;
			}
			secondLinkedListToAdd.insertinFront(0);
		}
		//printLinkedList(secondLinkedListToAdd.getHead());
		
	}
	else if(firstCount < secondCount) {
		
		for(int i=0; i< secondCount; i++) {
			if(firstNode!=null) {
				firstLinkedListToAdd.insertAtEnd(firstNode.data);
				firstNode =firstNode.next;
				continue;
			}
			firstLinkedListToAdd.insertinFront(0);
		}
		//printLinkedList(firstLinkedListToAdd.getHead());
		
	}
	if(firstLinkedListToAdd.getHead()==null) {
		firstNode  = firstLinkedListToAdd.getHead();
	}
if(secondLinkedListToAdd.getHead()==null) {
		
	}
	firstNode = firstLinkedListToAdd.reverse(firstNode);
	secondNode = secondLinkedListToAdd.reverse(secondNode);
//	Node firstNode1 =firstLinkedListToAdd.getHead();
//	Node secondNode1 = secondLinkedListToAdd.getHead();
	int sum = 0;
	int carry =0;
	while(firstNode!=null) {
		if(carry ==1) {
			sum = firstNode.data + secondNode.data + carry;
			carry =0;
		}else {
		 sum = firstNode.data + secondNode.data;
		}
		 firstNode = firstNode.next;
		 secondNode = secondNode.next;
		 if(sum>=10) {
			 carry =1;
		 }
		 newAddedLinkedList.insertAtEnd(sum);
//		 if(sum %10 ==1) {
//			 newAddedLinkedList.insertAtEnd(sum-10);
//		 }else {
//			 newAddedLinkedList.insertAtEnd(sum);
//		 }
	}
	int firstData = filterTheCarryOver(newAddedLinkedList.getHead());
	
//	if(newAddedLinkedList.getHead().data >=10) {
//		int a = newAddedLinkedList.getHead().data ;
//		int b = a-10;
//		Node newNode = new Node(newAddedLinkedList.getHead().data- 10);
//		Node newNode1 = new Node(1);
//	}
	
	return  addFront(firstData, newAddedLinkedList.reverse(newAddedLinkedList.getHead()));
}

private LinkedListNode addFront(int a, LinkedListNode node) {
	// TODO Auto-generated method stub
	LinkedListNode newNode = new LinkedListNode(a- 10);
	LinkedListNode newNode1 = new LinkedListNode(1);
	newNode1.next = newNode;
	newNode.next = node.next;
	 
	return newNode1;
	
}

private int filterTheCarryOver(LinkedListNode head) {
	// TODO Auto-generated method stub
	LinkedListNode node = head;
	while(node.next!=null) {
		if(node.next.data /10 == 1 ) {
			node.data -= 10;
		}
		node = node.next;
	}
	System.out.println("FUUUUUUKKK ME Bitch");
	return node.data;
	
//	node = head;
//	if(node.next.data /10 == 1) {
//		node.data+=1;
//	}
//	 node = head;
//	while(node!=null) {
//		if(node.data /10 == 1 ) {
//			node.data -=10; 
//		}
//		node = node.next;
//	}
}

public int getCount(LinkedListNode nodeToBeCounted) {
	int count =0;
	while(nodeToBeCounted!=null) {
		count++;
		nodeToBeCounted = nodeToBeCounted.next;
	}
	
	return count;
}

public void printLinkedList(LinkedListNode node)
{
    while (node != null)
    {
        System.out.print(node.data + " ");
        node = node.next;
    }
}
public static void main(String[] args) {
	LinkedList first = new LinkedList();
	first.insertAtEnd(1);
	first.insertAtEnd(2);
	first.insertAtEnd(9);
	first.insertAtEnd(3);
	first.insertAtEnd(7);
	first.insertAtEnd(8);
	
	LinkedList second = new LinkedList();
	second.insertAtEnd(9);
	second.insertAtEnd(3);
	second.insertAtEnd(5);
	second.insertAtEnd(8);
	second.insertAtEnd(0);
	new MathOperationsOnLinkedList(first.getHead(), second.getHead());
}
}