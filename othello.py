from copy import deepcopy
import random
from game_config import PLAYER_1_TYPE, PLAYER_1_STRENGTH, PLAYER_2_TYPE, PLAYER_2_STRENGTH, VALID_PLAYER_TYPES, PLAYER_1_EVAL, PLAYER_2_EVAL, VALID_EVAL_TYPES, VISIBLE_BOARD
import pygame
import sys

# Define colors
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
BOARD_COLOR = (200, 200, 200)
LINE_COLOR = (0, 0, 0)

CELL_SIZE = 50
GRID_SIZE = 8
WINDOW_SIZE = GRID_SIZE * CELL_SIZE


# Board representation
BLACK = "B"
WHITE = "W"
NOTHING = "N"

INITIAL_BOARD = [[NOTHING for _ in range(8)] for _ in range(8)]
INITIAL_BOARD[3][3] = WHITE
INITIAL_BOARD[3][4] = BLACK
INITIAL_BOARD[4][3] = BLACK
INITIAL_BOARD[4][4] = WHITE


def initialize_pygame_board():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Othello Game")
    return screen


def get_board_position_from_click(pos):
    """Convert pixel position to board row, col."""
    x, y = pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col


def handle_human_click(board, current_player):
    """Waits for a human player's click and returns the (row, col) coordinates if valid."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_board_position_from_click(pos)
                if (row, col) in get_valid_moves(board, current_player):
                    return row, col


def update_pygame_board(screen, board):
    screen.fill(BOARD_COLOR)
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, WINDOW_SIZE))
        pygame.draw.line(screen, LINE_COLOR, (0, x), (WINDOW_SIZE, x))

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_value = board[row][col]
            if cell_value == BLACK:
                pygame.draw.circle(screen, BLACK_COLOR,
                                   (col * CELL_SIZE + CELL_SIZE // 2,
                                    row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - 5)
            elif cell_value == WHITE:
                pygame.draw.circle(screen, WHITE_COLOR,
                                   (col * CELL_SIZE + CELL_SIZE // 2,
                                    row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - 5)

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def print_grid(board: list[list[str]]) -> None:
    # PRINT THE BOARD
    for row in board:
        print(" | ".join(row).replace(NOTHING, " "))


def notation_to_index(coord: str) -> (int, int):
    col = ord(coord[0].upper()) - ord('A')
    row = int(coord[1]) - 1
    return row, col


def get_valid_moves(board: list[list[str]], player: str) -> list[tuple[int, int]]:
    opponent = BLACK if player == WHITE else WHITE
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    valid_moves = []

    for row in range(8):
        for col in range(8):
            if board[row][col] != NOTHING:
                continue

            for dr, dc in directions:
                r, c = row + dr, col + dc
                found_opponent = False

                while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
                    found_opponent = True
                    r += dr
                    c += dc

                if found_opponent and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                    valid_moves.append((row, col))
                    break

    return valid_moves


def play_move(board: list[list[str]],
              row: int,
              col: int,
              player: str) -> list[list[str]] | None:
    if (row, col) not in get_valid_moves(board, player):
        print_grid(board)
        print(f"Invalid move {row} {col}, {player}")
        return None

    new_board = deepcopy(board)
    opponent = BLACK if player == WHITE else WHITE
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    new_board[row][col] = player

    for dr, dc in directions:
        r, c = row + dr, col + dc
        to_flip = []

        while 0 <= r < 8 and 0 <= c < 8 and new_board[r][c] == opponent:
            to_flip.append((r, c))
            r += dr
            c += dc

        if 0 <= r < 8 and 0 <= c < 8 and new_board[r][c] == player:
            for flip_r, flip_c in to_flip:
                new_board[flip_r][flip_c] = player

    return new_board


def is_game_done(board: list[list[str]]) -> bool:
    has_black_moves = bool(get_valid_moves(board, BLACK))
    has_white_moves = bool(get_valid_moves(board, WHITE))

    if not has_black_moves and not has_white_moves:
        return True
    for row in board:
        if NOTHING in row:
            return False

    return True


def compute_score(board: list[list[str]]) -> tuple[int, int]:
    black_score = 0
    white_score = 0

    for row in board:
        for cell in row:
            if cell == BLACK:
                black_score += 1
            elif cell == WHITE:
                white_score += 1

    return black_score, white_score


def play_game():
    board = INITIAL_BOARD
    if VISIBLE_BOARD:
        screen = initialize_pygame_board()
        update_pygame_board(screen, board)

    current_player = BLACK
    while not is_game_done(board):
        valid_moves = get_valid_moves(board, current_player)
        if valid_moves:
            if current_player == BLACK and PLAYER_1_TYPE == "BOT":
                if PLAYER_1_EVAL == "RANDOM":
                    row, col = pick_random_move(board, current_player)
                else:
                    eval, row, col = minimax(
                        board, PLAYER_1_STRENGTH, current_player, eval_type=PLAYER_1_EVAL)
                board = play_move(board, row, col, current_player)

            elif current_player == WHITE and PLAYER_2_TYPE == "BOT":
                if PLAYER_2_EVAL == "RANDOM":
                    row, col = pick_random_move(board, current_player)
                else:
                    eval, row, col = minimax(
                        board, PLAYER_2_STRENGTH, current_player, eval_type=PLAYER_2_EVAL)
                board = play_move(board, row, col, current_player)
                if board == None:
                    print(eval, row, col)

            else:  # HUMAN PICK
                row, col = handle_human_click(board, current_player)
                board = play_move(board, row, col, current_player)

        if VISIBLE_BOARD:
            update_pygame_board(screen, board)

        current_player = WHITE if current_player == BLACK else BLACK

    print("Résultat:")
    print_grid(board)
    black_score, white_score = compute_score(board)
    if black_score > white_score:
        print(f"black win, {black_score}, {white_score}")
    elif white_score > black_score:
        print(f"white win, {black_score}, {white_score}")
    else:
        print(f"tie, {black_score}, {white_score}")


"""
FROM THERE ON, EVAL FUNCTIONS AND MINIMAX ALGOS
"""


def pick_random_move(board: list[list[str]], player: str) -> tuple[int, int] | None:
    valid_moves = get_valid_moves(board, player)

    return random.choice(valid_moves) if valid_moves else None


def simple_score_scheme(board):
    bs, ws = compute_score(board)
    if is_game_done(board) and bs > ws:
        return 800
    elif is_game_done(board) and ws < bs:
        return -800
    return bs - ws


def weighted_score_scheme(board):
    bs, ws = compute_score(board)
    WEIGHTS = [[30, -25, 10, 5, 5, 10, -25,  30,],
               [-25, -25,  1, 1, 1,  1, -25, -25,],
               [10,   1,  5, 2, 2,  5,   1,  10,],
               [5,   1,  2, 1, 1,  2,   1,   5,],
               [5,   1,  2, 1, 1,  2,   1,   5,],
               [10,   1,  5, 2, 2,  5,   1,  10,],
               [-25, -25,  1, 1, 1,  1, -25, -25,],
               [30, -25, 10, 5, 5, 10, -25,  30,],]

    if is_game_done(board) and bs > ws:
        return 800
    elif is_game_done(board) and ws < bs:
        return -800

    score = 0
    for row in range(8):
        for col in range(8):
            if board[row][col] == BLACK:
                score += WEIGHTS[row][col]
            elif board[row][col] == WHITE:
                score -= WEIGHTS[row][col]

    return score


def f_eval(board, eval_type):
    if eval_type == "SCORE":
        return simple_score_scheme(board)
    elif eval_type == "WEIGHTS":
        return weighted_score_scheme(board)
    else:
        return simple_score_scheme(board)


def minimax(board: list, depth: int, player, alpha=-1000, beta=1000, eval_type="WEIGHTS"):
    next_player = WHITE if player == BLACK else BLACK

    if depth == 0 or is_game_done(board):
        return f_eval(board, eval_type), None, None
    if not is_game_done(board) and not bool(get_valid_moves(board, player)):
        return minimax(board, depth - 1, next_player, alpha, beta, eval_type)

    best_move = (None, None)
    best_eval = -900 if player == BLACK else 900

    for move in get_valid_moves(board, player):
        row, col = move
        new_board = play_move(board, row, col, player)

        eval, _, _ = minimax(new_board, depth - 1, next_player,
                             alpha=alpha, beta=beta, eval_type=eval_type)

        if player == BLACK:
            if eval > best_eval:
                best_move = (row, col)
                best_eval = eval
            alpha = max(alpha, best_eval)
        else:
            if eval < best_eval:
                best_move = (row, col)
                best_eval = eval
            beta = min(beta, best_eval)

        if alpha >= beta:
            return best_eval, best_move[0], best_move[1]

    return best_eval, best_move[0], best_move[1]


if __name__ == "__main__":
    play_game()
