#include <iostream>

using namespace std;

class Node {
	int id;
	string name;
	Node *next;

	friend class Graph;
	friend class Stack;
	friend class Queue;

	public:
	Node() {
		next = NULL;
	}
};

class Queue {
	int q[20];
	int front, rear;

	public:
	Queue() {
		front = -1;
		rear = -1;
	}

	void insert(int temp) {
		q[++rear] = temp;
	}

	int del() {
		return q[++front];
	}

	int empty() {
		return front == rear;
	}
};

class Stack {
	int st[20];
	int top;

	friend class Graph;

	public:
	Stack() {
		top = -1;
	}

	void push(int temp) {
		st[++top] = temp;
	}

	int pop() {
		return st[top--];
	}

	int empty() {
		return top == -1;
	}
};

class Graph {
	Node* head[20];
	int visited[20];
	int n;

	public:
	void accept_nodes() {
		cout << "Enter number of vertices: ";
		cin >> n;
		for (int i = 0; i < n; i++) {
			head[i] = new Node();
			cout << "Enter name of user #" << i <<  ": ";
			cin >> head[i]->name;
			head[i]->id = i;
		}
	}

	void create_adj_list() {
		for (int i = 0; i < n; i++) {
			auto node = head[i];
			cout << "===== Vertices adjacent to #"
				<< node->id << " (" << node->name << ") =====\n";
			while (1) {
				cout << "Would you like to add an adjacent vertex? ";
				char ch; cin >> ch;
				if (ch == 'Y' || ch == 'y') {
					auto temp = new Node();
					cout << "Enter vertex: ";
					cin >> temp->id;
					// TODO: What if vertex not exist?
					// TODO: What if vertex alr in list?
					// TODO: Sort adj list too
					temp->name = head[temp->id]->name;
					node->next= temp;
					node = temp;
				} else break;
			}
		}
	}

	void display() {
		for (int i = 0; i < n; i++) {
			auto node = head[i];
			cout << "===== Connections of user #" << node->id
				<< " (" << node->name << ") =====\n";
			node = node->next;
			if (node == NULL) {
				cout << "None" << endl;
				continue;
			}
			while (node != NULL) {
				cout << "- #" << node->id << ": " << node->name << "\n";
				node = node->next;
			}
		}
	}

	void dft_rec() {
		cout << "Enter starting vertex: ";
		int id; cin >> id;

		for (int i = 0; i < n; i++) {
			visited[i] = 0;
		}
		dft_rec(id);
		cout << endl;
	}

	void dft_rec(int id) {
		cout << id << "(" + head[id]->name + ")" << " ";
		visited[id] = 1;
		auto next = head[id]->next;
		while (next != NULL) {
			if (!visited[next->id]) dft_rec(next->id);
			next = next->next;
		}
	}

	void dft_non_rec() {
		cout << "Enter starting vertex: ";
		int id; cin >> id;

		for (int i = 0; i < n; i++) visited[i] = 0;
		Stack s;
		s.push(id); visited[id] = 1;
		while (!s.empty()) {
			id = s.pop();
			cout << id << " (" + head[id]->name + ")" << " ";
			auto next = head[id]->next;
			while (next != NULL) {
				if (!visited[next->id]) {
					s.push(next->id);
					visited[next->id] = 1;
				}
				next = next->next;
			}
		}
		cout << endl;
	}

	void bft() {
		cout << "Enter starting vertex: ";
		int id; cin >> id;

		for (int i = 0; i < n; i++) visited[i] = 0;
		Queue s;
		s.insert(id); visited[id] = 1;
		while (!s.empty()) {
			id = s.del();
			cout << id << "(" + head[id]->name + ")" << " ";
			auto next = head[id]->next;
			while (next != NULL) {
				if (!visited[next->id]) {
					s.insert(next->id);
					visited[next->id] = 1;
				}
				next = next->next;
			}
		}
		cout << endl;
	}
};

int main() {
	Graph g;
	g.accept_nodes();
	g.create_adj_list();
	g.display();

	cout << "Recursive DFT traversal\n";
	g.dft_rec();
	cout << "Non-recursive DFT traversal\n";
	g.dft_non_rec();

	cout << "BFT traversal\n";
	g.bft();

	return 0;
}
