package com.java.datastructure;

/**
 * Class to compress strings.
 */
public class StringCompression
{
    /**
     * @param stringToCompare
     */
    private static void compress(final String stringToCompare)
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

        System.out.println(
                stringToCompare.length() <= newString.length() ? stringToCompare : newString);
    }

    public static void main(String[] args)
    {
        compress("aaasddddddddcccccccssdddsssppppppssss");
        compress("aaasddddddddddddddcccccccssdddsssppppppppppssss");
        compress("abcd");
        compress("aabbccdd");
        compress("aabbbcd");
        compress("a");
        compress("aa");
    }
}
