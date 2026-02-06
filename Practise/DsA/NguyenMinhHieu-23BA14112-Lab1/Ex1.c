// We have a number n 
// Firstly, we find number of digits that number own (divide n by 10 until n = 0)
// n = first_digit * 10 ^ (num_digit - 1) + b + last_digit
// n_re = last_digit * 10 ^ (num_digit - 1) + first_digit


#include <stdio.h>

int count(int n){
  int d = 0;
  while (n > 0){
    d += 1;
    n /= 10;
  }
  
  return d;
}

int reverse(int n){
  int num_digit = count(n);
  
  int fact = 1;
  for (int i = 0; i < num_digit - 1; i++){
    fact *= 10;
  }
  
  return (n % 10) * fact + (n % fact - n % 10) + n / fact;
  
}

int main(){
  int n;
  scanf("%d", &n);
  
  printf("%d", reverse(n));
  
}
