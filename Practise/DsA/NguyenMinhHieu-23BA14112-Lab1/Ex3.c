#include <stdio.h>

typedef struct {
  double real;
  double complex;
} complex_number;

complex_number add2num(complex_number a, complex_number b){
  complex_number res;
  
  res.real = a.real + b.real;
  res.complex = a.complex + b.complex;
  
  return res;
}

complex_number mul2num(complex_number a, complex_number b){
  complex_number res;
  
  res.real = a.real * b.real - a.complex * b.complex;
  res.complex = a.real * b.complex + a.complex * b.real;
  
  return res;
}

int main(){
  //Test
  
  complex_number n1 = {1, 3};
  complex_number n2 = {2, 4};
  complex_number resadd = add2num(n1, n2);
  
  printf("%f+%fi", resadd.real, resadd.complex);
  
}
