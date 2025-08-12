"""AIESL Assignment 3: Tic-Tac-Toe Minimax"""


def evaluate(board):
    # Check rows for X/O victory
    for row in range(0, 3):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            if board[row][0] == 'x':
                return +10
            elif board[row][0] == 'o':
                return -10
    # Check columns for X/O victory
    for col in range(0, 3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            if board[0][col] == 'x':
                return +10
            elif board[0][col] == 'o':
                return -10
    # Check diagonals for X/O victory
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == 'x':
            return +10
        elif board[0][0] == 'o':
            return -10
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] == 'x':
            return +10
        elif board[0][2] == 'o':
            return -10
    return 0


def is_board_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True


def get_next_moves(board, is_maximiser):
    next_moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                new_board = [r.copy() for r in board]
                new_board[row][col] = 'x' if is_maximiser else 'o'
                next_moves.append(new_board)
    return next_moves


def minimax(board, depth, is_maximiser):
    board_value = evaluate(board)
    if board_value == 10 or board_value == -10 or is_board_full(board):
        return board_value

    best_val = float('-inf') if is_maximiser else float('inf')
    best_move = None
    for board in get_next_moves(board, is_maximiser):
        board_value = minimax(board, depth + 1, not is_maximiser)
        if is_maximiser and board_value > best_val:
            best_val = board_value
            best_move = board
        elif not is_maximiser and board_value < best_val:
            best_val = board_value
            best_move = board
    return best_val if depth > 0 else best_move


def print_board(board):
    for row in board:
        print("|".join(row))


def main():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    board = minimax(board, 0, True)  # Start as X (maximiser)
    while not is_board_full(board) and evaluate(board) == 0:
        print_board(board)
        row = int(input("Enter row (1-3): ")) - 1
        col = int(input("Enter column (1-3): ")) - 1
        if board[row][col] == ' ':
            board[row][col] = 'o'
        else:
            print("Invalid move, try again.")
            continue
        board = minimax(board, 0, True)

    if evaluate(board) == 10:
        print("X wins!")
    elif evaluate(board) == -10:
        print("O wins!")
    else:
        print("It's a draw!")
    print_board(board)


if __name__ == "__main__":
    main()
