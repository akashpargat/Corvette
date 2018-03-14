package com.java.datastructure.trees;

import static com.java.datastructure.trees.GraphTypes.addEdge;
import static com.java.datastructure.trees.GraphTypes.printGraph;

import java.util.Iterator;
import java.util.LinkedList;

import com.java.datastructure.util.AdjacencyListGraph;

public class BreadthFirstSearchGraph
{
    private static int numberOfVertices = 7;
    public static AdjacencyListGraph graph;
    static boolean visited[];

    private void breadthFirstSearch(int s)
    {
        // Mark all the vertices as not visited(By default
        // set as false)

        // Create a queue for BFS
        LinkedList<Integer> queue = new LinkedList<Integer>();

        // Mark the current node as visited and enqueue it
        visited[s] = true;
        queue.add(s);

        while (queue.size() != 0)
        {
            // Dequeue a vertex from queue and print it
            s = queue.poll();
            System.out.print(s + " ");

            // Get all adjacent vertices of the dequeued vertex s
            // If a adjacent has not been visited, then mark it
            // visited and enqueue it
            Iterator<Integer> i = graph.adjListArray[s].listIterator();
            while (i.hasNext())
            {
                int n = i.next();
                if (!visited[n])
                {
                    visited[n] = true;
                    queue.add(n);
                }
            }
        }
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
        addEdge(graph, 2, 1);
        addEdge(graph, 1, 4);
        addEdge(graph, 1, 3);
        addEdge(graph, 2, 3);
        addEdge(graph, 2, 5);
        addEdge(graph, 5, 6);
        addEdge(graph, 4, 6);
        addEdge(graph, 3, 6);
        addEdge(graph, 6, 5);
        printGraph(graph);
        // graph.preOrderTraversal(graph.root);
        System.out.println();
        BreadthFirstSearchGraph bfs = new BreadthFirstSearchGraph();
        bfs.breadthFirstSearch(2);
    }

}
