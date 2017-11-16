package com.java.datastructure;

public class BinarySearch {
	public static void main(String[] args) {
		// TODO Auto-generated method stub
binarySearch(BubbleSort.bubbleSort(new int[]{32,41,2,34,5,6,6,4,3,2,7,8,8,65,4,33,22,45,6}), 6);
	}
	private static boolean binarySearch(int[] bubbleSort, int numberTofind) {
		int length = bubbleSort.length/2;
		int middle = bubbleSort[length];
		if(middle == numberTofind) {
			System.out.println("Found the number and it is" + bubbleSort[middle]);
			return true;
			}
		else
			binarySearch(bubbleSort, numberTofind);
		return false;
	}
}
