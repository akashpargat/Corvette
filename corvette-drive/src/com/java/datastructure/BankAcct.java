package com.java.datastructure;

import java.io.IOException;

import com.java.datastructure.sorts.SelectionSort;

public class BankAcct extends SelectionSort
{
	private class akash{
		akash(){
			System.out.println("This is Akash.");
		}
	}
	private int x;
    private int y;
    public static int mystMethod(int st, int mv)
    {
         if (mv > st)
         {
              int diff = mv - st;
              mv--;
              return diff + mystMethod(st, mv);
         }
         else if (mv < st)
         {
              int diff = st - mv;
              mv++;
              return diff + mystMethod(st, mv);
         }
         else
              return st;
         }
    public BankAcct()
    {
         this.x = 0;
         this.y = 0;
    }

    public BankAcct(int _x, int _y)
    {
         this.x = _x;
         this.y = _y;
    }

     public void move(int dx, int dy)
    {
         this.x += dx;
         this.y += dy;
    }

    public void moveTo(int new_x, int new_y)
    {
         this.x = new_x;
         this.y = new_y;
    }

    public String toString()
    {


    	double d = (double)1 / 3;
    	 System.out.println(d);
         return "(" + this.x + ", " + this.y + ")";
    }
     
     public static void main(String[] args) throws IOException {
    	 BankAcct pt = new BankAcct(4, 8);
    	 pt.move(-3, 7);
    	 pt.moveTo(-3, 7);
    	 pt.move(-3, 7);
   
    	 String str  = "Akash";
int num = 30;
    	 while (num != 0)
    	 {
    		 System.out.println("Fuck You");
    	  num /= 2;
    	  
    	 }
    	 BankAcct ak = new BankAcct();
    	 
 	}
}