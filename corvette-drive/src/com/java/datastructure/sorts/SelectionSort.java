package com.java.datastructure.sorts;

import java.io.IOException;
import java.util.Scanner;

public class SelectionSort {
	public String name;
	private int id;
	protected double assets;

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
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		int[] num =SelectionSort.selectionSort(new int[] {43,56,24,28,21,31,12,1,2,3,53,2,5,63,36,6});
		for(int i=0;i<num.length ; i++) {
			//System.out.println(num[i]);
		}
//		Scanner sc = new Scanner(System.in);
//		int num1 =sc.nextInt();
		for (int height = 4; height >= 0; height--)
		{
		     for (int x = height; x >= 0; x--)
		          System.out.print('*');
		     System.out.println();
		}

	}
	
	
}
