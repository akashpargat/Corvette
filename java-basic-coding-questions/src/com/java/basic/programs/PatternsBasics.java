package com.java.basic.programs;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class PatternsBasics {

	public PatternsBasics() {
		// TODO Auto-generated constructor stub
	}
private static  void printPyramidOne() {
	for(int i = 5; i>0 ; i--) {
		for(int j= 0 ; j<i; j++) {
			System.out.print("*");
		}
		System.out.println();
	}
}
private static  void printPyramidTwo() {
	for(int i = 0; i<5 ; i++) {
		for(int j= 0 ; j<=i; j++) {
			System.out.print("*");
		}
		System.out.println();
	}
}
private static  void printPyramidThree() {
	for(int i = 5; i>0 ; i--) {
		for(int j= 0 ; j<i; j++) {
			System.out.print("*");
		}
		System.out.println("");
		for(int k = 5; k>0 ; k--) {
			
			System.out.print(" ");
		}
	}
}

public static int[] anagramMappings(int[] A, int[] B) {
    if (A == null || B == null || A.length == 0) {
        return null;
    }

    final int[] result = new int[A.length];
    final Map<Integer, ArrayList<Integer>> map = new HashMap<>();
    
    // Prepare the keys
    for (int element : A) {
        if (!map.containsKey(element)) {
            map.put(element, new ArrayList<Integer>());
        }
    }
    // Prepare the indexes
    for (int i = 0; i < B.length; i++) {
        map.get(B[i]).add(i);
    }
    
    for (int i = 0; i < A.length; i++) {
        final ArrayList<Integer> list = map.get(A[i]);
        result[i] = list.get(0);
        list.remove(0);            
    }
    return result;
}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
printPyramidOne();
//printPyramidTwo();
printPyramidThree();
System.out.println(anagramMappings(new int[]{21,23,11}, new int [] {23,11,21}));

	}

}
