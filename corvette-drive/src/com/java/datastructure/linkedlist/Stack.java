package com.java.datastructure.linkedlist;

import java.util.EmptyStackException;

import com.java.datastructure.util.StackNode;

public class Stack<T> {

	private StackNode<T> top;
	public T pop() {
		if(top == null) throw new EmptyStackException();
		T item  = top.data;
		top = top.next;
		return item;
	}
	
	public void push(T item) {
		if(top == null) throw new EmptyStackException();
		StackNode<T> newItem = new StackNode<T>(item);
		newItem.next =top;
		top = newItem;
	}
	
	public T peek() {
		if(top == null) throw new EmptyStackException();
		return top.data;
	}
	
	public boolean isEmpty() {
		return top == null;
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
