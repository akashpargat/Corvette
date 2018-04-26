package com.java.basic.programs;

import java.util.HashMap;
import java.util.Map;

class Solution
{

    // Write your function here

    public static void main(String[] args)
    {
        // Content, user ID, timestamp
        String[][] userContentLikes = new String[][] { { "http://yahoo.com", "user3", "201999" },
                { "http://google.com/maps", "user2", "201004" },
                { "http://google.com/maps", "user1", "201015" },
                { "http://google.com", "user4", "201004" },
                { "http://google.com", "user2", "201012" },
                { "http://google.com/maps", "user2", "201008" },
                { "http://google.com/maps", "user2", "201013" },
                { "http://google.com/maps", "user2", "201030" },
                { "http://altavista.net/q?f=12344", "user3", "100002" },
                { "http://google.com/maps", "user3", "201015" },
                { "http://yahoo.com", "user2", "201035" },
                { "http://altavista.net/q?f=12344", "user1", "99999" },
                { "http://altavista.net/q?f=12344", "user1", "100004" },
                { "http://geocities.com", "user1", "100007" },
                { "http://geocities.com", "user3", "100009" }, };

        Map<String, String[]> myRes = new HashMap<>();

        int[] myarr = new int[10];
        myarr[3] = 3;

        for (int i = 0; i < userContentLikes.length; i++)
        {
            if (myRes.containsKey(userContentLikes[i][0]))
            {
                if (Integer.parseInt(myRes.get(userContentLikes[i][0])[2]) > Integer
                        .parseInt(userContentLikes[i][2]))
                {
                    myRes.put(userContentLikes[i][0], userContentLikes[i]);
                    continue;
                }
            }
            // TIB-3150-LCIQ
            else
            {
                myRes.put(userContentLikes[i][0], userContentLikes[i]);
            }
        }

        for (String[] name : myRes.values())
        {
            System.out.println(name[0] + " => " + name[1]);
        }

    }

}
