package com.java.basic.programs;

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
	public static void main(String[] args) {
		// TODO Auto-generated method stub
printPyramidOne();
//printPyramidTwo();
printPyramidThree();
	}

}
