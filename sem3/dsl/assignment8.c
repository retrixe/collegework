#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct tbtnode{
	char data[64];
	struct tbtnode* left;
	int lbit;
	struct tbtnode* right;
	int rbit;	
} tbtnode;

void insert(tbtnode* head) {
	tbtnode* temp = head->left;
	tbtnode* curr = (tbtnode*)malloc(sizeof(tbtnode));
	printf("Enter data for new node: ");
	fgets(curr->data, 64, stdin); curr->data[strcspn(curr->data, "\n")] = 0;
	curr->lbit = 0;
	curr->rbit = 0;
	while (1) {
		printf("Insert node at left or right of '%s' (L/R)? ", temp->data);
		char choice[4]; fgets(choice, 4, stdin);
		if (choice[0] == 'L' || choice[0] == 'l') {
			if (temp->lbit == 0) {
				curr->left = temp->left;
				curr->right = temp;
				temp->left = curr;
				temp->lbit = 1;
				break;
			} else {
				temp = temp->left;
			}
		} else if (choice[0] == 'R' || choice[0] == 'r') {
			if (temp->rbit == 0) {
				curr->left = temp;
				curr->right = temp->right;
				temp->right = curr;
				temp->rbit = 1;
				break;
			} else {
				temp = temp->right;
			}
		} else printf("Invaid choice!\n");
	}
}

tbtnode* create() {
	tbtnode* head = (tbtnode*)malloc(sizeof(tbtnode));
	head->lbit = 0;
	head->left = head;
	head->rbit = 1;
	head->right = head;
	tbtnode* root = (tbtnode*)malloc(sizeof(tbtnode));
	root->lbit = 0;
	root->left = head;
	root->rbit = 0;
	root->right = head;
	printf("Enter data for root: ");
	fgets(root->data, 64, stdin); root->data[strcspn(root->data, "\n")] = 0;
	head->lbit = 1;
	head->left = root;
	while (1) {
		printf("Would you like to add a new node (Y/N)? ");
		char choice[4]; fgets(choice, 4, stdin);
		if (choice[0] == 'N' || choice[0] == 'n') break;
		insert(head);
	}
	return head;
}

tbtnode* inordersuccessor(tbtnode* node) {
	tbtnode* x = node->right;
	if (node->rbit == 1) {
		while (x->lbit == 1) x = x->left;
	}
	return x;
}

void inorder(tbtnode* head) {
	tbtnode* temp = head;
	while (1) {
		temp = inordersuccessor(temp);
		if (temp == head) break;
		printf("%s\n", temp->data);
	}
}

void preorder(tbtnode* head) {
	tbtnode* temp = head->left;
	while (temp != head) {
		printf("%s\n", temp->data);
		while (temp->lbit != 0) {
			temp = temp->left;
			printf("%s\n", temp->data);
		}
		while (temp->rbit == 0) temp = temp->right;
		temp = temp->right;
	}
}

int main() {
	tbtnode* head = create();
	printf("===============\n");
	printf("1. Insert new node\n");
	printf("2. Inorder traversal\n");
	printf("3. Preorder traversal\n");
	printf("0. Exit\n");
	while (1) {
		printf("===============\n");
		printf("Enter choice: ");
		char choice[4]; fgets(choice, 4, stdin);
		switch (choice[0]) {
			case '1': insert(head); break;
			case '2': inorder(head); break;
			case '3': preorder(head); break;
			case '0': return 0;
			default: printf("Invalid choice!\n");
		}
	}
	return 0;
}
