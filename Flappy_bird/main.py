import pygame
import sys
import random

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

screen_width = 580
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))

bg = pygame.image.load("graphics/background-day.png").convert()
bg = pygame.transform.scale(bg, (screen_width, screen_height))

# Game variables
gravity = 0.25
game_font = pygame.font.Font('font/04B_19.TTF', 40)

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)


class Bird:
    def __init__(self):
        self.midflap = pygame.transform.scale2x(pygame.image.load("graphics/bluebird-midflap.png").convert_alpha())
        self.downflap = pygame.transform.scale2x(pygame.image.load('graphics/bluebird-downflap.png').convert_alpha())
        self.upflap = pygame.transform.scale2x(pygame.image.load('graphics/bluebird-upflap.png').convert_alpha())
        self.frames = [self.downflap, self.midflap, self.upflap]
        self.index = 0
        self.image = self.frames[self.index]

        self.rect = self.image.get_rect(center=(100, screen_height/2))
        self.movement = 0

        self.flap_sound = pygame.mixer.Sound('audio/sfx_wing.wav')

    def draw(self):
        rotated_bird = self.rotate_bird()
        screen.blit(rotated_bird, self.rect)

    def rotate_bird(self):
        new_bird = pygame.transform.rotozoom(self.image, self.movement * -3, 1)
        return new_bird

    def bird_animation(self):
        new_bird = self.frames[self.index]
        new_bird_rect = new_bird.get_rect(center=(100, self.rect.centery))
        return new_bird, new_bird_rect

    def move(self):
        self.movement += gravity
        self.rect.centery += self.movement


class Floor:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = int(screen_height - screen_height / 6)
        self.floor_surface = pygame.image.load("graphics/base.png").convert()
        self.floor_surface = pygame.transform.scale2x(self.floor_surface)
        self.floor_surface1 = self.floor_surface

        self.x1_pos = self.floor_surface.get_width()

    def display(self):
        screen.blit(self.floor_surface, (self.x_pos, self.y_pos))
        screen.blit(self.floor_surface1, (self.x1_pos, self.y_pos))

    def move(self):
        self.x_pos -= 1
        self.x1_pos -= 1
        if self.x_pos <= -self.floor_surface.get_width():
            self.x_pos = self.floor_surface.get_width()
        if self.x1_pos <= -self.floor_surface1.get_width():
            self.x1_pos = self.floor_surface1.get_width()


class Pipe:
    def __init__(self):
        self.image = pygame.image.load("graphics/pipe-green.png")
        self.image = pygame.transform.scale2x(self.image)
        self.list = []
        self.pipe_height = [200, 400, 500]

    def create_pipe(self):
        random_pipe_height = random.choice(self.pipe_height)
        bottom_pipe = self.image.get_rect(midtop=(screen_width + 150, random_pipe_height))
        top_pipe = self.image.get_rect(midbottom=(screen_width + 150, random_pipe_height-300))
        return bottom_pipe, top_pipe

    def move_pipes(self):
        for pipe in self.list:
            pipe.centerx -= 5

    def draw_pipes(self):
        for pipe in self.list:
            if pipe.bottom >= screen_height:
                screen.blit(self.image, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.image, False, True)
                screen.blit(flip_pipe, pipe)

    def remove_pipes(self):
        for pipe in self.list:
            if pipe.centerx <= -50:
                self.list.remove(pipe)


class Game:
    def __init__(self):
        self.floor = Floor()
        self.bird = Bird()
        self.pipe = Pipe()
        self.score = 0
        self.high_score = 0
        # self.game_state = 'main_game'
        self.active = True
        self.game_over_surface = pygame.transform.scale2x(pygame.image.load('graphics/message.png').convert_alpha())

        self.death_sound = pygame.mixer.Sound('audio/sfx_die.wav')
        self.hit_sound = pygame.mixer.Sound('audio/sfx_hit.wav')
        self.score_sound = pygame.mixer.Sound('audio/sfx_point.wav')

    def display_message(self):
        game_over_rect = self.game_over_surface.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(self.game_over_surface, game_over_rect)

    def score_display(self):
        if self.active:  # self.game_state == 'main_game':
            score_surface = game_font.render(f"Score: {self.score}", True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(288, 100))
            screen.blit(score_surface, score_rect)
        if self.active is False:  # self.game_state == 'game_over':
            score_surface = game_font.render(f"Score: {self.score}", True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(288, 100))
            screen.blit(score_surface, score_rect)

            high_score_surface = game_font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
            high_score_rect = score_surface.get_rect(center=(screen_width/2 - 50, screen_height - 100))
            screen.blit(high_score_surface, high_score_rect)

    def draw(self):
        self.pipe.draw_pipes()

        self.floor.display()
        self.score_display()
        self.bird.draw()

    def update(self):
        self.bird.move()
        self.floor.move()
        self.pipe.move_pipes()
        self.collisions()
        self.get_score()
        self.pipe.remove_pipes()

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def get_score(self):
        if self.pipe.list:
            if self.bird.rect.centerx - 5 < self.pipe.list[0].centerx < self.bird.rect.centerx + 5:
                self.score += 1
                self.score_sound.play()

    def restart(self):
        self.active = True
        self.update_high_score()
        self.score = 0
        self.pipe.list.clear()
        self.bird.rect.center = (100, screen_height/2)
        self.bird.movement = 0

    def check_active(self):
        if self.active:
            # self.game_state = 'main_game'
            self.draw()
            self.update()
        else:
            # self.game_state = 'game_over'
            self.display_message()
            self.score_display()

    def collisions(self):
        for pipe in self.pipe.list:
            if self.bird.rect.colliderect(pipe):
                self.hit_sound.play()
                self.active = False

        if self.bird.rect.top <= -100 or self.bird.rect.bottom >= self.floor.y_pos:
            self.death_sound.play()
            self.active = False


def main():
    main_game = Game()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and main_game.active:
                    main_game.bird.flap_sound.play()
                    main_game.bird.movement = 0
                    main_game.bird.movement -= 12
                if event.key == pygame.K_SPACE and main_game.active is False:
                    main_game.restart()

            if event.type == SPAWNPIPE:
                main_game.pipe.list.extend(main_game.pipe.create_pipe())  # extend allow to use a tuple

            if event.type == BIRDFLAP:
                if main_game.bird.index < 2:
                    main_game.bird.index += 1
                else:
                    main_game.bird.index = 0
                main_game.bird.image, main_game.bird.rect = main_game.bird.bird_animation()

        screen.blit(bg, (0, 0))

        main_game.check_active()

        pygame.display.update()
        clock.tick(120)


if __name__ == '__main__':
    main()
