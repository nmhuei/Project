#include <iostream>

/*
========================
BUBBLE SORT
Time:
- Best:    O(n^2) (do KHÔNG có cờ dừng sớm)
- Average: O(n^2)
- Worst:   O(n^2)
Space: O(1)
========================
*/
void bubbleSort(int a[], int n) {
    for (int i = 0; i < n - 1; i++) {          // chạy n lần
        for (int j = 0; j < n - i - 1; j++) {  // mỗi lần ~ n-i
            if (a[j] > a[j + 1]) {
                int tmp = a[j];
                a[j] = a[j + 1];
                a[j + 1] = tmp;
            }
        }
    }
}


/*
========================
SELECTION SORT
Time:
- Best / Average / Worst: O(n^2)
Space: O(1)
========================
*/
void selectionSort(int a[], int n) {
    for (int i = 0; i < n - 1; i++) {       // n vòng
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {   // duyệt n-i phần tử
            if (a[j] < a[minIdx])
                minIdx = j;
        }
        int tmp = a[i];
        a[i] = a[minIdx];
        a[minIdx] = tmp;
    }
}


/*
========================
INSERTION SORT
Time:
- Best:    O(n)   (mảng đã sắp xếp)
- Average: O(n^2)
- Worst:   O(n^2) (mảng ngược)
Space: O(1)
========================
*/
void insertionSort(int a[], int n) {
    for (int i = 1; i < n; i++) {      // n-1 lần
        int key = a[i];
        int j = i - 1;

        while (j >= 0 && a[j] > key) { // dịch phần tử
            a[j + 1] = a[j];
            j--;
        }
        a[j + 1] = key;
    }
}


/*
========================
MERGE SORT
Time:
- Best / Average / Worst: O(n log n)
Space: O(n) (mảng phụ)
========================
*/
void merge(int a[], int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;

    int L[n1], R[n2];   // tốn bộ nhớ phụ O(n)

    for (int i = 0; i < n1; i++)
        L[i] = a[l + i];
    for (int j = 0; j < n2; j++)
        R[j] = a[m + 1 + j];

    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {  // trộn O(n)
        if (L[i] <= R[j])
            a[k++] = L[i++];
        else
            a[k++] = R[j++];
    }

    while (i < n1) a[k++] = L[i++];
    while (j < n2) a[k++] = R[j++];
}

void mergeSort(int a[], int l, int r) {
    if (l < r) {
        int m = (l + r) / 2;
        mergeSort(a, l, m);       // chia đôi
        mergeSort(a, m + 1, r);   // chia đôi
        merge(a, l, m, r);        // trộn O(n)
    }
}


/*
========================
QUICK SORT (pivot = a[high])
Time:
- Best / Average: O(n log n)
- Worst: O(n^2)
Space:
- Average: O(log n)
- Worst: O(n)
========================
*/
int partition(int a[], int low, int high) {
    int pivot = a[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {  // O(n)
        if (a[j] < pivot) {
            i++;
            int tmp = a[i];
            a[i] = a[j];
            a[j] = tmp;
        }
    }

    int tmp = a[i + 1];
    a[i + 1] = a[high];
    a[high] = tmp;

    return i + 1;
}

void quickSort(int a[], int low, int high) {
    if (low < high) {
        int pi = partition(a, low, high);
        quickSort(a, low, pi - 1);
        quickSort(a, pi + 1, high);
    }
}


/*
========================
HEAP SORT
Time:
- Best / Average / Worst: O(n log n)
Space: O(1)
========================
*/
void heapify(int a[], int n, int i) {
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;

    if (l < n && a[l] > a[largest])
        largest = l;
    if (r < n && a[r] > a[largest])
        largest = r;

    if (largest != i) {
        int tmp = a[i];
        a[i] = a[largest];
        a[largest] = tmp;
        heapify(a, n, largest); // O(log n)
    }
}

void heapSort(int a[], int n) {
    for (int i = n / 2 - 1; i >= 0; i--) // build heap O(n)
        heapify(a, n, i);

    for (int i = n - 1; i > 0; i--) {    // n lần * log n
        int tmp = a[0];
        a[0] = a[i];
        a[i] = tmp;
        heapify(a, i, 0);
    }
}
