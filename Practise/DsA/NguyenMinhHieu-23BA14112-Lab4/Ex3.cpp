#include<stdio.h>

double countPi(int n){
  if (n == 0) return 4.0 - 4.0/3.0;
  return countPi(n - 1) + 4.0/(4.0 * n + 1) - 4.0/(4.0 * n + 3);
}

int main(){
  int n = 100;
  printf("Enter N: ");
  scanf("%d", &n);
  
  printf("When n = 10, pi = %.11f\n", countPi(10));
  printf("When n = 100, pi = %.11f\n", countPi(100));
  printf("When n = 1000, pi = %.11f\n", countPi(1000));
  
  printf("When n = %d, pi = %.11f\n", n, countPi(n));
}

// The complexity time is O(N)
// The complexity space is O(N)
