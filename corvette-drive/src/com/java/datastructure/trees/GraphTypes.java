package com.java.datastructure.trees;

import com.java.datastructure.util.AdjacencyListGraph;

public class GraphTypes {
	 // Adds an edge to an undirected graph
    static void addEdge(AdjacencyListGraph graph, int src, int dest)
    {
        // Add an edge from src to dest. 
        graph.adjListArray[src].addFirst(dest);
         
        // Since graph is undirected, add an edge from dest
        // to src also
        graph.adjListArray[dest].addFirst(src);
    }
    
    static void printGraph(AdjacencyListGraph graph)
    {       
        for(int v = 0; v < graph.value; v++)
        {
            System.out.println("Adjacency list of vertex "+ v);
            System.out.print("head");
            for(Integer pCrawl: graph.adjListArray[v]){
                System.out.print(" -> "+pCrawl);
            }
            System.out.println("\n");
        }
    }
    
    
    public static void main(String[] args) {
    	AdjacencyListGraph graph = new AdjacencyListGraph(5);
		addEdge(graph, 0, 1);
        addEdge(graph, 0, 4);
        addEdge(graph, 1, 2);
        addEdge(graph, 1, 3);
        addEdge(graph, 1, 4);
        addEdge(graph, 2, 3);
        addEdge(graph, 3, 4);
        printGraph(graph);
	}
}
