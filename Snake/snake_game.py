import pygame 
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
FPS = 20

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Все ячейки поля
ALL_CELLS = {
    (x * CELL_SIZE, y * CELL_SIZE) for x in range(WIDTH // CELL_SIZE) for y in range(HEIGHT // CELL_SIZE)
}

# Класс GameObject
class GameObject:
    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self, screen):
        pass  # Базовый класс не содержит рисующих действий

# Класс Apple
class Apple(GameObject):
    def __init__(self, snake_positions):
        super().__init__((0, 0), RED)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        available_cells = ALL_CELLS - set(snake_positions)
        if not available_cells:
            raise ValueError("No available cells left on the board!")
        self.position = random.choice(tuple(available_cells))

    def draw(self, screen):
        pygame.draw.rect(screen, self.body_color, (*self.position, CELL_SIZE, CELL_SIZE))

# Класс Snake
class Snake(GameObject):
    def __init__(self):
        super().__init__([(WIDTH // 2, HEIGHT // 2)], GREEN)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self, new_direction):
        if (self.direction[0] + new_direction[0], self.direction[1] + new_direction[1]) != (0, 0):
            self.next_direction = new_direction

    def move(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.position[0]
        new_head = (
            (head_x + self.direction[0] * CELL_SIZE) % WIDTH,
            (head_y + self.direction[1] * CELL_SIZE) % HEIGHT
        )
        self.position.insert(0, new_head)

        if len(self.position) > self.length:
            self.position.pop()

    def draw(self, screen):
        for pos in self.position:
            pygame.draw.rect(screen, self.body_color, (*pos, CELL_SIZE, CELL_SIZE))

    def get_head_position(self):
        return self.position[0]

    def reset(self):
        self.position = [(WIDTH // 2, HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

# Функция обработки нажатий клавиш
def handle_keys(snake):
    global FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)
            elif event.key == pygame.K_q:
                FPS -= 5
            elif event.key == pygame.K_w:
                FPS += 5

# Основная функция игры
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple(snake.position)

    running = True
    while running:
        handle_keys(snake)
        snake.move()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.position)

        # Проверка столкновения с самой собой
        if len(snake.position) != len(set(snake.position)):
            snake.reset()

        # Отрисовка
        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

        clock.tick(FPS)

if __name__ == "__main__":
    main()