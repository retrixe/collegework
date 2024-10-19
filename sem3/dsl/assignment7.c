#include <stdlib.h>
#include <stdio.h>
#include <string.h>

typedef struct bstnode{
	char keyword[32];
	char definition[256];
	struct bstnode* left;
	struct bstnode* right;
} bstnode;

void create(bstnode* root) {
	while (1) {
		printf("Would you like to add a new node (Y/N)? ");
		char choice[4];
		fgets(choice, 4, stdin);
		if (choice[0] == 'N' || choice[0] == 'n') break;

		bstnode* curr = (bstnode*)malloc(sizeof(bstnode));
		curr->left = NULL;
		curr->right = NULL;
		printf("Enter keyword: ");
		fgets(curr->keyword, 32, stdin);
		curr->keyword[strcspn(curr->keyword, "\n")] = 0;
		printf("Enter meaning: ");
		fgets(curr->definition, 256, stdin);
		curr->definition[strcspn(curr->definition, "\n")] = 0;

		bstnode* temp = root;
		while (1) {
			if (strcmp(curr->keyword, temp->keyword) < 0) {
				if (temp->left == NULL) {
					temp->left = curr;
					break;
				} else {
					temp = temp->left;
				}
			} else {
				if (temp->right == NULL) {
					temp->right = curr;
					break;
				} else {
					temp = temp->right;
				}
			}
		}
	}
}

void inorder_r(bstnode* temp) {
	if (temp != NULL) {
		inorder_r(temp->left);
		printf("%s (%s)\n", temp->keyword, temp->definition);
		inorder_r(temp->right);
	}
}

void insert(bstnode* root) {
	bstnode* curr = (bstnode*)malloc(sizeof(bstnode));
	curr->left = NULL;
	curr->right = NULL;
	printf("Enter keyword: ");
	fgets(curr->keyword, 32, stdin);
	curr->keyword[strcspn(curr->keyword, "\n")] = 0;
	printf("Enter meaning: ");
	fgets(curr->definition, 256, stdin);
	curr->definition[strcspn(curr->definition, "\n")] = 0;

	bstnode* temp = root;
	while (1) {
		if (strcmp(curr->keyword, temp->keyword) < 0) {
			if (temp->left == NULL) {
				temp->left = curr;
				break;
			} else {
				temp = temp->left;
			}
		} else {
			if (temp->right == NULL) {
				temp->right = curr;
				break;
			} else {
				temp = temp->right;
			}
		}
	}
}

void deletenode(bstnode** root) {
	printf("Enter keyword to delete: ");
	char keyword[32];
	fgets(keyword, 32, stdin);
	keyword[strcspn(keyword, "\n")] = 0;
	bstnode* parent = NULL;
	bstnode* curr = NULL;
	bstnode* temp = *root;
	while (temp != NULL) {
		int cmp = strcmp(keyword, temp->keyword);
		if (cmp == 0) {
			curr = temp;
			break;
		} else if (cmp < 0) {
			parent = temp;
			temp = temp->left;
		} else {
			parent = temp;
			temp = temp->right;
		}
	}

	if (curr == NULL) {
		printf("Keyword not found!\n");
		return;
	} else if (curr == *root) {
		if (curr->left == NULL) { *root = (*root)->right; }
		else if (curr->right == NULL) { *root = (*root)->left; }
		else {
			temp = (*root)->left;
			bstnode* s = (*root)->right;
			*root = (*root)->right;
			while (s->left != NULL) { s = s->left; }
			s->left = temp;
		}
	} else {
		if (curr->left == NULL && curr->right == NULL) {
			if (parent->left == curr) parent->left = NULL;
			if (parent->right == curr) parent->right = NULL;
		} else if (curr->left == NULL) {
			if (parent->left == curr) parent->left = curr->right;
			if (parent->right == curr) parent->right = curr->right;
		} else if (curr->right == NULL) {
			if (parent->left == curr) parent->left = curr->left;
			if (parent->right == curr) parent->right = curr->left;
		} else {
			temp = curr->left;
			bstnode* s = curr->right;
			while (s->left != NULL) { s = s->left; }
			s->left = temp;
			if (parent->left == curr) parent->left = curr->right;
			if (parent->right == curr) parent->right = curr->right;
		}
	}
	curr->left = NULL; curr->right = NULL; free(curr);
}

bstnode* search_rfn(bstnode* temp, char keyword[32]) {
	if (temp != NULL) {
		int cmp = strcmp(keyword, temp->keyword);
		if (cmp == 0) return temp;
		else if (cmp < 0) return search_rfn(temp->left, keyword);
		else return search_rfn(temp->right, keyword);
	}
}

void search_r(bstnode* root) {
	printf("Enter keyword to search: ");
	char keyword[32];
	fgets(keyword, 32, stdin);
	keyword[strcspn(keyword, "\n")] = 0;
	bstnode* result = search_rfn(root, keyword);
	if (result == NULL) {
		printf("Keyword not found!\n");
	} else {
		printf("%s (%s)\n", result->keyword, result->definition);
	}
}

void search_nr(bstnode* root) {
	printf("Enter keyword to search: ");
	char keyword[32];
	fgets(keyword, 32, stdin);
	keyword[strcspn(keyword, "\n")] = 0;
	bstnode* temp = root;
	bstnode* result = NULL;
	while (temp != NULL) {
		int cmp = strcmp(keyword, temp->keyword);
		if (cmp == 0) {
			result = temp;
			break;
		} else if (cmp < 0) {
			temp = temp->left;
		} else {
			temp = temp->right;
		}
	}

	if (result == NULL) {
		printf("Keyword not found!\n");
	} else {
		printf("%s (%s)\n", result->keyword, result->definition);
	}
}

void mirror_r(bstnode* root) {
	bstnode* temp = root->left;
	root->left = root->right;
	root->right = temp;
	if (root->left != NULL) mirror_r(root->left);
	if (root->right != NULL) mirror_r(root->right);
}

typedef struct queuenode{
	bstnode* data;
	struct queuenode* next;
} queuenode;

queuenode* queueFront;
queuenode* queueRear = NULL;

int queueIsEmpty() { return queueFront->next == NULL; }

void enqueue(bstnode* value) {
	queuenode* node = (queuenode*)malloc(sizeof(queuenode));
	node->data = value;
	node->next = NULL;
	if (queueIsEmpty()) {
		queueFront->next = node;
	} else {
		queueRear->next = node;
	}
	queueRear = node;
}

bstnode* dequeue() {
	if (queueIsEmpty()) {
		return NULL;
	}
	queuenode* temp = queueFront->next;
	bstnode* value = temp->data;
	queueFront->next = temp->next;
	free(temp);
	return value;
}


void mirror_nr(bstnode* root) {
	bstnode* temp = root;
	enqueue(temp);
	while (!queueIsEmpty()) {
		temp = dequeue();
		bstnode* prevleft = temp->left;
		temp->left = temp->right;
		temp->right = prevleft;
		if (temp->left != NULL) enqueue(temp->left);
		if (temp->right != NULL) enqueue(temp->right);
	}
}

void display_bfs(bstnode* root) {
	bstnode* temp = root;
	enqueue(temp);
	while (!queueIsEmpty()) {
		temp = dequeue();
		printf("%s (%s)\n", temp->keyword, temp->definition);
		if (temp->left != NULL) enqueue(temp->left);
		if (temp->right != NULL) enqueue(temp->right);
	}
}

bstnode* copy_r(bstnode* root) {
	bstnode* temp = NULL;
	if (root != NULL) {
		temp = (bstnode*)malloc(sizeof(bstnode));
		strcpy(temp->keyword, root->keyword);
		strcpy(temp->definition, root->definition);
		temp->left = copy_r(root->left);
		temp->right = copy_r(root->right);
	}
	return temp;
}

#define MAX 64
bstnode* stack1[MAX];
int stackTop1 = -1;

int stackIsFull1() {
	return stackTop1 == MAX - 1;
}

int stackIsEmpty1() {
	return stackTop1 == -1;
}

void stackPush1(bstnode* element) {
	if (stackIsFull1()) {
		printf("Stack is full\n");
	} else {
		stack1[++stackTop1] = element;
	}
}

bstnode* stackPop1() {
	if (stackIsEmpty1(stackTop1)) {
		return NULL;
	} else {
		return stack1[stackTop1--];
	}
}

bstnode* stack2[MAX];
int stackTop2 = -1;

int stackIsFull2() {
	return stackTop2 == MAX - 1;
}

int stackIsEmpty2() {
	return stackTop2 == -1;
}

void stackPush2(bstnode* element) {
	if (stackIsFull2()) {
		printf("Stack 2 is full\n");
	} else {
		stack2[++stackTop2] = element;
	}
}

bstnode* stackPop2() {
	if (stackIsEmpty2(stackTop2)) {
		return NULL;
	} else {
		return stack2[stackTop2--];
	}
}

bstnode* copy_nr(bstnode* root2) {
	bstnode* root1 = (bstnode*)malloc(sizeof(bstnode));
	bstnode* temp1 = root1;
	bstnode* temp2 = root2;
	strcpy(temp1->keyword, temp2->keyword);
	strcpy(temp1->definition, temp2->definition);
	while (1) {
		while (temp2 != NULL) {
			if (temp2->left != NULL) {
				temp1->left = (bstnode*)malloc(sizeof(bstnode));
				temp1->left->left = NULL; temp1->left->right = NULL;
				strcpy(temp1->left->keyword, temp2->left->keyword);
				strcpy(temp1->left->definition, temp2->left->definition);
			}
			if (temp2->right != NULL) {
				temp1->right = (bstnode*)malloc(sizeof(bstnode));
				temp1->right->left = NULL; temp1->right->right = NULL;
				strcpy(temp1->right->keyword, temp2->right->keyword);
				strcpy(temp1->right->definition, temp2->right->definition);
			}
			stackPush1(temp1);
			stackPush2(temp2);
			temp1 = temp1->left;
			temp2 = temp2->left;
		}
		if (stackIsEmpty1()) break;
		temp1 = stackPop1();
		temp2 = stackPop2();
		temp1 = temp1->right;
		temp2 = temp2->right;
	}
	return root1;
}

void deletetree(bstnode* root) {
	bstnode* temp = NULL;
	if (root != NULL) {
		deletetree(root->left);
		deletetree(root->right);
		root->left = NULL;
		root->right = NULL;
		free(root);
	}
}

// cat ant dog zebra mouse buffalo bat
// delete: bat ant cat
int main() {
	queueFront = (queuenode*)malloc(sizeof(queuenode));
	queueFront->next = NULL;

	bstnode* root = (bstnode*)malloc(sizeof(bstnode));
	root->left = NULL;
	root->right = NULL;
	printf("Enter keyword: ");
	fgets(root->keyword, 32, stdin);
	root->keyword[strcspn(root->keyword, "\n")] = 0;
	printf("Enter meaning: ");
	fgets(root->definition, 256, stdin);
	root->definition[strcspn(root->definition, "\n")] = 0;

	create(root);
	bstnode* copy;
	while (1) {
		printf("==========\n");
		printf("1. Inorder traversal (recursive)\n");
		printf("2. Breadth traversal\n");
		printf("3. Insert a new word\n");
		printf("4. Delete a word\n");
		printf("5. Copy tree (recursive)\n");
		printf("6. Copy tree (non-recursive)\n");
		printf("7. Mirror the tree (recursive)\n");
		printf("8. Mirror the tree (non-recursive)\n");
		printf("9. Search for a word (recursive)\n");
		printf("10. Search for a word (non-recursive)\n");
		printf("Enter choice: ");
		char choice[4]; fgets(choice, 4, stdin);
		int ch; sscanf(choice, "%d", &ch);
		switch (ch) {
			case 1: inorder_r(root); break;
			case 2: display_bfs(root); break;
			case 3: insert(root); break;
			case 4: deletenode(&root); break;
			case 5:
			case 6:
				if (ch == 5) copy = copy_r(root);
				else copy = copy_nr(root);
				printf("Inorder traversal of copy:\n");
				inorder_r(copy);
				printf("Breadth first traversal of copy::\n");
				display_bfs(copy);
				deletetree(copy);
				break;
			case 7: mirror_r(root); break;
			case 8: mirror_r(root); break;
			case 9: search_r(root); break;
			case 10: search_nr(root); break;
			default: printf("Incorrect choice!\n");
		}
	}
	return 0;
}
