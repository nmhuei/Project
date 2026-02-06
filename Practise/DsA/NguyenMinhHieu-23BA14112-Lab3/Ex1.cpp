#include<iostream>
using namespace std;

typedef struct {
  char name;
  int quantity;
  double price;
} Item;

Item *initItem(char _name, int N, int _price){
  Item *i = new Item;
  i->name = _name;
  i->quantity = N;
  i->price = _price;
  
  return i;
}

int isEmptyItem(Item *i){
  return (i->quantity == 0);
}

int canBuy(Item *i, int k){
  return (i->quantity >= k);
}

typedef struct {
  int size;
  int capacity;
  Item *list;
} Shop;

Shop *initShop(int N){
  Shop *s = new Shop;
  s->capacity = N;
  s->size = 0;
  s->list = new Item[N];
  
  return s;
}

void addNewItem(Shop *s, Item *i){
  if (s->size == s->capacity){
    cout << "Shop Full!!!";
    return;
  }
  
  Item &desk = s->list[s->size];
  desk.name = i->name;
  desk.price = i->price;
  desk.quantity = i->quantity;
  s->size++;
  
  return;
}

void removeItem(Shop *s, int pos){
  if (pos < 0 || pos > s->size){
    cout << "Invalid position!";
    return;
  }
  
  for (int i = pos; i < s->size - 1; i++){
    s->list[i] = s->list[i+1];
  }
  
  s->size--;
}

int findItem(Shop *s, char _name){
  for (int i = 0; i < s->size; i++){
    if (s->list[i].name == _name){return i;}
  }
  
  return -1;
}

//Buy k items from Item <nameItem>
typedef struct {
  int k;
  char nameItem;
} Person;

Person *initPerson(int _k, char _name){
  Person *p = new Person;
  p->k = _k;
  p->nameItem = _name;
  
  return p;
}

typedef struct {
  Person *customers;
  int capacity;
  int front, back;
} Queue;

Queue *init(int N){
  Queue *list = new Queue;
  list->capacity = N;
  list->front = 0;
  list->back = 0;
  list->customers = new Person[N];
  
  return list;
}

int isEmptyQueue(Queue *list){
  return (list->back - list->front == 0);
}

int sizeQueue(Queue *list){
  return (list->back - list->front) % list->capacity; 
}

void enqueue(Queue *list, Person *p){
  if (sizeQueue(list) == list->capacity){
    cout << "Queue full!\n";
    return;
  }
  
  Person &cus = list->customers[list->back];
  cus.k = p->k;
  cus.nameItem = p->nameItem;
  
  list->back++;
}

Person *dequeue(Queue *list){
  if (isEmptyQueue(list)){
    cout << "No customers, here!";
    return NULL;
  }
  Person *p = &list->customers[list->front];
  list->front++;
  
  return p;
}

int main() {
    Shop *s = initShop(5);


    Item *item1 = initItem('A', 10, 50000);
    Item *item2 = initItem('B', 5, 120000);
    Item *item3 = initItem('C', 7, 75000);


    addNewItem(s, item1);
    addNewItem(s, item2);
    addNewItem(s, item3);

    cout << "Shop list :\n";
    for (int i = 0; i < s->size; i++) {
        cout << "Item " << i+1 << ": "
             << s->list[i].name << ", "
             << "Quantity: " << s->list[i].quantity << ", "
             << "Price: " << s->list[i].price << endl;
    }
    cout << endl;


    Queue *list = init(10);


    Person *p1 = initPerson(3, 'A');
    Person *p2 = initPerson(2, 'B');
    Person *p3 = initPerson(5, 'C');
    Person *p4 = initPerson(8, 'A'); // Sẽ không đủ hàng


    enqueue(list, p1);
    enqueue(list, p2);
    enqueue(list, p3);
    enqueue(list, p4);

    cout << "Processing customers : \n";

    while (!isEmptyQueue(list)){
      Person *p = dequeue(list);
      if (p == NULL) break;
      
      int pos = findItem(s, p->nameItem);
      if (pos >= 0){
        Item *i = &s->list[pos];
        if (canBuy(i, p->k)){
          cout << "Customer buy " << p->k
               << " items from Item " << p->nameItem
               << " , You may pay " << i->price * p->k << " euro for them!" << endl;
          i->quantity -= p->k;
        } else {
          cout << "Customer buy " << p->k
               << " items from Item " << p->nameItem
               << " , Run out of Item!" << endl;
        }
      } else {
        cout << "Customer buy " << p->k
             << " items from Item " << p->nameItem
             << " , Item not found!" << endl;
      }
    }
    
    
    cout << endl;


    cout << "=== SHOP LIST AFTER SALES ===\n";
    for (int i = 0; i < s->size; i++) {
        cout << "Item " << i+1 << ": "
             << s->list[i].name << ", "
             << "Quantity: " << s->list[i].quantity << ", "
             << "Price: " << s->list[i].price << endl;
    }


    delete[] s->list;
    delete s;
    delete[] list->customers;
    delete list;
    delete item1;
    delete item2;
    delete item3;
    delete p1;
    delete p2;
    delete p3;
    delete p4;

    return 0;
}

