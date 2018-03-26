package com.java.datastructure;

import java.util.Arrays;
import java.util.Scanner;

public class Permutation
{
    private static final Scanner scan = new Scanner(System.in);

    public static void determinePermutation(String firstString, String secondString)
    {
        char first[] = firstString.toCharArray();
        char second[] = secondString.toCharArray();

        Arrays.sort(first);
        Arrays.sort(second);
        if (first.length != second.length)
        {
            System.out.println("Asshole this can never be a permutation.");
        }
        if (Arrays.equals(first, second))
        {
            System.out.println("The given string is the permutaiton of each other.");
            return;
        }

        System.out.println("The given string is not the permutaiton of each other.");
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        determinePermutation("Akash", "shakA");

        int n = Integer.parseInt(scan.nextLine().trim());

        int[] arr = new int[n];

        String[] arrItems = scan.nextLine().split(" ");

        for (int arrItr = 0; arrItr < n; arrItr++)
        {
            int arrItem = Integer.parseInt(arrItems[arrItr].trim());
            arr[arrItr] = arrItem;
        }
        for (int i = arr.length - 1; i >= 0; i--)
        {
            System.out.print(arrItems[i]);
        }
    }

}
