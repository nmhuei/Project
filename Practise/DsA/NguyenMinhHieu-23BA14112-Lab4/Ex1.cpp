// pseudo-code

// n = input()
// while n % 10 <> 0 do
// 	sum = sum + n % 10
// 	n = n / 10
	
// print(sum)

#include <iostream>

int sumDigitRec(int n){
  if (n < 10) return n;
  return n % 10 + sumDigitRec(n / 10);
}

int sumDigitNRec(int n){
    int sum = 0;
	while (n % 10 != 0) {
		sum += n % 10;
		n /= 10;
	}  

    return sum;
}

int main(){
        int n;
	std::cout << "Enter a number, N = " ;
	std::cin >> n;
	
	std::cout << "The digit sum of " << n << " (Recursion) is " << sumDigitRec(n) << std::endl;
	std::cout << "The digit sum of " << n << " (Not Recursion) is " << sumDigitNRec(n) << std::endl;
}


// The conplexity time is O(K) with K is the number of digits of N, because while loop run for each digit of N and the complexity space is O(1)
// The conplexity time is O(K) with K is the number of digits of N, because recursion function run for each digit of N and the complexity space is O(K)


