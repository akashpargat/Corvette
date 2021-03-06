package com.java.percolation;

import java.awt.Frame;

import javax.swing.JOptionPane;

/**
 * Class to find the Dynamic Connectivity between the given pair.
 * 
 * @author Akash Pargat
 */
public class QuickFindUF
{
    private int id[];

    /**
     * Public constructor.
     * 
     * @param numberOfId
     *            Number of Id in the grid.
     */
    public QuickFindUF(final int numberOfId)
    {
        id = new int[numberOfId];
        for (int index = 0; index < numberOfId; index++)
        {
            id[index] = index;
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
        return id[firstPair] == id[secondPair];
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
        int firstNumberId = id[firstNumber];
        int secondNumberId = id[secondNumber];

        for (int index = 0; index < id.length; index++)
        {
            if (id[index] == firstNumberId)
            {
                id[index] = secondNumberId;
            }
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
        QuickFindUF quickFind = new QuickFindUF(10);
        quickFind.union(5, 7);
        quickFind.union(6, 2);
        quickFind.union(3, 2);

        quickFind.showDialog(quickFind.connected(6, 3));
        quickFind.showDialog(quickFind.connected(7, 3));
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
