import pygame
import sys
import random

pygame.init()
pygame.font.init()

cell_size = 50

screen_width = 700
screen_height = 800
FPS = 60

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 200)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris!')

shapes = [
            ['xxx'],
            ['x',
             'x',
             'x'],
            ['xxx',
             '  x']
        ]

colors = ['yellow', 'blue', 'purple', 'orange', 'green']

LIGHT_GRAY = (128, 128, 128)


class Block(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, color):
        super().__init__()
        self.image = pygame.Surface((cell_size, cell_size))
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.image.fill(color)
        self.speed = cell_size

    def update(self):
        self.rect.y += self.speed

        if self.rect.y >= screen_height:
            self.rect.y = screen_height - cell_size - 10
            self.speed = 0


class Game:
    def __init__(self):
        self.sc_width = screen_width - 250
        self.sc_height = screen_height - (cell_size * 2)
        self.game_surface = pygame.Surface((self.sc_width, self.sc_height))
        self.blocks = pygame.sprite.Group()

    def create_block(self):
        color = random.choice(colors)
        for row_index, row in enumerate(random.choice(shapes)):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = col_index * cell_size
                    y = row_index * cell_size
                    block = Block(x, y, color)
                    self.blocks.add(block)

    def update(self):
        self.blocks.update()

    def draw_blocks(self):
        self.blocks.draw(self.game_surface)

    def run(self):
        self.draw_game_box()
        self.draw_blocks()
        self.draw_grid()

    def draw_game_box(self):
        screen.fill('black')

        box = pygame.Rect(cell_size - 1, cell_size - 1, self.sc_width + 2, self.sc_height + 2)
        pygame.draw.rect(screen, 'red', box)
        self.game_surface.fill('black')

        screen.blit(self.game_surface, (cell_size, cell_size))

    def draw_grid(self):
        # Drawing a grid
        for width in range(cell_size, self.sc_width, cell_size):
            pygame.draw.line(self.game_surface, LIGHT_GRAY, (width, 0), (width, self.sc_height), 1)

        for height in range(cell_size, self.sc_height, cell_size):
            pygame.draw.line(self.game_surface, LIGHT_GRAY, (0, height), (self.sc_width, height), 1)

        screen.blit(self.game_surface, (cell_size, cell_size))


def main():
    clock = pygame.time.Clock()
    game = Game()
    game.create_block()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                game.update()

        game.run()
        pygame.display.update()


if __name__ == '__main__':
    main()
