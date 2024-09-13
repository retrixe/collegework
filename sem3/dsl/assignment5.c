#include <stdio.h>
#include <stdlib.h>

typedef struct node{
	char name[10];
	char pos;
	int id;
	struct node* next;
} node;

void create(node* head);

int len(node* head);

void insert(node* head);

void deletion(node* head);

void sort(node* head);

void display(node* head);

int main() {
	node* head = (node*)malloc(sizeof(node));
	head->next = NULL;
	create(head);
	//sort(head);
	display(head);
	while (1) {
		printf("===== Enter choice =====\n");
		printf("1. Insert member\n");
		printf("2. Delete member\n");
		printf("3. Display members\n");
		printf("4. Get member count\n");
		printf("0. Exit\n");
		int choice; scanf("%d", &choice);
		switch (choice) {
			case 0: return 0;
			case 1: insert(head); break;
			case 2: deletion(head); break;
			case 3: display(head); break;
			case 4: printf("Length: %d\n", len(head)); break;
			default: printf("Invalid choice!\n");
		}
	}
}

void create(node* head) {
	int count;
	printf("How many members would you like to input? ");
	scanf("%d", &count);
	node* curr = head;
	for (int i = 0; i < count; i++) {
		node* newnode = (node*)malloc(sizeof(node));
		printf("Enter member name, ID and position: ");
		scanf("%s %d %c", newnode->name, &newnode->id, &newnode->pos);
		newnode->next = NULL;
		curr->next = newnode;
		curr = newnode;
	}
}

int len(node* head) {
	node* curr = head->next;
	int count = 0;
	while (curr != NULL) {
		curr = curr->next;
		count++;
	}
	return count;
}

/* void sort(node* head) {
	int length = len(head);
	for (int i = 0; i < length - 1; i++) {
		node* prev = head;
		node* curr = head->next;
		// FIXME more efficient
		for (int j = 0; j < length - 1; j++) {
			// FIXME incorrect comparison
			node* future = curr->next;
			if (future->id < curr->id) {
//				pos(future->id) < pos(curr->id)) {
				curr->next = future->next;
				future->next = curr;
				prev->next = future;
				prev = future;
			} else {
				prev = curr;
				curr = curr->next;
			}
		}
	}
} */

void display(node* head) {
	node* curr = head->next;
	int count = 1;
	while (curr != NULL) {
		printf("======== Member #%d ========\n", count++);
		printf("ID: %d\n", curr->id);
		printf("Name: %s\n", curr->name);
		printf("Position (P - president, S - secretary, M - member): %c\n", curr->pos);
		curr = curr->next;
	}
}

void insert(node* head) {
	printf("Enter position in list: ");
	int pos; scanf("%d", &pos); pos--;
	if (pos > len(head) || pos < 0) {
		printf("Position is outside list! (Size: %d)\n", len(head));
		return;
	}

	node* newnode = (node*)malloc(sizeof(node));
	printf("Enter member name, ID and position: ");
	scanf("%s %d %c", newnode->name, &newnode->id, &newnode->pos);

	node* curr = head;
	while (pos != 0) {
		curr = curr->next;
		pos--;
	}
	newnode->next = curr->next;
	curr->next = newnode;
}

void deletion(node* head) {
	printf("Enter position in list: ");
	int pos; scanf("%d", &pos); pos--;
	if (pos > len(head) || pos < 0) {
		printf("Position is outside list! (Size: %d)\n", len(head));
		return;
	}

	node* curr = head;
	while (pos != 0) {
		curr = curr->next;
		pos--;
	}
	node* deleted = curr->next;
	curr->next = deleted->next;
	free(deleted);
}
