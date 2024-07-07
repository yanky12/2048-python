import pygame
import random
import os
import time


pygame.init()

# Константы
SIZE = 4
TILE_SIZE = 100
TILES_DISTANCE = 10
TOP_SPACE = 100
WINDOW_HEIGHT = SIZE * TILE_SIZE + (SIZE + 1) * TILES_DISTANCE + TOP_SPACE
WINDOWS_WIDTH = SIZE * TILE_SIZE + (SIZE + 1) * TILES_DISTANCE

# Цвета для светлой темы игры
LIGHT_BACKGROUND_COLOR = (187, 173, 160)
LIGHT_BUTTON_COLOR = (121, 100, 79)
ALT_LIGHT_BUTTON_COLOR = (121 + 15, 100 + 15, 79 + 15)
LIGHT_BUTTON_FONT_COLOR = (203, 203, 203)
LIGHT_FONT_COLOR = (119, 110, 101)
LIGHT_FONT_COLOR_LATE_GAME = (255, 255, 255)
LIGHT_TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Цвета для темной темы игры
DARK_BACKGROUND_COLOR = (68, 82, 95)
DARK_BUTTON_COLOR = (134, 155, 176)
ALT_DARK_BUTTON_COLOR = (134+15, 155+15, 176+15)
DARK_BUTTON_FONT_COLOR = (52, 52, 52)
DARK_FONT_COLOR = (136, 145, 154)
DARK_FONT_COLOR_LATE_GAME = (0, 0, 0)
DARK_TILE_COLORS = {
    0: (50, 62, 75),
    2: (17, 27, 37),
    4: (18, 31, 55),
    8: (13, 78, 134),
    16: (10, 106, 156),
    32: (9, 131, 160),
    64: (9, 161, 196),
    128: (18, 48, 141),
    256: (18, 51, 158),
    512: (18, 55, 175),
    1024: (18, 58, 192),
    2048: (18, 61, 209),
}

# Настройка эрана игры
screen = pygame.display.set_mode((WINDOWS_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('2048')
pygame.display.set_icon(pygame.image.load("2048_logo.svg.png"))

# Создание шрифтов
small_font = pygame.font.SysFont('franklingothicmedium', 20)
font = pygame.font.SysFont('franklingothicmedium', 24)
medium_font = pygame.font.SysFont('franklingothicmedium', 30)
big_font = pygame.font.SysFont('franklingothicmedium', 43)
biggest_font = pygame.font.SysFont('franklingothicmedium', 64)

# Переменные для хранения счета и количества сделанных ходов
score, count_move = 0, 0


# Инициализация игрового поля
def init_game():
    board = [[0] * SIZE for _ in range(SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    clear_statistics()
    return board


# Увеличить переменную score
def increase_score(points: int):
    global score
    score += points


# Увеличить переменную count_move
def increase_count_move():
    global count_move
    count_move += 1


# Очистить переменные score и move_count
def clear_statistics():
    global score, count_move
    score = 0
    count_move = 0


# Добавление плитки с числом 2 или 4 в случайном месте
def add_new_tile(board: list):
    empty_tiles = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        board[r][c] = 2 if random.random() < 0.9 else 4


# Отображение игрового поля
def draw_board(board: list, dark_theme: bool, elapsed_time):
    # Изменение цветов в зависимости от выбранной темы
    if dark_theme:
        screen.fill(DARK_BACKGROUND_COLOR)
        button_color, alt_button_color = DARK_BUTTON_COLOR, ALT_DARK_BUTTON_COLOR
        font_color, button_font_color = DARK_FONT_COLOR, DARK_BUTTON_FONT_COLOR
    else:
        screen.fill(LIGHT_BACKGROUND_COLOR)
        button_color, alt_button_color = LIGHT_BUTTON_COLOR, ALT_LIGHT_BUTTON_COLOR
        font_color, button_font_color = LIGHT_FONT_COLOR, LIGHT_BUTTON_FONT_COLOR

    high_score_surface = font.render(f'Record: {load_high_score()}', True, font_color)
    screen.blit(high_score_surface, (TILES_DISTANCE, TILES_DISTANCE))

    score_surface = font.render(f'Score: {score}', True, font_color)
    screen.blit(score_surface, (TILES_DISTANCE, TILES_DISTANCE+30))

    timer_surface = font.render(f'Time: {elapsed_time:.0f}с', True, font_color)
    screen.blit(timer_surface, (TILES_DISTANCE, TILES_DISTANCE+60))

    button_position = (WINDOWS_WIDTH - TILES_DISTANCE - 115, TILES_DISTANCE)
    button_rect = draw_button("new game", font, button_position, (115, 30),
                              button_color, alt_button_color, button_font_color)

    theme_button_position = (WINDOWS_WIDTH - TILES_DISTANCE - 155, TILES_DISTANCE + 35)
    theme_button_rect = draw_button("change theme", font, theme_button_position, (155, 30),
                                    font_color, alt_button_color, button_font_color)

    # Отображение плиток с числовыми значениями
    for r in range(SIZE):
        for c in range(SIZE):
            value = board[r][c]
            if dark_theme:
                color = DARK_TILE_COLORS.get(value, DARK_TILE_COLORS[2048])
            else:
                color = LIGHT_TILE_COLORS.get(value, LIGHT_TILE_COLORS[2048])
            pygame.draw.rect(screen, color, (
                c * TILE_SIZE + (c + 1) * TILES_DISTANCE,
                r * TILE_SIZE + (r + 1) * TILES_DISTANCE + TOP_SPACE,
                TILE_SIZE, TILE_SIZE))
            if value:
                if dark_theme:
                    if 16 <= value <= 64:
                        text_surface = big_font.render(f'{value}', True, DARK_FONT_COLOR_LATE_GAME)
                    else:
                        text_surface = big_font.render(f'{value}', True, DARK_FONT_COLOR)
                else:
                    if 8 <= value:
                        text_surface = big_font.render(f'{value}', True, LIGHT_FONT_COLOR_LATE_GAME)
                    else:
                        text_surface = big_font.render(f'{value}', True, LIGHT_FONT_COLOR)
                text_rect = text_surface.get_rect(center=(
                    c * TILE_SIZE + (c + 1) * TILES_DISTANCE + TILE_SIZE / 2,
                    r * TILE_SIZE + (r + 1) * TILES_DISTANCE + TILE_SIZE / 2 + TOP_SPACE))
                screen.blit(text_surface, text_rect)

    pygame.display.update()
    return button_rect, theme_button_rect


# Передвежение плиткок влево
def move_left(board: list):
    moved = False
    for r in range(SIZE):
        tiles = [value for value in board[r] if value != 0]
        for i in range(len(tiles) - 1):
            if tiles[i] == tiles[i + 1]:
                tiles[i] *= 2
                tiles[i + 1] = 0
                increase_score(tiles[i])
        new_row = [value for value in tiles if value != 0]
        new_row += [0] * (SIZE - len(new_row))
        if new_row != board[r]:
            board[r] = new_row
            moved = True
    return moved


# Передвежение плиткок вправо
def move_right(board: list):
    moved = False
    for r in range(SIZE):
        tiles = [value for value in board[r] if value != 0]
        for i in range(len(tiles) - 1, 0, -1):
            if tiles[i] == tiles[i - 1]:
                tiles[i] *= 2
                tiles[i - 1] = 0
                increase_score(tiles[i])
        new_row = [value for value in tiles if value != 0]
        new_row = [0] * (SIZE - len(new_row)) + new_row
        if new_row != board[r]:
            board[r] = new_row
            moved = True
    return moved


# Передвежение плиткок вверх
def move_up(board: list):
    moved = False
    for c in range(SIZE):
        tiles = []
        old_row = []
        for r in range(SIZE):
            value = board[r][c]
            old_row.append(value)
            if value != 0:
                tiles.append(value)
        for i in range(len(tiles) - 1):
            if tiles[i] == tiles[i + 1]:
                tiles[i] *= 2
                tiles[i + 1] = 0
                increase_score(tiles[i])
        new_row = [value for value in tiles if value != 0]
        new_row += [0] * (SIZE - len(new_row))
        if new_row != old_row:
            for r in range(SIZE):
                board[r][c] = new_row[r]
            moved = True
    return moved


# Передвежение плиткок вниз
def move_down(board: list):
    moved = False
    for c in range(SIZE):
        tiles = []
        old_row = []
        for r in range(SIZE):
            value = board[r][c]
            old_row.append(value)
            if value != 0:
                tiles.append(value)
        for i in range(len(tiles) - 1, 0, -1):
            if tiles[i] == tiles[i - 1]:
                tiles[i] *= 2
                tiles[i - 1] = 0
                increase_score(tiles[i])
        new_row = [value for value in tiles if value != 0]
        new_row = [0] * (SIZE - len(new_row)) + new_row
        if new_row != old_row:
            for r in range(SIZE):
                board[r][c] = new_row[r]
            moved = True
    return moved


# Проверка на поражение
def is_game_over(board: list):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                return False
            if c < SIZE - 1 and board[r][c] == board[r][c + 1]:
                return False
            if r < SIZE - 1 and board[r][c] == board[r + 1][c]:
                return False
    return True


# Отображение кнопки
def draw_button(text, _font, position, size, main_color, alt_color, text_color):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(position, size)
    color = alt_color if button_rect.collidepoint(mouse_pos) else main_color

    pygame.draw.rect(screen, color, button_rect)
    text_surface = _font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect


# Отображение экрана поражения
def show_game_over_screen(new_record: bool, dark_theme: bool, elapsed_time):
    # Изменение цветов в зависимости от выбранной темы
    if dark_theme:
        screen.fill(DARK_BACKGROUND_COLOR)
        button_color, font_color, button_font_color, alt_button_color = (DARK_BUTTON_COLOR, DARK_FONT_COLOR,
                                                                         DARK_BUTTON_FONT_COLOR, ALT_DARK_BUTTON_COLOR)
    else:
        screen.fill(LIGHT_BACKGROUND_COLOR)
        button_color, font_color, button_font_color, alt_button_color = (LIGHT_BUTTON_COLOR, LIGHT_FONT_COLOR,
                                                                         LIGHT_BUTTON_FONT_COLOR, ALT_LIGHT_BUTTON_COLOR)

    # Изменение надписи при достижении нового рекорда
    if new_record:
        high_score_surface = font.render(f'New record!', True, font_color)
        high_score_rect = high_score_surface.get_rect(center=(WINDOWS_WIDTH / 2, 110))
        screen.blit(high_score_surface, high_score_rect)
    else:
        high_score_surface = font.render(f'Record: {load_high_score()}', True, font_color)
        high_score_rect = high_score_surface.get_rect(center=(WINDOWS_WIDTH / 2, 110))
        screen.blit(high_score_surface, high_score_rect)

    score_surface = medium_font.render(f'{score}', True, font_color)
    score_rect = score_surface.get_rect(center=(WINDOWS_WIDTH / 2, 180))
    screen.blit(score_surface, score_rect)

    text_surface = big_font.render('Game Over', True, font_color)
    text_rect = text_surface.get_rect(center=(WINDOWS_WIDTH / 2, WINDOW_HEIGHT / 2 - 25))
    screen.blit(text_surface, text_rect)

    button_position = (WINDOWS_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 40)
    button_rect = draw_button("new game", medium_font, button_position, (200, 50),
                              button_color, alt_button_color, button_font_color)

    timer_surface = font.render(f'Time played: {elapsed_time:.1f}с', True, font_color)
    timer_rect = timer_surface.get_rect(center=(WINDOWS_WIDTH / 2, WINDOW_HEIGHT / 2 + 150))
    screen.blit(timer_surface, timer_rect)

    count_surface = font.render(f'Count of moves: {count_move}', True, font_color)
    count_rect = count_surface.get_rect(center=(WINDOWS_WIDTH / 2, WINDOW_HEIGHT / 2 + 200))
    screen.blit(count_surface, count_rect)

    pygame.display.update()
    return button_rect


# Отображение начального экрана
def show_start_screen(dark_theme):
    if dark_theme:
        screen.fill(DARK_BACKGROUND_COLOR)
        button_color, alt_button_color = DARK_BUTTON_COLOR, ALT_DARK_BUTTON_COLOR
        font_color, button_font_color = DARK_FONT_COLOR, DARK_BUTTON_FONT_COLOR
    else:
        screen.fill(LIGHT_BACKGROUND_COLOR)
        button_color, alt_button_color = LIGHT_BUTTON_COLOR, ALT_LIGHT_BUTTON_COLOR
        font_color, button_font_color = LIGHT_FONT_COLOR, LIGHT_BUTTON_FONT_COLOR

    high_score_surface = font.render(f'Record: {load_high_score()}', True, font_color)
    high_score_rect = high_score_surface.get_rect(center=(WINDOWS_WIDTH / 2, TILES_DISTANCE * 5))
    screen.blit(high_score_surface, high_score_rect)

    theme_button_position = (0, 0)
    theme_button_rect = draw_button("change theme", font, theme_button_position, (450, 30),
                                    font_color, alt_button_color, button_font_color)

    text_surface = biggest_font.render("2048", True, font_color)
    text_rect = text_surface.get_rect(center=(WINDOWS_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
    screen.blit(text_surface, text_rect)

    button_position = (WINDOWS_WIDTH / 2 - 75, WINDOW_HEIGHT / 2 + 25)
    button_rect = draw_button("play", medium_font, button_position, (150, 60),
                              font_color, alt_button_color, button_font_color)

    pygame.display.update()
    return button_rect, theme_button_rect


# Загрузить файл с рекордом
def load_high_score():
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", 'r') as file:
            return int(file.read())
    return 0


# Записать новый рекорд в файл
def save_high_score(high_score):
    with open("high_score.txt", 'w') as file:
        file.write(str(high_score))


# Основной цикл игры
def main():
    board = init_game()
    running = True
    start = True
    game_over = False
    new_record = False
    high_score = load_high_score()
    dark_theme = False
    start_time = 0
    elapsed_time = 0

    while running:
        if start:
            button_rect, theme_button_rect = show_start_screen(dark_theme)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        start_time = time.time()
                        start = False
                    elif theme_button_rect.collidepoint(event.pos):
                        dark_theme = not dark_theme
        elif game_over:
            button_rect = show_game_over_screen(new_record, dark_theme, elapsed_time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        board = init_game()
                        start_time = time.time()
                        game_over = False
                        new_record = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        board = init_game()
                        start_time = time.time()
                        game_over = False
                        new_record = False
        else:
            elapsed_time = time.time() - start_time
            button_rect, theme_button_react = draw_board(board, dark_theme, elapsed_time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        board = init_game()
                        start_time = time.time()
                        game_over = False
                        new_record = False
                    elif theme_button_react.collidepoint(event.pos):
                        dark_theme = not dark_theme
                elif event.type == pygame.KEYDOWN:
                    moved = False
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        moved = move_left(board)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        moved = move_right(board)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        moved = move_up(board)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        moved = move_down(board)
                    if moved:
                        increase_count_move()
                        add_new_tile(board)
                        if score > high_score:
                            high_score = score
                            new_record = True
                            save_high_score(high_score)
                        if is_game_over(board):
                            game_over = True

    pygame.quit()


if __name__ == '__main__':
    main()


