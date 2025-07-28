"""
DRAGON'S LAIR RPG - Dragon Module
=================================

This module contains the Dragon class for cutscene dragons.
"""

import pygame
import random
import math
from config.constants import *

class Dragon:
    """
    Decorative dragon for the title screen with fire breathing animation.
    This is a visual element, not a combat enemy.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_frame = 0
        self.fire_frame = 0
        self.fire_active = False
        self.flap_direction = 1
        self.flap_speed = 0.1
        
    def draw(self, surface):
        """Draw the detailed dragon with animations"""
        # Main dragon body
        pygame.draw.ellipse(surface, DRAGON_COLOR, (self.x, self.y + 30, 180, 70))
        pygame.draw.circle(surface, DRAGON_COLOR, (self.x + 180, self.y + 50), 35)
        
        # Dragon eye
        pygame.draw.circle(surface, (255, 255, 255), (self.x + 195, self.y + 45), 10)
        pygame.draw.circle(surface, (0, 0, 0), (self.x + 195, self.y + 45), 5)
        
        # Dragon horns
        pygame.draw.polygon(surface, (200, 100, 50), [
            (self.x + 180, self.y + 25),
            (self.x + 190, self.y + 10),
            (self.x + 195, self.y + 20)
        ])
        pygame.draw.polygon(surface, (200, 100, 50), [
            (self.x + 205, self.y + 25),
            (self.x + 215, self.y + 10),
            (self.x + 210, self.y + 20)
        ])
        
        # Animated wings
        wing_y_offset = math.sin(self.animation_frame) * 12
        pygame.draw.polygon(surface, (200, 50, 50), [
            (self.x + 40, self.y + 50),
            (self.x, self.y + 15 + wing_y_offset),
            (self.x + 50, self.y + 30)
        ])
        pygame.draw.polygon(surface, (200, 50, 50), [
            (self.x + 40, self.y + 50),
            (self.x, self.y + 85 - wing_y_offset),
            (self.x + 50, self.y + 70)
        ])
        
        # Dragon tail
        pygame.draw.polygon(surface, DRAGON_COLOR, [
            (self.x, self.y + 50),
            (self.x - 50, self.y + 20),
            (self.x - 50, self.y + 80)
        ])
        
        # Tail spikes
        for i in range(3):
            offset = i * 15
            pygame.draw.polygon(surface, (200, 50, 50), [
                (self.x - 50 + offset, self.y + 50 - offset//2),
                (self.x - 55 + offset, self.y + 40 - offset//2),
                (self.x - 45 + offset, self.y + 40 - offset//2)
            ])
        
        # Fire breathing effect
        if self.fire_active:
            for i in range(15):
                fire_size = 5 + i * 1.5
                alpha = max(0, 200 - i * 10)
                fire_color = (255, 215, 0, alpha)
                
                fire_surf = pygame.Surface((fire_size*2, fire_size*2), pygame.SRCALPHA)
                pygame.draw.circle(fire_surf, fire_color, (fire_size, fire_size), fire_size)
                surface.blit(
                    fire_surf, 
                    (
                        self.x + 180 + 35 + i*15 + self.fire_frame*2, 
                        self.y + 40
                    )
                )
        
        self.animation_frame += self.flap_speed
        
    def breathe_fire(self):
        """Activate fire breathing animation"""
        self.fire_active = True
        self.fire_frame = 0
        
    def update(self):
        """Update dragon animation"""
        if self.fire_active:
            self.fire_frame += 1
            if self.fire_frame > 30:
                self.fire_active = False 