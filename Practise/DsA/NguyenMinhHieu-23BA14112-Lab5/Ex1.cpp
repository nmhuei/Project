#include <iostream>
using namespace std;

int find_max_pos(int *l, int size){
    int max = l[0];
    int pos = 0;

    for (int i = 1; i < size; i++){
        if (l[i] > max){
            max = l[i];
            pos = i;
        }
    }

    return pos;
}

void flip(int *l, int a, int b){
    for (int i = 0; i < (b - a + 1) / 2; i++){
        int temp = l[a + i];
        l[a + i] = l[b - i];
        l[b - i] = temp;
    }

    return;
}

int check_sorted(int *l, int size){
    for (int i = 1; i < size; i++){
        if (l[i] < l[i - 1]) 
    
        return 0;
    }

    return 1;
}

int main(){
    int n;
    cin >> n;

    int *a = new int[n]; 
    for (int i = 0; i < n; i++) cin >> a[i];

    int current_size = n;
    while (current_size > 1){
        int max_pos = find_max_pos(a, current_size);

        if (max_pos != current_size - 1){
            flip(a, 0, max_pos);        
            flip(a, 0, current_size-1); 
        }
        current_size--;
    }

    for (int i = 0; i < n; i++){
        cout << a[i] << " ";
    }

    delete[] a;
}
