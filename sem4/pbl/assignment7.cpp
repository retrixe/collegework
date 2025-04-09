#include <iostream>

using namespace std;

int x[10000] = {};

void print_soln(int n) {
    for (int i = 1; i <= n; i++) {
        cout << x[i] << " ";
    }
    cout << endl;
}

bool place(int k, int i) {
    for (int j = 1; j < k; j++) {
        if (x[j] == i || abs(x[j] - i) == abs(j - k)) return false;
    }
    return true;
}

void nqueen(int k, int n) {
    for (int i = 1; i <= n; i++) {
        if (place(k, i)) {
            x[k] = i;
            if (k == n) {
                print_soln(n);
            } else {
                nqueen(k + 1, n);
            }
        }
    }
}

int main() {
    int n = 0;
    cout <<  "Enter number of queens in N-Queen problem: ";
    cin >> n;

    nqueen(1, n);
}
