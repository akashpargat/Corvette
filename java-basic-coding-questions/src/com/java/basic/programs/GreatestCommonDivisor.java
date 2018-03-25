package com.java.basic.programs;

public class GreatestCommonDivisor {

	/*
	 * * Java method to find GCD of two number using Euclid's method * @return GDC
	 * of two numbers in Java
	 */
	private static int findGCD(int number1, int number2) { // base case
		if (number2 == 0) {
			return number1;
		}
		return findGCD(number2, number1 % number2);
	}


	public static void main(String[] args) {
		// TODO Auto-generated method stub
System.out.println(findGCD(15, 10));
	}

}
