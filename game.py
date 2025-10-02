import numpy as np
import pygame
import utils
from utils import minimax
from board import Board
from button import Button

WIDTH, HEIGHT = (1000, 850)

COLOR_1 = 'red'
COLOR_2 = 'yellow'
COLOR_BG = 'white'
COLOR_WINNER = 'orange'
COLOR_BOARD = (50, 50, 200)
COLOR_MENU = 'cadetblue1'
COLOR_TEXT = 'dark blue'
COLOR_BUTTON = 'blue'
COLOR_BUTTON_HOVER = 'purple'
COLOR_BUTTON_SELECTED = 'dark orchid 4'

COLOR_HIGHLIGHT_KEYS = {1: COLOR_1, 2: COLOR_2}

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
BUTTON_MODE = Button(text_input='MODE', pos=(WIDTH / 2, HEIGHT / 2 - 200),
                     font=FONT_MEDIUM, base_color=COLOR_BUTTON,
                     hover_color=COLOR_BUTTON_HOVER)
BUTTON_MODE_1 = Button(text_input='TWO PLAYER', pos=(WIDTH / 2, HEIGHT / 2 - 200),
                       font=FONT_MEDIUM, base_color=COLOR_BUTTON,
                       hover_color=COLOR_BUTTON_HOVER)
BUTTON_MODE_2 = Button(text_input='ONE PLAYER', pos=(WIDTH / 2, HEIGHT / 2 - 100),
                       font=FONT_MEDIUM, base_color=COLOR_BUTTON,
                       hover_color=COLOR_BUTTON_HOVER)
BUTTON_MODE_3 = Button(text_input='AUTO', pos=(WIDTH / 2, HEIGHT / 2),
                       font=FONT_MEDIUM, base_color=COLOR_BUTTON,
                       hover_color=COLOR_BUTTON_HOVER)
BUTTON_BACK = Button(text_input='BACK', pos=(WIDTH - 150, HEIGHT - 100),
                     font=FONT_SMALL, base_color=COLOR_BUTTON,
                     hover_color=COLOR_BUTTON_HOVER)

# Difficulty buttons (default: Medium)
BUTTON_DIFFICULTY = Button(text_input='DIFFICULTY', pos=(WIDTH / 2, HEIGHT / 2 - 100),
                           font=FONT_MEDIUM, base_color=COLOR_BUTTON,
                           hover_color=COLOR_BUTTON_HOVER)
BUTTON_DIFF_EASY = Button(text_input='EASY', pos=(WIDTH / 2 - 200, HEIGHT / 2 - 50),
                          font=FONT_MEDIUM, base_color=COLOR_BUTTON,
                          hover_color=COLOR_BUTTON_HOVER)
BUTTON_DIFF_MED = Button(text_input='MEDIUM', pos=(WIDTH / 2, HEIGHT / 2 - 50),
                         font=FONT_MEDIUM, base_color=COLOR_BUTTON_SELECTED,
                         hover_color=COLOR_BUTTON_HOVER, selected=True)
BUTTON_DIFF_HARD = Button(text_input='HARD', pos=(WIDTH / 2 + 200, HEIGHT / 2 - 50),
                          font=FONT_MEDIUM, base_color=COLOR_BUTTON,
                          hover_color=COLOR_BUTTON_HOVER)

# Board size buttons (default: 7x6)
BUTTON_BOARD = Button(text_input='BOARD', pos=(WIDTH / 2, HEIGHT / 2),
                      font=FONT_MEDIUM, base_color=COLOR_BUTTON,
                      hover_color=COLOR_BUTTON_HOVER)
BUTTON_VARIANTS = Button(text_input='VARIANTS', pos=(WIDTH / 2, HEIGHT / 2 + 100),
                         font=FONT_MEDIUM, base_color=COLOR_BUTTON,
                         hover_color=COLOR_BUTTON_HOVER)
BUTTON_VARIANT_NO_GRAV = Button(text_input='NO GRAVITY', pos=(WIDTH / 2, HEIGHT / 2 - 50),
                                font=FONT_MEDIUM, base_color=COLOR_BUTTON,
                                hover_color=COLOR_BUTTON_HOVER)
BUTTON_BOARD_7x6 = Button(text_input='7x6', pos=(WIDTH / 2 - 200, HEIGHT / 2 - 50),
                         font=FONT_MEDIUM, base_color=COLOR_BUTTON_SELECTED,
                         hover_color=COLOR_BUTTON_HOVER, selected=True)
BUTTON_BOARD_8x7 = Button(text_input='8x7', pos=(WIDTH / 2, HEIGHT / 2 - 50),
                         font=FONT_MEDIUM, base_color=COLOR_BUTTON,
                         hover_color=COLOR_BUTTON_HOVER)
BUTTON_BOARD_9x7 = Button(text_input='9x7', pos=(WIDTH / 2 + 200, HEIGHT / 2 - 50),
                         font=FONT_MEDIUM, base_color=COLOR_BUTTON,
                         hover_color=COLOR_BUTTON_HOVER)

NUM_KEYS = range(48, 58)

MODE = 2  # 1: pvp, 2: pvc, 3: cvc

# max depth for each difficulty
DIFFICULTIES = {'EASY': 2, 'MEDIUM': 3, 'HARD': 4}

DROP_DELAY = 100

class Connect4:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Connect 4')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.mouse_pos = pygame.mouse.get_pos()
        self.board_size = (6, 7)
        self.rows = 6
        self.cols = 7
        self.col_width = WIDTH / self.cols
        self.game_board = Board(self.rows, self.cols)
        self.draw_board()
        self.mode = 2
        self.difficulty = 'MEDIUM'
        self.gravity = True
        # ensure utils knows the gravity setting used for move generation (if supported)
        setter = getattr(utils, 'set_gravity', None)
        if callable(setter):
            setter(self.gravity)
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
            if self.state == 'Variants Select':
                self.variants_selector()
            if self.state == 'Mode Select':
                self.mode_selector()
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
        for button in [BUTTON_MODE, BUTTON_DIFFICULTY, BUTTON_BOARD, BUTTON_VARIANTS, BUTTON_BACK]:
            button.check_hover(self.mouse_pos)
            button.update(self.screen)

    def variants_selector(self):
        self.screen.fill(COLOR_MENU)
        if self.gravity:
            BUTTON_VARIANTS.base_color = COLOR_BUTTON
            BUTTON_VARIANTS.selected = False
            BUTTON_VARIANT_NO_GRAV.base_color = COLOR_BUTTON
            BUTTON_VARIANT_NO_GRAV.selected = False
        else:
            BUTTON_VARIANTS.base_color = COLOR_BUTTON_SELECTED
            BUTTON_VARIANTS.selected = True
            BUTTON_VARIANT_NO_GRAV.base_color = COLOR_BUTTON_SELECTED
            BUTTON_VARIANT_NO_GRAV.selected = True

        for button in [BUTTON_BACK]:
            button.check_hover(self.mouse_pos)
            button.update(self.screen)

    def mode_selector(self):
        self.screen.fill(COLOR_MENU)
        for i, button in enumerate([BUTTON_MODE_1, BUTTON_MODE_2, BUTTON_MODE_3, BUTTON_BACK]):
            if self.mode == i + 1:
                button.base_color = COLOR_BUTTON_SELECTED
                button.selected = True
            else:
                button.base_color = COLOR_BUTTON
                button.selected = False
            button.check_hover(self.mouse_pos)
            button.update(self.screen)

    def board_selector(self):
        self.screen.fill(COLOR_MENU)
        # draw board size options
        for i, button in enumerate([BUTTON_BOARD_7x6, BUTTON_BOARD_8x7, BUTTON_BOARD_9x7, BUTTON_BACK]):
            selected = (i == 0 and self.board_size == (6, 7)) or \
                       (i == 1 and self.board_size == (7, 8)) or \
                       (i == 2 and self.board_size == (7, 9))
            if selected:
                button.base_color = COLOR_BUTTON_SELECTED
                button.selected = True
            else:
                button.base_color = COLOR_BUTTON
                button.selected = False
            button.check_hover(self.mouse_pos)
            button.update(self.screen)

    def difficulty_selector(self):
        self.screen.fill(COLOR_MENU)
        # draw difficulty options
        for i, button in enumerate([BUTTON_DIFF_EASY, BUTTON_DIFF_MED, BUTTON_DIFF_HARD, BUTTON_BACK]):
            # map selected difficulty
            if i < 3:
                selected = (i == 0 and self.difficulty == 'EASY') or \
                           (i == 1 and self.difficulty == 'MEDIUM') or \
                           (i == 2 and self.difficulty == 'HARD')
                if selected:
                    button.base_color = COLOR_BUTTON_SELECTED
                    button.selected = True
                else:
                    button.base_color = COLOR_BUTTON
                    button.selected = False
            button.check_hover(self.mouse_pos)
            button.update(self.screen)

    def play(self):
        self.draw_board()
        if pygame.time.get_ticks() >= self.delay_start + DROP_DELAY * self.rows and not self.falling:
            if self.mode == 1:
                self.player_vs_player()
            if self.mode == 2:
                self.player_vs_computer()
            if self.mode == 3:
                self.computer_vs_computer()

    def player_vs_player(self):
        self.draw_highlight()
        if 0 <= self.piece_col < self.cols:
            # Check if row is full first
            # If so, they get to re-pick move
            if all(self.game_board.board[:, self.piece_col]):
                return
            # Otherwise drop piece
            self.piece_row = 0
            self.falling = True
            self.delay_start = pygame.time.get_ticks()

    def player_vs_computer(self):
        if self.turn == 1:
            # Highlight column
            self.draw_highlight()
            if 0 <= self.piece_col < self.cols:
                if all(self.game_board.board[:, self.piece_col]):
                    print('column full')
                    return
                self.piece_row = 0
                self.falling = True

        else:
            pygame.display.flip()
            new_board, _ = minimax(self.game_board, 0, True, -np.inf, np.inf, max_depth=DIFFICULTIES[self.difficulty])
            diff = new_board.board - self.game_board.board
            for col in range(self.cols):
                if any(diff[:, col]):
                    self.piece_col = col
            self.piece_row = 0
            self.falling = True
            self.delay_start = pygame.time.get_ticks()

    def computer_vs_computer(self):
        if pygame.time.get_ticks() >= self.delay_start + DROP_DELAY * self.rows:
            if self.turn == 1:
                new_board, _ = minimax(self.game_board, 0, False, -np.inf, np.inf)
            else:
                new_board, _ = minimax(self.game_board, 0, True, -np.inf, np.inf)
            diff = new_board.board - self.game_board.board
            for col in range(self.cols):
                if any(diff[:, col]):
                    self.piece_col = col
            self.piece_row = 0
            self.falling = True
            self.delay_start = pygame.time.get_ticks()

    def go_back(self):
        if self.state == 'Play':
            self.state = 'Menu'
        if self.state == 'Options':
            self.state = 'Menu'
        if self.state == 'Mode Select':
            self.state = 'Options'
        if self.state == 'Board Select':
            self.state = 'Options'
        if self.state == 'Difficulty Select':
            self.state = 'Options'
        if self.state == 'Variants Select':
            self.state = 'Options'

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

        for i in range(self.rows):
            for j in range(self.cols):
                w, h = WIDTH // self.cols, HEIGHT // self.rows
                # Create a circle for each space
                circle_rect = pygame.rect.Rect(w * j + 10, h * i + 10, w - 20, h - 20)
                if self.game_board.board[i, j] == 1:
                    color = COLOR_1
                elif self.game_board.board[i, j] == 2:
                    color = COLOR_2
                else:
                    color = COLOR_BG
                pygame.draw.ellipse(self.screen, color, circle_rect)

    def draw_highlight(self):
        highlight_col = self.mouse_pos[0] // self.col_width
        highlight = pygame.Surface((self.col_width, HEIGHT))
        highlight.fill(COLOR_HIGHLIGHT_KEYS[self.turn])
        highlight.set_alpha(100)
        self.screen.blit(highlight, (highlight_col * self.col_width, 0))

    def check_win(self):
        winning_positions = self.game_board.check_win()
        if winning_positions:
            for _ in range(5):  # Blink 5 times
                # Highlight winning pieces
                self.highlight_winning_pieces(winning_positions[0])
                pygame.display.flip()
                pygame.time.wait(300)
                self.draw_board()
                pygame.display.flip()
                pygame.time.wait(300)

            # Wait for input to continue
            text = FONT_MEDIUM.render('Press any key to play again', True, COLOR_WINNER)
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        waiting = False
                        break
                    if event.type == pygame.QUIT:
                        quit()

            self.game_board.reset_board()

    def highlight_winning_pieces(self, positions):
        color = COLOR_WINNER
        for (i, j) in positions:
            w, h = WIDTH // self.cols, HEIGHT // self.rows
            circle_rect = pygame.rect.Rect(w * j + 10, h * i + 10, w - 20, h - 20)
            pygame.draw.ellipse(self.screen, color, circle_rect)

    def handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.go_back()
                    self.reset()
                if event.key in NUM_KEYS:
                    if pygame.time.get_ticks() >= self.delay_start + DROP_DELAY * self.rows:
                        # Set column to key number
                        self.piece_col = event.key - 49
                if event.key == pygame.K_SPACE:
                    print(self.piece_col)
                    print(self.turn)

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

                elif self.state == 'Options':
                    if BUTTON_MODE.check_hover(self.mouse_pos):
                        self.state = 'Mode Select'
                    if BUTTON_DIFFICULTY.check_hover(self.mouse_pos):
                        self.state = 'Difficulty Select'
                    if BUTTON_BOARD.check_hover(self.mouse_pos):
                        self.state = 'Board Select'
                    if BUTTON_VARIANTS.check_hover(self.mouse_pos):
                        self.state = 'Variants Select'

                elif self.state == 'Mode Select':
                    if BUTTON_MODE_1.check_hover(self.mouse_pos):
                        self.mode = 1
                    if BUTTON_MODE_2.check_hover(self.mouse_pos):
                        self.mode = 2
                    if BUTTON_MODE_3.check_hover(self.mouse_pos):
                        self.mode = 3

                elif self.state == 'Variants Select':
                    if BUTTON_VARIANT_NO_GRAV.check_hover(self.mouse_pos):
                        self.gravity = not self.gravity

                elif self.state == 'Board Select':
                    if BUTTON_BOARD_7x6.check_hover(self.mouse_pos):
                        # 7 columns x 6 rows stored as (rows, cols)
                        self.board_size = (6, 7)
                    if BUTTON_BOARD_8x7.check_hover(self.mouse_pos):
                        self.board_size = (7, 8)
                    if BUTTON_BOARD_9x7.check_hover(self.mouse_pos):
                        self.board_size = (7, 9)
                    self.rows, self.cols = self.board_size
                    self.game_board = Board(self.rows, self.cols)
                    self.col_width = WIDTH / self.cols

                elif self.state == 'Difficulty Select':
                    if BUTTON_DIFF_EASY.check_hover(self.mouse_pos):
                        self.difficulty = 'EASY'
                    if BUTTON_DIFF_MED.check_hover(self.mouse_pos):
                        self.difficulty = 'MEDIUM'
                    if BUTTON_DIFF_HARD.check_hover(self.mouse_pos):
                        self.difficulty = 'HARD'

                elif self.state == 'Play':
                    # In gravity mode we select a column and start falling animation
                    if self.gravity:
                        if pygame.time.get_ticks() >= self.delay_start + DROP_DELAY * self.rows and not self.falling:
                            self.piece_col = int(self.mouse_pos[0] // self.col_width)
                    else:
                        # No-gravity variant: place piece directly where clicked (row, col)
                        if pygame.time.get_ticks() >= self.delay_start + DROP_DELAY * self.rows:
                            col = int(self.mouse_pos[0] // self.col_width)
                            row = int(self.mouse_pos[1] // (HEIGHT / self.rows))
                            if 0 <= row < self.rows and 0 <= col < self.cols:
                                if self.game_board.board[row, col] == 0:
                                    self.game_board.board[row, col] = self.turn
                                    # Check for win
                                    winning_positions = self.game_board.check_win()
                                    if winning_positions:
                                        for _ in range(5):
                                            self.highlight_winning_pieces(winning_positions[0])
                                            pygame.display.flip()
                                            pygame.time.wait(300)
                                            self.draw_board()
                                            pygame.display.flip()
                                            pygame.time.wait(300)
                                        # After win, go back to menu
                                        self.state = 'Menu'
                                        self.reset()
                                        return
                                    # switch turns
                                    self.turn = 2 if self.turn == 1 else 1
                                    self.delay_start = pygame.time.get_ticks()

                if BUTTON_BACK.check_hover(self.mouse_pos):
                    self.go_back()

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

                        self.check_win()
                        
                        if self.turn == 1:
                            self.turn = 2
                        else:
                            self.turn = 1

                        # Check for draw
                        empty_spaces = (self.game_board.board == 0).sum()
                        if empty_spaces == 0:
                            self.draw_board()
                            pygame.display.flip()
                            pygame.time.wait(2000)
                            self.game_board.reset_board()


if __name__ == '__main__':
    game = Connect4()
    game.main_loop()
