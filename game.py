import numpy as np
import pygame
import random as rand
from utils import minimax


ROWS, COLS = (6, 7)
WIDTH, HEIGHT = (1000, 800)

COLOR_1 = 'blue'
COLOR_2 = 'red'
COLOR_BG = 'white'

NUM_KEYS = range(48, 58)

MODE = 3  # 1: pvp, 2: pvc, 3: cvc

DELAY = 100

winners = {1: 0, 2: 0}


class Connect4:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Connect 4')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.create_board()
        self.draw_board()
        self.turn = 1
        self.delay_start = 0

    def create_board(self):
        self.rows = ROWS
        self.cols = COLS
        self.board = np.array([[0 for i in range(COLS)] for j in range(ROWS)])

    def main_loop(self):
        while True:

            self.move = 0
            self.handle_inputs()

            if MODE == 1:

                if self.move:
                    success = self.player_turn(self.turn)
                    if not success:
                        continue
                    self.draw_board()
                    winner = self.find_winners()
                    if winner:
                        break
                    if self.turn == 1:
                        self.turn = 2
                    else:
                        self.turn = 1
            
            if MODE == 2:

                if self.turn == 1:
                    if self.move:
                        success = self.player_turn(1)
                        if not success:
                            continue
                        self.draw_board()
                        winner = self.find_winners()
                        if winner:
                            pygame.time.wait(2000)
                            self.create_board()
                            self.draw_board()
                        self.turn = 2
                        self.delay_start = pygame.time.get_ticks()

                elif pygame.time.get_ticks() >= self.delay_start + DELAY:
                    self.board = minimax(self.board)
                    self.draw_board()
                    winner = self.find_winners()
                    if winner:
                        pygame.time.wait(2000)
                        self.create_board()
                        self.draw_board()
                    self.turn = 1

            
            if MODE == 3:
                
                if pygame.time.get_ticks() >= self.delay_start + DELAY:
                    
                    if self.turn == 1:
                        self.move = rand.randint(1, COLS)
                        success = self.player_turn(1)
                        if not success:
                            continue
                        self.turn = 2
                    else:
                        self.board = minimax(self.board)
                        self.turn = 1
                    
                    self.draw_board()
                    winner = self.find_winners()
                    if winner:
                        pygame.time.wait(2000)
                        self.create_board()
                    self.delay_start = pygame.time.get_ticks()

        
        print(f'Player {winner} wins!')
        while True:
            self.handle_inputs()

    def handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(winners)
                quit()

            if event.type == pygame.KEYDOWN:
                # print(event.key)
                if event.key in NUM_KEYS:
                    # print(event.key - 48)
                    self.move = event.key - 48
                if event.key == pygame.K_SPACE:
                    print(winners)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

    def draw_board(self):
        self.screen.fill((255, 225, 0, 255))  # yellow

        for i in range(ROWS):
            for j in range(COLS):
                w, h = WIDTH / COLS, HEIGHT / ROWS
                # pygame.draw.rect(self.screen, 'blue', [w*j, h*i, w+1, h+1], 5)  # grid
                circle_rect = pygame.rect.Rect(w*j+10, h*i+10, w-20, h-20)  # circle parameters
                if self.board[i, j] == 1:
                    color = COLOR_1
                elif self.board[i, j] == 2:
                    color = COLOR_2
                else:
                    color = COLOR_BG
                pygame.draw.ellipse(self.screen, color, circle_rect)

        pygame.display.flip()

    def valid_move(self, row, col):
        if row < 1 or row > self.rows:
            return False
        if col < 1 or col > self.cols:
            return False
        if self.board[row - 1, col - 1] != 0:
            return False
        return True
    
    def player_turn(self, player_num):
        
        col = self.move
        row = self.rows

        while not self.valid_move(row, col):
            row -= 1
            if row < 1:
                # print('You cannot play in that column.')
                return False
        
        self.board[row - 1, col - 1] = player_num
        return True
    
    def computer_turn(self, player_num):
        col = self.move
        row = self.rows

        while not self.valid_move(row, col):
            row -= 1
            if row < 1:
                print('You cannot play in that column.')
                return False
        
        self.board[row - 1, col - 1] = player_num
        return True

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
                    winners[1] += 1
                    return 1

                
                if (all(horizontal == 2) or all(vertical == 2) or
                    all(ascending == 2) or all(descending == 2)):
                    winners[2] += 1
                    return 2

        return 0


if __name__ == '__main__':
    game = Connect4()
    game.main_loop()

