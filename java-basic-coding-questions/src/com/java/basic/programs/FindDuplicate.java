package com.java.basic.programs;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class FindDuplicate {

	private static void printDuplicate(final String word) {
		char[] chars = word.toCharArray();
		Map<Character, Integer> newMap = new HashMap<>();
		for (Character myChar : chars) {
			if (newMap.containsKey(myChar)) {
				newMap.put(myChar, newMap.get(myChar) + 1);
			} else {
				newMap.put(myChar, 1);
			}
		}
		System.out.println("In the given string : " + word);
		for (Map.Entry<Character, Integer> entry : newMap.entrySet()) {
			if (entry.getValue() > 1) {
				System.out.println("The character " + entry.getKey() + " is repeated " + entry.getValue() + " times.");
			}
		}
	}

	private static boolean isAnagram(String word1, String word2) {

		char[] charFromWord = word1.toCharArray();
		char[] charFromAnagram = word2.toCharArray();
		Arrays.sort(charFromWord);
		Arrays.sort(charFromAnagram);

		return Arrays.equals(charFromWord, charFromAnagram);
	}

	public static boolean checkAnagram(String first, String second) {
		char[] characters = first.toCharArray();
		StringBuilder sbSecond = new StringBuilder(second);
		for (char ch : characters) {
			int index = sbSecond.indexOf("" + ch);
			if (index != -1) {
				sbSecond.deleteCharAt(index);
			} else {
				return false;
			}
		}
		return sbSecond.length() == 0 ? true : false;
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		printDuplicate("AkkiCool");
		System.out.println(isAnagram("Akash", "Akash"));
		System.out.println(checkAnagram("Akash", "Akash"));
	}
}
