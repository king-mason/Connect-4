import numpy as np
import time

MAX_DEPTH = 3
turn = 2


def valid_move(board, row, col):
    rows = len(board)
    cols = len(board[0])
    
    if row < 1 or row > rows:
        return False
    if col < 1 or col > cols:
        return False
    if board[row - 1, col - 1] != 0:
        return False
    if row < rows:
        if board[row, col - 1] == 0:
            return False
    return True


def moves(board):
    children = []
    for col in range(1, len(board[0]) + 1):
        row = len(board)
        while not valid_move(board, row, col):
            row -= 1
            if row < 1:
                break
        if valid_move(board, row, col):
            new_board = board.copy()
            new_board[row - 1, col - 1] = turn
            children.append(new_board)
    # print(children)
    return children
        

def maximize(board, depth):
    # print('maximizing')
    global turn
    turn = 2
    empty_spaces = len(board[board == 0])

    if empty_spaces == 0 or depth == MAX_DEPTH:
        # print(board)
        # print(calc_score(board))
        return None, calc_score(board)
    
    max_score = -np.inf
    max_score_move = None

    for move in moves(board):
        (new_board, _) = minimize(move, depth + 1)
        if new_board is None:
            new_board = board
        score = calc_score(new_board)
        if score > max_score:
            max_score_move = move
            max_score = score

    return max_score_move, max_score


def minimize(board, depth):
    # print('minimizing')
    global turn
    turn = 1
    empty_spaces = len(board[board == 0])

    if empty_spaces == 0 or depth == MAX_DEPTH:
        # print(board)
        # print(calc_score(board))
        return None, calc_score(board)
    
    min_score = np.inf
    min_score_move = None

    for move in moves(board):
        (new_board, _) = maximize(move, depth + 1)
        if new_board is None:
            new_board = board
        score = calc_score(new_board)
        if score < min_score:
            min_score_move = move
            min_score = score

    return min_score_move, min_score


# ASSUMES COMPUTER IS ALWAYS PLAYER 2
def calc_score(board):

    score = 0

    rows = len(board)
    cols = len(board[0])

    for i in range(rows):
        for j in range(cols):

            # check across
            if j < cols - 3:
                horizontal = board[i, j:j+4]

            # check down
            if i < rows - 3:
                vertical = board[i:i+4, j]

            # check diagonals
            if j < cols - 3 and i < rows - 3:
                ascending = np.array([board[i+3-k, j+k] for k in range(4)])
                descending = np.array([board[i+k, j+k] for k in range(4)])
    

            if (all(horizontal == 1) or all(vertical == 1) or
                all(ascending == 1) or all(descending == 1)):
                return -10
            
            if (all(horizontal == 2) or all(vertical == 2) or
                all(ascending == 2) or all(descending == 2)):
                return 10
            
    for i in range(rows):
        for j in range(cols):

            # check across
            if j < cols - 3:
                horizontal = board[i, j:j+4]

            # check down
            if i < rows - 3:
                vertical = board[i:i+4, j]

            # check diagonals
            if j < cols - 3 and i < rows - 3:
                ascending = np.array([board[i+3-k, j+k] for k in range(4)])
                descending = np.array([board[i+k, j+k] for k in range(4)])

            # print(horizontal)
            # print(vertical)
            # print(ascending)
            # print(descending)
    

            if (all(horizontal[:3] == 1) and horizontal[3] == 0):
                score -= 2
            if (all(vertical[:3] == 1) and vertical[3] == 0):
                score -= 2
            if (all(ascending[:3] == 1) and ascending[3] == 0):
                score -= 2
            if (all(descending[:3] == 1) and descending[3] == 0):
                score -= 2
            
            if (all(horizontal[:3] == 2) and horizontal[3] == 0):
                score += 2
            if (all(vertical[:3] == 2) and vertical[3] == 0):
                score += 2
            if (all(ascending[:3] == 2) and ascending[3] == 0):
                score += 2
            if (all(descending[:3] == 2) and descending[3] == 0):
                score += 2

            if (all(horizontal[1:4] == 1) and horizontal[0] == 0):
                score -= 2
            if (all(vertical[1:4] == 1) and vertical[0] == 0):
                score -= 2
            if (all(ascending[1:4] == 1) and ascending[0] == 0):
                score -= 2
            if (all(descending[1:4] == 1) and descending[0] == 0):
                score -= 2
            
            if (all(horizontal[1:4] == 2) and horizontal[0] == 0):
                score += 2
            if (all(vertical[1:4] == 2) and vertical[0] == 0):
                score += 2
            if (all(ascending[1:4] == 2) and ascending[0] == 0):
                score += 2
            if (all(descending[1:4] == 2) and descending[0] == 0):
                score += 2

    return score
            


def minimax(board):
    move, score = maximize(board, 0)

    print(move, score)

    return move


if __name__ == '__main__':
    rows, cols = (6, 7)
    arr = [[0 for _ in range(cols)] for _ in range(rows)]
    arr = np.array(arr)
    # arr[-1, ::2] = 1
    # arr[-1, 1::2] = 2
    # arr[-2, ::2] = 1
    # arr[-2, 1::2] = 2

    # arr[-3, 1] = 2


    arr[-1, 1] = 1

    print()
    print('board:')
    print(arr)
    # print(calc_score(arr))
    time.sleep(3)
    print()
    print('best move:')
    minimax(arr)


