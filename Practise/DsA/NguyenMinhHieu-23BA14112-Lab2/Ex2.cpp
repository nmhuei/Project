#include <iostream>
#include <cstring>
#include <cstdlib>
using namespace std;

typedef struct Car {
    int passengers;
    int capacity;
    char id[10];
    Car *cNext;
} Car;

typedef struct Train {
    int size;
    Car *cHead;
} Train;

Car *initCar(int _passengers, const char _id[]) {
    Car *car = (Car *)malloc(sizeof(Car));
    car->passengers = _passengers;
    car->capacity = 20;
    strcpy(car->id, _id);
    car->cNext = NULL;
    
    return car;
}

Train *initTrain() {
    Train *tr = (Train *)malloc(sizeof(Train));
    tr->size = 0;
    tr->cHead = NULL;
    
    return tr;
}

int isEmptyTrain(Train *tr) {
    return (tr->size == 0);
}

int isEmptyCar(Car *car) {
    return (car->passengers == 0);
}

void insertFirst(Train *tr, Car *car) {
    car->cNext = tr->cHead;
    tr->cHead = car;
    tr->size++;
}

void insertAfter(Train *tr, Car *pcar, Car *car) {
    car->cNext = pcar->cNext;
    pcar->cNext = car;
    tr->size++;
}

void removeAt(Train *tr, int pos) {
    if (pos < 1 || pos >= tr->size) {
        cout << "Invalid position\n";
        return;
    }

    Car *cur = tr->cHead;
    Car *p = NULL;
    
    for (int i = 0; i < pos; i++) {
        p = cur;
        cur = cur->cNext;
    }

    p->cNext = cur->cNext;
    free(cur);
    tr->size--;
}


void removeAllEmptyCar(Train *tr) {
    while (tr->cHead != NULL && tr->cHead->passengers == 0) {
        Car *del = tr->cHead;
        tr->cHead = tr->cHead->cNext;
        free(del);
        tr->size--;
    }

    if (tr->cHead == NULL) return;

    Car *p = tr->cHead;
    Car *cur = p->cNext;

    while (cur != NULL) {
        if (cur->passengers == 0) {
            p->cNext = cur->cNext;
            free(cur);
            tr->size--;
            cur = p->cNext;
        } else {
            p = cur;
            cur = cur->cNext;
        }
    }
}

void displayTrain(Train *tr) {
    Car *cur = tr->cHead;
    while (cur != NULL) {
        cout << "Car ID: " << cur->id
             << ", Passengers: " << cur->passengers
             << ", Capacity: " << cur->capacity << endl;
        cur = cur->cNext;
    }
    cout << "Train size = " << tr->size << endl;
}


int main() {
    Train *tr = initTrain();

    insertFirst(tr, initCar(10, "huei"));
    insertFirst(tr, initCar(0, "hai"));  
    insertFirst(tr, initCar(5, "phan"));
    insertFirst(tr, initCar(0, "DBV"));  

    cout << "Before remove:\n";
    displayTrain(tr);

    removeAllEmptyCar(tr);

    cout << "\nAfter remove:\n";
    displayTrain(tr);

    return 0;
}
