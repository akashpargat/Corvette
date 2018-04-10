package com.java.basic.programs;

public class BinarySearchRotatedSorted
{

    public static int search(int A[], int target)
    {
        int n = A.length;
        int lo = 0, hi = n - 1;
        while (lo < hi)
        {
            int mid = (lo + hi) / 2;
            if (A[mid] > A[hi])
                lo = mid + 1;
            else
                hi = mid;
        }
        int rot = lo;
        lo = 0;
        hi = n - 1;
        // The usual binary search and accounting for rotation.
        while (lo <= hi)
        {
            int mid = (lo + hi) / 2;
            int realmid = (mid + rot) % n;
            if (A[realmid] == target)
                return realmid;
            if (A[realmid] < target)
                lo = mid + 1;
            else
                hi = mid - 1;
        }
        return -1;
    }

    int binarySearch_advanced(int[] nums, int target)
    {
        if (nums == null || nums.length == 0)
            return -1;

        int left = 0, right = nums.length;
        while (left < right)
        {
            // Prevent (left + right) overflow
            int mid = left + (right - left) / 2;
            if (nums[mid] == target)
            {
                return mid;
            }
            else if (nums[mid] < target)
            {
                left = mid + 1;
            }
            else
            {
                right = mid;
            }
        }

        // Post-processing:
        // End Condition: left == right
        if (left != nums.length && nums[left] == target)
            return left;
        return -1;
    }

    public static int firstBadVersion(int n)
    {

        int start = 1;
        int end = n;
        while (start < end)
        {
            int mid = start + (end - start) / 2;
            if (isBadVersion(mid))
            {
                end = mid;
            }
            else
            {
                start = mid + 1;
            }
        }

        return start;
    }

    public static boolean isBadVersion(int n)
    {
        for (int i = 6; i <= n; i++)
        {
            if (i == i)
            {
                return true;
            }
        }
        return false;
    }

    public static int findPeakElement(int[] nums)
    {
        if (nums.length == 0 || nums == null)
        {
            return 0;
        }
        int start = 0;
        int end = nums.length - 1;
        while (start <= end)
        {
            int mid = start + (end - start) / 2;
            if (nums[mid] > nums[mid + 1])
            {
                return mid;
            }
            else if (nums[mid] > nums[mid + 1])
            {
                start = mid + 1;
            }
            else
            {
                end = mid;
            }
        }
        return end;
    }

    public static int findMin(int[] nums)
    {
        if (nums.length == 0 || nums == null)
        {
            return 0;
        }
        if (nums.length == 1)
        {
            return 1;
        }
        int start = 0;
        int end = nums.length - 1;
        while (start < end)
        {
            int mid = start + (end - start) / 2;
            if (nums[mid] > nums[mid + 1])
            {
                start = mid + 1;
            }
            else
            {
                end = mid;
            }

        }
        return nums[end];
    }

    public static void main(String[] args)
    {
        int num[] = { 2, 3, 4, 5, 1 };
        // System.out.println(search(num, 0));
        // System.out.println(firstBadVersion(10));
        // System.out.println(findPeakElement(num));
        System.out.println(findMin(num));
    }
}
