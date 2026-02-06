#include <iostream>

// d is the number of digits of n
// O(d)
int length(int n){
    int len = 0;
    
    while (n != 0) {
        len++;
        n /= 10;
    }

    return len;
}

// O(d)
int pow(int a, int b){
    int res = 1;

    for (int i = 0; i < b; i++){
        res *= a;
    }

    return res;
}

//O(log(n))
int countingRecursive(int n){
    int k = length(n);
    if (k == 1) return n;

    int _pow = pow(10, k / 2);
    int a = n / _pow;
    int b = n % _pow;
    if (k / 2 * 2 != k){
        b *= 10;
    }

    return countingRecursive(a + b);
}

int countingLoop(int n){
    int k = length(n);
    int _pow, a, b;

    while (k != 1){
        int _pow = pow(10, k / 2);
        int a = n / _pow;
        int b = n % _pow;
        if (k / 2 * 2 != k){
            b *= 10;
        }

        n = a + b;
        k = length(n);
    }

    return n;
}

int main(){
    // Test with n = 10924
    int n = 47360;
    std::cout << "Test with n = " << n << std::endl;

    // Result with using recursive
    std::cout << "Result with using recursive: " << countingRecursive(n) << std::endl; 
    // Result with using loop
    std::cout << "Result with using loop: " << countingLoop(n) << std::endl;
}