package com.java.datastructure;

public class SelectionSort {

	public static int[] selectionSort(final int[] number) {
		
		for(int i =0; i<number.length ; i++){
			int smallest =i;
			for(int j = i; j<number.length ;j++) {
				if(number[smallest] > number[j]) {
					smallest = j;
				}
				int temp = number[i];
				number[i]=number[smallest];
				number[smallest] =temp;
			}
		}
		return number;
		
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int[] num =SelectionSort.selectionSort(new int[] {43,56,24,28,21,31,12,1,2,3,53,2,5,63,36,6});
		for(int i=0;i<num.length ; i++) {
			System.out.println(num[i]);
		}
	}
}
