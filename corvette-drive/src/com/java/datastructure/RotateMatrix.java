package com.java.datastructure;

/**
 * Class to rotate the Matrix by 90 degree.
 */
public class RotateMatrix
{
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

        rotateMatrix(N, matrix);
        // Print rotated matrix
        displayMatrix(N, matrix);
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
}
