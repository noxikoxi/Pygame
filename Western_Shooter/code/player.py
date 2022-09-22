import sys

import pygame
from pygame.math import Vector2 as Vector
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, path, collision_sprites, create_bullet):
        super().__init__(pos, groups, path, collision_sprites)

        self.create_bullet = create_bullet
        self.bullet_shot = False

        # shoot sound
        self.shoot_sound = pygame.mixer.Sound('../sound/bullet.wav')
        self.shoot_sound.set_volume(0.3)

    def get_status(self):
        # idle
        if self.direction == Vector(0, 0):
            self.status = self.status.split('_')[0] + '_idle'

        # attacking
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

        if keys[pygame.K_SPACE]:
            self.attacking = True
            self.direction = Vector()
            self.frame_index = 0
            self.bullet_shot = False

            match self.status.split('_')[0]:
                case 'left': self.bullet_direction = Vector(-1, 0)
                case 'right': self.bullet_direction = Vector(1, 0)
                case 'up': self.bullet_direction = Vector(0, -1)
                case 'down': self.bullet_direction = Vector(0, 1)

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if int(self.frame_index) == 2 and self.attacking and not self.bullet_shot:
            self.create_bullet(self.rect.center + self.bullet_direction * 80, self.bullet_direction)
            self.bullet_shot = True
            self.shoot_sound.play()

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def check_dead(self):
        if self.health <= 0:
            pygame.quit()
            sys.exit()

    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
        self.blink()

        self.vulnerability_timer()
        self.check_dead()
