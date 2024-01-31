"""
Modification of the standard snake game.

Differences compared to the original assignment:
- Graphics have been revamped, resolution increased to 1280 x 1100 pixels.
- A scoring system has been added with a bonus of x1 x2 x3 for
  every 5 cats eaten.
- Added 4 types of different "apples"
  (the number of objects depends on the game's speed):
    Green Cat - 30 points and increases speed by "1".
    Red Cat - 20 points and increases speed by "1".
    Orange Cat - 10 points and increases speed by "1".
    Black-and-White Cat - Slows down speed by "1", increases score bonus by 1.
- Added friendly Badger object - 4 pcs., eating a friendly object reduces
  the "snake" by 3 sections.
- Game Over occurs if the snake eats a friendly object and becomes = 0,
  or if the snake eats itself.
- "Badger" and "Black-and-White Cat" objects move randomly by one cell
  (their speed of movement depends on the game's speed).

In the case of eating red, orange, green cats - all cats' positions are
randomized. The cats are generated in new colors.
If you want to change this mechanic, you need to delete the block
(see comments in the code).

In the case of eating a black-and-white cat - there is no change in the
location of other objects, but depending on the game's speed - a new
black-and-white cat is added.

In the case of eating a friendly object - the position of all friendly
objects and cats is randomized.
If you want to change this mechanic, you need to delete the block
(see comments in the code).
"""

from random import choice, randint
import pygame

# PyGame initialization.
pygame.init()

pygame.font.init()  # Initializing the font module.
font = pygame.font.SysFont('Arial', 16)
font_small = pygame.font.SysFont('Arial', 12)

# Constants for field and grid sizes.
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 960
GRID_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Константы для начальной позиции змейки:
START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Movement directions.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Background color - black.
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Cell border color.
BORDER_COLOR = (30, 30, 30)

# Apple color.
APPLE_COLOR = (255, 0, 0)

# Snake color.
SNAKE_COLOR = (30, 30, 30)

# Snake movement speed.
# SPEED = 4

# Setting up the game window.
MAX_APPLES = 5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 50),
                                 0, 32)

# Loading graphics for snake and badger friends (obstacles).
badger_image = pygame.image.load('images/badger.png')
badger_friend_image = pygame.image.load('images/badger.png')

# Loading graphics for differently colored cats (apples).
cat_orange = pygame.image.load('images/cat.png')
cat_green = pygame.image.load('images/cat_green.png')
cat_red = pygame.image.load('images/cat_red.png')
black_cat = pygame.image.load('images/black_cat.png')

# Loading the background picture and Game Over image.
background_image = pygame.image.load('images/background.jpg')
background = pygame.transform.scale(background_image,
                                    (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_image = pygame.image.load('images/game_over.jpg')

# Game field window title.
pygame.display.set_caption('Badgers & Cats')

# Time setup.
clock = pygame.time.Clock()

class GameObject:
    """Base class for objects such as Snake, Apple, Badger, BlackCat."""

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

class Snake(GameObject):
    """
    Snake object class - responsible for rendering
    and controlling the badger-snake.
    """

    def __init__(self):
        self.length = 1
        self.positions = [(10 * GRID_SIZE, 10 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        super().__init__(self.positions[0], SNAKE_COLOR)

    def update_direction(self):
        """Changing the movement direction."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Snake movement."""
        cur = self.positions[0]
        x, y = self.direction
        new = (round(((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH)),
               round((cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT))
        self.positions.insert(0, new)
        while len(self.positions) > (self.length + 1):
            self.positions.pop()

    def reset(self, surface):
        """Game reset."""
        self.length = 1
        self.positions = [(10 * GRID_SIZE, 10 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        surface.blit(game_over_image, (0, 0))
        pygame.display.update()
        # Pause until spacebar is pressed after game over.
        waiting_for_space = True
        while waiting_for_space:
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_SPACE):
                    waiting_for_space = False



    def draw(self, surface):
        """Rendering the snake."""
        for i, position in enumerate(self.positions[:-1]):
            if i % 2 == 0:
                badger_color = (40, 40, 40)
            else:
                badger_color = (80, 80, 80)

            rect = pygame.Rect((position[0], position[1]),
                               (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, badger_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Drawing the snake's head.
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        surface.blit(badger_image, head_rect)


class Apple(GameObject):
    """
    Apple object class - responsible for
    rendering cats of 3 different colors.
    """

    def __init__(self, position=START_POSITION):
        self.color = ['orange', 'red', 'green']
        body_color = choice(self.color)
        super().__init__(position, body_color)

    def randomize_position(self):
        """Randomizing the position for a cat."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.body_color = choice(self.color)

    def draw(self, surface):
        """Rendering the cat."""
        rect = pygame.Rect((self.position[0], self.position[1]),
                           (GRID_SIZE, GRID_SIZE))

        if self.body_color == 'orange':
            surface.blit(cat_orange, rect)
        elif self.body_color == 'red':
            surface.blit(cat_red, rect)
        elif self.body_color == 'green':
            surface.blit(cat_green, rect)


class Badger(GameObject):
    """
    Badger object class - responsible for rendering and
    moving friendly objects.
    """

    def __init__(self, position=START_POSITION, body_color=APPLE_COLOR):
        position = self.randomize_position()
        super().__init__(position, body_color)
        self.directions = [UP, DOWN, LEFT, RIGHT]

    def randomize_position(self):
        """Randomizing position for a friendly badger."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        return self.position

    def randomize_move(self):
        """Randomly moving a friendly object."""
        direction = choice(self.directions)
        new_x = (self.position[0] + direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (self.position[1] + direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        self.position = (new_x, new_y)

    def draw(self, surface):
        """Rendering a friendly badger."""
        rect = pygame.Rect((self.position[0], self.position[1]),
                           (GRID_SIZE, GRID_SIZE))
        surface.blit(badger_friend_image, rect)


class BlackCat(Badger):
    """
    BlackCat object class - responsible for rendering and
    moving a black-and-white cat.
    """

    def __init__(self, position=START_POSITION, body_color=APPLE_COLOR):
        super().__init__(position, body_color)

    def draw(self, surface):
        """Rendering a black-and-white cat."""
        rect = pygame.Rect((self.position[0], self.position[1]),
                           (GRID_SIZE, GRID_SIZE))
        surface.blit(black_cat, rect)

def handle_keys(game_object):
    """Function to handle user actions."""
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
    """Method for updating direction after pressing a button."""
    if self.next_direction:
        self.direction = self.next_direction
        self.next_direction = None


def draw_length(surface, length, game_speed, score, bonus, apple_points):
    """Rendering the lower part of the screen - score, bonuses, game speed."""
    text = font.render('Badger length: ' + str(length)
                       + ' | Badger Speed:' + str(game_speed)
                       + ' | Score: ' + str(score)
                       + ' | BONUS: x' + str(bonus),
                       True, (255, 255, 255))
    surface.blit(text, (10, 975))
    surface.blit(badger_friend_image, (1050, 965))
    badger_friend_text1 = font_small.render('Bonus x1',
                                            True, (255, 0, 0))
    badger_friend_text2 = font_small.render('Speed +1',
                                            True, (255, 0, 0))
    badger_friend_text3 = font_small.render('Length -3',
                                            True, (255, 0, 0))
    surface.blit(badger_friend_text1, (1100, 963))
    surface.blit(badger_friend_text2, (1100, 975))
    surface.blit(badger_friend_text3, (1100, 988))

    # Rendering cats with hints at the bottom of the screen.
    green_apple = apple_points['green'] * bonus
    red_apple = apple_points['red'] * bonus
    orange_apple = apple_points['orange'] * bonus

    surface.blit(black_cat, (600, 965))
    orange_apple_text = font.render('+ 1 BONUS!',
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
    """Function to add another cat (depends on game speed)."""
    new_apple = Apple()
    new_apple.randomize_position()
    apples.append(new_apple)


def main():
    """Here we need to create instances of classes."""
    game_speed = 3
    score = 0
    bonus = 1
    apple_for_bonus = 0
    frame_counter = 0  # Frame counter.
    # Number of frames between movements of badger_friends objects.
    badger_move_interval = 15
    black_cat_move_interval = 30
    snake = Snake()
    badger_friends = [Badger() for _ in range(4)]
    apple = Apple()
    # Bonuses for cats of different colors.
    apple_points = {'orange': 10, 'red': 20, 'green': 30}
    apples = [Apple() for _ in range(1)]
    apple.randomize_position()
    black_cat = BlackCat()

    while True:
        clock.tick(game_speed)
        frame_counter += 1
        # Describe the main logic of the game here.
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Moving friendly objects.
        if frame_counter % badger_move_interval == 0:
            for badger_friend in badger_friends:
                badger_friend.randomize_move()

        # Moving the black-and-white cat.
        if frame_counter % black_cat_move_interval == 0:
            black_cat.randomize_move()

        # Check if a friendly object is eaten.
        for badger_friend in badger_friends:
            if snake.positions[0] == badger_friend.position:

                # Reducing snake length, increasing game speed, resetting
                # the count of eaten cats (apples) and decreasing the score.
                snake.length -= 3
                game_speed += 2
                score -= 200
                apple_for_bonus = 0
                bonus = apple_for_bonus // 5 + 1

                # Adding another apple (cat) if the game speed exceeds
                # a certain value.
                if game_speed % 5 == 0 and len(apples) < MAX_APPLES:
                    add_apple(apples)

                # Checking the snake, if its length becomes
                # less than 0 - game over.
                if snake.length <= 0:
                    snake.reset(screen)
                    game_speed = 3
                    score = 0
                    apples = [Apple() for _ in range(1)]

                # If you delete this block, then eating one of the badgers
                # will not trigger the randomization of all objects.
                for apple in apples:
                    apple.randomize_position()

                for badger_friend in badger_friends:
                    badger_friend.randomize_position()

                # ------------------------------------------------------
                # in case of block removal - uncomment the line below.
                # badger_friend.randomize_position()

        if snake.positions[0] in snake.positions[1:]:
            snake.reset(screen)
            score = 0
            game_speed = 3
            apples = [Apple() for _ in range(1)]

        # Checking if the black cat object is eaten.
        if snake.positions[0] == black_cat.position:
            game_speed -= 1
            apple_for_bonus += 5
            bonus = apple_for_bonus // 5 + 1
            black_cat.randomize_position()

        # Checking if one of the cats is eaten.
        for apple in apples:
            if snake.positions[0] == apple.position:
                score += apple_points[apple.body_color] * bonus
                snake.length += 1
                game_speed += 1
                apple_for_bonus += 1
                bonus = apple_for_bonus // 5 + 1

                # Adding another apple (cat) if the game speed exceeds
                # a certain value.
                if game_speed % 5 == 0 and len(apples) < MAX_APPLES:
                    add_apple(apples)

                # If you delete this block, then eating one of the apples
                # will not trigger the randomization of all objects.
                for apple in apples:
                    apple.randomize_position()

                for badger_friend in badger_friends:
                    badger_friend.randomize_position()

                # -------------------------------------------------------
                # in case of block removal - uncomment the line below.
                # apple.randomize_position()

        # Refreshing the screen.
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
            frame_counter = 0  # Resetting the frame counter.


if __name__ == '__main__':
    main()
