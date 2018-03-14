package com.java.datastructure.trees;

import com.java.datastructure.linkedlist.Queue;
import com.java.datastructure.util.TreeNode;
import com.java.datastructure.util.TreePrinter;

public class BreadthFirstSearchTree {

	public BinaryTree tree = new BinaryTree();
	public TreeNode node;
	
	public Queue<TreeNode> queue = new Queue<>();
	
	private void enQueue(TreeNode data) {
		if(queue!= null) {
			queue.add(data);
		}
	}
	
	private TreeNode deQueue() {
		TreeNode  queueTopElement = null;
		if(queue!= null) {
			  queueTopElement = queue.peek();
			queue.remove();
		}
		
		return queueTopElement;
	}
	
	private void breadthFirstSearch(BinaryTree treeToSearch) {
		enQueue(treeToSearch.getRoot());
		while(!queue.isEmpty()) {
			TreeNode newNode = deQueue();
			System.out.println(newNode.value);
			if(newNode.left!=null) {
				enQueue(newNode.left);
			}
			if(newNode.right!=null) {
				enQueue(newNode.right);
			}
		}
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		BinaryTree tree = new BinaryTree();
		tree.add("5");
		tree.add("1");
		tree.add("3");
		tree.add("4");
		tree.add("7");
		tree.add("6");
		tree.add("10");
		tree.add("2");
		tree.add("13");
		tree.add("9");
		tree.add("0");
		TreePrinter.print(tree.root);
		BreadthFirstSearchTree bfs = new BreadthFirstSearchTree();
		bfs.breadthFirstSearch(tree);
	}

}
