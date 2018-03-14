package com.java.datastructure.util;

public class AdjacencyMatrixGraph {

	public int value;
	public boolean index[][];
	     
	    // constructor 
	    public AdjacencyMatrixGraph(int value, int x, int y)
	    {
	        this.value = value;
	         this.index=  new boolean[x][y];
	    }
	    
	    public void addEdge(int i, int j) {
	    	index[i][j] = true;
	    }
	    public void removeEdge(int i, int j) {
	    	index[i][j] = false;
	    }
	    public boolean hasEdge(int i, int j) {
	        return index[i][j];
	    }
}
