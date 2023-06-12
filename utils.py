import numpy as np
import time
from board import Board
import random

MAX_DEPTH = 4
MAX_TT_ITEMS = 2000
turn = 2
counter = 0
step = 0

# transposition table
tt = dict()
queue = list()


# class TranspositionTable:
#     def __init__(self):
#         self.table = dict()
#         self.queue = list()


def valid_move(board: Board, row: int, col: int):
    rows = board.rows
    cols = board.cols

    if row < 1 or row > rows:
        return False
    if col < 1 or col > cols:
        return False
    if board.board[row - 1, col - 1] != 0:
        return False
    if row < rows:
        if board.board[row, col - 1] == 0:
            return False
    return True


def moves(board: Board):
    possible_moves = []
    for col in range(1, board.cols + 1):
        # start at bottom row
        row = board.rows
        while not valid_move(board, row, col):
            row -= 1
            if row < 1:
                break
        if valid_move(board, row, col):
            new_board = board.copy()
            new_board.board[row - 1, col - 1] = turn
            possible_moves.append(new_board)
    return possible_moves


def minimax(board: Board, depth: int, max_player: bool, alpha: float, beta: float):
    global turn
    global counter
    global step
    counter += 1
    empty_spaces = (board.board == 0).sum()

    if depth == 1:
        step += 1
        print(f'{step}/7')
        if step == 7:
            step = 0

    if empty_spaces == 0 or depth == MAX_DEPTH or board.check_win():
        return None, calc_score(board)

    if max_player:
        turn = 2
        move_possibilities = moves(board)
        random.shuffle(move_possibilities)  # randomize move order
        move_possibilities.sort(key=lambda x: x.search_board(turn, 4, 0))  # prioritize wins
        max_score = -np.inf
        max_score_move = None

        for move in move_possibilities:
            # check if move already has been evaluated
            id = move.get_id()
            score = tt.get(id, None)
            if score is None:
                score = minimax(move, depth + 1, False, alpha, beta)[1]
            if score > max_score:
                max_score_move = move
                max_score = score
            alpha = max(alpha, max_score)
            if alpha >= beta:
                break

        if depth > 2:
            id = max_score_move.get_id()
            if depth > 3 or max_score < alpha:
                if tt.get(id, None) is not None:
                    if id in queue:
                        queue.remove(id)
                queue.append(id)
            tt[id] = max_score
            if len(tt) > MAX_TT_ITEMS:
                if len(queue) == 0:
                    queue.append(random.choice(list(tt.keys())))
                del tt[queue.pop(0)]

        return max_score_move, max_score

    else:  # Minimizing player
        turn = 1
        move_possibilities = moves(board)
        random.shuffle(move_possibilities)  # randomize move order
        move_possibilities.sort(key=lambda x: x.search_board(turn, 4, 0))  # prioritize wins
        min_score = np.inf
        min_score_move = None

        for move in move_possibilities:
            id = move.get_id()
            score = tt.get(id, None)
            if score is None:
                score = minimax(move, depth + 1, True, alpha, beta)[1]
            if score < min_score:
                min_score_move = move
                min_score = score
            beta = min(beta, min_score)
            if alpha >= beta:
                break

        if depth > 2:
            id = min_score_move.get_id()
            if depth > 3 or min_score > beta:
                if tt.get(id, None) is not None:
                    if id in queue:
                        # reset spot in queue
                        queue.remove(id)
                queue.append(id)
            tt[id] = min_score
            if len(tt) > MAX_TT_ITEMS:
                if len(queue) == 0:
                    queue.append(random.choice(list(tt.keys())))
                del tt[queue.pop(0)]

        return min_score_move, min_score


def negamax(board: Board, depth: int, max_player: bool):
    global turn
    if max_player:
        turn = 2
    else:
        turn = 1
    empty_spaces = (board.board == 0).sum()

    if empty_spaces == 0 or depth == 0 or board.check_win():
        if max_player:
            return None, calc_score(board)
        else:
            return None, calc_score(board) * -1

    max_score = -np.inf
    max_score_move = None

    for move in moves(board):
        (new_board, score) = negamax(move, depth - 1, not max_player)
        if new_board is None:
            new_board = board
        print(score)
        # score = calc_score(new_board)
        # print(new_board, score)
        if score > max_score:
            max_score_move = move
            max_score = score

    return max_score_move, -max_score


# ASSUMES COMPUTER IS ALWAYS PLAYER 2
def calc_score(board: Board):
    score = 0

    # computer
    wins = board.search_board(2, 4, 0)
    score += wins * 1000

    threes = board.search_board(2, 4, 1)
    score += threes * 15

    twos = board.search_board(2, 4, 2)
    score += twos * 8

    # opponent
    wins = board.search_board(1, 4, 0)
    score -= wins * 1000

    threes = board.search_board(1, 4, 1)
    score -= threes * 10

    twos = board.search_board(1, 4, 2)
    score -= twos * 5

    # bonus points for center pieces
    center_pieces = board.board[:, board.cols // 2]
    score += list(center_pieces).count(2)

    # check possible wins
    comp_possible_wins = 0
    opp_possible_wins = 0
    for i in range(4):
        comp_possible_wins += board.search_board(2, 4, i + 1)
        opp_possible_wins += board.search_board(1, 4, i + 1)
    score += comp_possible_wins - opp_possible_wins

    return score


def main():
    rows, cols = (6, 7)
    my_board = Board(rows, cols)

    test_id = '000000000000000000000000000000000002011000'
    my_board.set_board(test_id)

    print()
    print('board:')
    my_board.print_board()
    # print(calc_score(arr))
    time.sleep(3)
    print()
    print('best move:')
    move, score = minimax(my_board, 0, True, -np.inf, np.inf)
    # move, score = negamax(my_board, MAX_DEPTH, True)
    move.print_board()
    print(score)


if __name__ == '__main__':
    main()
    print(counter)
