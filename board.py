import numpy as np


class Board:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.board = self.create_empty_board()

    def create_empty_board(self):
        return np.array([[0 for _ in range(self.cols)] for _ in range(self.rows)])

    def print_board(self):
        print('+' + '—' * (self.cols * 2 + 1) + '+')
        for row in self.board:
            print('|', end=' ')
            row_str = [str(x) for x in row]
            print(' '.join(row_str), end=' ')
            print('|')
        print('+' + '—' * (self.cols * 2 + 1) + '+')

    def search_board(self, player_num: int, length: int, blank_spaces: int):
        '''Generalized search method that will count and return all of the rows, columns, and diagonals
           that contain only the given player number and the exact amount of blank spaces.'''

        def valid_section(section):
            count = (section == player_num).sum()
            zeros = (section == 0).sum()
            if (count == length - blank_spaces and zeros == blank_spaces):
                return True

        total = 0

        for i in range(self.rows):
            for j in range(self.cols):

                # check across
                if j < self.cols - (length - 1):
                    horizontal = self.board[i, j:j+length]
                    if valid_section(horizontal):
                        total += 1
                    
                # check down
                if i < self.rows - (length - 1):
                    vertical = self.board[i:i+length, j]
                    if valid_section(vertical):
                        total += 1

                # check diagonals
                if j < self.cols - (length - 1) and i < self.rows - (length - 1):

                    # check positive sloped diagonals
                    ascending = np.array([self.board[i+(length-1)-k, j+k] for k in range(length)])
                    if valid_section(ascending):
                        total += 1

                    # check negative sloped diagonals
                    descending = np.array([self.board[i+k, j+k] for k in range(length)])
                    if valid_section(descending):
                        total += 1
                    
        return total
    
    def check_win(self):

        if self.search_board(1, 4, 0) > 0:
            return 1
        
        if self.search_board(2, 4, 0) > 0:
            return 2

        return 0

    def get_id(self):
        id = ''
        for row in self.board:
            row = [str(x) for x in row]
            id += ''.join(row)
        return id
    
    def set_board(self, id):
        arr = []
        for i in range(self.rows):
            row = id[self.cols * i:self.cols * (i + 1)]
            row = [int(x) for x in list(row)]
            arr.append(row)
        self.board = np.array(arr)

    def copy(self):
        id = self.get_id()
        new_board = Board(self.rows, self.cols)
        new_board.set_board(id)
        return new_board

    def reset_board(self):
        self.board = self.create_empty_board()

    def __str__(self):
        return str(self.board)


def main():
    board = Board(5, 5)
    board.board[0, 0] = 1
    board.board[1, 1] = 1
    board.board[0, 1] = 2
    board.board[-1, :4] = 1

    board.print_board()

    print(board.search_board(1, 4, 0))
    print('id:', board.get_id())

    print()
    sample_id = '01020' * 5
    print('sample id:', sample_id)
    board.set_board(sample_id)
    board.print_board()

    print(board.create_empty_board())
    board.print_board()
    print(board)


if __name__ == '__main__':
    main()

