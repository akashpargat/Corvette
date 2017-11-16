package com.java.datastructure;

public class MergeSort {
public static int [] split(final int[] number) {
	
	int length = number.length;
	int[] left ;
	int[] right;
	if(length % 2==0) {
		left = new int[length /2];
		right = new int[length/2];
	}else {
		left = new int[length/2];
		right = new int[length/2 +1];
	}
	
	 for (int i = 0; i < length; i++) {
	        if (i < length/2) {
	            left[i] = number[i];
	        }
	        else {
	            right[i-length/2] = number[i];
	        }
	    }
	left = split(left);
	right = split(right);
	return mergeSort(left, right);
}

public static int[] mergeSort(final int left[], final int[]right) {
	
	return right;
}
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
