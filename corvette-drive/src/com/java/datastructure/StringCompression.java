package com.java.datastructure;

/**
 * Input: aaasddddddddcccccccssdddsssppppppssss Output: a3s1d8c7s2d3s3p6s4
 * 
 * @author AP027887
 */
public class StringCompression
{

    private static void compare(final String stringToCompare)
    {
        int count = 0;
        StringBuffer newString = new StringBuffer();
        for (int i = 0; i < stringToCompare.length(); i++)
        {
            count++;
            if (i + 1 == stringToCompare.length()
                    || stringToCompare.charAt(i) != stringToCompare.charAt(i + 1))
            {
                newString.append(stringToCompare.charAt(i));
                newString.append(count);
                count = 0;
            }
        }
        System.out.println(newString);
    }

    // a3s1d8c7s2d3s3p6s4
    public static void main(String[] args)
    {
        compare("aaasddddddddcccccccssdddsssppppppssss");
    }
}
