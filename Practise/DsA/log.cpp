#include <iostream>
using namespace std;

const int MAX = 100;

// ============ ARRAY LIST ============
struct ArrayList {
    int data[MAX];
    int size;
};

// Time: O(1), Space: O(1)
ArrayList* initArrayList() {
    ArrayList* L = new ArrayList;
    L->size = 0;
    return L;
}

// Time: O(1), Space: O(1)
bool isEmpty(ArrayList* L) {
    return L->size == 0;
}

// Time: O(1), Space: O(1)
bool isFull(ArrayList* L) {
    return L->size == MAX;
}

// Time: O(1), Space: O(1)
int getSize(ArrayList* L) {
    return L->size;
}

// Time: O(n), Space: O(1) - n là số phần tử cần dịch chuyển
bool insertAt(ArrayList* L, int pos, int x) {
    if (isFull(L) || pos < 0 || pos > L->size) 
        return false;
    for (int i = L->size; i > pos; i--)
        L->data[i] = L->data[i - 1];
    L->data[pos] = x;
    L->size++;
    return true;
}

// Time: O(1), Space: O(1) - thêm vào cuối
bool append(ArrayList* L, int x) {
    return insertAt(L, L->size, x);
}

// Time: O(n), Space: O(1) - n là số phần tử cần dịch chuyển
bool removeAt(ArrayList* L, int pos) {
    if (isEmpty(L) || pos < 0 || pos >= L->size) 
        return false;
    for (int i = pos; i < L->size - 1; i++)
        L->data[i] = L->data[i + 1];
    L->size--;
    return true;
}

// Time: O(1), Space: O(1) - truy cập trực tiếp qua index
int get(ArrayList* L, int pos) {
    if (pos < 0 || pos >= L->size)
        return -1; // Error value
    return L->data[pos];
}

// Time: O(n), Space: O(1) - tìm kiếm tuyến tính
int search(ArrayList* L, int x) {
    for (int i = 0; i < L->size; i++)
        if (L->data[i] == x) return i;
    return -1;
}

// Time: O(n), Space: O(1)
void display(ArrayList* L) {
    cout << "[";
    for (int i = 0; i < L->size; i++) {
        cout << L->data[i];
        if (i < L->size - 1) cout << ", ";
    }
    cout << "]" << endl;
}

// Time: O(1), Space: O(1)
void clearArrayList(ArrayList* L) {
    L->size = 0;
}

// Time: O(1), Space: O(1)
void destroyArrayList(ArrayList* L) {
    delete L;
}

// Sorting functions for ArrayList

// BUBBLE SORT - Sắp xếp nổi bọt
// Time: Best O(n), Average O(n²), Worst O(n²)
// Space: O(1)
// Stable: Yes
void bubbleSort(ArrayList* L) {
    for (int i = 0; i < L->size - 1; i++) {
        for (int j = 0; j < L->size - i - 1; j++) {
            if (L->data[j] > L->data[j + 1]) {
                int temp = L->data[j];
                L->data[j] = L->data[j + 1];
                L->data[j + 1] = temp;
            }
        }
    }
}

// SELECTION SORT - Sắp xếp chọn
// Time: Best O(n²), Average O(n²), Worst O(n²)
// Space: O(1)
// Stable: No
void selectionSort(ArrayList* L) {
    for (int i = 0; i < L->size - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < L->size; j++) {
            if (L->data[j] < L->data[minIdx])
                minIdx = j;
        }
        if (minIdx != i) {
            int temp = L->data[i];
            L->data[i] = L->data[minIdx];
            L->data[minIdx] = temp;
        }
    }
}

// INSERTION SORT - Sắp xếp chèn
// Time: Best O(n), Average O(n²), Worst O(n²)
// Space: O(1)
// Stable: Yes
// Tốt cho dữ liệu gần như đã sắp xếp
void insertionSort(ArrayList* L) {
    for (int i = 1; i < L->size; i++) {
        int key = L->data[i];
        int j = i - 1;
        while (j >= 0 && L->data[j] > key) {
            L->data[j + 1] = L->data[j];
            j--;
        }
        L->data[j + 1] = key;
    }
}

// QUICK SORT - Phân hoạch và sắp xếp
// Time: Best O(n log n), Average O(n log n), Worst O(n²)
// Space: O(log n) - do đệ quy
// Stable: No
// Thuật toán nhanh nhất trong thực tế
int partition(ArrayList* L, int low, int high) {
    int pivot = L->data[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        if (L->data[j] < pivot) {
            i++;
            int temp = L->data[i];
            L->data[i] = L->data[j];
            L->data[j] = temp;
        }
    }
    int temp = L->data[i + 1];
    L->data[i + 1] = L->data[high];
    L->data[high] = temp;
    return i + 1;
}

void quickSortHelper(ArrayList* L, int low, int high) {
    if (low < high) {
        int pi = partition(L, low, high);
        quickSortHelper(L, low, pi - 1);
        quickSortHelper(L, pi + 1, high);
    }
}

void quickSort(ArrayList* L) {
    if (L->size > 1)
        quickSortHelper(L, 0, L->size - 1);
}

// MERGE SORT - Chia để trị
// Time: Best O(n log n), Average O(n log n), Worst O(n log n)
// Space: O(n) - cần mảng phụ
// Stable: Yes
// Hiệu suất ổn định nhất
void merge(ArrayList* L, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    int* leftArr = new int[n1];
    int* rightArr = new int[n2];
    
    for (int i = 0; i < n1; i++)
        leftArr[i] = L->data[left + i];
    for (int j = 0; j < n2; j++)
        rightArr[j] = L->data[mid + 1 + j];
    
    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (leftArr[i] <= rightArr[j]) {
            L->data[k] = leftArr[i];
            i++;
        } else {
            L->data[k] = rightArr[j];
            j++;
        }
        k++;
    }
    
    while (i < n1) {
        L->data[k] = leftArr[i];
        i++;
        k++;
    }
    
    while (j < n2) {
        L->data[k] = rightArr[j];
        j++;
        k++;
    }
    
    delete[] leftArr;
    delete[] rightArr;
}

void mergeSortHelper(ArrayList* L, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSortHelper(L, left, mid);
        mergeSortHelper(L, mid + 1, right);
        merge(L, left, mid, right);
    }
}

void mergeSort(ArrayList* L) {
    if (L->size > 1)
        mergeSortHelper(L, 0, L->size - 1);
}

// HEAP SORT - Sắp xếp vun đống
// Time: Best O(n log n), Average O(n log n), Worst O(n log n)
// Space: O(1)
// Stable: No
// Không cần thêm bộ nhớ phụ
void heapify(ArrayList* L, int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    
    if (left < n && L->data[left] > L->data[largest])
        largest = left;
    
    if (right < n && L->data[right] > L->data[largest])
        largest = right;
    
    if (largest != i) {
        int temp = L->data[i];
        L->data[i] = L->data[largest];
        L->data[largest] = temp;
        heapify(L, n, largest);
    }
}

void heapSort(ArrayList* L) {
    for (int i = L->size / 2 - 1; i >= 0; i--)
        heapify(L, L->size, i);
    
    for (int i = L->size - 1; i > 0; i--) {
        int temp = L->data[0];
        L->data[0] = L->data[i];
        L->data[i] = temp;
        heapify(L, i, 0);
    }
}

// ============ LINKED LIST ============
struct Node {
    int data;
    Node* next;
};

struct LinkedList {
    Node* head;
    int size;
};

// Time: O(1), Space: O(1)
Node* createNode(int x) {
    Node* p = new Node;
    p->data = x;
    p->next = NULL;
    return p;
}

// Time: O(1), Space: O(1)
LinkedList* initLinkedList() {
    LinkedList* L = new LinkedList;
    L->head = NULL;
    L->size = 0;
    return L;
}

// Time: O(1), Space: O(1)
bool isEmpty(LinkedList* L) {
    return L->head == NULL;
}

// Time: O(1), Space: O(1)
int getSize(LinkedList* L) {
    return L->size;
}

// Time: O(1), Space: O(1) - thêm vào đầu
void insertHead(LinkedList* L, int x) {
    Node* p = createNode(x);
    p->next = L->head;
    L->head = p;
    L->size++;
}

// Time: O(n), Space: O(1) - duyệt đến cuối
void insertTail(LinkedList* L, int x) {
    Node* p = createNode(x);
    if (!L->head) {
        L->head = p;
    } else {
        Node* cur = L->head;
        while (cur->next) cur = cur->next;
        cur->next = p;
    }
    L->size++;
}

// Time: O(n), Space: O(1) - duyệt đến vị trí pos
bool insertAt(LinkedList* L, int pos, int x) {
    if (pos < 0 || pos > L->size) return false;
    if (pos == 0) {
        insertHead(L, x);
        return true;
    }
    Node* p = createNode(x);
    Node* cur = L->head;
    for (int i = 0; i < pos - 1; i++)
        cur = cur->next;
    p->next = cur->next;
    cur->next = p;
    L->size++;
    return true;
}

// Time: O(1), Space: O(1) - xóa đầu
bool deleteHead(LinkedList* L) {
    if (!L->head) return false;
    Node* temp = L->head;
    L->head = L->head->next;
    delete temp;
    L->size--;
    return true;
}

// Time: O(n), Space: O(1) - duyệt đến node trước cuối
bool deleteTail(LinkedList* L) {
    if (!L->head) return false;
    if (!L->head->next) {
        delete L->head;
        L->head = NULL;
        L->size--;
        return true;
    }
    Node* cur = L->head;
    while (cur->next->next) cur = cur->next;
    delete cur->next;
    cur->next = NULL;
    L->size--;
    return true;
}

// Time: O(n), Space: O(1) - duyệt đến vị trí pos
bool deleteAt(LinkedList* L, int pos) {
    if (pos < 0 || pos >= L->size) return false;
    if (pos == 0) return deleteHead(L);
    Node* cur = L->head;
    for (int i = 0; i < pos - 1; i++)
        cur = cur->next;
    Node* temp = cur->next;
    cur->next = temp->next;
    delete temp;
    L->size--;
    return true;
}

// Time: O(n), Space: O(1) - tìm kiếm tuyến tính
int search(LinkedList* L, int x) {
    Node* cur = L->head;
    int pos = 0;
    while (cur) {
        if (cur->data == x) return pos;
        cur = cur->next;
        pos++;
    }
    return -1;
}

// Time: O(n), Space: O(1)
void display(LinkedList* L) {
    cout << "[";
    Node* cur = L->head;
    while (cur) {
        cout << cur->data;
        if (cur->next) cout << " -> ";
        cur = cur->next;
    }
    cout << "]" << endl;
}

// Time: O(n), Space: O(1)
void clearLinkedList(LinkedList* L) {
    while (L->head) deleteHead(L);
}

// Time: O(n), Space: O(1)
void destroyLinkedList(LinkedList* L) {
    clearLinkedList(L);
    delete L;
}

// Sorting functions for LinkedList

// BUBBLE SORT cho Linked List
// Time: Best O(n), Average O(n²), Worst O(n²)
// Space: O(1)
// Stable: Yes
void bubbleSort(LinkedList* L) {
    if (L->size < 2) return;
    bool swapped;
    do {
        swapped = false;
        Node* cur = L->head;
        while (cur && cur->next) {
            if (cur->data > cur->next->data) {
                int temp = cur->data;
                cur->data = cur->next->data;
                cur->next->data = temp;
                swapped = true;
            }
            cur = cur->next;
        }
    } while (swapped);
}

// SELECTION SORT cho Linked List
// Time: Best O(n²), Average O(n²), Worst O(n²)
// Space: O(1)
// Stable: No
void selectionSort(LinkedList* L) {
    if (L->size < 2) return;
    Node* cur = L->head;
    while (cur) {
        Node* minNode = cur;
        Node* temp = cur->next;
        while (temp) {
            if (temp->data < minNode->data)
                minNode = temp;
            temp = temp->next;
        }
        if (minNode != cur) {
            int tempData = cur->data;
            cur->data = minNode->data;
            minNode->data = tempData;
        }
        cur = cur->next;
    }
}

// INSERTION SORT cho Linked List
// Time: Best O(n), Average O(n²), Worst O(n²)
// Space: O(1)
// Stable: Yes
void insertionSort(LinkedList* L) {
    if (L->size < 2) return;
    Node* sorted = NULL;
    Node* cur = L->head;
    
    while (cur) {
        Node* next = cur->next;
        if (!sorted || sorted->data >= cur->data) {
            cur->next = sorted;
            sorted = cur;
        } else {
            Node* temp = sorted;
            while (temp->next && temp->next->data < cur->data)
                temp = temp->next;
            cur->next = temp->next;
            temp->next = cur;
        }
        cur = next;
    }
    L->head = sorted;
}

// MERGE SORT cho Linked List - TỐT NHẤT cho Linked List!
// Time: Best O(n log n), Average O(n log n), Worst O(n log n)
// Space: O(log n) - do đệ quy
// Stable: Yes
// Phù hợp nhất với cấu trúc Linked List
Node* mergeLists(Node* left, Node* right) {
    if (!left) return right;
    if (!right) return left;
    
    Node* result = NULL;
    if (left->data <= right->data) {
        result = left;
        result->next = mergeLists(left->next, right);
    } else {
        result = right;
        result->next = mergeLists(left, right->next);
    }
    return result;
}

Node* getMid(Node* head) {
    if (!head) return head;
    Node* slow = head;
    Node* fast = head->next;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;
}

Node* mergeSortHelper(Node* head) {
    if (!head || !head->next) return head;
    
    Node* mid = getMid(head);
    Node* left = head;
    Node* right = mid->next;
    mid->next = NULL;
    
    left = mergeSortHelper(left);
    right = mergeSortHelper(right);
    
    return mergeLists(left, right);
}

void mergeSort(LinkedList* L) {
    L->head = mergeSortHelper(L->head);
}

// ============ STACK ============
struct Stack {
    int data[MAX];
    int top;
};

// Time: O(1), Space: O(1)
Stack* initStack() {
    Stack* s = new Stack;
    s->top = -1;
    return s;
}

// Time: O(1), Space: O(1)
bool isEmpty(Stack* s) {
    return s->top == -1;
}

// Time: O(1), Space: O(1)
bool isFull(Stack* s) {
    return s->top == MAX - 1;
}

// Time: O(1), Space: O(1)
int getSize(Stack* s) {
    return s->top + 1;
}

// Time: O(1), Space: O(1)
bool push(Stack* s, int x) {
    if (isFull(s)) return false;
    s->data[++s->top] = x;
    return true;
}

// Time: O(1), Space: O(1)
bool pop(Stack* s, int &x) {
    if (isEmpty(s)) return false;
    x = s->data[s->top--];
    return true;
}

// Time: O(1), Space: O(1)
bool peek(Stack* s, int &x) {
    if (isEmpty(s)) return false;
    x = s->data[s->top];
    return true;
}

// Time: O(n), Space: O(1)
void display(Stack* s) {
    cout << "Stack (top -> bottom): [";
    for (int i = s->top; i >= 0; i--) {
        cout << s->data[i];
        if (i > 0) cout << ", ";
    }
    cout << "]" << endl;
}

// Time: O(1), Space: O(1)
void clearStack(Stack* s) {
    s->top = -1;
}

// Time: O(1), Space: O(1)
void destroyStack(Stack* s) {
    delete s;
}

// ============ QUEUE ============
struct Queue {
    int data[MAX];
    int front, rear, size;
};

// Time: O(1), Space: O(1)
Queue* initQueue() {
    Queue* q = new Queue;
    q->front = 0;
    q->rear = -1;
    q->size = 0;
    return q;
}

// Time: O(1), Space: O(1)
bool isEmpty(Queue* q) {
    return q->size == 0;
}

// Time: O(1), Space: O(1)
bool isFull(Queue* q) {
    return q->size == MAX;
}

// Time: O(1), Space: O(1)
int getSize(Queue* q) {
    return q->size;
}

// Time: O(1), Space: O(1)
bool enqueue(Queue* q, int x) {
    if (isFull(q)) return false;
    q->rear = (q->rear + 1) % MAX;
    q->data[q->rear] = x;
    q->size++;
    return true;
}

// Time: O(1), Space: O(1)
bool dequeue(Queue* q, int &x) {
    if (isEmpty(q)) return false;
    x = q->data[q->front];
    q->front = (q->front + 1) % MAX;
    q->size--;
    return true;
}

// Time: O(1), Space: O(1)
bool peek(Queue* q, int &x) {
    if (isEmpty(q)) return false;
    x = q->data[q->front];
    return true;
}

// Time: O(n), Space: O(1)
void display(Queue* q) {
    cout << "Queue (front -> rear): [";
    for (int i = 0; i < q->size; i++) {
        cout << q->data[(q->front + i) % MAX];
        if (i < q->size - 1) cout << ", ";
    }
    cout << "]" << endl;
}

// Time: O(1), Space: O(1)
void clearQueue(Queue* q) {
    q->front = 0;
    q->rear = -1;
    q->size = 0;
}

// Time: O(1), Space: O(1)
void destroyQueue(Queue* q) {
    delete q;
}

// ============ BINARY TREE ============
struct TreeNode {
    int data;
    TreeNode *left, *right;
};

struct BinaryTree {
    TreeNode* root;
};

// Time: O(1), Space: O(1)
TreeNode* createTreeNode(int x) {
    TreeNode* p = new TreeNode;
    p->data = x;
    p->left = p->right = NULL;
    return p;
}

// Time: O(1), Space: O(1)
BinaryTree* initBinaryTree() {
    BinaryTree* tree = new BinaryTree;
    tree->root = NULL;
    return tree;
}

// Time: Average O(log n), Worst O(n), Space: O(1)
// Chèn vào Binary Search Tree
bool insert(BinaryTree* tree, int x) {
    if (!tree->root) {
        tree->root = createTreeNode(x);
        return true;
    }
    TreeNode* cur = tree->root;
    while (true) {
        if (x < cur->data) {
            if (!cur->left) {
                cur->left = createTreeNode(x);
                return true;
            }
            cur = cur->left;
        } else if (x > cur->data) {
            if (!cur->right) {
                cur->right = createTreeNode(x);
                return true;
            }
            cur = cur->right;
        } else {
            return false; // Duplicate
        }
    }
}

// Time: Average O(log n), Worst O(n), Space: O(1)
// Tìm kiếm trong Binary Search Tree
bool search(BinaryTree* tree, int x) {
    TreeNode* cur = tree->root;
    while (cur) {
        if (x == cur->data) return true;
        cur = (x < cur->data) ? cur->left : cur->right;
    }
    return false;
}

// Time: O(n), Space: O(h) - h là chiều cao cây (đệ quy)
// Duyệt cây theo thứ tự: Root - Left - Right
void preorderHelper(TreeNode* node) {
    if (!node) return;
    cout << node->data << " ";
    preorderHelper(node->left);
    preorderHelper(node->right);
}

// Time: O(n), Space: O(h)
// Duyệt cây theo thứ tự: Left - Root - Right (Sorted cho BST)
void inorderHelper(TreeNode* node) {
    if (!node) return;
    inorderHelper(node->left);
    cout << node->data << " ";
    inorderHelper(node->right);
}

// Time: O(n), Space: O(h)
// Duyệt cây theo thứ tự: Left - Right - Root
void postorderHelper(TreeNode* node) {
    if (!node) return;
    postorderHelper(node->left);
    postorderHelper(node->right);
    cout << node->data << " ";
}

void preorder(BinaryTree* tree) {
    cout << "Preorder: ";
    preorderHelper(tree->root);
    cout << endl;
}

void inorder(BinaryTree* tree) {
    cout << "Inorder: ";
    inorderHelper(tree->root);
    cout << endl;
}

void postorder(BinaryTree* tree) {
    cout << "Postorder: ";
    postorderHelper(tree->root);
    cout << endl;
}

// Time: O(n), Space: O(h) - tính chiều cao cây
int heightHelper(TreeNode* node) {
    if (!node) return 0;
    int leftH = heightHelper(node->left);
    int rightH = heightHelper(node->right);
    return 1 + (leftH > rightH ? leftH : rightH);
}

int height(BinaryTree* tree) {
    return heightHelper(tree->root);
}

// Time: O(n), Space: O(h) - đếm số node
int countHelper(TreeNode* node) {
    if (!node) return 0;
    return 1 + countHelper(node->left) + countHelper(node->right);
}

int count(BinaryTree* tree) {
    return countHelper(tree->root);
}

// Time: O(n), Space: O(h) - giải phóng tất cả nodes
void clearHelper(TreeNode* node) {
    if (!node) return;
    clearHelper(node->left);
    clearHelper(node->right);
    delete node;
}

void clearBinaryTree(BinaryTree* tree) {
    clearHelper(tree->root);
    tree->root = NULL;
}

// Time: O(n), Space: O(h)
void destroyBinaryTree(BinaryTree* tree) {
    clearBinaryTree(tree);
    delete tree;
}

// ============ DEMO ============
int main() {
    cout << "=== ARRAY LIST TEST ===" << endl;
    ArrayList* arr = initArrayList();
    append(arr, 10);
    append(arr, 20);
    append(arr, 30);
    insertAt(arr, 1, 15);
    display(arr);
    removeAt(arr, 2);
    display(arr);
    cout << "Size: " << getSize(arr) << endl;
    
    cout << "\n--- ArrayList Sorting Test ---" << endl;
    ArrayList* arr2 = initArrayList();
    append(arr2, 64);
    append(arr2, 34);
    append(arr2, 25);
    append(arr2, 12);
    append(arr2, 22);
    append(arr2, 11);
    append(arr2, 90);
    cout << "Original: ";
    display(arr2);
    
    bubbleSort(arr2);
    cout << "Bubble Sort: ";
    display(arr2);
    
    // Reset array
    clearArrayList(arr2);
    append(arr2, 64); append(arr2, 34); append(arr2, 25);
    append(arr2, 12); append(arr2, 22); append(arr2, 11); append(arr2, 90);
    selectionSort(arr2);
    cout << "Selection Sort: ";
    display(arr2);
    
    // Reset array
    clearArrayList(arr2);
    append(arr2, 64); append(arr2, 34); append(arr2, 25);
    append(arr2, 12); append(arr2, 22); append(arr2, 11); append(arr2, 90);
    insertionSort(arr2);
    cout << "Insertion Sort: ";
    display(arr2);
    
    // Reset array
    clearArrayList(arr2);
    append(arr2, 64); append(arr2, 34); append(arr2, 25);
    append(arr2, 12); append(arr2, 22); append(arr2, 11); append(arr2, 90);
    quickSort(arr2);
    cout << "Quick Sort: ";
    display(arr2);
    
    // Reset array
    clearArrayList(arr2);
    append(arr2, 64); append(arr2, 34); append(arr2, 25);
    append(arr2, 12); append(arr2, 22); append(arr2, 11); append(arr2, 90);
    mergeSort(arr2);
    cout << "Merge Sort: ";
    display(arr2);
    
    // Reset array
    clearArrayList(arr2);
    append(arr2, 64); append(arr2, 34); append(arr2, 25);
    append(arr2, 12); append(arr2, 22); append(arr2, 11); append(arr2, 90);
    heapSort(arr2);
    cout << "Heap Sort: ";
    display(arr2);
    
    destroyArrayList(arr);
    destroyArrayList(arr2);
    
    cout << "\n=== LINKED LIST TEST ===" << endl;
    LinkedList* list = initLinkedList();
    insertTail(list, 10);
    insertTail(list, 20);
    insertHead(list, 5);
    display(list);
    deleteHead(list);
    display(list);
    cout << "Size: " << getSize(list) << endl;
    
    cout << "\n--- LinkedList Sorting Test ---" << endl;
    LinkedList* list2 = initLinkedList();
    insertTail(list2, 64);
    insertTail(list2, 34);
    insertTail(list2, 25);
    insertTail(list2, 12);
    insertTail(list2, 22);
    insertTail(list2, 11);
    insertTail(list2, 90);
    cout << "Original: ";
    display(list2);
    
    bubbleSort(list2);
    cout << "Bubble Sort: ";
    display(list2);
    
    // Reset list
    clearLinkedList(list2);
    insertTail(list2, 64); insertTail(list2, 34); insertTail(list2, 25);
    insertTail(list2, 12); insertTail(list2, 22); insertTail(list2, 11);
    insertTail(list2, 90);
    selectionSort(list2);
    cout << "Selection Sort: ";
    display(list2);
    
    // Reset list
    clearLinkedList(list2);
    insertTail(list2, 64); insertTail(list2, 34); insertTail(list2, 25);
    insertTail(list2, 12); insertTail(list2, 22); insertTail(list2, 11);
    insertTail(list2, 90);
    insertionSort(list2);
    cout << "Insertion Sort: ";
    display(list2);
    
    // Reset list
    clearLinkedList(list2);
    insertTail(list2, 64); insertTail(list2, 34); insertTail(list2, 25);
    insertTail(list2, 12); insertTail(list2, 22); insertTail(list2, 11);
    insertTail(list2, 90);
    mergeSort(list2);
    cout << "Merge Sort: ";
    display(list2);
    
    destroyLinkedList(list);
    destroyLinkedList(list2);
    
    cout << "\n=== STACK TEST ===" << endl;
    Stack* s = initStack();
    push(s, 10);
    push(s, 20);
    push(s, 30);
    display(s);
    int val;
    pop(s, val);
    cout << "Popped: " << val << endl;
    display(s);
    destroyStack(s);
    
    cout << "\n=== QUEUE TEST ===" << endl;
    Queue* q = initQueue();
    enqueue(q, 10);
    enqueue(q, 20);
    enqueue(q, 30);
    display(q);
    dequeue(q, val);
    cout << "Dequeued: " << val << endl;
    display(q);
    destroyQueue(q);
    
    cout << "\n=== BINARY TREE TEST ===" << endl;
    BinaryTree* tree = initBinaryTree();
    insert(tree, 50);
    insert(tree, 30);
    insert(tree, 70);
    insert(tree, 20);
    insert(tree, 40);
    insert(tree, 60);
    insert(tree, 80);
    preorder(tree);
    inorder(tree);
    postorder(tree);
    cout << "Height: " << height(tree) << endl;
    cout << "Count: " << count(tree) << endl;
    cout << "Search 40: " << (search(tree, 40) ? "Found" : "Not found") << endl;
    destroyBinaryTree(tree);
    
    return 0;
}