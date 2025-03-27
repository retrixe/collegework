#include <iostream>
#include <vector>

using namespace std;

int main() {
    int capacity = 0;
    int item_count = 0;
    cout << "Enter capacity: ";
    cin >> capacity;
    cout << "Enter item count: ";
    cin >> item_count;

    int values[item_count];
    int weights[item_count];
    for (int i = 0; i < item_count; i++) {
        cout << "Enter item " << i + 1 << ": ";
        cin >> weights[i] >> values[i];
    }

    int soln[item_count + 1][capacity + 1] = {};
    for (int current_item = 1; current_item <= item_count; current_item++) {
        int value = values[current_item - 1];
        int weight = weights[current_item - 1];

        for (int current_weight = 1; current_weight <= capacity; current_weight++) {
            int previous_value = soln[current_item - 1][current_weight];
            if (weight <= current_weight) {
                int calculated_value = value + soln[current_item - 1][current_weight - weight];
                soln[current_item][current_weight] =
                    calculated_value > previous_value ? calculated_value : previous_value;
            } else {
                soln[current_item][current_weight] = previous_value;
            }
        }
    }

    vector<int> result;
    int column = capacity;
    for (int row = item_count; row > 0; row--) {
        if (soln[row][column] != soln[row - 1][column]) {
            result.push_back(row);
            column -= weights[row - 1];
        }
    }

    cout << "The solution is: " << endl;
    for (int item : result) {
        cout <<  item << " ";
    }
    cout << endl;
}
