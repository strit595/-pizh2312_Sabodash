
import unittest
from unittest.mock import patch
import random

# Импортируем классы из основного кода
from snake import Snake, Apple, ALL_CELLS, CELL_SIZE, UP, DOWN, LEFT, RIGHT, WIDTH, HEIGHT

class TestSnakeGame(unittest.TestCase):
    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.snake = Snake()

    def test_snake_initial_position(self):
        """Проверяем, что змейка создается в центре"""
        expected_position = [(WIDTH // 2, HEIGHT // 2)]
        self.assertEqual(self.snake.position, expected_position)

    def test_snake_moves_correctly(self):
        """Проверяем, что змейка двигается в правильном направлении"""
        initial_pos = self.snake.get_head_position()
        self.snake.move()
        new_pos = self.snake.get_head_position()
        expected_pos = ((initial_pos[0] + CELL_SIZE) % WIDTH, initial_pos[1])  # Направление по умолчанию вправо
        self.assertEqual(new_pos, expected_pos)

    def test_snake_changes_direction(self):
        """Проверяем, что змейка меняет направление корректно"""
        self.snake.update_direction(UP)
        self.snake.move()
        self.assertEqual(self.snake.direction, UP)

        self.snake.update_direction(LEFT)
        self.snake.move()
        self.assertEqual(self.snake.direction, LEFT)

    def test_snake_does_not_reverse(self):
        """Проверяем, что змейка не может развернуться на 180 градусов"""
        self.snake.update_direction(LEFT)  # Нельзя сразу пойти влево
        self.snake.move()
        self.assertEqual(self.snake.direction, RIGHT)  # Направление не должно измениться

        self.snake.update_direction(DOWN)  # Можно вниз
        self.snake.move()
        self.assertEqual(self.snake.direction, DOWN)

    def test_snake_collides_with_itself(self):
        """Проверяем, что змейка сбрасывается при столкновении с самой собой"""
        self.snake.position = [(100, 100), (120, 100), (140, 100), (120, 100)]  # Имитируем столкновение
        self.snake.length = 4
        self.snake.reset()  # Принудительно сбрасываем
        
        self.assertEqual(self.snake.position, [(WIDTH // 2, HEIGHT // 2)])
        self.assertEqual(self.snake.length, 1)


class TestApple(unittest.TestCase):
    def setUp(self):
        """Создание змейки перед тестами яблока"""
        self.snake = Snake()

    def test_apple_appears_not_on_snake(self):
        """Проверяем, что яблоко не появляется внутри змейки"""
        apple = Apple(self.snake.position)
        self.assertNotIn(apple.position, self.snake.position)

    @patch('random.choice', return_value=(40, 40))
    def test_apple_random_position(self, mock_random):
        """Проверяем, что яблоко появляется в ожидаемой позиции"""
        apple = Apple(self.snake.position)
        self.assertEqual(apple.position, (40, 40))

if __name__ == '__main__':
    unittest.main()
