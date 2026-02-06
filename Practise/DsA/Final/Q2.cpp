#include <iostream>
#define MAX 100

struct Stack {
    int size;
    int data[MAX];
};

Stack *init(){
    Stack *st = new Stack;
    st->size = 0;

    return st;
}

int isEmpty(Stack *st){
    return (st->size == 0);
}

int isFull(Stack *st){
    return (st->size == MAX);
}

void push(Stack *st, int val){
    if (isFull(st)){
        return ;
    }

    st->data[st->size++] = val;
    return ;
}

int pop(Stack *st){
    if (isEmpty(st)){
        return -1;
    }

    return st->data[--st->size];
}

int top(Stack * st){
    if (isEmpty(st)){
        return -1;
    }

    return st->data[st->size - 1];
}

int getMin(Stack *minStack, int val){
    if (top(minStack) == -1) return val;

    if (top(minStack) > val) 
        return val;
    else 
        return top(minStack);
}

void display(Stack *st){
    for (int i = 0; i < st->size; i++){
        std::cout << st->data[i] << " " ;
    }

    std::cout << std::endl;
    return ;
}

int main(){
    // Init 2 stack : mainStack, minStack
    Stack *mainStack = init();
    Stack *minStack = init();

    // Put values [1, 4, 7, 3, 19, 0] in 2 stack
    push(mainStack, 10);
    push(minStack, getMin(minStack, 10));

    push(mainStack, 4);
    push(minStack, getMin(minStack, 4));

    push(mainStack, 7);
    push(minStack, getMin(minStack, 7));

    push(mainStack, 3);
    push(minStack, getMin(minStack, 3));

    push(mainStack, 19);
    push(minStack, getMin(minStack, 19));

    push(mainStack, 0);
    push(minStack, getMin(minStack, 0));

    // Show current element of 2 stack after push all number
    std::cout << "Show current element of 2 stack after push all number" << std::endl;
    display(mainStack);
    display(minStack);
    
    // Try pop something from mainStack and show min of mainStack
    int a, b, curMin;


    a = pop(mainStack);
    b = pop(minStack);
    curMin = top(minStack);

    std::cout << "pop a number in mainStack, Here's current min of mainStack : " << curMin << std::endl;


    a = pop(mainStack);
    b = pop(minStack);
    curMin = top(minStack);

    std::cout << "pop a number in mainStack, Here's current min of mainStack : " << curMin << std::endl;


    a = pop(mainStack);
    b = pop(minStack);
    curMin = top(minStack);

    std::cout << "pop a number in mainStack, Here's current min of mainStack : " << curMin << std::endl;


    a = pop(mainStack);
    b = pop(minStack);
    curMin = top(minStack);

    std::cout << "pop a number in mainStack, Here's current min of mainStack : " << curMin << std::endl;
}