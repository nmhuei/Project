// N = 10000
// prime[0..N] = array

// procedure sieve()

//     for i = 2 → N:
//         prime[i] = 1


//     for i = 4 → N step 2:
//         prime[i] = 0

//     for i = 3 → N step 2:
//         if prime[i] == 1:
//             for j = 3*i → N step 2*i:
//                 prime[j] = 0
// end procedure


// main:
//     input n
//     sieve()

//     d = 0


//     for i = 2 → n-1:
//         if n mod i == 0 AND prime[i] == 1:
            
//             if n mod (i*i) == 0:
//                 print "False"
//                 END PROGRAM

//             d = d + 1

//     if d == 3:
//         print "True"
//     else:
//         print "False"


#include <stdio.h>

int N = 10000;
int prime[10001];

void seive(){
  for (int i = 2; i < N; i++){prime[i] = 1;}
  
  for (int i = 4; i < N; i += 2){prime[i] = 0;}
  for (int i = 3; i < N; i += 2){
    if (prime[i] == 1){
      for (int j = 3*i; j < N; j += 2*i){
        prime[j] = 0;
      }
    }
  }

  for (int i = 0; i < 100; i++){if (prime[i]){printf("%d ", i);}}
}

int main(){
  int n;
  scanf("%d", &n);
  seive();

  int d = 0;
  for (int i = 2; i < n; i++){
    if ((n % i == 0) && (prime[i] == 1)){
      if (n % (i*i) == 0){
        printf("False");
      }
      d += 1;
    }
  }

  if (d == 3){printf("True");} else {printf("False");}
}

// Complexity O(N) + O(N loglogN)
// O(NloglogN) for seive()
