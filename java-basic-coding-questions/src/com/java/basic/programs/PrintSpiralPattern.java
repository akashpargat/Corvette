package com.java.basic.programs;

/**
 * Given a positive integer N, write an algorithm to populate an NxN int array in a clockwise spiral
 * pattern. Further modify to have M x N int array.
 * 
 * @author Akash Pargat
 *
 */
public class PrintSpiralPattern
{
    /**
     * Create a spiral matrix.
     * 
     * @param matrixDimentionX
     *            X dimension
     * @param matrixDimentionY
     *            Y dimension
     * @return A spiral matrix with provided dimensions.
     */
    private static int[][] createSpiralPatter(int matrixDimentionX, int matrixDimentionY)
    {
        if (matrixDimentionX == 0 || matrixDimentionY == 0)
        {
            return new int[0][0];
        }
        int k = 0, l = 0, last_col = matrixDimentionX - 1, last_row = matrixDimentionY - 1;
        int[][] newMatrix = new int[matrixDimentionY][matrixDimentionX];
        int count = 1;
        while (last_col >= l && last_row >= k)
        {
            for (int i = l; i <= last_col; i++)
            {
                newMatrix[k][i] = count++;
            }
            k++;
            for (int i = k; i <= last_row; i++)
            {
                newMatrix[i][last_col] = count++;
            }
            last_col--;

            if (k <= last_row)
            {
                for (int i = last_col; i >= l; i--)
                {
                    newMatrix[last_row][i] = count++;
                }
                last_row--;
            }
            if (l <= last_col)
            {
                for (int i = last_row; i >= k; i--)
                {
                    newMatrix[i][l] = count++;
                }
                l++;
            }
        }

        return newMatrix;
    }

    /**
     * Prints the given spiral matrix.
     * 
     * @param matrix
     *            the spiral matrix to print.
     */
    public static void printArray(int matrix[][])
    {
        if (matrix.length == 0)
        {
            System.out.println(
                    "Hey please help yourself as the array cannot be printed in spiral if you don't provide me the dimensions."); //$NON-NLS-1$
        }
        for (int row = 0; row < matrix.length; row++)
        {
            for (int column = 0; column < matrix[row].length; column++)
            {
                System.out.print(matrix[row][column] + "   "); //$NON-NLS-1$
            }
            System.out.println();
        }
    }

    public static void main(String[] args)
    {
        // Test Suites
        printArray(createSpiralPatter(4, 4));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(createSpiralPatter(5, 4));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(createSpiralPatter(6, 3));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(createSpiralPatter(3, 6));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(createSpiralPatter(1, 1));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(createSpiralPatter(0, 1));
    }
}
