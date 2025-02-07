#include <bits/stdc++.h>

using namespace std;

#define MAX 1000
#define INF 100000000

class Graph {
	int count;
	vector<string> names;
	int costs[MAX][MAX];

	public:
	void create() {
		cout << "Enter number of cities: ";
		cin >> count;
		for (int i = 0; i < count; i++) {
			cout << "Enter city " << i << " name: ";
			string name; cin >> name;
			names.push_back(name);
		}
		for (int i = 0; i < count; i++) {
			for (int j = i; j < count; j++) {
				if (i == j) {
					costs[i][j] = INF;
					continue;
				}
				cout << "Is there an edge between " << i << " and " << j << " (Y/N)? ";
				char choice; cin >> choice;
				if (choice != 'Y' && choice != 'y') {
					costs[i][j] = costs[j][i] = INF;
				} else {
					cout << "Enter cost of edge: ";
					int cost; cin >> cost;
					costs[i][j] = costs[j][i] = cost;
				}
			}
		}
	}

	void display() {
		cout << "====================" << endl;
		cout << "  Adjacency Matrix  " << endl;
		cout << "====================" << endl;
		for (int i = 0; i < count; i++) {
			for (int j = 0; j < count; j++) {
				if (costs[i][j] == INF) {
					cout << "X ";
				} else {
					cout << costs[i][j] << " ";
				}
			}
			cout << endl;
		}
	}

	void prims(int start_v) {
		int t[count - 1][3];
		int nearest[count];
		int mincost = 0;

		nearest[start_v] = -1;
		for (int i = 0; i < count; i++) {
			if (i != start_v) nearest[i] = start_v;
		}

		for (int i = 0; i < count - 1; i++) {
			int min = INF;
			int j = -1;
			for (int k = 0; k < count; k++) {
				if (nearest[k] != -1 && costs[k][nearest[k]] < min) {
					j = k;
					min = costs[k][nearest[k]];
				}
			}
			if (j == -1) {
				cout << "MST not possible to construct!" << endl;
				return;
			}

			t[i][0] = nearest[j];
			t[i][1] = j;
			t[i][2] = min;
			mincost += min;
			nearest[j] = -1;

			for (int k = 0; k < count; k++) {
				if (nearest[k] != -1 && costs[k][nearest[k]] > costs[k][j]) {
					nearest[k] = j;
				}
			}
		}

		cout << "MST: " << endl;
		cout << "vrt1: " << endl;
		for (int j = 0; j < count - 1; j++) {
			cout << t[j][0] << " ";
		}
		cout << endl;
		cout << "vrt2: " << endl;
		for (int j = 0; j < count - 1; j++) {
			cout << t[j][1] << " ";
		}
		cout << endl;
		cout << "cost: " << endl;
		for (int j = 0; j < count - 1; j++) {
			cout << t[j][2] << " ";
		}
		cout << endl;
		cout << "Minimum cost of MST: " << mincost << endl;
	}
};

int main() {
	Graph g;
	g.create();
	g.display();
	cout << "Enter starting vertex for Prim's algorithm: ";
	int start_v; cin >> start_v;
	g.prims(start_v);
	return 0;
}
