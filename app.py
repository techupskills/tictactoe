from flask import Flask, render_template, request, jsonify
from tictactoe import print_board, check_win, check_draw, get_computer_move

app = Flask(__name__)

board = [[" " for _ in range(3)] for _ in range(3)]
current_player = "X"
play_against_computer = False

@app.route('/')
def index():
    return render_template('index.html', board=board, current_player=current_player)

@app.route('/move', methods=['POST'])
def move():
    global current_player
    row = int(request.form['row'])
    col = int(request.form['col'])

    if board[row][col] != " ":
        return jsonify({'error': 'Invalid move. The cell is already occupied.'})

    board[row][col] = current_player

    if check_win(board, current_player):
        return jsonify({'winner': current_player})

    if check_draw(board):
        return jsonify({'draw': True})

    current_player = "O" if current_player == "X" else "X"

    if play_against_computer and current_player == "O":
        row, col = get_computer_move(board)
        board[row][col] = current_player

        if check_win(board, current_player):
            return jsonify({'winner': current_player})

        if check_draw(board):
            return jsonify({'draw': True})

        current_player = "X"

    return jsonify({'board': board, 'current_player': current_player})

@app.route('/set_mode', methods=['POST'])
def set_mode():
    global play_against_computer
    play_against_computer = request.form['mode'] == 'computer'
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
