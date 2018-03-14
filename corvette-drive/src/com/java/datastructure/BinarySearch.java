package com.java.datastructure;

import com.java.datastructure.sorts.BubbleSort;

public class BinarySearch 
	{
		public static void main(String[] args) {
			int [] arr =BubbleSort.bubbleSort(new int[]{5,7,3,2,1,4,6});
			System.out.println(binarySearch(arr, 6, 0,arr.length -1));
			System.out.println(19/10);
//			for(int i =0; i<=20; i++) {
//				System.out.println("Mod of number : "+ i + " = " +i%10);
//			}
	}
	private static String binarySearch(int[] bubbleSortArray, int numberTofind, int firstIndex, int lastIndex) {
		if(lastIndex>firstIndex) 
		{
			int mid = firstIndex + (lastIndex -firstIndex)/2;
			int middleElement = bubbleSortArray[mid];
			
			if(middleElement == numberTofind) 
				return "Found the number and it is " + middleElement;
			
			if(middleElement>numberTofind) 
				binarySearch(bubbleSortArray, numberTofind, firstIndex, mid-1);
		
			return binarySearch(bubbleSortArray, numberTofind, mid+1, lastIndex);
		}
		
		return "Sorry the number was not found in the given array.";
	}
}
