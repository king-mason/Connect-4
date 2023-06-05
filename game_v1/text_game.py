import numpy as np

rows, cols = (6, 7)

class Connect4:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        self.rows = rows
        self.cols = cols
        return np.array([[0 for i in range(cols)] for j in range(rows)])

    def main_loop(self):
        while True:
            self.player_turn(1)
            print(self.board)
            winner = self.find_winners()
            if winner:
                break

            self.player_turn(2)
            print(self.board)
            winner = self.find_winners()
            if winner:
                break
        
        print(f'Player {winner} wins!')

    def valid_move(self, row, col):
        if row < 1 or row > self.rows:
            return False
        if col < 1 or col > self.cols:
            return False
        if self.board[row - 1, col - 1] != 0:
            return False
        return True
    
    def player_turn(self, id):
        print('Player', id)

        col = int(input('Which column would you like to play? '))
        row = self.rows

        while not self.valid_move(row, col):
            row -= 1
            if row < 1:
                print('You cannot play in that column.')
                col = int(input('Please pick another: '))
                row = self.rows
        
        self.board[row - 1, col - 1] = id
        return row, col
    
    def find_winners(self):
        for i in range(self.rows):
            for j in range(self.cols):

                # check across
                if j < self.cols - 3:
                    horizontal = self.board[i, j:j+4]

                # check down
                if i < self.rows - 3:
                    vertical = self.board[i:i+4, j]

                # check diagonals
                if j < self.cols - 3 and i < self.rows - 3:
                    ascending = np.array([self.board[i+3-k, j+k] for k in range(4)])
                    descending = np.array([self.board[i+k, j+k] for k in range(4)])
        
                if (all(horizontal == 1) or all(vertical == 1) or
                    all(ascending == 1) or all(descending == 1)):
                    return 1
                
                if (all(horizontal == 2) or all(vertical == 2) or
                    all(ascending == 2) or all(descending == 2)):
                    return 2

        return 0


game = Connect4()
game.main_loop()

