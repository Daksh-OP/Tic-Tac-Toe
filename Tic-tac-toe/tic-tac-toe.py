import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Board
board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Functions
def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE//2), int(row * SQUARE_SIZE + SQUARE_SIZE//2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

def check_win(player):
    # Vertical
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    # Horizontal
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    # Diagonals
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return True

    return False

# --- Bot AI Functions ---
def get_empty_positions():
    return [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == 0]

# Easy AI → Random move
def ai_easy():
    return random.choice(get_empty_positions())

# Medium AI → Win if possible, else block
def ai_medium(player, opponent):
    for row, col in get_empty_positions():
        board[row][col] = player
        if check_win(player):
            board[row][col] = 0
            return (row, col)
        board[row][col] = 0
    for row, col in get_empty_positions():
        board[row][col] = opponent
        if check_win(opponent):
            board[row][col] = 0
            return (row, col)
        board[row][col] = 0
    return ai_easy()

# Hard AI → Minimax (Unbeatable)
def minimax(depth, is_maximizing, player, opponent):
    if check_win(player):
        return 1
    elif check_win(opponent):
        return -1
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -100
        for row, col in get_empty_positions():
            board[row][col] = player
            score = minimax(depth+1, False, player, opponent)
            board[row][col] = 0
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = 100
        for row, col in get_empty_positions():
            board[row][col] = opponent
            score = minimax(depth+1, True, player, opponent)
            board[row][col] = 0
            best_score = min(score, best_score)
        return best_score

def ai_hard(player, opponent):
    best_score = -100
    best_move = None
    for row, col in get_empty_positions():
        board[row][col] = player
        score = minimax(0, False, player, opponent)
        board[row][col] = 0
        if score > best_score:
            best_score = score
            best_move = (row, col)
    return best_move

# Main Game Loop
def main(mode="bot", bot_level="hard"):
    draw_lines()
    player = 1  # Circle (human)
    opponent = 2  # Cross (bot)
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and mode == "2p":
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE

                if available_square(mouseY, mouseX):
                    mark_square(mouseY, mouseX, player)
                    if check_win(player):
                        print(f"Player {player} wins!")
                        game_over = True
                    player = player % 2 + 1

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and mode == "bot":
                if player == 1:  # Human turn
                    mouseX = event.pos[0] // SQUARE_SIZE
                    mouseY = event.pos[1] // SQUARE_SIZE

                    if available_square(mouseY, mouseX):
                        mark_square(mouseY, mouseX, player)
                        if check_win(player):
                            print("Human wins!")
                            game_over = True
                        player = 2

        if mode == "bot" and player == 2 and not game_over:
            pygame.time.delay(500)
            if bot_level == "easy":
                row, col = ai_easy()
            elif bot_level == "medium":
                row, col = ai_medium(2, 1)
            else:
                row, col = ai_hard(2, 1)

            mark_square(row, col, 2)
            if check_win(2):
                print("Bot wins!")
                game_over = True
            player = 1

        draw_figures()
        pygame.display.update()
def draw_text_center(text, y, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(text_surface, text_rect)

def menu_screen():
    menu_font = pygame.font.SysFont(None, 70)
    option_font = pygame.font.SysFont(None, 48)
    info_font = pygame.font.SysFont(None, 32)
    selected_mode = 0  # 0: 2P, 1: Bot
    bot_levels = ["easy", "medium", "hard"]
    bot_level_idx = 0
    choosing_bot = False

    clock = pygame.time.Clock()

    while True:
        screen.fill(BG_COLOR)
        draw_text_center("Tic Tac Toe", 110, menu_font, CIRCLE_COLOR)

        # Highlight selection
        color_2p = RED if selected_mode == 0 and not choosing_bot else CROSS_COLOR
        color_bot = RED if selected_mode == 1 and not choosing_bot else CROSS_COLOR

        draw_text_center("2 Player", 240, option_font, color_2p)
        draw_text_center("Bot", 320, option_font, color_bot)

        if selected_mode == 1:
            # Show bot difficulty selection
            for i, level in enumerate(bot_levels):
                color = RED if choosing_bot and bot_level_idx == i else CIRCLE_COLOR
                draw_text_center(
                    f"{level.capitalize()}",
                    400 + i * 50,
                    option_font,
                    color
                )
            if choosing_bot:
                draw_text_center("←/→ to change, Enter to start", 570, info_font, LINE_COLOR)
            else:
                draw_text_center("Press Enter to select Bot", 570, info_font, LINE_COLOR)
        else:
            draw_text_center("Press Enter to start 2 Player", 570, info_font, LINE_COLOR)

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not choosing_bot:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected_mode = (selected_mode - 1) % 2
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        selected_mode = (selected_mode + 1) % 2
                    if event.key == pygame.K_RETURN:
                        if selected_mode == 0:
                            screen.fill(BG_COLOR)
                            pygame.display.update()
                            pygame.time.delay(200)
                            return "2p", None
                        else:
                            choosing_bot = True
                else:
                    if event.key == pygame.K_LEFT:
                        bot_level_idx = (bot_level_idx - 1) % len(bot_levels)
                    if event.key == pygame.K_RIGHT:
                        bot_level_idx = (bot_level_idx + 1) % len(bot_levels)
                    if event.key == pygame.K_RETURN:
                        screen.fill(BG_COLOR)
                        pygame.display.update()
                        pygame.time.delay(200)
                        return "bot", bot_levels[bot_level_idx]
                    if event.key == pygame.K_ESCAPE:
                        choosing_bot = False

# Run game: choose "2p" for 2-player, "bot" for bot mode
if __name__ == "__main__":
    mode, bot_level = menu_screen()
    if mode == "2p":
        main("2p")
    else:
        main("bot", bot_level)
