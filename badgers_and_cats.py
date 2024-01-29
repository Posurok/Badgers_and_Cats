"""
Модификация стандартной змейки.

В чем отличия по сравнению с заданием:
- Переработана графика, разрешение увеличено до 1280 х 1100 пикселей.
- Добавлена система очков и бонус х1 х2 х3 за каждый 5 съеденных котов.
- Добавлено 4 типа разных "яблок" (число объектов зависит от скорости игры):
    Зеленый кот     - 30 очков и увеличивает скорость на "1".
    Красный кот     - 20 очков и увеличивает скорость на "1".
    Оранжевый кот   - 10 очков и увеличивает скорость на "1".
    Черно-белый кот - Замедляет скорость на "1", увеличивает бонус к очкам на 1
- Добавлен дружественный объект Барсук - 4шт., при пожирании дружественного
  объекта происходит уменьшение "змейки" на 3 секции.
- Game Over происходит, если змейка сожрала дружественный объект и стала = 0,
  либо если змейки сожрала саму себя.
- Объекты "Барсук" и "Черно-белый кот" - рандомно двигаются на одну клетку
  (скорость их движения зависит от скорости игры).

В случае поедания красного, оранжевого, зеленого котов - происходит
рандомизация положения ВСЕХ котов. Коты генерируются нового цвета.
В случае, если хочется изменить эту механику, необходимо удалить блок
(см. комментарии в коде)

В случае поедания черно-белого кота - не происходит изменение местоположения
других объектов, но в зависимости от скорости игры - происходит добавление
нового черно-белого кота.

В случае поедания дружественного объекта - происходит рандомизация положения
всех дружественных объектов и котов.
В случае, если хочется изменить эту механику, необходимо удалить блок
(см. комментарии в коде).
"""

from random import choice, randint
import pygame

# Инициализация PyGame.
pygame.init()

pygame.font.init()  # Инициализация модуля шрифтов.
font = pygame.font.SysFont('Arial', 16)
font_small = pygame.font.SysFont('Arial', 12)

# Константы для размеров поля и сетки.
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 960
GRID_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный.
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки.
BORDER_COLOR = (30, 30, 30)

# Цвет яблока.
APPLE_COLOR = (255, 0, 0)

# Цвет змейки.
SNAKE_COLOR = (30, 30, 30)

# Скорость движения змейки.
# SPEED = 4

# Настройка игрового окна.
MAX_APPLES = 5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 50),
                                 0, 32
                                 )

# Загружаем графику для змейки и изображения
# барсуков-препятствий (badger_friends).
badger_image = pygame.image.load('images/badger.png')
badger_friend_image = pygame.image.load('images/badger.png')

# Загружаем графику для яблок (котов) разных цветов.
cat_orange = pygame.image.load('images/cat.png')
cat_green = pygame.image.load('images/cat_green.png')
cat_red = pygame.image.load('images/cat_red.png')
black_cat = pygame.image.load('images/black_cat.png')

# Загружаем фотоновую картинку и картинку Game Over.
background_image = pygame.image.load('images/background.jpg')
background = pygame.transform.scale(background_image,
                                    (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_image = pygame.image.load('images/game_over.jpg')

# Заголовок окна игрового поля.
pygame.display.set_caption('Badgers & Cats')

# Настройка времени.
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для объектов Snake, Apple, Badger, BlackCat."""

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color


class Snake(GameObject):
    """
    Класс объекта Snake - отвечает за отрисовку
    и управление барсуком-змейкой.
    """

    def __init__(self):
        self.length = 1
        self.positions = [(10 * GRID_SIZE, 10 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        super().__init__(self.positions[0], SNAKE_COLOR)

    def update_direction(self):
        """Смена направления движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки."""
        cur = self.positions[0]
        x, y = self.direction
        new = (round(((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH)),
               round((cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
               )
        if new in self.positions[2:]:
            self.reset(screen)
        else:
            self.positions.insert(0, new)
            while len(self.positions) > (self.length + 1):
                self.positions.pop()

    def reset(self, surface):
        """Обновление игры."""
        self.length = 1
        self.positions = [(10 * GRID_SIZE, 10 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        surface.blit(game_over_image, (0, 0))
        pygame.display.update()
        # Пауза до нажатия пробела после окончания игры.
        waiting_for_space = True
        while waiting_for_space:
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_SPACE):
                    waiting_for_space = False

    def draw(self, surface):
        """Отрисовка отрисовка змейки."""
        for i, position in enumerate(self.positions[:-1]):
            if i % 2 == 0:
                badger_color = (40, 40, 40)
            else:
                badger_color = (80, 80, 80)

            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, badger_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки.
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        surface.blit(badger_image, head_rect)


class Apple(GameObject):
    """Класс объекта Apple - отвечает за отрисовку котов 3х разных цветов."""

    def __init__(self, position=(640, 480)):
        self.color = ['orange', 'red', 'green']
        body_color = choice(self.color)
        super().__init__(position, body_color)

    def randomize_position(self):
        """Установка рандомной позиции для кота."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.body_color = choice(self.color)

    def draw(self, surface):
        """Отрисовка кота."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )

        surface.blit(cat_orange, rect) if self.body_color == 'orange' else None
        surface.blit(cat_red, rect) if self.body_color == 'red' else None
        surface.blit(cat_green, rect) if self.body_color == 'green' else None


class Badger(GameObject):
    """
    Класс объекта Badger - отвечает за отрисовку и
    перемещение дружественных объектов.
    """

    def __init__(self, position=(640, 480), body_color=APPLE_COLOR):
        position = self.randomize_position()
        super().__init__(position, body_color)
        self.directions = [UP, DOWN, LEFT, RIGHT]

    def randomize_position(self):
        """Установка рандомной позиции для дружественного барсука."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE
                         )
        return self.position

    def randomize_move(self):
        """Случайное перемещение дружественного объекта."""
        direction = choice(self.directions)
        new_x = (self.position[0] + direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (self.position[1] + direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        self.position = (new_x, new_y)

    def draw(self, surface):
        """Отрисовка дружественного барсука."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        surface.blit(badger_friend_image, rect)


class BlackCat(Badger):
    """
    Класс объекта BlackCat - отвечает за отрисовку и
    перемещения черно-белого кота.
    """

    def __init__(self, position=(640, 480), body_color=APPLE_COLOR):
        super().__init__(position, body_color)

    def draw(self, surface):
        """Отрисовка черно-белого котка."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        surface.blit(black_cat, rect)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def update_direction(self):
    """Метод обновления направления после нажатия на кнопку."""
    if self.next_direction:
        self.direction = self.next_direction
        self.next_direction = None


def draw_length(surface, length, game_speed, score, bonus, apple_points):
    """Отрисовываем нижнюю часть экрана - счет, бонусы, скорость игры."""
    text = font.render('Длина барсука: ' + str(length)
                       + ' | Скорость барсука:' + str(game_speed)
                       + ' | СЧЕТ: ' + str(score)
                       + ' | БОНУС: x' + str(bonus),
                       True, (255, 255, 255))
    surface.blit(text, (10, 975))
    surface.blit(badger_friend_image, (1050, 965))
    badger_friend_text1 = font_small.render('Бонус х1',
                                            True, (255, 0, 0))
    badger_friend_text2 = font_small.render('Скорость +1',
                                            True, (255, 0, 0))
    badger_friend_text3 = font_small.render('Длина -3',
                                            True, (255, 0, 0))
    surface.blit(badger_friend_text1, (1100, 963))
    surface.blit(badger_friend_text2, (1100, 975))
    surface.blit(badger_friend_text3, (1100, 988))

    # Отрисовка котов с подсказкой внизу экрана.
    green_apple = apple_points['green'] * bonus
    red_apple = apple_points['red'] * bonus
    orange_apple = apple_points['orange'] * bonus

    surface.blit(black_cat, (600, 965))
    orange_apple_text = font.render('+ 1 БОНУС!',
                                    True, (255, 165, 0))
    surface.blit(orange_apple_text, (650, 975))

    surface.blit(cat_orange, (750, 965))
    orange_apple_text = font.render('+' + str(orange_apple),
                                    True, (255, 165, 0))
    surface.blit(orange_apple_text, (790, 975))

    surface.blit(cat_red, (850, 965))
    red_apple_text = font.render('+' + str(red_apple),
                                 True, (255, 0, 0))
    surface.blit(red_apple_text, (890, 975))

    surface.blit(cat_green, (950, 965))
    green_apple_text = font.render('+' + str(green_apple),
                                   True, (0, 128, 0))
    surface.blit(green_apple_text, (990, 975))


def add_apple(apples):
    """Функция добавления еще одного кота (зависит от скорости игры)."""
    new_apple = Apple()
    new_apple.randomize_position()
    apples.append(new_apple)


def main():
    """Тут нужно создать экземпляры классов."""
    game_speed = 3
    score = 0
    bonus = 1
    apple_for_bonus = 0
    frame_counter = 0  # Счетчик кадров.
    # Количество кадров между смещением объектов badger_friends.
    badger_move_interval = 15
    black_cat_move_interval = 30
    snake = Snake()
    badger_friends = [Badger() for _ in range(4)]
    apple = Apple()
    # Бонусы за котов разного цвета.
    apple_points = {'orange': 10, 'red': 20, 'green': 30}
    apples = [Apple() for _ in range(1)]
    apple.randomize_position()
    black_cat = BlackCat()

    while True:
        clock.tick(game_speed)
        frame_counter += 1
        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Перемещение дружественных объектов.
        if frame_counter % badger_move_interval == 0:
            for badger_friend in badger_friends:
                badger_friend.randomize_move()

        # Перемещение черно-белого кота.
        if frame_counter % black_cat_move_interval == 0:
            black_cat.randomize_move()

        # Проверка не съеден ли дружественный объект.
        for badger_friend in badger_friends:
            if snake.positions[0] == badger_friend.position:

                # Уменьшение змейки, ускорение игры, обнуление
                # счетчика съеденных котов (apple) уменьшение счетчика очков.
                snake.length -= 3
                game_speed += 2
                score -= 200
                apple_for_bonus = 0
                bonus = apple_for_bonus // 5 + 1

                # Добавление еще одного кота (apple), если превышено
                # определенное значение скорости.
                if game_speed % 5 == 0 and len(apples) < MAX_APPLES:
                    add_apple(apples)

                # Проверка змейки, если ее длина стала меньше 0 - конец игры.
                if snake.length <= 0:
                    snake.reset(screen)
                    game_speed = 3
                    score = 0
                    apples = [Apple() for _ in range(1)]

                # Если удалить этот блок, то при съедении одного из барсуков
                # не будет происходить рандомизация всех объектов.
                for apple in apples:
                    apple.randomize_position()

                for badger_friend in badger_friends:
                    badger_friend.randomize_position()

                # ------------------------------------------------------
                # в случае удаления блока - раскоментируйте строчку ниже.
                # badger_friend.randomize_position()

        if snake.positions[0] in snake.positions[1:]:
            snake.reset(screen)
            game_speed = 3
            score = 0
            apples = [Apple() for _ in range(1)]

        # Проверка не съеден ли объект черный кот.
        if snake.positions[0] == black_cat.position:
            game_speed -= 1
            apple_for_bonus += 5
            bonus = apple_for_bonus // 5 + 1
            black_cat.randomize_position()

        # Проверка не съеден ли один из котов.
        for apple in apples:
            if snake.positions[0] == apple.position:
                score += apple_points[apple.body_color] * bonus
                snake.length += 1
                game_speed += 1
                apple_for_bonus += 1
                bonus = apple_for_bonus // 5 + 1

                # Добавление еще одного кота (apple), если превышено
                # определенное значение скорости.
                if game_speed % 5 == 0 and len(apples) < MAX_APPLES:
                    add_apple(apples)

                # Если удалить этот блок, то при съедении одного из яблок
                # не будет происходить рандомизация всех объектов.
                for apple in apples:
                    apple.randomize_position()

                for badger_friend in badger_friends:
                    badger_friend.randomize_position()

                # -------------------------------------------------------
                # в случае удаления блока - раскоментируйте строчку ниже.
                # apple.randomize_position()

        # Обновление экрана.
        screen.fill(BOARD_BACKGROUND_COLOR)
        screen.blit(background, (0, 0))
        snake.draw(screen)
        black_cat.draw(screen) if game_speed > 15 else None

        for apple in apples:
            apple.draw(screen)

        for badger_friend in badger_friends:
            badger_friend.draw(screen)

        draw_length(screen, snake.length, game_speed,
                    score, bonus, apple_points)
        pygame.display.update()

        if frame_counter >= black_cat_move_interval:
            frame_counter = 0  # Сброс счетчика кадров.


if __name__ == '__main__':
    main()
