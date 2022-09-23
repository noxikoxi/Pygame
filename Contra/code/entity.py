import pygame
from settings import *
from pygame.math import Vector2 as Vector
from os import walk
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, path, groups, shoot):
        super().__init__(groups)

        # graphics setup
        self.import_assets(path)
        self.status = 'right'
        self.frame_index = 0

        # image setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = LAYERS['Level']

        self.mask = pygame.mask.from_surface(self.image)

        # float based movement
        self.direction = Vector()
        self.pos = Vector(self.rect.topleft)
        self.speed = 400

        # shoot setup
        self.shoot = shoot
        self.can_shoot = True
        self.shoot_time = None
        self.cooldown = 300

        # health
        self.health = 3

        # invulnerability
        self.invulnerable = False
        self.hit_time = None
        self.invulnerable_timer = 400

        # audio
        self.hit_sound = pygame.mixer.Sound('../audio/hit.wav')
        self.shoot_sound = pygame.mixer.Sound('../audio/bullet.wav')
        self.hit_sound.set_volume(0.2)
        self.shoot_sound.set_volume(0.3)

        self.duck = False

    def import_assets(self, path):
        self.animations = {}

        for index, folder in enumerate(walk(path)):
            if index == 0:
                for file_name in folder[1]:
                    self.animations[file_name] = []
            else:
                for file_name in sorted(folder[2], key=lambda string: int(string.split('.')[0])):
                    status = folder[0].split('\\')[1]
                    path = folder[0].replace('\\', '/') + '/' + file_name
                    self.animations[status].append(pygame.image.load(path).convert_alpha())

    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.cooldown:
                self.can_shoot = True

    def invul_timer(self):
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > self.invulnerable_timer:
                self.invulnerable = False

    def blink(self):
        if self.invulnerable:
            if self.wave_value():
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0, 0, 0))
                self.image = white_surf

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return True
        else:
            return False

    def damage(self):
        if not self.invulnerable:
            self.health -= 1
            self.invulnerable = True
            self.hit_time = pygame.time.get_ticks()
            self.hit_sound.play()

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def animate(self, dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)
