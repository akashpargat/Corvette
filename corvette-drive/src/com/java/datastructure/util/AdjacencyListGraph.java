package com.java.datastructure.util;

import java.util.LinkedList;

public class AdjacencyListGraph
{
    public int value;
    public LinkedList<Integer> adjListArray[];
     
    // constructor 
    public AdjacencyListGraph(int value)
    {
        this.value = value;
         
        // define the size of array as 
        // number of vertices
        adjListArray = new LinkedList[value];
         
        // Create a new list for each vertex
        // such that adjacent nodes can be stored
        for(int i = 0; i < value ; i++){
            adjListArray[i] = new LinkedList<>();
        }
    }
}