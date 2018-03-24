package com.java.basic.programs;

public class Palindrome {
	
String pal;
private static boolean isPalindrome(final int number) {
	int palindrome = number; // copied number into variable
    int reverse = 0;

    while (palindrome != 0) {
        int remainder = palindrome % 10;
        reverse = reverse * 10 + remainder;
        palindrome = palindrome / 10;
    }

    // if original and reverse of number is equal means
    // number is palindrome
    if (number == reverse) {
        return true;
    }
    return false;
}

	
	private static boolean isPalindrome(final String str) {
		
		int length = str.length();
		for(int i =0; i< length/2; i++) {
			if(str.charAt(i)!= str.charAt(length-i-1)) {
				return false;
			}
		}
		return true;
	}
	
	private static boolean isPalindromeRecursion(String s) {
	    int length = s.length();

	    if (length < 2) // If the string only has 1 char or is empty
	        return true;
	    else {
	        // Check opposite ends of the string for equality
	        if (s.charAt(0) != s.charAt(length - 1))
	            return false;
	        // Function call for string with the two ends snipped off
	        else
	            return isPalindrome(s.substring(1, length - 1));
	    }
	}
	
	private static boolean isArmstrong(final int number) {
		int dummy = number;
		int val = 0;
		int cube = 0;
		while(dummy !=0) {
			val = dummy %10;
			cube += (val*val*val);
			dummy = dummy/10;
		}
		if(cube == number) {
			return true;
		}
		return false;
	}
	public static void main(String[] args) {
		System.out.println(isPalindrome("aaaabbbaaaa"));
		System.out.println(isPalindromeRecursion("aaaabbbaaaa"));
		System.out.println(isPalindrome("Akki"));
		System.out.println(isPalindromeRecursion("Akki"));
		System.out.println(isPalindrome(152251));
		System.out.println(isPalindrome(1234));
		System.out.println(isArmstrong(152));
	}
}
