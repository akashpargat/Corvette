package com.java.basic.programs;

/**
 * Given a positive integer N, write an algorithm to populate an NxN int array in a clockwise spiral
 * pattern. Place “1” in the center, and spiral out clockwise until you get to N^2. Assume that the
 * starting coordinate (the location of “1”) has been calculated for you and is passed into the
 * function:
 * 
 * public int[][] spiral (int n, Point start);
 * 
 * Example results for a given value of N:
 * 
 * N = 1
 * 
 * 1
 * 
 * N = 2
 * 
 * 1 2 <br>
 * 4 3
 * 
 * N = 3
 * 
 * 7 8 9 <br>
 * 6 1 2 <br>
 * 5 4 3
 * 
 * Can you fill N = 4 below?
 * 
 * 7 8 9 10 6 1 2 11 5 4 3 12 16 15 14 13
 */
public class PrintSpiralNerd
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
    private static int[][] createSpiralPatter(int matrixDimentionX, int matrixDimentionY,
            Point startPoint)
    {
        if (matrixDimentionX == 0 || matrixDimentionY == 0)
        {
            return new int[0][0];
        }
        int k = startPoint.x, l = startPoint.y, last_col = startPoint.x + 1,
                last_row = startPoint.y + 1;
        int[][] newMatrix = new int[matrixDimentionY][matrixDimentionX];
        int count = 1;

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
        Point startingPoint = new Point(1, 1);
        // Test Suites
        printArray(createSpiralPatter(4, 4, startingPoint));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(createSpiralPatter(5, 4, startingPoint));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(createSpiralPatter(6, 3, startingPoint));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(createSpiralPatter(3, 6, startingPoint));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(createSpiralPatter(1, 1, startingPoint));
        System.out.println("**********************"); //$NON-NLS-1$
        printArray(createSpiralPatter(0, 1, startingPoint));
    }
}

/**
 * Inner class for the starting point.
 * 
 * @author Akash Pargat
 */
class Point
{
    int x;
    int y;

    /**
     * Constructor to initialize the staring points.
     * 
     * @param X
     * @param Y
     */
    Point(int X, int Y)
    {
        x = X;
        y = Y;
    }
}
