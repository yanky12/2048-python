import time
import random


# Функция для инициализации игрового поля
def init_game(size):
    board = [[0] * size for _ in range(size)]
    add_new_tile(board, size)
    add_new_tile(board, size)
    return board


# Функция для добавления новой плитки на игровое поле
def add_new_tile(board, size):
    empty_tiles = [(i, j) for i in range(size) for j in range(size) if board[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        board[i][j] = 2 if random.random() < 0.9 else 4


# Функция для перемещения плиток влево
def move_left(board, size):
    moved = False
    for r in range(size):
        tiles = [value for value in board[r] if value != 0]
        for i in range(len(tiles) - 1):
            if tiles[i] == tiles[i + 1]:
                tiles[i] *= 2
                tiles[i + 1] = 0
        new_row = [value for value in tiles if value != 0]
        new_row += [0] * (size - len(new_row))
        if new_row != board[r]:
            board[r] = new_row
            moved = True
    return moved


# Функция для тестирования асимптотики
def test_algorithm():
    sizes = [4, 8, 16, 32]  # Разные размеры игрового поля
    results = {'init': [], 'add_tile': [], 'move': []}

    for size in sizes:
        # Тестирование инициализации игрового поля
        start_time = time.time()
        init_game(size)
        results['init'].append(time.time() - start_time)

        # Тестирование добавления новой плитки
        board = init_game(size)
        start_time = time.time()
        add_new_tile(board, size)
        results['add_tile'].append(time.time() - start_time)

        # Тестирование перемещения плиток
        start_time = time.time()
        move_left(board, size)
        results['move'].append(time.time() - start_time)

    return results


# Проведение тестирования
results = test_algorithm()

# Вывод результатов
for operation, times in results.items():
    print(f"Operation: {operation}")
    for size, time_taken in zip([4, 8, 16, 32], times):
        print(f"  Size: {size}x{size} - Time: {time_taken:.6f} seconds")