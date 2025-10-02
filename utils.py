import numpy as np
import time
from board import Board
import random
import pygame

pygame.init()

MAX_DEPTH = 4  # default
MAX_TT_ITEMS = 100_000
turn = 2
counter = 0
step = 0

# transposition table
tt = dict()
queue = list()


def handle_inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()


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


def minimax(board: Board, depth: int, max_player: bool, alpha: float, beta: float, max_depth: int = MAX_DEPTH):
    global turn
    global counter
    global step
    counter += 1
    empty_spaces = (board.board == 0).sum()

    handle_inputs()

    if depth == 1:
        step += 1
        print(f'{step}/7')
        if step == 7:
            step = 0

    if empty_spaces == 0 or depth == max_depth or board.check_win():
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
            id_ = move.get_id()
            score = tt.get(id_, None)
            if score is None:
                score = minimax(move, depth + 1, False, alpha, beta, max_depth)[1]
                if not score:
                    continue
            if score > 5_000:
                return move, score
            if score > max_score:
                max_score_move = move
                max_score = score
            alpha = max(alpha, max_score)
            if alpha >= beta:
                break

        if not max_score_move:
            return -np.inf, None

        if depth > 2:
            id_ = max_score_move.get_id()
            if depth > 3 or max_score < alpha:
                if tt.get(id_, None) is not None:
                    if id_ in queue:
                        queue.remove(id_)
                queue.append(id_)
            tt[id_] = max_score
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
            id_ = move.get_id()
            score = tt.get(id_, None)
            if score is None:
                score = minimax(move, depth + 1, True, alpha, beta, max_depth)[1]
            if not score:
                continue
            if score < -5000:
                return move, score
            if score < min_score:
                min_score_move = move
                min_score = score
            beta = min(beta, min_score)
            if alpha >= beta:
                break

        if not min_score_move:
            return np.inf, None

        if depth > 2:
            id_ = min_score_move.get_id()
            if depth > 3 or min_score > beta:
                if tt.get(id_, None) is not None:
                    if id_ in queue:
                        # reset spot in queue
                        queue.remove(id_)
                queue.append(id_)
            tt[id_] = min_score
            if len(tt) > MAX_TT_ITEMS:
                if len(queue) > 0:
                    del tt[queue.pop(0)]
                else:
                    del tt[random.choice(list(tt.keys()))]

        return min_score_move, min_score


# Note: Calculates score in terms of player 2
def calc_score(board: Board):
    score = 0

    # computer
    wins = len(board.search_board(2, 4, 0))
    score += wins * 10000

    threes = len(board.search_board(2, 4, 1))
    score += threes * 15

    twos = len(board.search_board(2, 4, 2))
    score += twos * 8

    # opponent
    wins = len(board.search_board(1, 4, 0))
    score -= wins * 10000

    threes = len(board.search_board(1, 4, 1))
    score -= threes * 10

    twos = len(board.search_board(1, 4, 2))
    score -= twos * 5

    # bonus points for pieces in the center
    center_pieces = board.board[:, board.cols // 2]
    score += list(center_pieces).count(2)

    # check possible wins
    comp_possible_wins = 0
    opp_possible_wins = 0
    for i in range(4):
        comp_possible_wins += len(board.search_board(2, 4, i + 1))
        opp_possible_wins += len(board.search_board(1, 4, i + 1))
    score += comp_possible_wins - opp_possible_wins

    return score


def main():
    rows, cols = (6, 7)
    my_board = Board(rows, cols)

    test_id = '000000000000000000000002100010120002211200'
    my_board.set_board(test_id)

    print()
    print('Current Board:')
    my_board.print_board()
    print(calc_score(my_board))
    time.sleep(3)
    print()
    print('Best move:')
    move, score = minimax(my_board, 0, True, -np.inf, np.inf)
    diff = my_board.board - move.board
    for col in range(my_board.cols):
        if any(diff[:, col]):
            print('Playing in column', col + 1)
    move.print_board()
    print('Score:', score)
    print(f'Called minimax {counter} times')


if __name__ == '__main__':
    main()
