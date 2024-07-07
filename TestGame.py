import unittest
import random
from main import init_game, add_new_tile, move_left, is_game_over


class TestGame2048(unittest.TestCase):
    def setUp(self):
        # Установка начальных значений для тестов
        self.board = init_game()

    def test_init_game(self):
        # Проверка инициализации игрового поля
        board = init_game()
        non_zero_tiles = sum(tile != 0 for row in board for tile in row)
        # Инициализация должна добавить ровно 2 плитки
        self.assertEqual(non_zero_tiles, 2)

    def test_add_new_tile(self):
        # Проверка добавления новой плитки
        initial_non_zero_tiles = sum(tile != 0 for row in self.board for tile in row)
        add_new_tile(self.board)
        new_non_zero_tiles = sum(tile != 0 for row in self.board for tile in row)
        # Должна быть добавлена одна новая плитка
        self.assertEqual(new_non_zero_tiles, initial_non_zero_tiles + 1)

    def test_move_left(self):
        # Проверка перемещения плиток влево
        self.board = [
            [2, 0, 0, 2],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        expected_board = [
            [4, 0, 0, 0],
            [8, 0, 0, 0],
            [4, 4, 0, 0],
            [0, 0, 0, 0]
        ]
        move_left(self.board)
        # Плитки должны корректно перемещаться влево и объединяться
        self.assertEqual(self.board, expected_board)

    def test_is_game_over(self):
        # Проверка на окончание игры
        self.board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        # Игра должна завершиться, если нет доступных ходов
        self.assertTrue(is_game_over(self.board))

        # Игра не должна завершиться, если есть доступные ходы
        self.board[0][0] = 0
        self.assertFalse(is_game_over(self.board))


if __name__ == '__main__':
    unittest.main()
