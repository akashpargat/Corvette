package com.java.datastructure;

import java.util.Scanner;

public class TowersOfHanoi {

	   public void towerOfHanoi(int n, String start, String auxiliary, String end) {
	       if (n == 1) {
	           System.out.println(start + " -> " + end);
	       } else {
	           towerOfHanoi(n - 1, start, end, auxiliary);
	           System.out.println(start + " -> " + end);
	           towerOfHanoi(n - 1, auxiliary, start, end);
	       }
	   }

	   public static void main(String[] args) {
	       TowersOfHanoi towersOfHanoi = new TowersOfHanoi();
	       System.out.print("Enter number of discs: ");
	       Scanner scanner = new Scanner(System.in);
	       int discs = scanner.nextInt();
	       towersOfHanoi.towerOfHanoi(discs, "A", "B", "C");
	       scanner.close();
	   }
	}