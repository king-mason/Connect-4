import numpy as np
import pygame
from utils import minimax
from board import Board
from button import Button

ROWS, COLS = (6, 7)
WIDTH, HEIGHT = (1000, 800)

COLOR_1 = 'cyan'
COLOR_2 = 'darkorchid'
COLOR_BG = 'white'
COLOR_BOARD = (255, 225, 0, 255)  # yellow
COLOR_MENU = 'yellow'
COLOR_TEXT = 'dark blue'
COLOR_BUTTON = (0, 0, 255, 255)  # blue
COLOR_BUTTON_HOVER = (100, 100, 100, 100)  # gray

LARGE_FONT = pygame.font.SysFont('Corbel', 100, bold=True)
MEDIUM_FONT = pygame.font.SysFont('Corbel', 50, bold=True)
SMALL_FONT = pygame.font.SysFont('Corbel', 30, bold=True)

PLAY_BUTTON = Button(text_input='START', pos=(WIDTH / 2, HEIGHT / 2),
                     font=LARGE_FONT, base_color=COLOR_BUTTON,
                     hover_color=COLOR_BUTTON_HOVER)
OPTIONS_BUTTON = Button(text_input='OPTIONS', pos=(WIDTH / 2, HEIGHT / 2 + 200),
                        font=MEDIUM_FONT, base_color=COLOR_BUTTON,
                        hover_color=COLOR_BUTTON_HOVER)
QUIT_BUTTON = Button(text_input='QUIT', pos=(WIDTH / 2, HEIGHT / 2 + 260),
                     font=MEDIUM_FONT, base_color=COLOR_BUTTON,
                     hover_color=COLOR_BUTTON_HOVER)

NUM_KEYS = range(48, 58)

MODE = 1  # 1: pvp, 2: pvc, 3: cvc

DROP_DELAY = 200
DELAY = DROP_DELAY * ROWS

winners = {1: 0, 2: 0}


class Connect4():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Connect 4')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.rows = ROWS
        self.cols = COLS
        self.board = Board(ROWS, COLS)
        self.draw_board()
        self.turn = 1
        self.piece_row = -1
        self.piece_col = -1
        self.falling = False
        self.delay_start = 0
        self.state = 'Menu'
        self.drop_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.drop_timer, DROP_DELAY)

    def main_loop(self):
        while True:
            self.move = 0
            self.handle_inputs()
            if self.state == 'Menu':
                self.main_menu()
            if self.state == 'Play':
                self.play()
            if self.state == 'Options':
                self.options()
            if self.state == 'Board Select':
                self.board_selector()
            if self.state == 'Difficulty Select':
                self.difficulty_selector()
            pygame.display.flip()

    def main_menu(self):
        self.screen.fill(COLOR_MENU)
        title_text = LARGE_FONT.render('CONNECT 4', True, COLOR_TEXT)
        title_text_rect = title_text.get_rect(center=(WIDTH/2, 150))
        self.screen.blit(title_text, title_text_rect)

        mouse_pos = pygame.mouse.get_pos()

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.check_hover(mouse_pos)
            button.update(self.screen)

    def options(self):
        self.handle_inputs()
        self.screen.fill(COLOR_MENU)
        # self.screen.blit(self.text, (100, 150))

        mouse_pos = pygame.mouse.get_pos()

    def board_selector(self):
        self.state = 'Board'
        while True:
            self.handle_inputs()
            self.screen.fill(COLOR_MENU)
            # self.screen.blit(self.text, (100, 150))

            mouse_pos = pygame.mouse.get_pos()

            pygame.display.flip()

    def difficulty_selector(self):
        self.state = 'Difficulty'
        while True:
            self.handle_inputs()
            self.screen.fill(COLOR_MENU)
            # self.screen.blit(self.text, (100, 150))

            mouse_pos = pygame.mouse.get_pos()

            pygame.display.flip()

    def play(self):
        self.draw_board()

        if MODE == 1:
            self.play_pvp()
        if MODE == 2:
            self.play_pvc()
        if MODE == 3:
            self.play_cvc()

    def play_pvp(self):
        if (0 <= self.piece_col < self.cols and 
            pygame.time.get_ticks() >= self.delay_start + DELAY):
            
            self.piece_row = 0
            success = self.player_turn(self.turn)
            # if not success:
            #     return
            self.draw_board()
            winner = self.board.check_win()
            if winner:
                pygame.time.wait(2000)
                self.board.reset_board()
                self.state = 'Menu'
                self.main_menu()
            if self.turn == 1:
                self.turn = 2
            else:
                self.turn = 1
            self.delay_start = pygame.time.get_ticks()

    def play_pvc(self):
        if self.turn == 1:
            if self.move:
                success = self.player_turn(1)
                if not success:
                    return
                self.draw_board()
                winner = self.board.check_win()
                if winner:
                    pygame.time.wait(2000)
                    self.board.reset_board()
                    self.draw_board()
                self.turn = 2
                self.delay_start = pygame.time.get_ticks()

        elif pygame.time.get_ticks() >= self.delay_start + DELAY:
            self.board, _ = minimax(self.board, 0, True, -np.inf, np.inf)
            self.draw_board()
            winner = self.board.check_win()
            if winner:
                pygame.time.wait(2000)
                self.board.reset_board()
                self.draw_board()
            self.turn = 1

    def play_cvc(self):
        if pygame.time.get_ticks() >= self.delay_start + DELAY:

            if self.turn == 1:
                self.board, _ = minimax(self.board, 0, False, -np.inf, np.inf)
                self.turn = 2
            else:
                self.board, _ = minimax(self.board, 0, True, -np.inf, np.inf)
                self.turn = 1

            self.draw_board()
            winner = self.board.check_win()
            if winner:
                pygame.time.wait(2000)
                self.board.reset_board()
                self.draw_board()
            self.delay_start = pygame.time.get_ticks()

    def handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(winners)
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print(winners)
                    self.state = 'Menu'
                if event.key in NUM_KEYS:
                    if pygame.time.get_ticks() >= self.delay_start + DELAY:
                        # Set column to key number
                        self.piece_col = event.key - 49
                if event.key == pygame.K_SPACE:
                    print(winners)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # holds (x, y) coordinates of mouse
                mouse_pos = pygame.mouse.get_pos()

                if self.state == 'Menu':
                    if PLAY_BUTTON.check_hover(mouse_pos):
                        self.state = 'Play'
                    if OPTIONS_BUTTON.check_hover(mouse_pos):
                        self.state = 'Options'
                    if QUIT_BUTTON.check_hover(mouse_pos):
                        quit()

                if self.state == 'Options':
                    pass

                if self.state == 'Play':
                    if pygame.time.get_ticks() >= self.delay_start + DELAY:
                        pass

            # Falling animation
            if event.type == self.drop_timer:

                if self.falling:

                    # Move piece
                    self.board.board[self.piece_row, self.piece_col] = self.turn
                    if self.piece_row != 0:
                        self.board.board[self.piece_row - 1, self.piece_col] = 0
                    self.piece_row += 1

                    # Check for bottom
                    if self.piece_row == self.rows:
                        self.falling = False
                        self.piece_col = -1
                    # Check for piece
                    elif self.board.board[self.piece_row, self.piece_col] != 0:
                        self.falling = False
                        self.piece_col = -1
                    

    def draw_board(self):
        self.screen.fill(COLOR_BOARD)

        for i in range(ROWS):
            for j in range(COLS):
                w, h = WIDTH / COLS, HEIGHT / ROWS
                # pygame.draw.rect(self.screen, 'blue', [w*j, h*i, w+1, h+1], 5)  # grid
                circle_rect = pygame.rect.Rect(w * j + 10, h * i + 10, w - 20, h - 20)  # circle parameters
                if self.board.board[i, j] == 1:
                    color = COLOR_1
                elif self.board.board[i, j] == 2:
                    color = COLOR_2
                else:
                    color = COLOR_BG
                pygame.draw.ellipse(self.screen, color, circle_rect)

        pygame.display.flip()

    def valid_move(self, row, col):
        if row < 1 or row > self.board.rows:
            return False
        if col < 1 or col > self.board.cols:
            return False
        if self.board.board[row - 1, col - 1] != 0:
            return False
        return True

    def player_turn(self, player_num):

        # Check if row is full
        if all(self.board.board[:, self.piece_col - 1]):
            return False

        # Fall down a space
        # every drop event (100 ms)
        self.falling = True
        
        # self.board.board[self.piece_row - 1, self.piece_col - 1] = player_num
        return True

    def computer_turn(self, player_num):
        col = self.move
        row = self.rows

        while not self.valid_move(row, col):
            row -= 1
            if row < 1:
                print('You cannot play in that column.')
                return False

        self.board.board[row - 1, col - 1] = player_num
        return True


if __name__ == '__main__':
    game = Connect4()
    game.main_loop()
