"""Play game snake."""

from random import randint
from abc import abstractmethod
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
MIDDLE_W = GRID_WIDTH // 2 * GRID_SIZE
MIDDLE_H = GRID_HEIGHT // 2 * GRID_SIZE
MIDDLE = (MIDDLE_W, MIDDLE_H)
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Base class for other game objects inherit methods from."""

    @abstractmethod
    def __init__(
            self,
            body_color: tuple = BORDER_COLOR,
            position: tuple = MIDDLE
    ) -> None:
        """Init method."""
        self.position = position
        self.body_color = body_color

    @abstractmethod
    def draw(self):
        """Abstract method to be redefined."""
        pass


class Apple(GameObject):
    """Apple gameobject class."""

    def randomize_position(self) -> None:
        """Randomizes position of apple."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def __init__(self, body_color=APPLE_COLOR) -> None:
        """Init method of apple."""
        super().__init__(body_color=body_color)
        self.randomize_position()

    def draw(self):
        """Draw apple gameobject method."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Class representing a snake in the game."""

    def __init__(
            self,
            body_color=SNAKE_COLOR,
            position=MIDDLE
    ) -> None:
        """Init method of snake."""
        super().__init__(position=position, body_color=body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self) -> None:
        """Update direction of where snake heading off."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Move snake."""
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        self.last = self.positions[-1]
        while len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self) -> tuple:
        """Return head position of snake."""
        return self.positions[0]

    def draw(self):
        """Draw snake gameobject method."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self) -> None:
        """Reset snake size."""
        self.__init__()


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Change direction based on key pressed."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit


def position_obj(obj: GameObject, snake: Snake) -> None:
    """Positions object not inside snake."""
    while obj.position in snake.positions:
        obj.randomize_position()


def main():
    """Start the game main cycle."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    solid = Snake()
    mre = Apple()
    while mre.position in solid.positions:
        mre.randomize_position()

    while True:
        clock.tick(SPEED)
        handle_keys(solid)
        solid.update_direction()
        solid.move()
        if mre.position == solid.get_head_position():
            solid.length += 1
            position_obj(mre, solid)
        solid_count = sum(solid.positions.count(i) for i in solid.positions)
        if solid_count != len(solid.positions):
            screen.fill(BOARD_BACKGROUND_COLOR)
            solid.reset()
            position_obj(mre, solid)
        solid.draw()
        mre.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
