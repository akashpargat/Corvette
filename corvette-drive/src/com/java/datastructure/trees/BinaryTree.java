package com.java.datastructure.trees;

import com.java.datastructure.util.DoublyLinkedListNode;
import com.java.datastructure.util.TreeNode;
import com.java.datastructure.util.TreePrinter;

public class BinaryTree {
public TreeNode root;

private TreeNode addRecursive(TreeNode current, String value) {
    if (current == null) {
        return new TreeNode(value);
    }
 
    if (Integer.parseInt(value) < Integer.parseInt((current.value))) {
        current.left = addRecursive(current.left, value);
    } else if (Integer.parseInt(value) > Integer.parseInt((current.value))) {
        current.right = addRecursive(current.right, value);
    } else {
        // value already exists
        return current;
    }
 
    return current;
}

public void add(String value) {
    root = addRecursive(root, value);
}

public void inOrderTraversal(TreeNode node) {
	if(node!=null) {
		inOrderTraversal(node.left);
		printElement(node.value);
		inOrderTraversal(node.right);
	}
}

public void postOrderTraversal(TreeNode node) {
	if(node!=null) {
		inOrderTraversal(node.left);
		inOrderTraversal(node.right);
		printElement(node.value);
	}
}

public void preOrderTraversal(TreeNode node) {
	if(node!=null) {
		printElement(node.value);
		inOrderTraversal(node.left);
		inOrderTraversal(node.right);
	}
}
private void printElement(String value) {
	// TODO Auto-generated method stub
	System.out.print(value+"->");
}

public static void main(String[] args) {
BinaryTree tree = new BinaryTree();
tree.add("5");
tree.add("1");
tree.add("3");
tree.add("4");
tree.add("7");
//tree.add("6");
tree.add("10");
tree.add("2");
//tree.add("13");
tree.add("9");
tree.add("0");
TreeNode nodeToPrint = tree.root;
TreePrinter.print(nodeToPrint);
System.out.println("In Order Traversal: ");
tree.inOrderTraversal(nodeToPrint);
nodeToPrint = tree.root;
System.out.println("\nPre Order Traversal: ");
tree.preOrderTraversal(nodeToPrint);
nodeToPrint = tree.root;
System.out.println("\nPost Order Traversal: ");
tree.postOrderTraversal(nodeToPrint);
}

}
