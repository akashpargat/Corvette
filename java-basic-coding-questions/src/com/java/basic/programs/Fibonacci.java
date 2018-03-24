package com.java.basic.programs;

import java.util.Scanner;

/** 1,1,2,3,5,8,13,21,34,55,89,144,...
 * Often, especially in modern usage, the sequence is extended by one more initial term:
 * 0,1,1,2,3,5,8,13,21,34,55,89,144,...
 * The Fibonacci spiral: an approximation of the golden spiral created by drawing circular arcs 
 * connecting the opposite corners of squares in the Fibonacci tiling;[4] this one uses squares of sizes 
 * 1, 1, 2, 3, 5, 8, 13 and 21. By definition, the first two numbers in the Fibonacci sequence 
 * are either 1 and 1, or 0 and 1, depending on the chosen starting point of the sequence, 
 * and each subsequent number is the sum of the previous two.*/
public class Fibonacci {

	private int getFibonacci(final int number) {
		if(number <= 0) {
			return 0;
		}
		if(number == 1 || number == 2) {
			return 1;
		}
		
		return getFibonacci(number-1) + getFibonacci(number-2);
	}
	@SuppressWarnings("resource")
	public static void main(String[] args) {
		//Test Case
		System.out.println("Enter number upto which Fibonacci series to print: "); 
		int number = new Scanner(System.in).nextInt(); 
		System.out.println("Fibonacci series upto " + number +" numbers : "); 
		for(int i=1; i<=number; i++){ 
			System.out.print(new Fibonacci().getFibonacci(i) +" "); 
			}
	}
}
