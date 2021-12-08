import pygame
import sys

from scripts import obstacle
from scripts.player import Player
from scripts.alien import Alien, Extra
from scripts.laser import Laser
from random import choice, randint

pygame.init()
pygame.mixer.init(44100, -16, 2, 512)
screen_width = 600
screen_height = 600
FPS = 60

bg_color = (30, 30, 30)

screen = pygame.display.set_mode((screen_width, screen_height))


class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Health and score setup
        self.lives = 3
        self.live_surface = pygame.image.load('Graphics/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surface.get_size()[0] * 2 + 20)

        self.score = 0
        self.font = pygame.font.Font('Font/Rose_Velt.ttf', 24)

        # Obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions,
                                       x_start=(screen_width - (screen_width / self.obstacle_amount *
                                                                (self.obstacle_amount - 1) + 11 * self.block_size)) / 2,
                                       y_start=screen_height - 120)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()

        # Extra
        # noinspection PyArgumentList
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400, 800)

        # Audio
        music = pygame.mixer.Sound('Sounds/bg_music.wav')
        music.set_volume(0.05)
        music.play(loops=-1)

        self.laser_sound = pygame.mixer.Sound('Sounds/laser_sound.wav')
        self.laser_sound.set_volume(0.3)
        self.explosion_sound = pygame.mixer.Sound('Sounds/explosion_sound.wav')
        self.explosion_sound.set_volume(0.1)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for x in offset:
            self.create_obstacle(x_start, y_start, x)

    def alien_setup(self, rows, cols, x_distance=60, y_distance=45, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, screen_height, 6)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), screen_width))
            self.extra_spawn_time = randint(400, 600)

    def collision_checks(self):

        # player laser
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()

                # extra collisions
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    laser.kill()
                    self.score += 500

        # alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # player collisions
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        # aliens
        if self.aliens:
            for alien in self.aliens:
                # obstacle collisions
                pygame.sprite.spritecollide(alien, self.blocks, True)

                # player collisions
                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surface.get_size()[0] + 10))
            screen.blit(self.live_surface, (x, 8))

    def display_score(self):
        text = self.font.render(f"Score: {self.score}", False, (255, 255, 255))
        screen.blit(text, (10, 8))

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('You won', False, (255, 255, 255))
            victory_rect = victory_surf.get_rect(center=(screen_width/2, screen_height/2))
            screen.blit(victory_surf, victory_rect)

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.extra.update()

        self.alien_position_checker()
        self.alien_lasers.update()
        self.extra_alien_timer()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.display_lives()
        self.display_score()
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.victory_message()


def main():
    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

        screen.fill(bg_color)
        game.run()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
