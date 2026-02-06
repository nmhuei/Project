#include<iostream>
using namespace std;

int countDistinctPrime(int n, int p = 2){
  if (n == 1) return 0;
  if (p * p > n) return 1;
  
  if (n % (p * p) == 0) return -1000;
  
  if (n % p == 0){
    while (n % p == 0){
      n /= p;
    }
    
    return 1 + countDistinctPrime(n, p + 1);
  }
  
  return countDistinctPrime(n, p + 1);
}

bool isSphenic(int n){
  return countDistinctPrime(n) == 3;
}

int main(){
  int n;
  cout << "Enter n: ";
  cin >> n;
   
  cout << "Sphenic number from 1 to " << n << " : ";
  bool found = false;
  for (int i = 1; i <= n; i++){
    if (isSphenic(i)){
      cout << i << " ";
      found = true;
    }
  }
  
  if (found == false){
    cout << "None.";
  }
}

// To check isSphenic, recursion function need the complexity O(sqrt(N))
// So the complexity time of this program is O(n * sqrt(n))
// The complexity space is O(sqrt(N))
