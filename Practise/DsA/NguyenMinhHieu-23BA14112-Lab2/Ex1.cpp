#include<iostream>
#include<cstring>
using namespace std;

typedef struct {
  int data[100];
  int size;
} List;

List *init(){
  List *l = (List *)malloc(sizeof(List));
  l->size = 1;
  l->data[0] = 1;
  return l;
}

void changeSign(List *l){
  l->data[0] = -(l->data[0]);
}

int length(List *l){
  return l->size - 1;
}

int isEmpty(List *l){
  return (l->size == 0) ? 1 : 0;
}

void remove(List *l, int pos){
 if (isEmpty(l)){
  cout << "Empty set\n";
  return;
 }
 
 if (pos < 1 || pos > l->size){
  cout << "Invalid position\n";
  return;
 }
 
 for (int i = pos; i < l->size; i++){
  l->data[i] = l->data[i+1];
 }
 
 l->size--;
}

void insert(List *l, int _val, int pos){
  if (l->size == 100){
  cout << "Fully set\n";
  return;
 }
 
 if (pos < 1 || pos > l->size){
  cout << "Invalid position\n";
  return;
 }
 
 for (int i = l->size + 1; i > pos; i--){
  l->data[i] = l->data[i-1];
 }
 
 l->data[pos] = _val;
 l->size++;
}

void display(List *l){
  if (l->data[0] == -1){cout << "-";}
  for (int i = 1; i <= length(l); i++){
    cout << l->data[i];
  }
  cout << endl;
}

int cal_sum(List *l){
  int length = l->size;
  int sum = 0;
  for (int i = 1; i <= length; i++){
    sum += l->data[i];
  }
  
  return sum;
}

int main(){
  List *l = init();
  
  // Enter input (number = 12345678)
  char number[57];
  fgets(number, sizeof(number), stdin);
  
  int k = 0;
  if (number[0] == '-'){changeSign(l);k=1;}
  
  for (int i = k; i < strlen(number) - 1; i++){
    insert(l, (int)number[i] - 48, i + 1 - k);
  }
  
  cout << "The input number is ";
  display(l);
  
  cout << "Remove a digit in position 5: ";
  remove(l, 5);
  display(l);
  
  cout << "Insert number 5 in position 6: ";
  insert(l, 5, 6);
  display(l);
  
  cout << "Sum of all digits of number after change: ";
  cout << cal_sum(l) << endl;
}

