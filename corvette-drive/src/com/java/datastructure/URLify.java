package com.java.datastructure;

import java.util.ArrayList;
import java.util.Arrays;

public class URLify {
public static int countBlankSpace(String str) {
	int count =0;
	char []actualString = str.toCharArray();
	for(int i=0; i< actualString.length;i++) {
		if(actualString[i]== ' ') {
			count++;
		}
	}
	return count;
}

public static char[]  urlIfy(String str) {
	int newStringLength =str.length()+countBlankSpace(str)*2;
	char [] oldString = str.toCharArray();
	char[] newString = new char[newStringLength];

	for(int i=oldString.length-1; i>=0; i--) {
		if(oldString[i] == ' ') {
			newString[newStringLength-1]='0';
			newString[newStringLength-2]='2';
			newString[newStringLength-3]='%';
			newStringLength = newStringLength-3;
		}else {
			newString[newStringLength-1]=oldString[i];
			newStringLength--;
		}
	}

	return newString;
}

public class salary{
	public salary() {
		// TODO Auto-generated constructor stub
	}
	private void salary_print() {
		// TODO Auto-generated method stub
System.out.println("Fuck you see I am  in the salaray class.");
	}
}

private class employee extends salary{
	private void salary_print() {
		// TODO Auto-generated method stub
System.out.println("Fuck you see I am  in the employee class.");
	}
}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
System.out.println(urlIfy("Yo Mr. Diggle how is it going?"));
URLify ur = new URLify();
ur.mockInfo();
	}

	void mockInfo(){

salary sal = new salary();
sal.salary_print();
salary sl = new employee();
sl.salary_print();
employee e = new employee();
	}
}
