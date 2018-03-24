package com.java.basic.programs;

public class Factorial {
	int result = 1;
	private int getFactorial(final int number) {
		if(number < 0) {
			return 0;
		}
		if(number == 0) {
			return 1;
		}
		
		 result = number * getFactorial(number-1);
		return result ;
	}
	public static void main(String[] args) {
		//Test Cases
		System.out.println(new Factorial().getFactorial(-1));
		System.out.println(new Factorial().getFactorial(0));
		System.out.println(new Factorial().getFactorial(1));
		System.out.println(new Factorial().getFactorial(2));
		System.out.println(new Factorial().getFactorial(3));
		System.out.println(new Factorial().getFactorial(5));
	}
}
