package com.java.datastructure;

public class TwoHighestNumber {

	
	private int getLargest(final int num[]) {
		boolean swap = false;
		do{
			swap = false;
		for(int i = 0 ; i<num.length -1 ;i++) {
			if(num[i] > num[i+1]) {
				int temp = num[i+1];
				num[i+1] = num[i];
				num[i]= temp;
				swap = true;
			}
		}
		
		}while(swap ==true);
		return num[num.length -2]* num[num.length-1];
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
TwoHighestNumber number = new TwoHighestNumber();
int [] num = new int[] {7,5,14,2,8,8,10,1,2,3};
System.out.println(number.getLargest(num));
for(int i =0 ; i<num.length-1; i++) {
	System.out.println(num[i]);
}
	}

}
