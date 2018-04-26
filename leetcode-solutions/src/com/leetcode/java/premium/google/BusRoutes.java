package com.leetcode.java.premium.google;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Queue;
import java.util.Set;
import java.util.TreeSet;

public class BusRoutes implements Pair<Integer, Integer>
{

    public static int numBusesToDestination(int[][] routes, int S, int T)
    {
        Map<Integer, List<Integer>> busRoutes = new HashMap<>();
        Set<Integer> stops = new TreeSet<Integer>();

        for (int busNumber = 0; busNumber < routes.length; busNumber++)
        {
            List<Integer> route = new ArrayList<Integer>();
            for (Integer val : routes[busNumber])
            {
                route.add(val);
                stops.add(val);
            }
            busRoutes.put(busNumber, route);
        }
        Map<Integer, List<Integer>> busRoutes_eachStop = new HashMap<>();
        for (Integer lst_stop : stops)
        {
            List<Integer> busNumbers = new ArrayList<>();
            for (Entry<Integer, List<Integer>> entry : busRoutes.entrySet())
            {
                if (entry.getValue().contains(lst_stop))
                {
                    busNumbers.add(entry.getKey());
                }
            }
            busRoutes_eachStop.put(lst_stop, busNumbers);
        }

        Queue<int[]> toVisit = new LinkedList<>();
        int[] stop = { S, 0 };
        toVisit.add(stop);
        Set<Integer> visited = new TreeSet<>();
        visited.add(S);

        while (!toVisit.isEmpty())
        {
            int stop_number = toVisit.peek()[0];
            int bus_numbers = toVisit.peek()[1];
            if (stop_number == T)
            {
                return bus_numbers;
            }
            toVisit.poll();
            for (Integer busNumbers : busRoutes_eachStop.get(stop_number))
            {
                System.out.println(bus_numbers);
            }
        }
        return -1;
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        int[][] routes = { { 1, 2, 7 }, { 3, 6, 7 } };
        int start = 7;
        int end = 6;

        System.out.println(numBusesToDestination(routes, start, end));
    }

    @Override
    public Integer getL()
    {
        // TODO Auto-generated method stub
        return null;
    }

    @Override
    public Integer getR()
    {
        // TODO Auto-generated method stub
        return null;
    }

}
