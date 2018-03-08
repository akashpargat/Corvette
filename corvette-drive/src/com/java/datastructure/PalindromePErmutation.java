package com.java.datastructure;

public class PalindromePErmutation {
	public static String palindrome(String str) {
		char []strArray = str.toCharArray();
		int index =str.length()-1;
		for(int i =0; i<str.length(); i++) {
			if(strArray[i]==' ') {
				i++;
			}
			if(strArray[index]==' ') {
				index--;
			}
			if(strArray[i]!=strArray[index]) {
				return "The give string is not a palindrome.";
			}
			
			index--;
		}
		return "The given string is a palindrome.";
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println(palindrome("?eva, can i stab bats in a c,ave?"));
	}
}
