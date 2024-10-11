#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct treenode {
	char data[64];
	struct treenode* left;
	struct treenode* right;
} treenode;

char input[4];

#define MAX 64
treenode* stack[MAX];
int stackTop = -1;

int stackIsFull() {
	return stackTop == MAX - 1;
}

int stackIsEmpty() {
	return stackTop == -1;
}

void stackPush(treenode* element) {
	if (stackIsFull()) {
		printf("Stack is full\n");
	} else {
		stack[++stackTop] = element;
	}
}

treenode* stackPop() {
	if (stackIsEmpty(stackTop)) {
		return NULL;
	} else {
		return stack[stackTop--];
	}
}

void display_inorder(treenode* root) {
	if (root != NULL) {
		display_inorder(root->left);
		printf("%s\n", root->data);
		display_inorder(root->right);
	}
}

void display_preorder(treenode* root) {
	if (root != NULL) {
		printf("%s\n", root->data);
		display_preorder(root->left);
		display_preorder(root->right);
	}
}

void display_postorder(treenode* root) {
	if (root != NULL) {
		display_postorder(root->left);
		display_postorder(root->right);
		printf("%s\n", root->data);
	}
}

void display_inorder_nr(treenode *root) {
	treenode* temp = root;
	while (1) {
		while (temp != NULL) {
			stackPush(temp);
			temp = temp->left;
		}
		if (stackIsEmpty()) break;
		temp = stackPop();
		printf("%s\n", temp->data);
		temp = temp->right;
	}
}

void display_preorder_nr(treenode *root) {
	treenode* temp = root;
	while (1) {
		while (temp != NULL) {
			printf("%s\n", temp->data);
			stackPush(temp);
			temp = temp->left;
		}
		if (stackIsEmpty()) break;
		temp = stackPop();
		temp = temp->right;
	}
}

void display_postorder_nr(treenode *root) {
	treenode* temp = root;
	while (1) {
		while (temp != NULL) {
			stackPush(temp);
			temp = temp->left;
		}
		if (stack[stackTop]->right == NULL) {
			temp = stackPop();
			printf("%s\n", temp->data);
		}
		while (!stackIsEmpty() && stack[stackTop]->right == temp) {
			temp = stackPop();
			printf("%s\n", temp->data);
		}
		if (stackIsEmpty()) break;
		temp = stack[stackTop]->right;
	}
}

void create_r(treenode* root) {
	char ch;
	printf("Add data to left of \"%s\"? (Y/N) ", root->data);
	fgets(input, 4, stdin); sscanf(input, "%c", &ch);
	if (ch == 'Y' || ch == 'y') {
		treenode* curr = (treenode*)malloc(sizeof(treenode));
		curr->left = NULL;
		curr->right = NULL;
		printf("Enter node data: ");
		fgets(curr->data, 64, stdin); curr->data[strcspn(curr->data, "\n")] = 0;
		root->left = curr;
		create_r(curr);
	}
	printf("Add data to right of \"%s\"? (Y/N) ", root->data);
	fgets(input, 4, stdin); sscanf(input, "%c", &ch);
	if (ch == 'Y' || ch == 'y') {
		treenode* curr = (treenode*)malloc(sizeof(treenode));
		curr->left = NULL;
		curr->right = NULL;
		printf("Enter node data: ");
		fgets(curr->data, 64, stdin); curr->data[strcspn(curr->data, "\n")] = 0;
		root->right = curr;
		create_r(curr);
	}
}

void create_nr(treenode* root) {
	while (1) {
		treenode* temp = root;
		treenode* curr = (treenode*)malloc(sizeof(treenode));
		printf("Enter data for new node: ");
		fgets(curr->data, 64, stdin); curr->data[strcspn(curr->data, "\n")] = 0;
		curr->left = NULL; curr->right = NULL;
		while (1) {
			printf("Add node to left or right of \"%s\"? (L/R) ", temp->data);
			char ch; fgets(input, 4, stdin); sscanf(input, "%c", &ch);

			if ((ch == 'l' || ch == 'L') && temp->left == NULL) {
				temp->left = curr; break;
			} else if ((ch == 'r' || ch == 'R') && temp->right == NULL) {
				temp->right = curr; break;
			}
			if (ch == 'l' || ch == 'L') {
				temp = temp->left;
			} else if (ch == 'r' || ch == 'R') {
				temp = temp->right;
			}
		}
		printf("Add another node? (Y/N) ");
		char ch; fgets(input, 4, stdin); sscanf(input, "%c", &ch);
		if (ch != 'y' && ch != 'Y') break;
	}
}

typedef struct queuenode{
	treenode* data;
	struct queuenode* next;
} queuenode;

queuenode* queueFront;
queuenode* queueRear = NULL;

int queueIsEmpty() { return queueFront->next == NULL; }

void enqueue(treenode* value) {
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

treenode* dequeue() {
	if (queueIsEmpty()) {
		return NULL;
	}
	queuenode* temp = queueFront->next;
	treenode* value = temp->data;
	queueFront->next = temp->next;
	free(temp);
	return value;
}

void display_bfs(treenode* root) {
	treenode* temp = root;
	enqueue(temp);
	while (!queueIsEmpty()) {
		temp = dequeue();
		printf("%s\n", temp->data);
		if (temp->left != NULL) enqueue(temp->left);
		if (temp->right != NULL) enqueue(temp->right);
	}
}

void mirror_r(treenode* root) {
	treenode* temp = root->left;
	root->left = root->right;
	root->right = temp;
	if (root->left != NULL) mirror_r(root->left);
	if (root->right != NULL) mirror_r(root->right);
}

int main() {
	queueFront = (queuenode*)malloc(sizeof(queuenode));
	queueFront->next = NULL;

	treenode* root = (treenode*)malloc(sizeof(treenode));
	root->left = NULL;
	root->right = NULL;
	printf("Enter root node data: ");
	fgets(root->data, 64, stdin); root->data[strcspn(root->data, "\n")] = 0;
	printf("Use recursive? (Y/N) ");
	char ch; fgets(input, 4, stdin); sscanf(input, "%c", &ch);
	if (ch == 'Y' || ch == 'y') create_r(root);
	else create_nr(root);

	while (1) {
		printf("Enter choices:\n");
		printf("1) DFS recursive traversals\n");
		printf("2) DFS non-recursive traversals\n");
		printf("3) BFS traversals\n");
		printf("4) Mirror tree recursively\n");
		// printf("5) Mirror tree non-recursively\n");
		printf("0) Exit\n");
		int choice;
		fgets(input, 4, stdin); sscanf(input, "%d", &choice);

		if (choice == 1) {
			printf("DFS inorder traversal (recursive):\n");
			display_inorder(root);
			printf("DFS postorder traversal (recursive):\n");
			display_postorder(root);
			printf("DFS preorder traversal (recursive):\n");
			display_preorder(root);
		} else if (choice == 2) {
			printf("DFS inorder traversal (non recursive):\n");
			display_inorder_nr(root);
			printf("DFS postorder traversal (non recursive):\n");
			display_postorder_nr(root);
			printf("DFS preorder traversal (non recursive):\n");
			display_preorder_nr(root);
		} else if (choice == 3) {
			printf("BFS traversal:\n");
			display_bfs(root);
		} else if (choice == 4) {
			mirror_r(root);
			printf("Mirrored tree recursively!\n");
		} else if (choice == 0) return 0;
	}
}
