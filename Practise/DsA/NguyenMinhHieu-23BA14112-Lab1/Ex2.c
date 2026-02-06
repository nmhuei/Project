#include <stdio.h>

void findMax(int *max, int a){
  if (a > *max) {
    *max = a;
  }
}

int main(){
  int max = 0;
  
  //Test
  int a = 123;
  int b = 231983;
  
  findMax(&max, a);
  findMax(&max, b);
  
  printf("%d", max);
}
