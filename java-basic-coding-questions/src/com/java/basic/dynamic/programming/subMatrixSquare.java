package com.java.basic.dynamic.programming;

import java.util.HashMap;
import java.util.Map;

public class subMatrixSquare
{
    public static int subArray(int[][] arr)
    {
        int x = arr.length;
        if (x == 0)
            return 0;
        int y = arr[0].length;
        if (y == 0)
            return 0;
        int max = 0;
        int[][] sizes = new int[x][y];
        for (int i = 0; i < x; i++)
        {
            for (int j = 0; j < y; j++)
            {
                if (i == 0 || j == 0)
                {
                    sizes[i][j] = arr[i][j];
                }
                else if (arr[i][j] == 1)
                {
                    sizes[i][j] = Math.min(Math.min(arr[i][j - 1], arr[i - 1][j]),
                            arr[i - 1][j - 1]) + 1;
                }
                if (sizes[i][j] > max)
                {
                    max = sizes[i][j];
                }
            }
        }
        int[] a = new int[5];
        Map<String, int[]> an = new HashMap<>();

        return max;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub

        int[][] mat = { { 0, 0, 1 }, { 0, 1, 1 }, { 1, 1, 1 } };
        System.out.println(subArray(mat));

    }

}
