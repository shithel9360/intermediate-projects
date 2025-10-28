/*
 * Sorting and Searching Algorithms in Java
 * 
 * Demonstrates classic algorithms with clear, commented implementations and analysis.
 * Includes:
 * - Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort
 * - Linear Search, Binary Search
 * - Utility methods and runtime measurements
 * 
 * Author: Intermediate Projects Collection
 */

import java.util.Arrays;
import java.util.Random;

public class sorting_searching {

    // ===================== SORTING ALGORITHMS =====================

    // Bubble Sort: Repeatedly swaps adjacent elements if out of order
    // Time: O(n^2), Space: O(1), Stable: Yes
    public static void bubbleSort(int[] arr) {
        boolean swapped;
        for (int i = 0; i < arr.length - 1; i++) {
            swapped = false;
            for (int j = 0; j < arr.length - 1 - i; j++) {
                if (arr[j] > arr[j + 1]) {
                    swap(arr, j, j + 1);
                    swapped = true;
                }
            }
            if (!swapped) break; // Optimization: stop if already sorted
        }
    }

    // Selection Sort: Selects minimum and moves to correct position
    // Time: O(n^2), Space: O(1), Stable: No
    public static void selectionSort(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            int minIdx = i;
            for (int j = i + 1; j < arr.length; j++) {
                if (arr[j] < arr[minIdx]) {
                    minIdx = j;
                }
            }
            swap(arr, i, minIdx);
        }
    }

    // Insertion Sort: Builds sorted array one item at a time
    // Time: O(n^2), Space: O(1), Stable: Yes
    public static void insertionSort(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            int key = arr[i];
            int j = i - 1;
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    }

    // Merge Sort: Divide and conquer
    // Time: O(n log n), Space: O(n), Stable: Yes
    public static void mergeSort(int[] arr) {
        if (arr.length <= 1) return;
        mergeSort(arr, 0, arr.length - 1);
    }

    private static void mergeSort(int[] arr, int left, int right) {
        if (left >= right) return;
        int mid = left + (right - left) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }

    private static void merge(int[] arr, int left, int mid, int right) {
        int n1 = mid - left + 1;
        int n2 = right - mid;
        int[] L = new int[n1];
        int[] R = new int[n2];
        for (int i = 0; i < n1; i++) L[i] = arr[left + i];
        for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];

        int i = 0, j = 0, k = left;
        while (i < n1 && j < n2) {
            if (L[i] <= R[j]) {
                arr[k++] = L[i++];
            } else {
                arr[k++] = R[j++];
            }
        }
        while (i < n1) arr[k++] = L[i++];
        while (j < n2) arr[k++] = R[j++];
    }

    // Quick Sort: Divide and conquer using partitioning
    // Time: Avg O(n log n), Worst O(n^2), Space: O(log n), Stable: No
    public static void quickSort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }

    private static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int p = partition(arr, low, high);
            quickSort(arr, low, p - 1);
            quickSort(arr, p + 1, high);
        }
    }

    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high]; // Choose last element as pivot
        int i = low - 1;       // Place for swapping
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        swap(arr, i + 1, high);
        return i + 1;
    }

    // ===================== SEARCHING ALGORITHMS =====================

    // Linear Search: Scan every element
    // Time: O(n), Space: O(1)
    public static int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) return i;
        }
        return -1;
    }

    // Binary Search: Requires sorted array
    // Time: O(log n), Space: O(1)
    public static int binarySearch(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) left = mid + 1; else right = mid - 1;
        }
        return -1;
    }

    // ===================== UTILITY METHODS =====================

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    private static int[] randomArray(int size, int bound) {
        Random rand = new Random(42);
        int[] arr = new int[size];
        for (int i = 0; i < size; i++) {
            arr[i] = rand.nextInt(bound);
        }
        return arr;
    }

    private static void printArray(String label, int[] arr) {
        System.out.println(label + Arrays.toString(arr));
    }

    // Measure runtime for a sorting algorithm
    private static long timeSort(Runnable sortFunc) {
        long start = System.nanoTime();
        sortFunc.run();
        return System.nanoTime() - start;
    }

    // ===================== DEMONSTRATION =====================

    public static void main(String[] args) {
        System.out.println("\n" + "=".repeat(80));
        System.out.println("SORTING AND SEARCHING DEMONSTRATION");
        System.out.println("=".repeat(80) + "\n");

        int[] base = randomArray(20, 100);
        printArray("Original: ", base);

        // Bubble Sort
        int[] a1 = Arrays.copyOf(base, base.length);
        long t1 = timeSort(() -> bubbleSort(a1));
        printArray("Bubble  : ", a1);
        System.out.println("Bubble Sort time (ns): " + t1);

        // Selection Sort
        int[] a2 = Arrays.copyOf(base, base.length);
        long t2 = timeSort(() -> selectionSort(a2));
        printArray("Select  : ", a2);
        System.out.println("Selection Sort time (ns): " + t2);

        // Insertion Sort
        int[] a3 = Arrays.copyOf(base, base.length);
        long t3 = timeSort(() -> insertionSort(a3));
        printArray("Insert  : ", a3);
        System.out.println("Insertion Sort time (ns): " + t3);

        // Merge Sort
        int[] a4 = Arrays.copyOf(base, base.length);
        long t4 = timeSort(() -> mergeSort(a4));
        printArray("Merge   : ", a4);
        System.out.println("Merge Sort time (ns): " + t4);

        // Quick Sort
        int[] a5 = Arrays.copyOf(base, base.length);
        long t5 = timeSort(() -> quickSort(a5));
        printArray("Quick   : ", a5);
        System.out.println("Quick Sort time (ns): " + t5);

        // Searching demo (on sorted array)
        int[] sorted = Arrays.copyOf(a5, a5.length);
        Arrays.sort(sorted);
        int target = sorted[sorted.length / 2];
        System.out.println("\nTarget value for search: " + target);
        System.out.println("Linear Search index: " + linearSearch(sorted, target));
        System.out.println("Binary Search index: " + binarySearch(sorted, target));

        System.out.println("\n" + "=".repeat(80));
        System.out.println("DEMONSTRATION COMPLETED");
        System.out.println("=".repeat(80));
    }
}
