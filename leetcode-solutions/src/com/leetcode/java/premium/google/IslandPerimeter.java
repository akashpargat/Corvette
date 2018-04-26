package com.leetcode.java.premium.google;

public class IslandPerimeter
{
    public static int islandPerimeter(int[][] grid)
    {
        int count = 0;
        int row = grid.length;
        int column = grid[0].length;
        for (int i = 0; i < row; i++)
        {
            for (int j = 0; j < column; j++)
            {
                if (grid[i][j] == 0)
                {
                    continue;
                }
                if (grid[i][j] == 1)
                {
                    count += 4;
                }
                // Upper
                if (i != 0 && grid[i - 1][j] == 1)
                {
                    count--;
                }
                // Left
                if (j != 0 && grid[i][j - 1] == 1)
                {
                    count--;
                }
                // Neeche
                if (i < row - 1 && grid[i + 1][j] == 1)
                {
                    count--;
                }
                // Right
                if (j < column - 1 && grid[i][j + 1] == 1)
                {
                    count--;
                }
            }
        }
        return count;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        int[][] grid = { { 0, 1, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 1, 1, 0, 0 } };
        System.out.println(islandPerimeter(grid));
    }

}
