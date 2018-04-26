package com.java.basic.programs;

public class Reverse
{
    String newString = "";

    // public Reverse(final String stringToReverse) {
    // // TODO Auto-generated constructor stub
    // newString = stringToReverse;
    // }

    // Old school reverse string
    public static String reverseString(String newString)
    {
        String reverse = "";
        for (int i = newString.length() - 1; i >= 0; i--)
        {
            reverse = reverse + newString.charAt(i);
        }
        return reverse;
    }

    // Old school reverse string
    public static String reverseStringInPlace(String newString)
    {
        char[] newStringChar = newString.toCharArray();
        for (int i = 0; i < newStringChar.length / 2; i++)
        {
            char temp = newStringChar[i];
            newStringChar[i] = newStringChar[newStringChar.length - 1 - i];
            newStringChar[newStringChar.length - 1 - i] = temp;
        }
        // return Arrays.toString(newStringChar);
        // return new String(newStringChar);
        return String.valueOf(newStringChar);
    }

    /**
     * Java Method to reverse String array in place
     * 
     * @param array
     */
    public static String[] reverseInPlaceSentence(String[] array)
    {
        if (array == null || array.length < 2)
        {
            return null;
        }
        for (int i = 0; i < array.length / 2; i++)
        {
            String temp = array[i];
            array[i] = array[array.length - 1 - i];
            array[array.length - 1 - i] = temp;
        }
        for (int i = 0; i < array.length; i++)
        {
            System.out.print(array[i] + " ");
        }

        return array;
    }

    public static String[] splitString(String sentence)
    {
        String[] newArray = sentence.split("\\s");

        return newArray;
    }

    public static String reverse(String sentence)
    {
        String[] newSentense = splitString(sentence);
        StringBuilder newStringBuilder = new StringBuilder();
        for (int i = 0; i < newSentense.length; i++)
        {
            newStringBuilder.append(reverseStringInPlace(newSentense[i]) + " ");
        }
        return newStringBuilder.toString();
    }

    public static int reverseInteger(final int numberToReverse)
    {
        int number = numberToReverse;
        int temp = 0;
        int newReversedNumber = 0;
        if (number == 0)
        {
            return 0;
        }
        while (number > 0)
        {
            temp = number % 10;
            newReversedNumber = (newReversedNumber + temp) * 10;
            number = number / 10;
        }

        return newReversedNumber / 10;
    }

    public static String reverseNew(String stringToReverse)
    {
        StringBuilder newReversedString = new StringBuilder();
        String[] stringArr = stringToReverse.split(" ");
        int length = stringArr.length;
        for (int i = 0; i < length / 2; i++)
        {
            String temp = stringArr[length - 1 - i];
            stringArr[length - 1 - i] = stringArr[i];
            stringArr[i] = temp;
        }
        for (int i = 0; i < stringArr.length; i++)
        {
            newReversedString.append(stringArr[i] + " ");
        }

        return newReversedString.toString();
    }

    public static String reverseWhole(String stringToReverse)
    {
        char[] stringChar = stringToReverse.toCharArray();
        int length = stringChar.length;
        for (int i = 0; i < length / 2; i++)
        {
            char temp = stringChar[length - 1 - i];
            stringChar[length - 1 - i] = stringChar[i];
            stringChar[i] = temp;
        }
        System.out.println(String.copyValueOf(stringChar));
        return String.copyValueOf(stringChar);
    }

    public static void main(String[] args)
    {
        // Using StringBuffer
        // String reverse = new StringBuffer("Akash").reverse().toString();
        // System.out.println(reverse);
        // // Using StringBuilder
        // reverse = new StringBuilder("WakeMeUp").reverse().toString();
        // System.out.println(reverse);
        //
        // //************My Code**************
        // System.out.println(reverseString("Akash"));
        //
        // String arr[] = {"Akki","57","Freaking", "Awesome"};
        // reverseInPlaceSentence(arr);
        //
        String stringToRevrse = "Hey this is Akash";
        // reverseInPlaceSentence(splitString(stringToRevrse));
        //
        // System.out.println(reverse("Hey this is Akash"));
        // System.out.println(reverseInteger(-1234));

        // System.out.println(
        // reverse(String.join(" ", reverseInPlaceSentence(splitString(stringToRevrse)))));

        System.out.println(reverseNew(reverseWhole(stringToRevrse)));
    }
}
