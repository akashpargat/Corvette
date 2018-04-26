package com.leetcode.java.premium.google;

public class LicenseKeyFormatting
{

    public static String licenseKeyFormatting(String S, int K)
    {
        S = S.replaceAll("-", "").toUpperCase();
        StringBuilder sb = new StringBuilder(S);
        // Starting from the end of sb, and going backwards.
        int i = sb.length() - K;
        while (i > 0)
        {
            sb.insert(i, '-');
            i = i - K;
        }
        return sb.toString();
    }

    public static void main(String[] args)
    {
        // TODO Auto-generated method stub
        System.out.println(licenseKeyFormatting("5F3Zy-2e-9-w", 4));
        System.out.println(licenseKeyFormatting("5F-3Zy-2e-9-w", 4));
        System.out.println(licenseKeyFormatting("5F-3Zy-2e-9-w", 0));
        System.out.println(licenseKeyFormatting("r", 1));
        System.out.println(licenseKeyFormatting("0123456789", 10));
    }

}
