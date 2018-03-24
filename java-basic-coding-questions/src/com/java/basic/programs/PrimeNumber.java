package com.java.basic.programs;

import java.util.Arrays;

public class PrimeNumber {
	
	static int[] prime ;
	//O(n* sqrt(n))
	private boolean isPrimeNumber(final int number) {
		// fast even test.
	    if(number > 2 && (number & 1) == 0)
	       return false;
	    // only odd factors need to be tested up to n^0.5
	    for(int i = 3; i * i <= number; i += 2)
	        if (number % i == 0) 
	            return false;
	    return true;
	}
	
	private static void findPrimeByEratosthenese(final int number) {
		 prime = new int[number+1];
		for(int i = 0; i<=number ; i++) {
			prime[i]=1;
		}
		prime[0]=0; prime[1]=0;
		for(int i = 2; i*i <= number; i++) {
			if(prime[i]==1) {
				for(int j =2; i*j <= number; j++) {
					prime[i*j] =0;
				}
			}
		}
	}
	public static void main(String[] args) {
		//Test Cases
		System.out.println(new PrimeNumber().isPrimeNumber(-1));
		System.out.println(new PrimeNumber().isPrimeNumber(0));
		System.out.println(new PrimeNumber().isPrimeNumber(1));
		System.out.println(new PrimeNumber().isPrimeNumber(2));
		System.out.println(new PrimeNumber().isPrimeNumber(3));
		System.out.println(new PrimeNumber().isPrimeNumber(5));
		System.out.println(new PrimeNumber().isPrimeNumber(33));
		System.out.println(new PrimeNumber().isPrimeNumber(121));
		findPrimeByEratosthenese(121);
		for(int i = 0; i< 120; i++) {
			if(prime[i]==1)
			System.out.println(" The number "+i +" is a Prime Number.");
		}
	}
}
