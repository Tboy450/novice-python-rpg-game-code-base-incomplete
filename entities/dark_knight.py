"""
Dark Knight Entity Module
========================

This module contains the DarkKnight class, which is a dark version of the dragon knight guard.
The dark knight features black armor, red accents, and dark dragon helmet flares.

RESOURCE: This module provides the DarkKnight class for use in battle encounters and cutscenes.
"""

import pygame
import random
from config.constants import *

class DarkKnight:
    """
    Dark Knight Entity - A dark version of the dragon knight guard
    
    This class represents a dark knight with black armor, red accents, and dark dragon helmet flares.
    Used for battle encounters and special cutscenes.
    
    Attributes:
        x (int): X position of the dark knight
        y (int): Y position of the dark knight
        width (int): Width of the dark knight
        height (int): Height of the dark knight
        color (tuple): Base color of the dark knight
        animation_offset (int): Vertical animation offset
        animation_timer (int): Animation timer for movement
        dialogue (list): Dialogue lines for cutscenes
        current_dialogue (int): Current dialogue index
        dialogue_timer (int): Timer for dialogue progression
        visible (bool): Whether the dark knight is visible
    """
    
    def __init__(self, x=500, y=300):
        """
        Initialize the Dark Knight
        
        Args:
            x (int): X position (default: 500)
            y (int): Y position (default: 300)
        """
        self.x = x
        self.y = y
        self.width = 40
        self.height = 70
        self.color = (40, 40, 60)  # Dark armor color
        self.animation_offset = 0
        self.animation_timer = 0
        self.dialogue = [
            "Halt, mortal! You dare approach the Dark Dragon's domain?",
            "I am Malakor's Dark Knight, guardian of the shadow realm.",
            "Your light will be extinguished in the depths of darkness!",
            "Prepare to face the power of the dark dragon!"
        ]
        self.current_dialogue = 0
        self.dialogue_timer = 0
        self.visible = True
    
    def update(self):
        """Update the dark knight's animation"""
        self.animation_timer += 1
        self.animation_offset = math.sin(self.animation_timer * 0.1) * 2
    
    def draw(self, surface):
        """
        Draw the dark knight with black armor and red accents
        
        Args:
            surface (pygame.Surface): The surface to draw on
        """
        if not self.visible:
            return
            
        # Base position with animation offset
        knight_x = self.x
        knight_y = self.y + self.animation_offset
        knight_w = self.width
        knight_h = self.height
        
        # Dark armor base
        pygame.draw.rect(surface, (30, 30, 50), (knight_x, knight_y, knight_w, knight_h))
        pygame.draw.rect(surface, (20, 20, 40), (knight_x, knight_y, knight_w, knight_h), 2)
        
        # Helmet (dark with red accents)
        helmet_y = knight_y - 15
        pygame.draw.rect(surface, (40, 40, 60), (knight_x + 5, helmet_y, knight_w - 10, 15))
        pygame.draw.rect(surface, (20, 20, 40), (knight_x + 5, helmet_y, knight_w - 10, 15), 2)
        pygame.draw.rect(surface, (60, 60, 80), (knight_x + 8, helmet_y + 2, knight_w - 16, 8))
        
        # Visor (red glow)
        pygame.draw.rect(surface, (80, 20, 20), (knight_x + 8, helmet_y + 5, knight_w - 16, 4))
        pygame.draw.rect(surface, (120, 40, 40), (knight_x + 9, helmet_y + 6, knight_w - 18, 2))
        
        # Dark Dragon Knight Helmet Flares (black with red edges)
        # Left flare
        left_flare_points = [
            (knight_x + 2, helmet_y + 3),
            (knight_x - 8, helmet_y + 1),
            (knight_x - 12, helmet_y + 5),
            (knight_x - 10, helmet_y + 8),
            (knight_x - 5, helmet_y + 10),
            (knight_x + 2, helmet_y + 8)
        ]
        pygame.draw.polygon(surface, (30, 30, 50), left_flare_points)
        pygame.draw.polygon(surface, (20, 20, 40), left_flare_points, 2)
        pygame.draw.polygon(surface, (80, 20, 20), [
            (knight_x + 2, helmet_y + 3),
            (knight_x - 6, helmet_y + 2),
            (knight_x - 8, helmet_y + 4),
            (knight_x - 4, helmet_y + 6),
            (knight_x + 2, helmet_y + 5)
        ])
        
        # Right flare
        right_flare_points = [
            (knight_x + knight_w - 2, helmet_y + 3),
            (knight_x + knight_w + 8, helmet_y + 1),
            (knight_x + knight_w + 12, helmet_y + 5),
            (knight_x + knight_w + 10, helmet_y + 8),
            (knight_x + knight_w + 5, helmet_y + 10),
            (knight_x + knight_w - 2, helmet_y + 8)
        ]
        pygame.draw.polygon(surface, (30, 30, 50), right_flare_points)
        pygame.draw.polygon(surface, (20, 20, 40), right_flare_points, 2)
        pygame.draw.polygon(surface, (80, 20, 20), [
            (knight_x + knight_w - 2, helmet_y + 3),
            (knight_x + knight_w + 6, helmet_y + 2),
            (knight_x + knight_w + 8, helmet_y + 4),
            (knight_x + knight_w + 4, helmet_y + 6),
            (knight_x + knight_w - 2, helmet_y + 5)
        ])
        
        # Helmet crest (dark dragon spine with red glow)
        crest_points = [
            (knight_x + knight_w//2 - 2, helmet_y - 8),
            (knight_x + knight_w//2, helmet_y - 15),
            (knight_x + knight_w//2 + 2, helmet_y - 8),
            (knight_x + knight_w//2 + 1, helmet_y - 5),
            (knight_x + knight_w//2 - 1, helmet_y - 5)
        ]
        pygame.draw.polygon(surface, (40, 40, 60), crest_points)
        pygame.draw.polygon(surface, (20, 20, 40), crest_points, 2)
        pygame.draw.line(surface, (80, 20, 20), 
                        (knight_x + knight_w//2, helmet_y - 15), 
                        (knight_x + knight_w//2, helmet_y - 8), 2)
        
        # Shoulder plates (dark with red trim)
        pygame.draw.rect(surface, (40, 40, 60), (knight_x - 5, knight_y + 5, 8, 12))
        pygame.draw.rect(surface, (80, 20, 20), (knight_x - 5, knight_y + 5, 8, 12), 1)
        pygame.draw.rect(surface, (40, 40, 60), (knight_x + knight_w - 3, knight_y + 5, 8, 12))
        pygame.draw.rect(surface, (80, 20, 20), (knight_x + knight_w - 3, knight_y + 5, 8, 12), 1)
        
        # Chest plate (dark with red accents)
        chest_x = knight_x + 5
        chest_y = knight_y + 12
        chest_w = knight_w - 10
        chest_h = 20
        pygame.draw.rect(surface, (30, 30, 50), (chest_x, chest_y, chest_w, chest_h))
        pygame.draw.rect(surface, (20, 20, 40), (chest_x, chest_y, chest_w, chest_h), 2)
        pygame.draw.rect(surface, (60, 60, 80), (chest_x + 2, chest_y + 2, chest_w - 4, 6))
        pygame.draw.rect(surface, (80, 20, 20), (chest_x + 4, chest_y + 8, chest_w - 8, 2))
        
        # Belt (dark with red buckle)
        pygame.draw.rect(surface, (20, 20, 40), (knight_x + 3, knight_y + 35, knight_w - 6, 4))
        pygame.draw.rect(surface, (80, 20, 20), (knight_x + knight_w//2 - 3, knight_y + 35, 6, 4))
        
        # Legs (dark armor)
        pygame.draw.rect(surface, (30, 30, 50), (knight_x + 5, knight_y + 40, 8, 20))
        pygame.draw.rect(surface, (30, 30, 50), (knight_x + knight_w - 13, knight_y + 40, 8, 20))
        pygame.draw.rect(surface, (80, 20, 20), (knight_x + 5, knight_y + 40, 8, 20), 1)
        pygame.draw.rect(surface, (80, 20, 20), (knight_x + knight_w - 13, knight_y + 40, 8, 20), 1)
        
        # Boots (dark with red trim)
        pygame.draw.rect(surface, (20, 20, 40), (knight_x + 3, knight_y + 60, 10, 8))
        pygame.draw.rect(surface, (20, 20, 40), (knight_x + knight_w - 13, knight_y + 60, 10, 8))
        pygame.draw.rect(surface, (80, 20, 20), (knight_x + 3, knight_y + 60, 10, 8), 1)
        pygame.draw.rect(surface, (80, 20, 20), (knight_x + knight_w - 13, knight_y + 60, 10, 8), 1)
        
        # Dark Sword (black with red glow)
        sword_x = knight_x + knight_w + 5
        sword_y = knight_y + 20
        pygame.draw.rect(surface, (30, 30, 50), (sword_x, sword_y, 4, 25))
        pygame.draw.rect(surface, (20, 20, 40), (sword_x, sword_y, 4, 25), 1)
        pygame.draw.rect(surface, (80, 20, 20), (sword_x + 1, sword_y + 1, 2, 8))
        
        # Sword handle (dark with red grip)
        pygame.draw.rect(surface, (40, 20, 20), (sword_x - 2, sword_y + 25, 8, 6))
        pygame.draw.rect(surface, (20, 10, 10), (sword_x - 2, sword_y + 25, 8, 6), 1)
        pygame.draw.rect(surface, (80, 20, 20), (sword_x, sword_y + 26, 4, 4))
        
        # Dark Shield (black with red emblem)
        shield_x = knight_x - 15
        shield_y = knight_y + 15
        pygame.draw.circle(surface, (30, 30, 50), (shield_x, shield_y), 12)
        pygame.draw.circle(surface, (20, 20, 40), (shield_x, shield_y), 12, 2)
        pygame.draw.circle(surface, (60, 60, 80), (shield_x, shield_y), 8)
        pygame.draw.circle(surface, (40, 40, 60), (shield_x, shield_y), 8, 1)
        # Red dragon emblem on shield
        pygame.draw.circle(surface, (80, 20, 20), (shield_x, shield_y), 4)
        pygame.draw.circle(surface, (120, 40, 40), (shield_x, shield_y), 2)
    
    def draw_dialogue(self, surface):
        """
        Draw the dark knight's dialogue box
        
        Args:
            surface (pygame.Surface): The surface to draw on
        """
        # Dark dialogue box
        dialogue_box = pygame.Surface((800, 150))
        dialogue_box.fill((20, 20, 40))  # Dark background
        pygame.draw.rect(dialogue_box, (80, 20, 20), (0, 0, 800, 150), 3)  # Red border
        
        # Draw dialogue text
        current_text = self.dialogue[self.current_dialogue]
        text_surface = font_cinematic.render(current_text, True, (200, 200, 200))  # Light text
        dialogue_box.blit(text_surface, (120, 60))
        
        # Draw continue indicator
        if self.dialogue_timer % 60 < 30:
            continue_text = font_small.render("Press SPACE to continue", True, (120, 120, 120))
            dialogue_box.blit(continue_text, (120, 120))
        
        # Position dialogue box at bottom of screen
        surface.blit(dialogue_box, (100, SCREEN_HEIGHT - 200))
    
    def next_dialogue(self):
        """Advance to the next dialogue line"""
        self.current_dialogue = (self.current_dialogue + 1) % len(self.dialogue)
        self.dialogue_timer = 0
    
    def update_dialogue(self):
        """Update dialogue timer"""
        self.dialogue_timer += 1 