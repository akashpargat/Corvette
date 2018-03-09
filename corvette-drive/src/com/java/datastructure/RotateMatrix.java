package com.java.datastructure;

import java.util.ArrayList;
import java.util.List;

/**
 * Class to rotate the Matrix by 90 degree.
 */
@SuppressWarnings("nls")
public class RotateMatrix
{
    /**
     * Main Method for entry point.
     * 
     * @param args
     */
    public static void main(String[] args)
    {
        int N = 4;
        // Test Case 1
        int matrix[][] = { { 1, 2, 3, 4 }, { 5, 6, 7, 8 }, { 9, 10, 11, 12 }, { 13, 14, 15, 16 } };
        // Test Case 2
        /*
         * int matrix[][] = { {1, 2, 3}, {4, 5, 6}, {7, 8, 9} };
         */
        // Test Case 3
        /*
         * int matrix[][] = { {1, 2}, {4, 5} };
         */

        // Test Case 1 for zero Matrix
        int zeroMatrix[][] = { { 1, 2, 3, 4 }, { 5, 6, 0, 8 }, { 9, 10, 11, 12 },
                { 13, 0, 15, 16 } };

        rotateMatrix(N, matrix);
        // Print rotated matrix
        displayMatrix(N, matrix);

        zeroMatrix(N, zeroMatrix);
        // Print rotated matrix
        displayMatrix(N, zeroMatrix);
    }

    /**
     * Function to rotate the matrix.
     * 
     * @param n
     *            Levels in a matrix.
     * @param matrix
     *            matrix to print
     */
    private static void rotateMatrix(final int n, final int[][] matrix)
    {
        for (int x = 0; x < n / 2; x++)
        {
            for (int y = x; y < n - 1 - x; y++)
            {
                int temp = matrix[x][y];
                matrix[x][y] = matrix[y][n - 1 - x];
                matrix[y][n - 1 - x] = matrix[n - 1 - x][n - 1 - y];
                matrix[n - 1 - x][n - 1 - y] = matrix[n - 1 - y][x];
                matrix[n - 1 - y][x] = temp;
            }
        }
    }

    /**
     * Function to print the matrix
     * 
     * @param N
     *            Levels in a matrix.
     * @param matrix
     *            matrix to print
     */
    static void displayMatrix(final int N, final int matrix[][])
    {
        for (int i = 0; i < N; i++)
        {
            for (int j = 0; j < N; j++)
            {
                System.out.print(" " + matrix[i][j]);
            }

            System.out.print("\n");
        }
        System.out.print("\n");
    }

    /**
     * Function to rotate the matrix. (Not an optimized way to do this.)
     * 
     * @param n
     *            Levels in a matrix.
     * @param matrix
     *            matrix to print
     */
    private static void zeroMatrix(final int n, final int[][] matrix)
    {
        List<Integer> row = new ArrayList<>();
        List<Integer> column = new ArrayList<>();
        for (int x = 0; x < n; x++)
        {
            for (int y = 0; y < n; y++)
            {
                if (matrix[x][y] == 0)
                {
                    System.out.println(matrix[x][y] + " : (" + x + y + ")");
                    row.add(x);
                    column.add(y);
                }
            }
        }

        for (int i = 0; i < row.size(); i++)
        {
            for (int y = 0; y < n; y++)
            {
                matrix[row.get(i)][y] = 0;
            }
        }
        for (int i = 0; i < column.size(); i++)
        {
            for (int y = 0; y < n; y++)
            {
                matrix[y][column.get(i)] = 0;
            }
        }
    }
}
