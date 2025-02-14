from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tictactoe import print_board, check_win, check_draw, get_computer_move

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

board = [[" " for _ in range(3)] for _ in range(3)]
current_player = "X"
play_against_computer = False

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "board": board, "current_player": current_player})

@app.post("/move")
async def move(request: Request):
    global current_player
    form = await request.form()
    row = int(form['row'])
    col = int(form['col'])

    if board[row][col] != " ":
        return JSONResponse({'error': 'Invalid move. The cell is already occupied.'})

    board[row][col] = current_player

    if check_win(board, current_player):
        return JSONResponse({'winner': current_player})

    if check_draw(board):
        return JSONResponse({'draw': True})

    current_player = "O" if current_player == "X" else "X"

    if play_against_computer and current_player == "O":
        row, col = get_computer_move(board)
        board[row][col] = current_player

        if check_win(board, current_player):
            return JSONResponse({'winner': current_player})

        if check_draw(board):
            return JSONResponse({'draw': True})

        current_player = "X"

    return JSONResponse({'board': board, 'current_player': current_player})

@app.post("/set_mode")
async def set_mode(request: Request):
    global play_against_computer
    form = await request.form()
    play_against_computer = form['mode'] == 'computer'
    return JSONResponse({'success': True})
