#include <iostream>

using namespace std;

class avlnode {
    string word, meaning;
    avlnode *left = NULL, *right = NULL;
public:
    friend class avltree;
};

class avltree {
    avlnode* root = NULL;
public:
    int height(avlnode* node) {
        int h = 0;
        if (node != NULL) {
            h = max(height(node->left), height(node->right)) + 1;
        }
        return h;
    }

    int diff(avlnode* node) {
        return height(node->left) - height(node->right);
    }

    avlnode* rr_rotation(avlnode* node) {
        auto temp = node->right;
        node->right = temp->left;
        temp->left = node;
        return temp;
    }

    avlnode* ll_rotation(avlnode* node) {
        auto temp = node->left;
        node->left = temp->right;
        temp->right = node;
        return temp;
    }

    avlnode* lr_rotation(avlnode* node) {
        auto temp = node->left;
        node->left = rr_rotation(temp);
        return ll_rotation(node);
    }

    avlnode* rl_rotation(avlnode* node) {
        auto temp = node->right;
        node->right = ll_rotation(temp);
        return rr_rotation(node);
    }

    avlnode* balance(avlnode* node) {
        int bal_factor = diff(node);
        if (bal_factor > 1) {
            if (diff(node->left) > 0) node = ll_rotation(node);
            else node = lr_rotation(node);
        } else if (bal_factor < -1) {
            if (diff(node->right) > 0) node = rl_rotation(node);
            else node = rr_rotation(node);
        }
        return node;
    }

    void insert() {
        char ch;
        do {
            avlnode* temp = new avlnode();
            cout << "Enter word and meaning: ";
            cin >> temp->word >> temp->meaning;
            root = insert(root, temp);
            cout << "Add more? (Y/N) ";
            cin >> ch;
        } while (ch == 'y' || ch == 'Y');
    }

    avlnode* insert(avlnode* node, avlnode* temp) {
        if (node == NULL) {
            return temp;
        } else if (temp->word < node->word) {
            node->left = insert(node->left, temp);
            node = balance(node);
        } else {
            node->right = insert(node->right, temp);
            node = balance(node);
        }
        return node;
    }

    void display() {
        display(root, 0);
    }

    void display(avlnode* ptr, int level) {
        if (ptr != NULL) {
            display(ptr->right, level + 1);
            cout << endl;
            if (ptr == root) cout << "Root -> ";
            for (int i = 0; i < level && ptr != root; i++) cout << " ";
            cout << ptr->word;
            display(ptr->left, level + 1);
        }
    }
};

int main() {
 	avltree tree;
    tree.insert();
    tree.display();
}

