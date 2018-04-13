package com.java.basic.programs;

import java.util.ArrayList;
import java.util.List;

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
            {
                lo = mid + 1;
            }
            else
            {
                hi = mid;
            }
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
            {
                return realmid;
            }
            if (A[realmid] < target)
            {
                lo = mid + 1;
            }
            else
            {
                hi = mid - 1;
            }
        }
        return -1;
    }

    int binarySearch_advanced(int[] nums, int target)
    {
        if (nums == null || nums.length == 0)
        {
            return -1;
        }

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
        {
            return left;
        }
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
        if (nums == null || nums.length == 0)
        {
            return -1;
        }

        if (nums.length == 1)
        {
            return nums[0];
        }

        int start = 0;
        int end = nums.length - 1;

        // not rotated
        if (nums[start] < nums[end])
        {
            return nums[start];
        }

        while (start <= end)
        {
            if (end - start == 1)
            {
                return nums[end];
            }

            int m = start + (end - start) / 2;

            if (nums[m] > nums[end])
            {
                start = m;
            }
            else
            {
                end = m;
            }
        }

        return nums[start];
    }

    public static int[] searchRange(int[] nums, int target)
    {
        if (nums.length == 0)
        {
            return new int[] { -1, -1 };
        }
        int start = 0;
        int end = nums.length - 1;
        int firstIndex = 0;
        if (nums[start] == nums[end] && nums[end] == target)
        {
            return new int[] { start, end };
        }
        while (start + 1 < end)
        {
            int mid = start + (end - start) / 2;
            if (nums[mid] == target)
            {
                firstIndex = mid;
                break;
            }
            else if (nums[mid] < target)
            {
                start = mid;
            }
            else
            {
                end = mid;
            }
        }
        if (nums[start] == target)
        {
            firstIndex = start;
        }
        if (nums[end] == target)
        {
            firstIndex = end;
        }
        if (nums[firstIndex] != target)
        {
            return new int[] { -1, -1 };
        }
        int secondIndex = firstIndex;
        while (firstIndex < nums.length && nums[firstIndex] == target)
        {
            firstIndex++;
        }
        while (secondIndex >= 0 && nums[secondIndex] == target)
        {
            secondIndex--;
        }
        return new int[] { secondIndex + 1, firstIndex - 1 };
    }

    public static List<Integer> findClosestElements(int[] nums, int numberOfClosest, int target)
    {
        List<Integer> newList = new ArrayList<>();
        int start = 0, end = nums.length - 1;
        int index = 0;
        while (start + 1 < end)
        {
            int mid = start + (end - start) / 2;
            if (nums[mid] == target)
            {
                index = mid;
                break;
            }
            if (nums[mid] < target)
            {
                start = mid;
            }
            else
            {
                end = mid;
            }
        }
        if (nums[index] != target)
        {
            index = start;
        }
        if (nums[start] == target)
        {
            index = start;
        }
        if (nums[end] == target)
        {
            index = end;
        }
        int secondIndex = index;
        int dummyNumberOfClosest = numberOfClosest;
        newList.add(nums[index]);
        while (index >= 0 && numberOfClosest > 0)
        {
            int gap1 = nums[index - 1];
            int gap2 = nums[index + 1];
            if (target - gap1 > gap2 - target)
            {
                index--;
            }
            // newList.add(nums[index]);
            numberOfClosest--;
        }
        while (dummyNumberOfClosest > 0)
        {
            index++;
            newList.add(nums[index]);
            dummyNumberOfClosest--;
        }
        return newList;
    }

    public static void main(String[] args)
    {
        // int num[] = { 0, 0, 1, 2, 3, 3, 4, 7, 7, 8 };
        int num[] = { 0, 0, 0, 1, 3, 5, 6, 7, 8, 8 };
        // int num[] = { 1, 2, 3, 4, 5, 6, 7, 8 };
        // System.out.println(search(num, 0));
        // System.out.println(firstBadVersion(10));
        // System.out.println(findPeakElement(num));
        // System.out.println(findMin(num));
        // int val[] = searchRange(num, 8);
        List<Integer> vals = findClosestElements(num, 2, 2);
        for (Integer val : vals)
        {
            System.out.print(val + ", "); //$NON-NLS-1$
        }
    }
}
