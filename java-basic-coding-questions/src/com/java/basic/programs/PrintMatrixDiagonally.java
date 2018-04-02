package com.java.basic.programs;

import static com.java.basic.programs.PrintSpiralPattern.printArray;

/**
 * Given a positive integer N, write an algorithm to populate an NxN int array diagonal pattern.
 * Further modify to have M x N int array.
 * 
 * @author Akash Pargat
 */
public class PrintMatrixDiagonally
{
    private static int[][] printMatrix(int matrixDimensionX, int matrixDimensionY)
    {
        int newArray[][] = new int[matrixDimensionX][matrixDimensionY];
        int i = 0, j = 0, count = 1;
        if (matrixDimensionX == 0 || matrixDimensionY == 0)
        {
            System.out.println("Come on....I mean please are you out of your mind???");
        }

        for (int k = 0; k <= matrixDimensionX - 1; k++)
        {
            i = k;
            j = 0;
            while (i >= 0 && j < matrixDimensionY)
            {
                newArray[i][j] = count++;
                i = i - 1;
                j = j + 1;
            }
        }

        for (int k = 1; k <= matrixDimensionY - 1; k++)
        {
            i = matrixDimensionX - 1;
            j = k;

            while (j <= matrixDimensionY - 1 && i >= 0)
            {
                newArray[i][j] = count++;
                i = i - 1;
                j = j + 1;
            }

        }
        return newArray;
    }

    public static void main(String[] args)
    {
        // Test Suites
        printArray(printMatrix(4, 4));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(printMatrix(5, 4));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(printMatrix(6, 3));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(printMatrix(3, 6));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(printMatrix(1, 1));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(printMatrix(0, 1));
    }
}
