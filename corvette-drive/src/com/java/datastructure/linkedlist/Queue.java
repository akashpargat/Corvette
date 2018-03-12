package com.java.datastructure.linkedlist;

import java.util.EmptyStackException;

import com.java.datastructure.util.QueueNode;

public class Queue<T> {

	private QueueNode<T> first;
	private QueueNode<T> last;
	public T remove() {
		if(first == null) throw new EmptyStackException();
		T item  = first.data;
		first = first.next;
		if(first ==null) {
			last =null;
		}
		return item;
	}
	
	public void add(T item) {
		QueueNode<T> newItem = new QueueNode<T>(item);
		if(last!=null) {
			last.next = newItem;
		}
		last = newItem;
		
		if(first==null) {
			first = last;			
		}

	}
	
	public T peek() {
		if(first == null) throw new EmptyStackException();
		return first.data;
	}
	
	public boolean isEmpty() {
		return first == null;
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
