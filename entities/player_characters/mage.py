from .character import CharacterBase
import math
import random
import pygame
from config.constants import *

class Mage(CharacterBase):
    """
    Mage character class. Handles all drawing, animation, and stat logic unique to Mage.
    """
    def __init__(self):
        self.type = "Mage"
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.max_health = 80
        self.max_mana = 120
        self.strength = 8
        self.defense = 6
        self.speed = 8
        self.health = self.max_health
        self.mana = self.max_mana
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.attack_cooldown = 0
        self.kills = 0
        self.items_collected = 0
        self.animation_offset = 0
        self.attack_animation = 0
        self.hit_animation = 0
        self.last_boss_level = 0  # Track the last boss level encountered
        self.just_leveled_up = False
        self.boss_cooldown = False  # Prevent boss battles during cooldown

    def gain_exp(self, amount):
        """Add experience and check for level up"""
        self.exp += amount
        if self.exp >= self.exp_to_level:
            self.level_up()

    def level_up(self):
        """Level up the character and increase stats"""
        print(f"🎉 LEVEL UP! Level {self.level} -> {self.level + 1}")
        self.level += 1
        self.exp -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.5)
        self.max_health += 20
        self.max_mana += 15
        self.strength += 3
        self.defense += 2
        self.speed += 1
        self.health = self.max_health
        self.mana = self.max_mana
        self.just_leveled_up = True
        self.boss_cooldown = False

    def update_animation(self):
        self.animation_offset = math.sin(pygame.time.get_ticks() * 0.005) * 2
        if self.attack_animation > 0:
            self.attack_animation -= 1
        if self.hit_animation > 0:
            self.hit_animation -= 1

    def draw(self, surface):
        # Use the modular animation system
        from .character_animation import draw
        draw(self, surface)

    def draw_stats(self, surface, x, y):
        from .character_animation import draw_stats
        draw_stats(self, surface, x, y)

    def start_attack_animation(self):
        from .character_animation import start_attack_animation
        start_attack_animation(self)

    def start_hit_animation(self):
        from .character_animation import start_hit_animation
        start_hit_animation(self)

    def move(self, dx, dy):
        new_x = self.x + dx * GRID_SIZE
        new_y = self.y + dy * GRID_SIZE
        
        # Check world boundaries (0 to WORLD_WIDTH/HEIGHT)
        if 0 <= new_x < WORLD_WIDTH:
            self.x = new_x
        if 0 <= new_y < WORLD_HEIGHT:
            self.y = new_y 