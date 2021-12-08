import pygame
import sys
import random

from pygame.math import Vector2

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.font.init()
cell_size = 40
cell_number = 19
WIDTH, HEIGHT = cell_size * cell_number, cell_size * cell_number,

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake!")
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

cherry = pygame.image.load('Graphics/cherry.png').convert_alpha()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FPS = 60


class Fruit:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pos = 0
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        WIN.blit(cherry, fruit_rect)
        # pygame.draw.rect(WIN, RED, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.head = None
        self.tail = None
        self.corner = None

        # Graphics
        self.head_up = pygame.image.load("Graphics/head-up.png").convert_alpha()
        self.head_down = pygame.image.load("Graphics/head-down.png").convert_alpha()
        self.head_left = pygame.image.load("Graphics/head-left.png").convert_alpha()
        self.head_right = pygame.image.load("Graphics/head-right.png").convert_alpha()

        self.tail_up = pygame.image.load("Graphics/tail-up.png").convert_alpha()
        self.tail_down = pygame.image.load("Graphics/tail-down.png").convert_alpha()
        self.tail_left = pygame.image.load("Graphics/tail-left.png").convert_alpha()
        self.tail_right = pygame.image.load("Graphics/tail-right.png").convert_alpha()

        self.body_horizontal = pygame.image.load("Graphics/body_horizontal.png").convert_alpha()
        self.body_vertical = pygame.image.load("Graphics/body_vertical.png").convert_alpha()

        self.body_corner_left = pygame.image.load("Graphics/body_corner_left.png").convert_alpha()
        self.body_corner_up = pygame.image.load("Graphics/body_corner_up.png").convert_alpha()
        self.body_corner_right = pygame.image.load("Graphics/body_corner_right.png").convert_alpha()
        self.body_corner_down = pygame.image.load("Graphics/body_corner_down.png").convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sound/Crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):  # enumerate gives index to a object
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                WIN.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                WIN.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    WIN.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    WIN.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        WIN.blit(self.body_corner_left, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        WIN.blit(self.body_corner_down, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        WIN.blit(self.body_corner_up, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        WIN.blit(self.body_corner_right, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class MAIN:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = 0
        self.font = pygame.font.Font("Rose_Velt.ttf", 32)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def show_score(self):
        sc = self.font.render("Score : " + str(self.score), True, (232, 23, 159))
        WIN.blit(sc, (5, 5))

    def draw_elements(self):
        self.draw_background()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.show_score()

    @staticmethod
    def draw_background():
        WIN.fill((170, 245, 93))
        grid_color = (204, 255, 153)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        bg_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(WIN, grid_color, bg_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        bg_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(WIN, grid_color, bg_rect)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.score += 1
            self.snake.play_crunch_sound()

            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()

    def save_score(self):
        file = open("score.txt", 'a')
        file.write("\n")
        file.write(str(self.score))
        file.close()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.save_score()
        sort()
        self.score = 0
        self.snake.reset()


def sort():
    with open("score.txt") as f:
        sc = f.read().split("\n")

    le = len(sc)

    for i in range(0, le - 1):
        for j in range(i + 1, le):
            if int(sc[j]) > int(sc[i]):
                sc[j], sc[i] = sc[i], sc[j]

    file = open("score.txt", "w")
    if len(sc) > 10:
        for i in range(0, 10):
            if i == 0:
                file.write(sc[i])
            else:
                file.write("\n")
                file.write(sc[i])
    else:
        for i in range(0, len(sc)):
            if i == 0:
                file.write(sc[i])
            else:
                file.write("\n")
                file.write(sc[i])

    file.close()


def main():
    clock = pygame.time.Clock()
    main_game = MAIN()

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.font.quit()
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)

        main_game.draw_elements()
        pygame.display.update()


if __name__ == "__main__":
    main()
