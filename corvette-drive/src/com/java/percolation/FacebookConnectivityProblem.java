package com.java.percolation;

import java.awt.Frame;

import javax.swing.JOptionPane;

/**
 * Class to find the Facebook Connectivity until everybody is a friend of friend of friend.....<br>
 * {Weighted. Much more efficient and take nlogn}
 * 
 * @author Akash Pargat
 */
public class FacebookConnectivityProblem
{
    private static int id[];
    private static int size[];

    /**
     * Public constructor.
     * 
     * @param numberOfId
     *            Number of Id in the grid.
     */
    public FacebookConnectivityProblem(int numberOfId)
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
        FacebookConnectivityProblem quickUnion = new FacebookConnectivityProblem(10);

        quickUnion.union(4, 3);
        isEveryoneFriendsOfFriendOnFacebook(4, 3);
        quickUnion.union(3, 8);
        isEveryoneFriendsOfFriendOnFacebook(3, 8);
        quickUnion.union(6, 5);
        isEveryoneFriendsOfFriendOnFacebook(6, 5);
        quickUnion.union(9, 4);
        isEveryoneFriendsOfFriendOnFacebook(9, 4);
        quickUnion.union(2, 1);
        isEveryoneFriendsOfFriendOnFacebook(2, 1);
        quickUnion.union(5, 0);
        isEveryoneFriendsOfFriendOnFacebook(5, 0);
        quickUnion.union(7, 2);
        isEveryoneFriendsOfFriendOnFacebook(7, 2);
        quickUnion.union(6, 1);
        isEveryoneFriendsOfFriendOnFacebook(6, 1);
        quickUnion.union(7, 3);
        isEveryoneFriendsOfFriendOnFacebook(7, 3);
        quickUnion.union(5, 3);
        isEveryoneFriendsOfFriendOnFacebook(5, 3);
        quickUnion.union(0, 9);
        isEveryoneFriendsOfFriendOnFacebook(0, 9);

    }

    /**
     * Determines if all are friend of friends on Facebook.
     * 
     * @param firstPerson
     *            Person who wants to connect to.
     * @param secondPerson
     *            Person who is being asked to connect to.
     */
    private static void isEveryoneFriendsOfFriendOnFacebook(int firstPerson, int secondPerson)
    {
        for (int index = 0; index < id.length; index++)
        {
            if (size[index] == id.length)
            {
                JOptionPane.showMessageDialog(new Frame(),
                        "All the persons are friends of friends of friends of friends of......friend after " //$NON-NLS-1$
                                + firstPerson + " and " + secondPerson + " is connected."); //$NON-NLS-1$//$NON-NLS-2$
                break;
            }
        }
    }
}
