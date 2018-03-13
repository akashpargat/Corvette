package com.java.datastructure.util;

public class TreeNode implements PrintableNode{
	public String value;
	public TreeNode left;
	public TreeNode right;
	public TreeNode(String value) {
		// TODO Auto-generated constructor stub
		this.value = value;
		right = null;
        left = null;
	}
	@Override
	public PrintableNode getLeft() {
		// TODO Auto-generated method stub
		return left;
	}
	@Override
	public PrintableNode getRight() {
		// TODO Auto-generated method stub
		return right;
	}
	@Override
	public String getText() {
		// TODO Auto-generated method stub
		return value;
	}
}
