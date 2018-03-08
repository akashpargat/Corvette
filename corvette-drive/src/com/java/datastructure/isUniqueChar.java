package com.java.datastructure;

public class isUniqueChar {

	public static String isUniqueChars(String str) {
		boolean[] value = new boolean[128];
		for(int i =0; i<str.length(); i++) {
			int uniCode = str.charAt(i);
			if(value[uniCode] ) {
				return "Fuck you bitch this is not a Unique string.";
			}
			value[uniCode] = true;
		}

return "The given string is unique.";
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
System.out.println(isUniqueChars("JATIN"));
	}

}
