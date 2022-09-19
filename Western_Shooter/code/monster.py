import pygame
from entity import Entity
from pygame.math import Vector2 as Vector


class Monster:
    def get_player_distance_direction(self):
        enemy_pos = Vector(self.rect.center)
        player_pos = Vector(self.player.rect.center)

        distance = (player_pos - enemy_pos).magnitude()
        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = Vector()

        return distance, direction

    def face_player(self):
        distance, direction = self.get_player_distance_direction()

        if distance < self.notice_radius:
            if -0.5 < direction.y < 0.5:
                if direction.x < 0:  # player to the left
                    self.status = 'left_idle'
                elif direction.x > 0:  # player to the right
                    self.status = 'right_idle'
            else:
                if direction.y < 0:  # player to the top
                    self.status = 'up_idle'
                elif direction.y > 0:  # player to the bottom
                    self.status = 'down_idle'

    def walk_to_player(self):
        distance, direction = self.get_player_distance_direction()
        if self.attack_radius < distance < self.walk_radius:
            self.direction = direction
            self.status = self.status.split('_')[0]
        else:
            self.direction = Vector()


class Coffin(Entity, Monster):
    def __init__(self, pos, groups, path, collision_sprites, player):
        super().__init__(pos, groups, path, collision_sprites)

        # overwrites
        self.speed = 150

        # player interaction
        self.player = player
        self.notice_radius = 550
        self.walk_radius = 400
        self.attack_radius = 50

    def attack(self):
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0

        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if int(self.frame_index) == 4 and self.attacking:
            if self.get_player_distance_direction()[0] < self.attack_radius:
                self.player.damage()

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.face_player()
        self.walk_to_player()
        self.attack()

        self.move(dt)
        self.animate(dt)
        self.blink()

        self.check_dead()
        self.vulnerability_timer()


class Cactus(Entity, Monster):
    def __init__(self, pos, groups, path, collision_sprites, player, create_bullet):
        super().__init__(pos, groups, path, collision_sprites)
        # overwrites
        self.speed = 90

        # player interaction
        self.player = player
        self.notice_radius = 600
        self.walk_radius = 500
        self.attack_radius = 350

        # bullet
        self.create_bullet = create_bullet
        self.bullet_shot = False

        # shoot sound
        self.shoot_sound = pygame.mixer.Sound('../sound/bullet.wav')
        self.shoot_sound.set_volume(0.3)

    def attack(self):
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0
            self.bullet_shot = False

        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if int(self.frame_index) == 6 and self.attacking and not self.bullet_shot:
            bullet_direction = self.get_player_distance_direction()[1]
            self.create_bullet(self.rect.center + (bullet_direction * 150), bullet_direction)
            self.bullet_shot = True
            self.shoot_sound.play()

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.face_player()
        self.walk_to_player()
        self.attack()

        self.move(dt)
        self.animate(dt)
        self.blink()

        self.check_dead()
        self.vulnerability_timer()

