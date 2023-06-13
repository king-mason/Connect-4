import numpy as np
import pygame
from utils import minimax
from board import Board
from button import Button

ROWS, COLS = (6, 7)
WIDTH, HEIGHT = (1000, 800)
COL_WIDTH = WIDTH / COLS

COLOR_1 = 'cyan'
COLOR_2 = 'darkorchid'
COLOR_BG = 'white'
COLOR_BOARD = (255, 225, 0, 255)  # yellow
COLOR_MENU = 'yellow'
COLOR_TEXT = 'dark blue'
COLOR_BUTTON = (0, 0, 255, 255)  # blue
COLOR_BUTTON_HOVER = (100, 100, 100, 100)  # gray

FONT_LARGE = pygame.font.SysFont('Corbel', 100, bold=True)
FONT_MEDIUM = pygame.font.SysFont('Corbel', 50, bold=True)
FONT_SMALL = pygame.font.SysFont('Corbel', 30, bold=True)

BUTTON_PLAY = Button(text_input='START', pos=(WIDTH / 2, HEIGHT / 2),
                     font=FONT_LARGE, base_color=COLOR_BUTTON,
                     hover_color=COLOR_BUTTON_HOVER)
BUTTON_OPTIONS = Button(text_input='OPTIONS', pos=(WIDTH / 2, HEIGHT / 2 + 200),
                        font=FONT_MEDIUM, base_color=COLOR_BUTTON,
                        hover_color=COLOR_BUTTON_HOVER)
BUTTON_QUIT = Button(text_input='QUIT', pos=(WIDTH / 2, HEIGHT / 2 + 260),
                     font=FONT_MEDIUM, base_color=COLOR_BUTTON,
                     hover_color=COLOR_BUTTON_HOVER)
BUTTON_MODE = None
BUTTON_DIFFICULTY = None
BUTTON_BOARD = None


NUM_KEYS = range(48, 58)

MODE = 1  # 1: pvp, 2: pvc, 3: cvc

DROP_DELAY = 100
DELAY = DROP_DELAY * ROWS

winners = {1: 0, 2: 0}


class Connect4:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Connect 4')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.mouse_pos = pygame.mouse.get_pos()
        self.rows = ROWS
        self.cols = COLS
        self.game_board = Board(ROWS, COLS)
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
            self.mouse_pos = pygame.mouse.get_pos()
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
        title_text = FONT_LARGE.render('CONNECT 4', True, COLOR_TEXT)
        title_text_rect = title_text.get_rect(center=(WIDTH / 2, 150))
        self.screen.blit(title_text, title_text_rect)

        for button in [BUTTON_PLAY, BUTTON_OPTIONS, BUTTON_QUIT]:
            button.check_hover(self.mouse_pos)
            button.update(self.screen)

    def options(self):
        self.screen.fill(COLOR_MENU)
        for button in []:
            button.check_hover(self.mouse_pos)
            button.update(self.screen)

    def board_selector(self):
        for button in []:
            button.check_hover(self.mouse_pos)
            button.update(self.screen)
        self.screen.fill(COLOR_MENU)

    def difficulty_selector(self):
        self.screen.fill(COLOR_MENU)

    def play(self):
        self.draw_board()
        if pygame.time.get_ticks() >= self.delay_start + DELAY and not self.falling:
            if MODE == 1:
                self.player_vs_player()
            if MODE == 2:
                self.player_vs_computer()
            if MODE == 3:
                self.computer_vs_computer()

    def player_vs_player(self):
        # Highlight column
        if 0 <= self.piece_col < self.cols:
            # Check if row is full first
            # If so, they get to re-pick move
            if all(self.game_board.board[:, self.piece_col - 1]):
                return
            # Otherwise drop piece
            self.piece_row = 0
            self.falling = True
            # Start delay between turns
            self.delay_start = pygame.time.get_ticks()

    def player_vs_computer(self):
        if self.turn == 1:
            if 0 <= self.piece_col < self.cols:
                if all(self.game_board.board[:, self.piece_col - 1]):
                    return
                self.piece_row = 0
                self.falling = True
                winner = self.game_board.check_win()
                if winner:
                    pygame.time.wait(2000)
                    self.game_board.reset_board()
                self.delay_start = pygame.time.get_ticks()

        else:
            new_board, _ = minimax(self.game_board, 0, True, -np.inf, np.inf)
            diff = new_board.board - self.game_board.board
            for col in range(COLS):
                if any(diff[:, col]):
                    self.piece_col = col
            self.piece_row = 0
            self.falling = True
            self.delay_start = pygame.time.get_ticks()

    def computer_vs_computer(self):
        if pygame.time.get_ticks() >= self.delay_start + DELAY:
            if self.turn == 1:
                new_board, _ = minimax(self.game_board, 0, False, -np.inf, np.inf)
            else:
                new_board, _ = minimax(self.game_board, 0, True, -np.inf, np.inf)
            diff = new_board.board - self.game_board.board
            for col in range(COLS):
                if any(diff[:, col]):
                    self.piece_col = col
            self.piece_row = 0
            self.falling = True
            self.delay_start = pygame.time.get_ticks()

    def reset(self):
        self.turn = 1
        self.piece_row = -1
        self.piece_col = -1
        self.falling = False
        self.delay_start = 0
        self.game_board.reset_board()
        self.draw_board()

    def draw_board(self):
        self.screen.fill(COLOR_BOARD)

        for i in range(ROWS):
            for j in range(COLS):
                w, h = WIDTH // COLS, HEIGHT // ROWS
                # pygame.draw.rect(self.screen, 'blue', [w*j, h*i, w+1, h+1], 5)  # grid
                circle_rect = pygame.rect.Rect(w * j + 10, h * i + 10, w - 20, h - 20)  # circle parameters
                if self.game_board.board[i, j] == 1:
                    color = COLOR_1
                elif self.game_board.board[i, j] == 2:
                    color = COLOR_2
                else:
                    color = COLOR_BG
                pygame.draw.ellipse(self.screen, color, circle_rect)

    def handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(winners)
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print(winners)
                    self.state = 'Menu'
                    self.reset()
                if event.key in NUM_KEYS:
                    if pygame.time.get_ticks() >= self.delay_start + DELAY:
                        # Set column to key number
                        self.piece_col = event.key - 49
                if event.key == pygame.K_SPACE:
                    print(winners)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == 'Menu':
                    if BUTTON_PLAY.check_hover(self.mouse_pos):
                        self.delay_start = pygame.time.get_ticks()
                        self.state = 'Play'
                        self.draw_board()
                    if BUTTON_OPTIONS.check_hover(self.mouse_pos):
                        self.state = 'Options'
                    if BUTTON_QUIT.check_hover(self.mouse_pos):
                        quit()

                if self.state == 'Options':
                    pass

                if self.state == 'Play':
                    if pygame.time.get_ticks() >= self.delay_start + DELAY and not self.falling:
                        self.piece_col = int(self.mouse_pos[0] // COL_WIDTH)

            # Falling animation
            if event.type == self.drop_timer:

                if self.falling:

                    # Move piece
                    self.game_board.board[self.piece_row, self.piece_col] = self.turn
                    if self.piece_row != 0:
                        self.game_board.board[self.piece_row - 1, self.piece_col] = 0
                    self.draw_board()
                    self.piece_row += 1

                    # Check if it hit the bottom or another piece
                    if self.piece_row == self.rows or self.game_board.board[self.piece_row, self.piece_col] != 0:
                        self.falling = False
                        self.piece_col = -1
                        if self.turn == 1:
                            self.turn = 2
                        else:
                            self.turn = 1

                        # Check for win
                        winner = self.game_board.check_win()
                        if winner:
                            self.draw_board()
                            pygame.time.wait(2000)
                            self.game_board.reset_board()


if __name__ == '__main__':
    game = Connect4()
    game.main_loop()
