"""
DRAGON'S LAIR RPG - Item Module
===============================

This module contains the Item class for collectible items.
"""

import pygame
import random
import math
from config.constants import *

class Item:
    """Collectible item class"""
    def __init__(self):
        self.size = ITEM_SIZE
        self.x = 0
        self.y = 0
        self.type = random.choice(["health", "mana"])
        self.color = ITEM_COLOR if self.type == "health" else MANA_COLOR
        self.pulse = 0
        self.float_offset = 0
    
    def update(self):
        """Update item animation"""
        # Update pulse and float offset for drawing
        self.pulse += 0.1
        self.float_offset = math.sin(pygame.time.get_ticks() * 0.003) * 3
    
    def draw(self, surface):
        """Draw the item with proper animations and details"""
        self.pulse += 0.1
        self.float_offset = math.sin(pygame.time.get_ticks() * 0.003) * 3
        
        pulse_size = self.size//2 + math.sin(self.pulse) * 3
        y_pos = self.y + self.float_offset
        
        pygame.draw.circle(surface, self.color, (self.x + self.size//2, y_pos + self.size//2), pulse_size)
        
        if self.type == "health":
            pygame.draw.rect(surface, (255, 255, 255), (self.x + 10, y_pos + 8, 10, 14), border_radius=2)
        else:
            pygame.draw.polygon(surface, (255, 255, 255), 
                              [(self.x + 15, y_pos + 8),
                               (self.x + 8, y_pos + 22),
                               (self.x + 22, y_pos + 22)]) 