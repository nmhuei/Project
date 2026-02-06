#include <iostream>
using namespace std;

typedef struct {
  string url;
  string title;
} Web;

typedef struct {
  int size;
  Web webs[100];
} Stack;


Stack *init(){
  Stack *st = new Stack;
  st->size = 0;
  
  return st;
}

int isEmpty(Stack *st){
  return st->size == 0;
}

int length(Stack *st){
  return st->size;
}

void push(Stack *st, Web w){
  if (st->size == 100) return;
  
  st->webs[st->size] = w;  
  st->size++;
}

Web *pop(Stack *st){
  if (isEmpty(st)) return nullptr;
  
  st->size--;
  return &st->webs[st->size];
}

void returnWeb(Stack* fs, Stack* bs) {
    Web* w = pop(bs);
    if (w != nullptr)
        push(fs, *w);
}

void nextWeb(Stack* fs, Stack* bs) {
    Web* w = pop(fs);
    if (w != nullptr)
        push(bs, *w);
}

void printCurrentWeb(Stack *st){
  cout << "url : " << st->webs[st->size - 1].url << ", "
       << "title : " << st->webs[st->size - 1].title << endl;
}

void display(Stack *st){
  for (int i  = 0; i < length(st); i++){
    cout << "Web " << i + 1 << ", " 
         << "url : " << st->webs[i].url << ", "
         << "title : " << st->webs[i].title << endl;
  }
}


int main() {
    // Built current history of web browser
    Stack* back = init();
    Stack* forward = init();

    Web w1 = {"google.com", "Google"};
    Web w2 = {"youtube.com", "YouTube"};

    push(back, w1);
    push(back, w2);
    push(back, w1);
    push(back, w2);
    push(back, w1);
    push(back, w2);
    push(back, w1);
    push(back, w2);

    cout << "History of website: \n";    
    display(back);
    cout << endl;
    
    cout << "Current website : ";
    printCurrentWeb(back);
    cout << endl;
    
    // Return to the previous website
    returnWeb(forward, back);
    cout << "Current website after back :";
    printCurrentWeb(back);
    cout << endl;
    
    // Retrive to the previous website
    nextWeb(forward, back);
    cout << "Current website after retrive :";
    printCurrentWeb(back);
    
    
    return 0;
}
