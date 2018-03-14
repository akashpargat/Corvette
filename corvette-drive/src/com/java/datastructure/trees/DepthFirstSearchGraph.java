package com.java.datastructure.trees;

import static com.java.datastructure.trees.GraphTypes.addEdge;
import static com.java.datastructure.trees.GraphTypes.printGraph;

import java.util.Iterator;

import com.java.datastructure.util.AdjacencyListGraph;

public class DepthFirstSearchGraph
{
    private static int numberOfVertices = 7;
    public static AdjacencyListGraph graph;
    static boolean visited[];

    private void depthFirstSearchGraph(int s)
    {
        visited[s] = true;
        System.out.print(s + " ");

        Iterator<Integer> i = graph.adjListArray[s].listIterator();
        while (i.hasNext())
        {
            int n = i.next();
            if (!visited[n])
            {
                depthFirstSearchGraph(n);
            }
        }
    }

    private String findRoute(int source, int destination)
    {
        depthFirstSearchGraph(source);
        if (visited[destination])
        {
            return "Ohh awesome man I found the route...!!";
        }
        System.out.println("Bullshit man I was not able to find the route...!!");
        return null;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        graph = new AdjacencyListGraph(numberOfVertices);
        visited = new boolean[numberOfVertices];
        addEdge(graph, 0, 1);
        addEdge(graph, 0, 2);
        addEdge(graph, 1, 0);
        addEdge(graph, 2, 0);
        addEdge(graph, 1, 2);
        // addEdge(graph, 2, 1);
        // addEdge(graph, 1, 4);
        // addEdge(graph, 1, 3);
        // addEdge(graph, 2, 3);
        addEdge(graph, 2, 5);
        addEdge(graph, 5, 6);
        addEdge(graph, 4, 6);
        // addEdge(graph, 3, 6);
        addEdge(graph, 6, 5);
        printGraph(graph);
        // graph.preOrderTraversal(graph.root);
        System.out.println();
        DepthFirstSearchGraph bfs = new DepthFirstSearchGraph();
        bfs.depthFirstSearchGraph(2);
        System.out.println(bfs.findRoute(2, 6));
    }

}
