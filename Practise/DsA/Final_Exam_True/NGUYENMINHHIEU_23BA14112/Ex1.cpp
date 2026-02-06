#include <iostream>
#define MAX_VALUE 1001
#define MAX 100

// I use to 2 integer array to store data: 1 for input array and one for frequence array
struct List {
    int size;
    int input_array[MAX];
    int frequence[MAX_VALUE];
};

/*
I just using one loop to put arr to input_array and count it's frequence so the complexity time is O(n) 
and don't use recursion so the space conplexity is O(1)
*/ 
List *init(int arr[], int n){
    List *l = new List;
    l-> size = n;
    for (int i = 0; i < MAX_VALUE; i++) l->frequence[i] = 0;

    for (int i = 0; i < n; i++){        
        l->input_array[i] = arr[i];
        l->frequence[arr[i]] += 1;
    }

    return l;
}

void display(List *l){
    for (int i = 0; i < MAX_VALUE; i++){
        if (l->frequence[i] != 0){
            for (int j = 0; j < l->frequence[i]; j++){
                std::cout << i << " " ;
            }
        }
    }

    std::cout << std::endl;
}


int main(){
    // Initial array
    int input_array[] = {1,3,4,5,4,32,123,4,123,1000,999};
    int n = 11;

    // Init data structure and sorting 
    List *l = init(input_array, n);

    // display array after sorted
    display(l);
}