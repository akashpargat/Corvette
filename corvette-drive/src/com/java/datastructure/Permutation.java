package com.java.datastructure;

import java.util.Arrays;

public class Permutation {

	public static void determinePermutation(String firstString, String secondString) {
		char first[] = firstString.toCharArray();
		char second[] = secondString.toCharArray();
		
		Arrays.sort(first);
		Arrays.sort(second);
		if(first.length!= second.length) {
			System.out.println("Asshole this can never be a permutation.");
		}
		if(Arrays.equals(first, second)) {
			System.out.println("The given string is the permutaiton of each other.");
			return;
		}
		
		System.out.println("The given string is not the permutaiton of each other.");
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
determinePermutation("Akash", "shakA");
	}

}
