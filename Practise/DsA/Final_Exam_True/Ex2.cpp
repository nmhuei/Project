#include <iostream>

void insert(int arr[], int j, int key){
    if (j < 0 || arr[j] <= key){
        arr[j+ 1] = key;
        return;
    }

    arr[j + 1] = arr[j];
    insert(arr, j - 1, key);
}

// We only change from using loop to recursive so this algorithms not faster than Insertion sort
void insertionSortRecursive(int arr[], int n, int i = 1){
    if (i == n) return;

    int key = arr[i];
    int j = i - 1;
    insert(arr, j , key);
    insertionSortRecursive(arr, n, i + 1);
}

int main(){
    int arr[] = {3,43,324,2,15,6,465,3};
    int n = 8;

    insertionSortRecursive(arr, n);

    for (int i = 0; i < n; i++){
        std::cout << arr[i] << " ";
    }
}