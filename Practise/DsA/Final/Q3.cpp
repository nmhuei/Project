#include <iostream>
using namespace std;

void swap(int *a, int *b){
    int temp = *a;
    *a = *b;
    *b = temp;

    return;
}

void sortingAlg(int *a, int n){
    int left = 0, right = n -1;

    while (left <= right){
        int minIdx = left, maxIdx = right;

        for (int i = left; i < right; i++){
            if (a[minIdx] > a[i]) minIdx = i;
            if (a[maxIdx] < a[i]) maxIdx = i;
        }

        swap(&a[minIdx], &a[left]);

        if (maxIdx == left){
            maxIdx = minIdx;
        }

        swap(&a[maxIdx], &a[right]);

        left++;
        right--;
    }
}
// O(n*n + (n-2) * (n - 2) + ... ) = O(n^2)

int main(){
    int a[] = {18,12,534,7,432,5,6,5463,7,23,54};
    int n = 11;

    sortingAlg(a, n);

    for (int i = 0; i < n; i++){
        cout << a[i] << " ";
    }
}