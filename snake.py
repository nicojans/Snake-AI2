import numpy as np
import pygame


class Game:

    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    DARK_GREY = (64, 64, 64)
    SIZE = 50
    FONT = 'comicsans'

    def __init__(self, width, height, walls_number, rewards):
        self._width = width
        self._height = height
        self._walls_number = walls_number
        self._rewards = rewards
        self._score = 0
        self._snake = None
        self._foods = None
        self._walls = None

    def reset(self):
        self._score = 0
        self._generate_snake()
        self._generate_walls()
        self._generate_foods()

    def move(self, direction):
        head = self._snake[0]
        new_head = None
        if direction == 0:
            new_head = self._translate(head, (0, -1))
        elif direction == 1:
            new_head = self._translate(head, (1, 0))
        elif direction == 2:
            new_head = self._translate(head, (0, 1))
        elif direction == 3:
            new_head = self._translate(head, (-1, 0))

        if self._is_dead(new_head):
            return False

        self._snake.insert(0, new_head)
        if not self._is_food(new_head):
            self._snake.pop()
        else:
            if len(self._snake) == self._width * self._height:
                return False
            else:
                self._score += self._generate_new_food(new_head)
        return True

    def state(self):
        image = np.zeros((2 * self._width + 1, 2 * self._height + 1, 3))
        x = self._width - self._snake[0][0]
        y = self._height - self._snake[0][1]
        count = len(self._snake)
        for elem in self._snake:
            pos = self._translate(elem, (x, y))
            image[pos[0]][pos[1]][0] = count
            count -= 1

        for wall in self._walls:
            pos = self._translate(wall, (x, y))
            image[pos[0]][pos[1]][1] = 1

        for food in self._foods:
            pos = self._translate(food[0:2], (x, y))
            image[pos[0]][pos[1]][2] = food[2]

        return image

    def play_new_game(self, speed, ai_next_movement=None):
        self.reset()
        game_width = self._width * self.SIZE
        game_height = self._height * self.SIZE
        pygame.init()
        screen = pygame.display.set_mode((game_width, game_height))
        counter = 0
        direction = 1
        done = False
        alive = True
        step = 0

        clock = pygame.time.Clock()
        font_score = pygame.font.SysFont(self.FONT, 20)
        font_game_over = pygame.font.SysFont(self.FONT, 50)

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.reset()
                    alive = True
                    direction = 1
                    step = 0
            if alive:
                if ai_next_movement is None:
                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_UP]:
                        direction = 0
                    if pressed[pygame.K_RIGHT]:
                        direction = 1
                    if pressed[pygame.K_DOWN]:
                        direction = 2
                    if pressed[pygame.K_LEFT]:
                        direction = 3
                else:
                    direction = ai_next_movement(self.state())

            counter += 1
            if counter == speed:
                alive = self.move(direction)
                counter = 0
                step += 1

            screen.fill((0, 0, 0))
            if alive:
                previous_elem = None
                size = int(self.SIZE * 0.8)
                double_size = int(self.SIZE * 1.8)
                offset = int(self.SIZE * 0.1)
                for elem in self._snake:
                    if previous_elem is None:
                        rect = pygame.Rect(elem[0] * self.SIZE, elem[1] * self.SIZE, self.SIZE, self.SIZE)
                        pygame.draw.rect(screen, self.GREEN, rect)
                    else:
                        if elem[0] - previous_elem[0] == 1:
                            rect = pygame.Rect((elem[0] - 1) * self.SIZE + offset, elem[1] * self.SIZE + offset, double_size, size)
                        elif elem[0] - previous_elem[0] == -1:
                            rect = pygame.Rect(elem[0] * self.SIZE + offset, elem[1] * self.SIZE + offset, double_size, size)
                        elif elem[1] - previous_elem[1] == 1:
                            rect = pygame.Rect(elem[0] * self.SIZE + offset, (elem[1] - 1) * self.SIZE + offset, size, double_size)
                        elif elem[1] - previous_elem[1] == -1:
                            rect = pygame.Rect(elem[0] * self.SIZE + offset, elem[1] * self.SIZE + offset, size, double_size)
                        pygame.draw.rect(screen, self.BLUE, rect)
                    previous_elem = elem
                for wall in self._walls:
                    rect = pygame.Rect(wall[0] * self.SIZE, wall[1] * self.SIZE, self.SIZE, self.SIZE)
                    pygame.draw.rect(screen, self.DARK_GREY, rect)
                    rect = pygame.Rect(wall[0] * self.SIZE + int(self.SIZE * 0.1), wall[1] * self.SIZE +
                                       int(self.SIZE * 0.1), int(self.SIZE * 0.8), int(self.SIZE * 0.8))
                    pygame.draw.rect(screen, self.GREY, rect)
                for food in self._foods:
                    rect = pygame.Rect(food[0] * self.SIZE, food[1] * self.SIZE, self.SIZE, self.SIZE)
                    pygame.draw.circle(screen, (10 * food[2], 0, 0), rect.center, int(self.SIZE * 0.4))
                text = font_score.render(str(self._score), True, self.WHITE)
                screen.blit(text, (game_width - text.get_width(), 15))
            else:
                text1 = font_game_over.render('GAME OVER', True, self.WHITE)
                text2 = font_game_over.render('Score: ' + str(self._score), True, self.WHITE)
                screen.blit(text1, ((game_width - text1.get_width()) / 2, (game_height - text1.get_height()) / 2 - 25))
                screen.blit(text2, ((game_width - text2.get_width()) / 2, (game_height - text2.get_height()) / 2 + 25))

            pygame.display.flip()

            clock.tick(60)

    def _generate_snake(self):
        h = int(self._height / 2)
        self._snake = [(3, h), (2, h), (1, h), (0, h)]

    def _generate_foods(self):
        self._foods = []
        for i in self._rewards:
            food = None
            while food is None:
                new_food = (np.random.randint(0, self._width), np.random.randint(0, self._height), i)
                food = new_food if not self._is_dead(new_food[0:2]) and not self._is_food(new_food[0:2]) else None
            self._foods += [new_food]

    def _generate_new_food(self, block):
        eaten_food = None
        reward = 0
        for food in self._foods:
            if food[0:2] == block:
                eaten_food = food
                reward = food[2]
        self._foods.remove(eaten_food)
        if len(self._snake) + len(self._rewards) + self._walls_number <= self._width * self._height:
            food = None
            while food is None:
                new_food = (np.random.randint(0, self._width), np.random.randint(0, self._height), reward)
                food = new_food if not self._is_dead(new_food[0:2]) and not self._is_food(new_food[0:2]) else None
            self._foods.append(new_food)
        return reward

    def _generate_walls(self):
        self._walls = []

        for x in range(0, self._width):
            self._walls += [(x, -1)]
            self._walls += [(x, self._height)]

        for y in range(0, self._height):
            self._walls += [(-1, y)]
            self._walls += [(self._width, y)]

        for i in range(0, self._walls_number):
            wall = None
            while wall is None:
                wall = (np.random.randint(0, self._width), np.random.randint(0, self._height))
                if wall[1] == int(self._height / 2):
                    wall = None
                else:
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if (x + y) % 2 == 0 and wall is not None and self._is_wall(self._translate(wall, (x, y))):
                                wall = None
            self._walls += [wall]

    def _is_dead(self, block):
        return self._is_wall(block) or self._is_snake(block)

    def _is_wall(self, block):
        for wall in self._walls:
            if wall == block:
                return True
        return False

    def _is_snake(self, block):
        for elem in self._snake:
            if elem == block:
                return True
        return False

    def _is_food(self, block):
        for food in self._foods:
            if food[0:2] == block:
                return True
        return False

    @staticmethod
    def _translate(block, translation):
        return block[0] + translation[0], block[1] + translation[1]

    @property
    def score(self):
        return self._score
