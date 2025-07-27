#include <algorithm>
#include <array>
#include <cstring>
#include <iostream>
#include <climits>
#include <map>
#include <queue>
#include <vector>

using namespace std;

// 2 8 3 1 6 4 0 7 5
// 1 2 3 8 0 4 7 6 5

array<array<int, 3>, 3> goalValues;

struct Node{
    array<array<int, 3>, 3> values{};

    bool operator==(const Node& other) const {
        return equal(this->values.begin(), this->values.end(), other.values.begin());
    }

    bool operator<(const Node& other) const {
        return this->values < other.values;
    }

    [[nodiscard]] int heuristic() const {
        int h = 0;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (this->values[i][j] != goalValues[i][j]) {
                    h++;
                }
            }
        }
        return h;
    }
};

vector<Node> reconstruct_path(const map<Node, Node>& cameFrom, Node &current) {
    vector<Node> total_path;
    total_path.push_back(current);
    while (cameFrom.contains(current)) {
        current = cameFrom.at(current);
        total_path.push_back(current);
    }
    ranges::reverse(total_path);
    return total_path;
}

// Function to calculate neighboring nodes for the 8-puzzle
std::vector<Node> get_neighbors(const Node &node) {
    std::vector<Node> neighbors;
    int gapX = -1; // Row of the gap (0)
    int gapY = -1; // Column of the gap (0)

    // 1. Find the position of the gap (0)
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (node.values[i][j] == 0) {
                gapX = i;
                gapY = j;
                break; // Found the gap, no need to continue inner loop
            }
        }
        if (gapX != -1) break; // Found the gap, no need to continue outer loop
    }

    // Define possible moves: (delta_row, delta_col)
    // Up, Down, Left, Right
    int dr[] = {-1, 1, 0, 0};
    int dc[] = {0, 0, -1, 1};

    // 2. Iterate through possible moves
    for (int i = 0; i < 4; ++i) {
        int newGapX = gapX + dr[i];
        int newGapY = gapY + dc[i];

        // 3. Check if the new position is within the grid boundaries (0-2 for both dimensions)
        if (newGapX >= 0 && newGapX < 3 && newGapY >= 0 && newGapY < 3) {
            // Create a new node by copying the current node's state
            Node neighbor_node = node;

            // Swap the gap (0) with the tile at the new position
            std::swap(neighbor_node.values[gapX][gapY], neighbor_node.values[newGapX][newGapY]);

            // Add the new valid neighbor to the list
            neighbors.push_back(neighbor_node);
        }
    }

    return neighbors;
}

map<Node, int> f_score;

vector<Node> a_star(const Node &start, const Node &goal) {
    struct CompareNode {
        bool operator()(const Node& a, const Node& b) const {
            return f_score[a] > f_score[b];
        }
    };

    // The set of discovered nodes that may need to be (re-)expanded.
    // Initially, only the start node is known.
    // This is usually implemented as a min-heap or priority queue rather than a hash-set.
    priority_queue<Node, vector<Node>, CompareNode> open_set;
    open_set.push(start);

    // For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from the start
    // to n currently known.
    map<Node, Node> came_from;

    // For node n, gScore[n] is the currently known cost of the cheapest path from start to n.
    map<Node, int> g_score;
    g_score[start] = 0;

    // For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    // how cheap a path could be from start to finish if it goes through n.
    f_score.clear(); // map<Node, int> f_score;
    f_score[start] = start.heuristic();

    while (!open_set.empty()) {
        // This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
        auto current = open_set.top();
        if (current == goal)
            return reconstruct_path(came_from, current);

        open_set.pop();
        auto neighbors = get_neighbors(current);
        for (auto neighbor : neighbors) {
            // d(current,neighbor) is the weight of the edge from current to neighbor
            // tentative_gScore is the distance from start to the neighbor through current
            int current_g_score = g_score[current];
            int neighbor_g_score = g_score.contains(neighbor) ? g_score[neighbor] : INT_MAX;
            auto tentative_g_score = current_g_score + 1; // d(current, neighbor) = 1
            if (tentative_g_score < neighbor_g_score) {
                // This path to neighbor is better than any previous one. Record it!
                came_from[neighbor] = current;
                g_score[neighbor] = tentative_g_score;
                f_score[neighbor] = tentative_g_score + neighbor.heuristic();
                open_set.push(neighbor);
            }
        }
    }

    // Open set is empty but goal was never reached
    vector<Node> empty;
    return empty;
}

int main() {
    Node initialState{};
    cout << "Enter initial state:" << endl;
    for (auto & value : initialState.values) {
        for (int & j : value) {
            cin >> j;
        }
    }

    Node goalState{};
    cout << "Enter goal state:" << endl;
    for (auto & value : goalState.values) {
        for (int & j : value) {
            cin >> j;
        }
    }
    goalValues = goalState.values;

    int i = 0;
    const auto path = a_star(initialState, goalState);
    if (path.empty()) {
        cout << "No path found" << endl;
        return 0;
    }
    for (auto node : path) {
        // Log path
        cout << "Node " << i++ << ":" << endl;
        cout << node.values[0][0] << " " << node.values[0][1] << " " << node.values[0][2] << endl;
        cout << node.values[1][0] << " " << node.values[1][1] << " " << node.values[1][2] << endl;
        cout << node.values[2][0] << " " << node.values[2][1] << " " << node.values[2][2] << endl;
        cout << endl;
    }
}
