import pygame
import sys
from random import choice

pygame.init()
pygame.font.init()

cell_size = 40

screen_width = 700
screen_height = 800
FPS = 60

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 360)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris!')

_ = [['....',
      'xxxx',
      '....',
      '....'],
     ['..x.',
      '..x.',
      '..x.',
      '..x.']]

L = [['.x..',
      '.x..',
      '.xx.',
      '....'],
     ['....',
      'xxx.',
      'x...',
      '....'],
     ['xx..',
      '.x..',
      '.x..',
      '....'],
     ['..x.',
      'xxx.',
      '....',
      '....']]

J = [['.x..',
      '.x..',
      'xx.',
      '....'],
     ['x...',
      'xxx.',
      '....',
      '....'],
     ['.xx.',
      '.x..',
      '.x..',
      '....'],
     ['....',
      'xxx.',
      '..x.',
      '....']]

T = [['.x..',
      'xxx.',
      '....',
      '....'],
     ['.x..',
      '.xx.',
      '.x..',
      '....'],
     ['....',
      'xxx.',
      '.x..',
      '....'],
     ['.x..',
      'xx..',
      '.x..',
      '....']]

Z = [['xx..',
      '.xx.',
      '....',
      '....'],
     ['..x.',
      '.xx.',
      '.x..',
      '....']]

S = [['..xx',
      '.xx.',
      '....',
      '....'],
     ['.x..',
      '.xx.',
      '..x.',
      '....']]

o = [['....',
      '.xx.',
      '.xx.',
      '....']]

shapes = [_, L, J, T, Z, S, o]

LIGHT_GRAY = (128, 128, 128)


class Block:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = 'green'
        self.rotation = 0


class Game:
    def __init__(self):
        self.sc_width = 10
        self.sc_height = 18
        self.game_surface = pygame.Surface((self.sc_width * cell_size, self.sc_height * cell_size))
        self.board = [[False for _ in range(self.sc_width)] for __ in range(self.sc_height)]
        self.current_block = Block((self.sc_width // 2) - 2, 0, choice(shapes))
        self.next_block = self.create_block()
        self.score = 0

        self.block_move = 1

    def run(self):
        self.draw_game_box()
        self.draw_current_block()
        self.draw_board()
        self.draw_grid()

        self.show_next_block()
        self.show_score()

        screen.blit(self.game_surface, (cell_size, cell_size))

    def convert_shape_format(self, next_rotation=False, next_block=False):
        positions = [[False for _ in range(4)] for __ in range(4)]
        if next_block:
            form = self.next_block.shape[0]
        else:
            if next_rotation:
                form = self.current_block.shape[(self.current_block.rotation + 1) % len(self.current_block.shape)]
            else:
                form = self.current_block.shape[self.current_block.rotation % len(self.current_block.shape)]

        for i, row in enumerate(form):
            for j, column in enumerate(row):
                if column == 'x':
                    positions[i][j] = True

        return positions

    def real_block_positions(self, next_rotation=False):
        if not next_rotation:
            positions = self.convert_shape_format()
        else:
            positions = self.convert_shape_format(next_rotation=True)

        real_positions = []

        for i, row in enumerate(positions):
            for j, col in enumerate(row):
                if positions[i][j]:
                    real_positions.append((self.current_block.x + j, self.current_block.y + i))

        return real_positions

    def show_score(self):
        font = pygame.font.SysFont("comicsansms", 40)
        text = font.render(f'Score:', True, (200, 100, 60))
        value = font.render(f'{self.score}', True, (200, 100, 60))
        screen.blit(text, (screen_width - 210, 50))
        screen.blit(value, (screen_width - 160, 90))

    def show_next_block(self):
        font = pygame.font.SysFont("comicsansms", 40)
        text = font.render("Next Block", True, (180, 150, 20))
        screen.blit(text, (screen_width - 230, 180))

        block_positions = self.convert_shape_format(next_block=True)
        for i, row in enumerate(block_positions):
            for j, column in enumerate(row):
                if block_positions[i][j]:
                    box = pygame.Rect(self.next_block.x + j * cell_size, self.next_block.y + i * cell_size,
                                      cell_size - 1, cell_size - 1)
                    pygame.draw.rect(screen, self.next_block.color, box)

    def create_block(self):
        return Block(screen_width - 210, 250, choice(shapes))

    def check_lose(self):
        for i in range(self.sc_width):
            if self.board[0][i]:
                self.score = 0
                del self.current_block
                self.board = [[False for _ in range(self.sc_width)] for __ in range(self.sc_height)]
                self.pass_next_block()

    def check_row(self):
        for i, row in enumerate(self.board):
            positive = 0  # number of True's
            for cell in row:
                if cell:
                    positive += 1
            if positive == self.sc_width:
                self.del_row(i)
                self.score += 100

    def del_row(self, row):
        for y in range(self.sc_width):
            self.board[row][y] = False

        while row > 0:
            positive = 0
            for y in range(self.sc_width):
                if self.board[row - 1][y]:
                    positive += 1
                self.board[row][y], self.board[row - 1][y] = self.board[row - 1][y], self.board[row][y]  # Swap values
            if positive == 0:
                break
            row -= 1

    def draw_board(self):
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                if self.board[i][j]:
                    box = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                    pygame.draw.rect(self.game_surface, 'red', box)

    def draw_current_block(self):
        block_positions = self.convert_shape_format()
        x = self.current_block.x * cell_size
        y = self.current_block.y * cell_size

        for i, row in enumerate(block_positions):
            for j, column in enumerate(row):
                if block_positions[i][j]:
                    box = pygame.Rect(x + j * cell_size, y + i * cell_size, cell_size, cell_size)
                    pygame.draw.rect(self.game_surface, self.current_block.color, box)

    def update(self):
        self.current_block.y += self.block_move
        self.hit_ground()
        self.check_collisions()
        self.check_row()
        self.check_lose()

    def check_collisions(self):
        real_pos_block = self.real_block_positions()
        for pos in real_pos_block:
            if self.board[pos[1]][pos[0]]:
                self.block_move = 0
                for pos1 in real_pos_block:
                    self.board[pos1[1] - 1][pos1[0]] = True

                self.pass_next_block()
                break

    def hit_ground(self):
        max_y = check_matrix_max_y(self.convert_shape_format()) + self.current_block.y
        if max_y >= self.sc_height:
            real_positions = self.real_block_positions()
            self.block_move = 0
            for pos in real_positions:
                self.board[pos[1] - 1][pos[0]] = True

            del self.current_block
            self.pass_next_block()

    def pass_next_block(self):
        self.current_block = self.next_block
        self.current_block.x, self.current_block.y = (self.sc_width // 2) - 2, 0
        self.next_block = self.create_block()
        self.block_move = 1

    def draw_game_box(self):
        screen.fill('black')

        box = pygame.Rect(cell_size - 1, cell_size - 1, self.sc_width * cell_size + 2, self.sc_height * cell_size + 2)
        pygame.draw.rect(screen, 'red', box)
        self.game_surface.fill('black')

    def draw_grid(self):
        # Drawing a grid
        for width in range(cell_size, self.sc_width * cell_size, cell_size):
            pygame.draw.line(self.game_surface, LIGHT_GRAY, (width, 0), (width, self.sc_height * cell_size), 1)

        for height in range(cell_size, self.sc_height * cell_size, cell_size):
            pygame.draw.line(self.game_surface, LIGHT_GRAY, (0, height), (self.sc_width * cell_size, height), 1)


def check_matrix_min_x(positions):
    for x in range(4):
        for y in range(4):
            if positions[y][x]:
                return x


def check_matrix_max_x(positions):
    for x in range(3, -1, -1):
        for y in range(4):
            if positions[y][x]:
                return x


def check_matrix_max_y(positions):
    for x in range(3, -1, -1):
        for y in range(4):
            if positions[x][y]:
                return x


def main():
    clock = pygame.time.Clock()
    game = Game()
    while True:
        clock.tick(FPS)
        positions = game.convert_shape_format()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.font.quit()
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    real_begin = game.current_block.x + check_matrix_min_x(positions)
                    possible_move = True

                    if real_begin > 0:
                        real_pos = game.real_block_positions()

                        most_to_the_left = []
                        for pos in real_pos:
                            if pos[0] == real_begin:
                                most_to_the_left.append((pos[0], pos[1]))

                        for pos in most_to_the_left:
                            if game.board[pos[1]][pos[0] - 1]:
                                possible_move = False

                    if real_begin > 0 and possible_move:
                        game.current_block.x -= 1

                if event.key == pygame.K_RIGHT:
                    real_end = game.current_block.x + check_matrix_max_x(positions)
                    possible_move = True

                    if real_end < game.sc_width - 1:
                        real_pos = game.real_block_positions()

                        most_to_the_right = []
                        for pos in real_pos:
                            if pos[0] == real_end:
                                most_to_the_right.append((pos[0], pos[1]))

                        for pos in most_to_the_right:
                            if game.board[pos[1]][pos[0] + 1]:
                                possible_move = False

                    if (real_end < game.sc_width - 1) and possible_move:
                        game.current_block.x += 1

                if event.key == pygame.K_UP:
                    next_positions = game.convert_shape_format(True)
                    next_rotation_real_begin = game.current_block.x + check_matrix_min_x(next_positions)
                    next_rotation_real_end = game.current_block.x + check_matrix_max_x(next_positions)
                    blocked_rotation = False

                    # Check if possible to rotate between locked positions
                    if next_rotation_real_begin > 0 and next_rotation_real_end < game.sc_width - 1:
                        real_pos_block = game.real_block_positions(next_rotation=True)
                        for pos in real_pos_block:
                            if game.board[pos[1]][pos[0]]:
                                blocked_rotation = True
                                break

                    if next_rotation_real_begin < 0 or next_rotation_real_end > game.sc_width - 1 or blocked_rotation:
                        pass
                    else:
                        game.current_block.rotation += 1

                if event.key == pygame.K_DOWN:
                    # if (check_matrix_max_y(positions) + game.current_block.y+1) < (game.sc_height - 1):
                    pygame.time.set_timer(SCREEN_UPDATE, 120)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pygame.time.set_timer(SCREEN_UPDATE, 360)

        game.run()
        pygame.display.update()


if __name__ == '__main__':
    main()
