package com.java.percolation;

import java.awt.Frame;

import javax.swing.JOptionPane;

/**
 * Class to find the Dynamic Connectivity between the given pair. {Weighted. Much more efficient and
 * take nlogn}
 * 
 * @author Akash Pargat
 */
public class QuickUnionUFWeighted
{
    private static int id[];
    private static int size[];

    /**
     * Public constructor.
     * 
     * @param numberOfId
     *            Number of Id in the grid.
     */
    public QuickUnionUFWeighted(int numberOfId)
    {
        id = new int[numberOfId];
        size = new int[numberOfId];
        for (int index = 0; index < numberOfId; index++)
        {
            id[index] = index;
            size[index] = 1;
        }
    }

    /**
     * Determines if the given pair is connected.
     * 
     * @param firstPair
     *            Number to determine the connectivity to.
     * @param secondPair
     *            Number to determine the connectivity with.
     * @return True, if the given pair is connected.
     */
    private boolean connected(int firstPair, int secondPair)
    {
        return root(firstPair) == root(secondPair);
    }

    /**
     * Determines the root of the given number.
     * 
     * @param element
     *            Tree element to the determine the root of.
     * @return The root of the given element.
     */
    private int root(int element)
    {
        while (element != id[element])
        {
            id[element] = id[id[element]];
            element = id[element];
        }
        return element;
    }

    /**
     * Adds a connection between given pairs.
     * 
     * @param firstNumber
     *            Number to connect to.
     * @param secondNumber
     *            Number to connect with.
     */
    private void union(int firstNumber, int secondNumber)
    {
        int firstNumberId = root(firstNumber);
        int secondNumberId = root(secondNumber);

        if (firstNumberId == secondNumberId)
        {
            return;
        }
        if (size[firstNumberId] < size[secondNumberId])
        {
            id[firstNumberId] = secondNumberId;
            size[secondNumberId] += size[firstNumberId];
        }
        else
        {
            id[secondNumberId] = firstNumberId;
            size[firstNumberId] += size[secondNumberId];
        }
    }

    /**
     * Main method to run the program.
     * 
     * @param args
     *            Argument.
     */
    public static void main(String[] args)
    {
        QuickUnionUFWeighted quickUnion = new QuickUnionUFWeighted(10);

        quickUnion.union(4, 3);
        quickUnion.union(3, 8);
        quickUnion.union(6, 5);
        quickUnion.union(9, 4);
        quickUnion.union(2, 1);
        quickUnion.showDialog(quickUnion.connected(8, 9));
        quickUnion.showDialog(quickUnion.connected(5, 4));
        quickUnion.union(5, 0);
        quickUnion.union(7, 2);
        quickUnion.union(6, 1);
        quickUnion.union(7, 3);
        quickUnion.showDialog(quickUnion.connected(5, 4));

        for (int index = 0; index < 10; index++)
        {
            System.out.print(id[index]);
        }
    }

    /**
     * Display a dialog message.
     * 
     * @param isConnected
     *            Boolean to determine what message to display.
     */
    private void showDialog(boolean isConnected)
    {
        if (isConnected)
        {
            JOptionPane.showMessageDialog(new Frame(),
                    "The given pairs are connected and have a path between them."); //$NON-NLS-1$
        }
        else
        {
            JOptionPane.showMessageDialog(new Frame(),
                    "The given pairs are not connected and don't have a path between them."); //$NON-NLS-1$
        }
    }
}
