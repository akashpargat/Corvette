package com.java.datastructure.linkedlist;

import com.java.datastructure.util.LinkedListNode;

public class FloydCycleDetection {
private LinkedListNode isALoop(LinkedListNode node) {
	LinkedListNode fastHelperNode = node;
	LinkedListNode slowHelperNode = node;
	while(slowHelperNode!= null && fastHelperNode!=null && fastHelperNode.next!= null) {
		fastHelperNode = fastHelperNode.next.next;
		slowHelperNode = slowHelperNode.next;
		if(fastHelperNode == slowHelperNode) {
			return slowHelperNode;
		}
	}
	return null;
}

private String startingCircularLoop(LinkedListNode node) {
LinkedListNode headNode = node;
LinkedListNode startNode = node;
LinkedListNode loopMeetingPoint = isALoop(headNode);
	while(startNode != loopMeetingPoint) {
		startNode = startNode.next;
		loopMeetingPoint = loopMeetingPoint.next;
	}
	
	return "Yo Bitch the loop meeting poing is : " +loopMeetingPoint.data;
}

public static void main(String[] args) {
	LinkedList list = new LinkedList();
    list.insertAtEnd(10);
    list.insertAtEnd(20);
    list.insertAtEnd(30);
    list.insertAtEnd(40);
    list.insertAtEnd(20);
    list.insertAtEnd(60);//Circular starts
    list.insertAtEnd(40);
    list.insertAtEnd(80);
    list.insertAtEnd(80);
    list.insertAtEnd(100);
    list.addCircularLinkedList();
    FloydCycleDetection detect = new FloydCycleDetection();
    System.out.println(detect.startingCircularLoop(list.getHead()));
}
}
