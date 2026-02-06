#include <iostream>
using namespace std;


struct TreeNode{
    int data;
    TreeNode *parent;
    TreeNode *tLeft;
    TreeNode *tRight;
};

TreeNode *init(int data, TreeNode *p){
    TreeNode *tree = new TreeNode;
    tree->data = data;
    tree->parent = p;
    tree->tLeft = nullptr;
    tree->tRight = nullptr;

    return tree;
}

void insertLeft(TreeNode *tree){
    TreeNode *newTree = init(0, tree);
    tree->tLeft = newTree;

    return;
}

bool isLeaf(TreeNode *tree){
    if (tree->tLeft == nullptr && tree->tRight == nullptr) {
        return true;
    } else {
        return false;
    }
}

void insertRight(TreeNode *tree){
    TreeNode *newTree = init(0, tree);
    tree->tRight = newTree;

    return;
}

void genTree(TreeNode *tParent, int h){
    if (h == 0) return;
    
    insertLeft(tParent);
    insertRight(tParent);

    genTree(tParent->tLeft, h-1);
    genTree(tParent->tRight, h-1);

    return;
}

void displayLRN(TreeNode *tree){
    if (tree == nullptr) return;

    displayLRN(tree->tLeft);
    displayLRN(tree->tRight);

    cout << tree->data << " ";
}

void fillLRN(TreeNode *tree, int *a, int *pos , int n, int E){
    if (tree == nullptr) return;

    fillLRN(tree->tLeft, a, pos, n, E);
    fillLRN(tree->tRight, a, pos, n, E);
    
    int data = 0;
    if (*pos < n) {
        data = a[*pos];
    } else {
        data = E;
    }

    if (isLeaf(tree)) {
        tree->data = data;
        *pos += 1;
    } else {
        tree->data = min(tree->tLeft->data, tree->tRight->data);
    }
}

int countHeightTree(int n){
    int height = 0;
    int leaves = 1;
    while (leaves < n){
        leaves *= 2;
        height++;
    }
    return height;
}

void sortLRN(TreeNode *tree, int *a, int n){
    int E = 0;
    for (int i = 0; i < n; i++){
        if (E < a[i]) E = a[i];
    }
    E++;

    int height = countHeightTree(n);
    genTree(tree, height);
    
    int pos = 0;
    fillLRN(tree, a, &pos, n, E);

    displayLRN(tree);

    return;
}

bool findTree(TreeNode *tree, int val){
    if (!tree) return false;

    if (tree->data == val){
        displayLRN(tree);  
        return true;
    }

    if (findTree(tree->tLeft, val)) return true;
    return findTree(tree->tRight, val);
}


int main(){
    int a[] = {8, 20, 41, 7, 2};
    int n = 5;

    TreeNode *tree = init(0, nullptr);

    sortLRN(tree, a, n);

    cout << endl;
    cout << findTree(tree, 5);
}

