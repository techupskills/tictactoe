import os
import random

def print_board(board):
    os.system('clear')
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_win(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    return [player, player, player] in win_conditions

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def get_move(player):
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-9): ")) - 1
            if move < 0 or move > 8:
                raise ValueError
            return move
        except ValueError:
            print("Invalid move. Please enter a number between 1 and 9.")

def get_computer_move(board):
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(available_moves)

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    play_against_computer = input("Do you want to play against the computer? (y/n): ").lower() == 'y'

    while True:
        print_board(board)
        if current_player == "X" or not play_against_computer:
            move = get_move(current_player)
            row, col = divmod(move, 3)
        else:
            row, col = get_computer_move(board)

        if board[row][col] != " ":
            print("Invalid move. The cell is already occupied. Try again.")
            continue

        board[row][col] = current_player

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()
