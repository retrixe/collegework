#include <algorithm>
#include <cmath>
#include <iostream>

using namespace std;

string encodeHamming(const string &data) {
    const int m = data.size();
    const int n = ceil(log2(m) + 1);
    cout << "m = "  << m << endl << "n = "  << n << endl;
    string result(m + n, '0'); // length = m + n

    // Copy data bits in reverse
    int d = m;
    for (int i = 1; i <= m + n; i++) {
        if (floor(log2(i)) == log2(i)) continue; // Skip over parity bits
        result[i - 1] = data[--d];
    }

    // Calculate parity bits
    for (int i = 0; i < n; i++) {
        const int r = floor(pow(2, i));
        int parity = 0;
        for (d = 1; d <= m + n; d++) {
            // Check if (d & r(i)) is true which are the bits covered by r(i), exclude r(i) itself
            if (d & r && d != r) {
                // Flip the parity bit if value is 1
                parity ^= result[d - 1] == '1' ? 1 : 0;
            }
        }
        result[r - 1] = parity ? '1'  : '0';
    }

    ranges::reverse(result);
    return result;
}

void decodeHamming(string &message) {
    const int n = ceil(log2(message.size()));
    const int m = message.size() - n;
    cout << "m = "  << m << endl << "n = "  << n << endl;
    ranges::reverse(message);

    // Calculate parity bits
    int errorPos = 0;
    for (int i = 0; i < n; i++) {
        const int r = floor(pow(2, i));
        int parity = 0;
        for (int d = 1; d <= m + n; d++) {
            // Check if (d & r(i)) is true which are the bits covered by r(i), exclude r(i) itself
            if (d & r && d != r) {
                // Flip the parity bit if value is 1
                parity ^= message[d - 1] == '1' ? 1 : 0;
            }
        }
        if ((parity ? '1' : '0') != message[r - 1]) {
            cout << "Error calculating parity bit " << r << "!" << endl;
            errorPos += r;
        }
    }

    // Correct error if exists
    if (errorPos) {
        cout << "Error detected at position: " <<  errorPos << endl;
        message[errorPos - 1] = message[errorPos - 1] == '1' ? '0' : '1';
        cout << "Corrected message: " << message << endl;
    }

    // Copy data bits
    string data(m, '0'); // length = m + n
    int d = m;
    for (int i = 1; i <= m + n; i++) {
        if (floor(log2(i)) == log2(i)) continue; // Skip over parity bits
        data[--d] = message[i - 1];
    }
    cout << "Received data: " << data << endl;
}

int main() {
    while (true) {
        cout << "===============\n"
            << "1. Encode Hamming code\n"
            << "2. Decode Hamming code\n"
            << "Enter choice: ";
        int choice; cin >> choice;
        if (choice != 1 && choice != 2) {
            cout << "Invalid option!" << endl;
            continue;
        }
        if (choice == 0) {
            return 0;
        }
        cout << "Enter data: ";
        string data; cin >> data;

        if (choice == 1) {
            string result = encodeHamming(data);
            cout << "Result: " << result << endl;
        } else {
            decodeHamming(data);
        }
    }
}
