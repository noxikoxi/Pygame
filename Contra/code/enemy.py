import pygame
from settings import *
from pygame.math import Vector2 as Vector
from entity import Entity


class Enemy(Entity):
    def __init__(self, pos, path, groups, shoot, player, collision_sprites):
        super().__init__(pos, path, groups, shoot)
        self.player = player
        for sprite in collision_sprites.sprites():
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = sprite.rect.top

        # shoot cooldown
        self.cooldown = 1000

    def get_status(self):
        if self.player.rect.centerx < self.rect.centerx:
            self.status = 'left'
        else:
            self.status = 'right'

    def check_fire(self):
        enemy_pos = Vector(self.rect.center)
        player_pos = Vector(self.player.rect.center)

        distance = (player_pos - enemy_pos).magnitude()
        same_y = True if self.rect.top - 20 < player_pos.y < self.rect.bottom + 20 else False

        if distance < 600 and same_y and self.can_shoot:
            bullet_direction = Vector(1, 0) if self.status == 'right' else Vector(-1, 0)
            y_offset = Vector(0, -16)
            pos = self.rect.center + bullet_direction * 60
            self.shoot(pos + y_offset, bullet_direction, self)

            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            self.shoot_sound.play()

    def update(self, dt):
        self.get_status()
        self.animate(dt)
        self.blink()

        self.shoot_timer()
        self.check_fire()
        self.invul_timer()

        # death
        self.check_death()
