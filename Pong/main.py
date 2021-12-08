import pygame
import sys
import random

from pygame.math import Vector2

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

WIDTH = 900
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
bg_color = pygame.Color('grey12')
LIGHT_GRAY = (200, 200, 200)
ORANGE = (235, 85, 0)

blocks_color = ORANGE
text_color = WHITE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong!")

game_font = pygame.font.Font("freesansbold.ttf", 32)
pong_sound = pygame.mixer.Sound("Sounds/hit.wav")


class Player:
    def __init__(self):
        self.width = 10
        self.height = 70
        self.pos = Vector2(5, HEIGHT/2 - self.height/2)
        self.speed = 0
        self.speed_value = 3
        self.score = 0
        self.text_pos = -30
        self.text = None
        self.rect = None

    def draw(self):
        self.rect = pygame.Rect(int(self.pos.x), int(self.pos.y), self.width, self.height)
        pygame.draw.rect(screen, blocks_color, self.rect)

    def move(self):
        self.pos.y += self.speed
        if self.pos.y <= 0:
            self.pos.y = 0
        if self.pos.y + self.height >= HEIGHT:
            self.pos.y = HEIGHT - self.height

    def draw_score(self):
        self.text = game_font.render(f"{self.score}", False, text_color)
        screen.blit(self.text, (WIDTH/2 + self.text_pos, HEIGHT/2))


class Ball:
    def __init__(self):
        self.radius = 16
        self.pos = Vector2(WIDTH/2 - self.radius/2, HEIGHT/2 - self.radius/2)
        self.speed_x = 5 * random.choice((-1, 1))
        self.speed_y = 5 * random.choice((-1, 1))
        self.score_time = True
        self.ball_rect = None

    def draw(self):
        self.ball_rect = pygame.Rect(int(self.pos.x), int(self.pos.y), self.radius, self.radius)
        pygame.draw.ellipse(screen, blocks_color, self.ball_rect)

        if self.ball_rect.top <= 0 or self.ball_rect.bottom >= HEIGHT:
            pygame.mixer.Sound.play(pong_sound)
            self.speed_y *= -1

    def move_update(self):
        self.pos.x += self.speed_x
        self.pos.y += self.speed_y

    def restart(self):
        current_time = pygame.time.get_ticks()
        self.pos = Vector2(WIDTH/2 - self.radius/2, HEIGHT/2)

        countdown_pos = Vector2(-10, 20)

        if current_time - self.score_time < 700:
            number_three = game_font.render("3", False, text_color)
            screen.blit(number_three, (WIDTH/2 + countdown_pos.x, HEIGHT/2 + countdown_pos.y))
        elif current_time - self.score_time < 1400:
            number_two = game_font.render("2", False, text_color)
            screen.blit(number_two, (WIDTH / 2 + countdown_pos.x, HEIGHT / 2 + countdown_pos.y))
        elif current_time - self.score_time < 2100:
            number_one = game_font.render("1", False, text_color)
            screen.blit(number_one, (WIDTH/2 + countdown_pos.x, HEIGHT/2 + countdown_pos.y))

        if current_time - self.score_time < 2100:
            self.speed_x, self.speed_y = 0, 0
        else:
            self.speed_x = 5 * random.choice((-1, 1))
            self.speed_y = 5 * random.choice((-1, 1))
            self.score_time = None


class Enemy(Player):
    def __init__(self):
        super().__init__()
        self.pos = Vector2(WIDTH - self.width - 5, HEIGHT/2 - self.height/2)
        self.speed = 3
        self.text_pos = 15

    def check_position(self):
        if self.pos.y <= 0:
            self.pos.y = 0
        if self.pos.y + self.height >= HEIGHT:
            self.pos.y = HEIGHT - self.height


class MainGame:

    def __init__(self):
        self.p1 = Player()
        self.opponent = Enemy()
        self.ball = Ball()
        self.score_sound = pygame.mixer.Sound("Sounds/scored.wav")

    @staticmethod
    def drawBg():
        screen.fill(bg_color)
        pygame.draw.aaline(screen, blocks_color, (WIDTH/2, 0), (WIDTH/2, HEIGHT))

    def draw_elements(self):
        self.drawBg()
        self.p1.draw_score()
        self.opponent.draw_score()
        self.p1.draw()
        self.opponent.draw()
        self.ball.draw()

    def opponent_move(self):
        self.opponent.check_position()
        if self.opponent.pos.y < self.ball.ball_rect.y:
            self.opponent.pos.y += self.opponent.speed
        if self.opponent.pos.y > self.ball.ball_rect.y:
            self.opponent.pos.y -= self.opponent.speed

    def onUpdate(self):
        self.ball_logic()
        self.ball.move_update()
        self.p1.move()
        self.opponent_move()

    def ball_logic(self):
        # Collisions
        if self.ball.ball_rect.colliderect(self.p1.rect) and self.ball.speed_x < 0:
            pygame.mixer.Sound.play(pong_sound)
            if abs(self.ball.ball_rect.left - self.p1.rect.right) < 10:
                self.ball.speed_x *= -1
            elif abs(self.ball.ball_rect.bottom - self.p1.rect.top) < 10 and self.ball.speed_y > 0:
                self.ball.speed_y *= -1
            elif abs(self.ball.ball_rect.top - self.p1.rect.bottom) < 10 and self.ball.speed_y < 0:
                self.ball.speed_y *= -1

        if self.ball.ball_rect.colliderect(self.opponent.rect) and self.ball.speed_x > 0:
            pygame.mixer.Sound.play(pong_sound)
            if abs(self.ball.ball_rect.right - self.opponent.rect.left) < 10:
                self.ball.speed_x *= -1
            elif abs(self.ball.ball_rect.bottom - self.opponent.rect.top) < 10 and self.ball.speed_y > 0:
                self.ball.speed_y *= -1
            elif abs(self.ball.ball_rect.top - self.opponent.rect.bottom) < 10 and self.ball.speed_y < 0:
                self.ball.speed_y *= -1

        # scoring
        if self.ball.ball_rect.left <= 0:
            pygame.mixer.Sound.play(self.score_sound)
            self.opponent.score += 1
            self.ball.score_time = pygame.time.get_ticks()

        if self.ball.ball_rect.right >= WIDTH:
            pygame.mixer.Sound.play(self.score_sound)
            self.p1.score += 1
            self.ball.score_time = pygame.time.get_ticks()

        if self.ball.score_time:
            self.ball.restart()


def main():
    clock = pygame.time.Clock()
    main_game = MainGame()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.font.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    main_game.p1.speed -= main_game.p1.speed_value
                if event.key == pygame.K_DOWN:
                    main_game.p1.speed += main_game.p1.speed_value
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    main_game.p1.speed += main_game.p1.speed_value
                if event.key == pygame.K_DOWN:
                    main_game.p1.speed -= main_game.p1.speed_value

        main_game.draw_elements()
        main_game.onUpdate()
        pygame.display.flip()


if __name__ == "__main__":
    main()
