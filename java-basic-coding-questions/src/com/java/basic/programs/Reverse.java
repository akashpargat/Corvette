package com.java.basic.programs;

public class Reverse {
	String newString = "";

	public Reverse(final String stringToReverse) {
		// TODO Auto-generated constructor stub
		newString = stringToReverse;
	}

	// Old school reverse string
	private String reverseString() {
		String reverse = "";
		for (int i = newString.length() - 1; i >= 0; i--) {
			reverse = reverse + newString.charAt(i);
		}
		return reverse;
	}

	/** 
	 *  Java Method to reverse String array in place
	 *   @param array 
	 */
	public static void reverseInPlace(String[] array) {
		if (array == null || array.length < 2) {
			return;
		}
		for (int i = 0; i < array.length / 2; i++) {
			String temp = array[i];
			array[i] = array[array.length - 1 - i];
			array[array.length - 1 - i] = temp;
		}
		for(int i =0; i <array.length; i++) {
			System.out.println(array[i]);
			}
	}
	
	public static String[] splitString(String sentence) {
		String [] newArray = sentence.split("\\s");
		
		return newArray;
	}

	public static void main(String[] args) {
		System.out.println(new Reverse("Akash").reverseString());
		// Using StringBuffer
		String reverse = new StringBuffer("Akash").reverse().toString();
		System.out.println(reverse);
		// Using StringBuilder
		reverse = new StringBuilder("WakeMeUp").reverse().toString();
		System.out.println(reverse);
		
		String arr[] = {"Akki","57","Freaking", "Awesome"};
		reverseInPlace(arr);
		
		String stringToRevrse = "Yo supp mah Nigga";
		reverseInPlace(splitString(stringToRevrse));
		}
}
