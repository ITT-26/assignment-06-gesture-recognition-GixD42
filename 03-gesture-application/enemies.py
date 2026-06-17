from constants import *
import random
import pyglet


class Enemy:
    def __init__(self, is_flying):
        self.x = ENEMY_SPAWN_X
        self.speed = random.randint(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
        self.is_flying = is_flying

        if self.is_flying:
            self.y = ENEMY_FLY_Y
            image_path = ENEMY_FLY_PATH
        else:
            self.y = ENEMY_GROUND_Y
            image_path = ENEMY_GROUND_PATH

        self.image = pyglet.image.load(str(image_path))
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x, y=self.y)


class EnemyManager:
    def __init__(self):
        self.enemies = []
        self.spawn_timer = random.uniform(
            ENEMY_SPAWN_TIME_MIN, ENEMY_SPAWN_TIME_MAX)

    def update(self, dt, spell_active=False):
        # update spawn timer and spawn new enemy if time

        if not spell_active:
            # is a spell active? if so don't spawn enemies
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                is_flying = random.random() < 0.5
                self.enemies.append(Enemy(is_flying))
                self.spawn_timer = random.uniform(
                    ENEMY_SPAWN_TIME_MIN, ENEMY_SPAWN_TIME_MAX)

        # update enemy positions
        for enemy in self.enemies:
            enemy.x -= enemy.speed * dt
            enemy.sprite.x = enemy.x

    # delete enemies that are flying
    def kill_all_flying(self):
        self.enemies = [e for e in self.enemies if not e.is_flying]

    # delete enemies that are on the ground
    def kill_all_ground(self):
        self.enemies = [e for e in self.enemies if e.is_flying]

    # delete all enemies
    def kill_all(self):
        self.enemies = []

    # draw all enemies
    def draw(self):
        for enemy in self.enemies:
            enemy.sprite.draw()
