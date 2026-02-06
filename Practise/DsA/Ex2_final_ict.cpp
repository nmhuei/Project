#include <iostream>
using namespace std;

typedef struct {
    int data;       // actual value
    int priority;   // smaller number => higher priority (0 is highest)
} Element;

typedef struct {
    int size;
    Element data[100];
} Queue;

// ---------- helper checks ----------
bool isEmpty(const Queue* q) {
    return q->size == 0;
}
// O(1)
bool isFull(const Queue* q) {
    return q->size == 100;
}
// O(1)

// ---------- initialize queue ----------
// O(1)
void init(Queue* q) {
    q->size = 0;
}

// ---------- display queue ----------
// Time: O(n), Space: O(1)
void display(const Queue* q) {
    if (isEmpty(q)) {
        cout << "[Queue is empty]" << endl;
        return;
    }
    cout << "Queue (front -> rear):" << endl;
    for (int i = 0; i < q->size; ++i) {
        cout << "  Data: " << q->data[i].data
             << " | Priority: " << q->data[i].priority << endl;
    }
}

// ---------- enqueue (insert by priority) ----------
// Insert so that elements with smaller priority value are closer to front.
// If equal priorities, new element is placed after existing ones (stable).
// Time: O(n) in worst case (shifts), Space: O(1)
bool enqueue(Queue* q, Element e) {
    if (isFull(q)) {
        cout << "Cannot enqueue: queue is full." << endl;
        return false;
    }

    // find insert position: first index i where current.priority > e.priority
    // (we keep equal priorities after existing elements → stable)
    int pos = q->size; // default: append at end
    for (int i = 0; i < q->size; ++i) {
        if (q->data[i].priority > e.priority) {
            pos = i;
            break;
        }
    }

    // shift right to make room
    for (int i = q->size - 1; i >= pos; --i) {
        q->data[i + 1] = q->data[i];
    }

    q->data[pos] = e;
    q->size++;
    return true;
}

// ---------- dequeue (remove front element) ----------
// Removes and returns the front element (highest priority).
// Time: O(n) due to shift, Space: O(1)
// If queue empty, returns Element with priority = -1 to indicate error.
Element dequeue(Queue* q) {
    Element err; err.data = -1; err.priority = -1;
    if (isEmpty(q)) {
        cout << "Cannot dequeue: queue is empty." << endl;
        return err;
    }

    Element front = q->data[0];
    // shift left all elements
    for (int i = 1; i < q->size; ++i) {
        q->data[i - 1] = q->data[i];
    }
    q->size--;
    return front;
}

// peek front (O(1))
Element peek(const Queue* q) {
    Element err; err.data = -1; err.priority = -1;
    if (isEmpty(q)) return err;
    return q->data[0];
}

// ---------- Demo main ----------
int main(){
    Queue q;
    init(&q);

    // initialize with at least 6 elements (data, priority)
    // Note: smaller priority number => higher priority (front)
    enqueue(&q, Element{30, 1});
    enqueue(&q, Element{25, 3});
    enqueue(&q, Element{15, 2});
    enqueue(&q, Element{40, 4});
    enqueue(&q, Element{5, 0});
    enqueue(&q, Element{20, 2});

    cout << "Initial queue after init (6 elements):" << endl;
    display(&q);
    cout << endl;

    // Example from problem: enqueue (10, 0)
    cout << "Enqueue (10, 0):" << endl;
    enqueue(&q, Element{10, 0});
    display(&q);
    cout << endl;

    // Dequeue once (should remove front)
    cout << "Dequeue (remove front):" << endl;
    Element removed = dequeue(&q);
    if (removed.priority != -1)
        cout << "  Removed: Data=" << removed.data << " | Priority=" << removed.priority << endl;
    cout << "Queue now:" << endl;
    display(&q);
    cout << endl;

    // Additional ops
    cout << "Enqueue (12,1) and (7,0):" << endl;
    enqueue(&q, Element{12, 1});
    enqueue(&q, Element{7, 0});
    display(&q);
    cout << endl;

    cout << "Pop all elements (dequeue until empty):" << endl;
    while (!isEmpty(&q)) {
        Element e = dequeue(&q);
        cout << e.data << "(" << e.priority << ") ";
    }
    cout << endl;

    return 0;
}
