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
        compress("aaasddddddddcccccccssdddsssppppppssss"); //$NON-NLS-1$
        compress("aaasddddddddddddddcccccccssdddsssppppppppppssss"); //$NON-NLS-1$
        compress("abcd"); //$NON-NLS-1$
        compress("aabbccdd"); //$NON-NLS-1$
        compress("aabbbcd"); //$NON-NLS-1$
        compress("a"); //$NON-NLS-1$
        compress("aa"); //$NON-NLS-1$
    }
}
