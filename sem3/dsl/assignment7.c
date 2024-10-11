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
					temp = temp->right;
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
				temp = temp->right;
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
	printf("Enter keyword to search: ");
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
			*root = (*root)->right;
			bstnode* s = (*root)->right;
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
	while (1) {
		printf("==========\n");
		printf("1. Inorder traversal (recursive)\n");
		printf("2. Breadth traversal\n");
		printf("3. Insert a new word\n");
		printf("4. Delete a word\n");
		printf("5. Copy binary search tree\n");
		printf("6. Mirror the tree\n");
		printf("7. Search for a word (recursive)\n");
		printf("8. Search for a word (non-recursive)\n");
		printf("Enter choice: ");
		char choice[4]; fgets(choice, 4, stdin);
		switch (choice[0]) {
			case '1': inorder_r(root); break;
			case '2': display_bfs(root); break;
			case '3': insert(root); break;
			case '4': deletenode(&root); break;
			case '6': mirror_r(root); break;
			case '7': search_r(root); break;
			case '8': search_nr(root); break;
			default: printf("Incorrect choice!\n");
		}
	}
	return 0;
}
