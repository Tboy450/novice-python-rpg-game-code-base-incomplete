"""
Guard Entity Module
==================

This module contains the Guard class, which is the original detailed dragon knight guard
from the pycore whole 2 file. This stores the complete original guard model with all
detailed armor, helmet, sword, and shield drawing code.

RESOURCE: This module provides the Guard class for use in town cutscenes and NPC interactions.
"""

import pygame
import math
from config.constants import *

class Guard:
    """
    Guard Entity - The original detailed dragon knight guard
    
    This class represents the original detailed guard from the pycore whole 2 file,
    with complete armor, helmet, sword, and shield drawing code.
    
    Attributes:
        x (int): X position of the guard
        y (int): Y position of the guard
        width (int): Width of the guard
        height (int): Height of the guard
        color (tuple): Base color of the guard
        animation_offset (int): Vertical animation offset
        animation_timer (int): Animation timer for movement
        dialogue (list): Dialogue lines for cutscenes
        current_dialogue (int): Current dialogue index
        dialogue_timer (int): Timer for dialogue progression
        visible (bool): Whether the guard is visible
    """
    
    def __init__(self, x=300, y=270):
        """
        Initialize the Guard
        
        Args:
            x (int): X position (default: 300)
            y (int): Y position (default: 270)
        """
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.color = (100, 150, 200)  # Blue uniform
        self.animation_offset = 0
        self.animation_timer = 0
        self.dialogue = [
            "Halt! Welcome to our fair town, traveler.",
            "I am Captain Marcus, keeper of the peace.",
            "You may enter freely, but mind our laws.",
            "If you need assistance, seek me out.",
            "Safe travels, adventurer!"
        ]
        self.current_dialogue = 0
        self.dialogue_timer = 0
        self.visible = True
    
    def update(self):
        """Update the guard's animation"""
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.animation_offset = 2 if self.animation_offset == 0 else 0
    
    def draw(self, surface):
        """
        Draw the detailed dragon knight guard with complete armor
        
        Args:
            surface (pygame.Surface): The surface to draw on
        """
        if not self.visible:
            return
            
        # Base position with animation offset
        guard_x = self.x
        guard_y = self.y + self.animation_offset
        guard_w = self.width
        guard_h = self.height
        
        # Dragon Knight shadow
        pygame.draw.ellipse(surface, (0, 0, 0), (guard_x + 2, guard_y + 62, guard_w - 4, 8))
        
        # Silver armor with detailed shading
        armor_base = (180, 180, 200)  # Silver base
        armor_highlight = (220, 220, 240)  # Bright silver
        armor_shadow = (140, 140, 160)  # Dark silver
        armor_detail = (100, 100, 120)  # Darker detail lines
        
        # Main armor body
        pygame.draw.rect(surface, armor_base, (guard_x + 2, guard_y + 12, guard_w - 4, guard_h - 12))
        # Armor highlight
        pygame.draw.rect(surface, armor_highlight, (guard_x + 4, guard_y + 14, guard_w - 8, 8))
        # Armor shadow
        pygame.draw.rect(surface, armor_shadow, (guard_x + 2, guard_y + 12, 4, guard_h - 12))
        
        # Dragon scale pattern on chest
        for i in range(3):
            for j in range(2):
                scale_x = guard_x + 8 + i * 8
                scale_y = guard_y + 20 + j * 8
                pygame.draw.ellipse(surface, armor_detail, (scale_x, scale_y, 6, 4))
                pygame.draw.ellipse(surface, armor_highlight, (scale_x + 1, scale_y + 1, 4, 2))
        
        # Dragon Knight head with detailed helmet
        head_x = guard_x + guard_w//2 - 10
        head_y = guard_y - 15
        
        # Head shadow
        pygame.draw.circle(surface, (180, 140, 100), (head_x + 10 + 1, head_y + 10 + 1), 10)
        # Head base
        pygame.draw.circle(surface, (240, 200, 150), (head_x + 10, head_y + 10), 10)
        # Head highlight
        pygame.draw.circle(surface, (255, 220, 180), (head_x + 8, head_y + 8), 4)
        # Head outline
        pygame.draw.circle(surface, (200, 150, 100), (head_x + 10, head_y + 10), 10, 1)
        
        # Dragon Knight full helmet with flares
        helmet_color = (160, 160, 180)
        helmet_highlight = (200, 200, 220)
        helmet_shadow = (120, 120, 140)
        helmet_detail = (100, 100, 120)
        
        # Helmet base (full coverage)
        helmet_base_points = [
            (head_x + 2, head_y), (head_x + 18, head_y),  # Top
            (head_x + 20, head_y + 2), (head_x + 20, head_y + 8),  # Right side
            (head_x + 18, head_y + 12), (head_x + 2, head_y + 12),  # Bottom
            (head_x, head_y + 8), (head_x, head_y + 2)  # Left side
        ]
        pygame.draw.polygon(surface, helmet_color, helmet_base_points)
        pygame.draw.polygon(surface, helmet_highlight, [
            (head_x + 4, head_y + 1), (head_x + 16, head_y + 1),
            (head_x + 18, head_y + 3), (head_x + 18, head_y + 7),
            (head_x + 16, head_y + 10), (head_x + 4, head_y + 10),
            (head_x + 2, head_y + 7), (head_x + 2, head_y + 3)
        ])
        pygame.draw.polygon(surface, helmet_shadow, [
            (head_x + 2, head_y), (head_x, head_y + 2), (head_x, head_y + 8),
            (head_x + 2, head_y + 12), (head_x + 4, head_y + 12)
        ])
        
        # Helmet crown with dragon motifs
        crown_points = [
            (head_x + 2, head_y), (head_x + 18, head_y),
            (head_x + 16, head_y - 2), (head_x + 14, head_y - 4),
            (head_x + 12, head_y - 6), (head_x + 8, head_y - 6),
            (head_x + 6, head_y - 4), (head_x + 4, head_y - 2)
        ]
        pygame.draw.polygon(surface, helmet_color, crown_points)
        pygame.draw.polygon(surface, helmet_highlight, [
            (head_x + 4, head_y - 1), (head_x + 16, head_y - 1),
            (head_x + 14, head_y - 3), (head_x + 12, head_y - 5),
            (head_x + 8, head_y - 5), (head_x + 6, head_y - 3)
        ])
        
        # Dragon horns on helmet (larger and more detailed)
        horn_color = (140, 140, 160)
        horn_highlight = (180, 180, 200)
        
        # Left horn (curved)
        left_horn_points = [
            (head_x + 4, head_y), (head_x + 2, head_y - 2), (head_x + 1, head_y - 6),
            (head_x + 2, head_y - 10), (head_x + 4, head_y - 12), (head_x + 6, head_y - 10),
            (head_x + 7, head_y - 6), (head_x + 6, head_y - 2)
        ]
        pygame.draw.polygon(surface, horn_color, left_horn_points)
        pygame.draw.polygon(surface, horn_highlight, [
            (head_x + 4, head_y), (head_x + 3, head_y - 2), (head_x + 2, head_y - 6),
            (head_x + 3, head_y - 10), (head_x + 5, head_y - 10), (head_x + 6, head_y - 6),
            (head_x + 5, head_y - 2)
        ])
        
        # Right horn (curved)
        right_horn_points = [
            (head_x + 12, head_y), (head_x + 14, head_y - 2), (head_x + 15, head_y - 6),
            (head_x + 14, head_y - 10), (head_x + 12, head_y - 12), (head_x + 10, head_y - 10),
            (head_x + 9, head_y - 6), (head_x + 10, head_y - 2)
        ]
        pygame.draw.polygon(surface, horn_color, right_horn_points)
        pygame.draw.polygon(surface, horn_highlight, [
            (head_x + 12, head_y), (head_x + 13, head_y - 2), (head_x + 14, head_y - 6),
            (head_x + 13, head_y - 10), (head_x + 11, head_y - 10), (head_x + 10, head_y - 6),
            (head_x + 11, head_y - 2)
        ])
        
        # Helmet visor (full face coverage with multiple slits)
        visor_points = [
            (head_x + 3, head_y + 3), (head_x + 17, head_y + 3),
            (head_x + 18, head_y + 5), (head_x + 18, head_y + 9),
            (head_x + 17, head_y + 11), (head_x + 3, head_y + 11),
            (head_x + 2, head_y + 9), (head_x + 2, head_y + 5)
        ]
        pygame.draw.polygon(surface, (80, 80, 100), visor_points)
        pygame.draw.polygon(surface, (120, 120, 140), [
            (head_x + 4, head_y + 4), (head_x + 16, head_y + 4),
            (head_x + 17, head_y + 6), (head_x + 17, head_y + 8),
            (head_x + 16, head_y + 10), (head_x + 4, head_y + 10),
            (head_x + 3, head_y + 8), (head_x + 3, head_y + 6)
        ])
        
        # Multiple visor slits for better visibility
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 4, head_y + 4, 2, 2))
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 7, head_y + 4, 2, 2))
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 10, head_y + 4, 2, 2))
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 13, head_y + 4, 2, 2))
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 4, head_y + 7, 2, 2))
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 7, head_y + 7, 2, 2))
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 10, head_y + 7, 2, 2))
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 13, head_y + 7, 2, 2))
        
        # Chin guard (full face and chin coverage)
        chin_guard_points = [
            (head_x + 2, head_y + 11), (head_x + 18, head_y + 11),  # Top
            (head_x + 20, head_y + 13), (head_x + 20, head_y + 18),  # Right side
            (head_x + 18, head_y + 20), (head_x + 2, head_y + 20),   # Bottom
            (head_x, head_y + 18), (head_x, head_y + 13)             # Left side
        ]
        pygame.draw.polygon(surface, helmet_color, chin_guard_points)
        pygame.draw.polygon(surface, helmet_highlight, [
            (head_x + 4, head_y + 12), (head_x + 16, head_y + 12),
            (head_x + 18, head_y + 14), (head_x + 18, head_y + 17),
            (head_x + 16, head_y + 19), (head_x + 4, head_y + 19),
            (head_x + 2, head_y + 17), (head_x + 2, head_y + 14)
        ])
        pygame.draw.polygon(surface, helmet_shadow, [
            (head_x + 2, head_y + 11), (head_x, head_y + 13), (head_x, head_y + 18),
            (head_x + 2, head_y + 20), (head_x + 4, head_y + 20)
        ])
        
        # Chin guard breathing holes
        pygame.draw.circle(surface, (60, 60, 80), (head_x + 6, head_y + 15), 1)
        pygame.draw.circle(surface, (60, 60, 80), (head_x + 14, head_y + 15), 1)
        pygame.draw.circle(surface, (60, 60, 80), (head_x + 6, head_y + 17), 1)
        pygame.draw.circle(surface, (60, 60, 80), (head_x + 14, head_y + 17), 1)
        
        # Helmet flares (larger decorative metal pieces)
        flare_color = (180, 180, 200)
        flare_highlight = (220, 220, 240)
        
        # Left flare (larger)
        left_flare_points = [
            (head_x, head_y + 4), (head_x - 6, head_y + 1), (head_x - 8, head_y + 4),
            (head_x - 6, head_y + 7), (head_x, head_y + 10)
        ]
        pygame.draw.polygon(surface, flare_color, left_flare_points)
        pygame.draw.polygon(surface, flare_highlight, [
            (head_x, head_y + 4), (head_x - 3, head_y + 2), (head_x - 6, head_y + 4),
            (head_x - 3, head_y + 7), (head_x, head_y + 9)
        ])
        
        # Right flare (larger)
        right_flare_points = [
            (head_x + 20, head_y + 4), (head_x + 26, head_y + 1), (head_x + 28, head_y + 4),
            (head_x + 26, head_y + 7), (head_x + 20, head_y + 10)
        ]
        pygame.draw.polygon(surface, flare_color, right_flare_points)
        pygame.draw.polygon(surface, flare_highlight, [
            (head_x + 20, head_y + 4), (head_x + 23, head_y + 2), (head_x + 26, head_y + 4),
            (head_x + 23, head_y + 7), (head_x + 20, head_y + 9)
        ])
        
        # Helmet details (extensive rivets and engravings)
        for i in range(5):
            rivet_x = head_x + 3 + i * 4
            rivet_y = head_y + 2
            pygame.draw.circle(surface, helmet_detail, (rivet_x, rivet_y), 1)
            pygame.draw.circle(surface, helmet_highlight, (rivet_x, rivet_y), 1, 1)
        
        # Additional rivets on sides
        for i in range(3):
            rivet_x = head_x + 2
            rivet_y = head_y + 4 + i * 4
            pygame.draw.circle(surface, helmet_detail, (rivet_x, rivet_y), 1)
            pygame.draw.circle(surface, helmet_highlight, (rivet_x, rivet_y), 1, 1)
            
            rivet_x = head_x + 18
            pygame.draw.circle(surface, helmet_detail, (rivet_x, rivet_y), 1)
            pygame.draw.circle(surface, helmet_highlight, (rivet_x, rivet_y), 1, 1)
        
        # Dragon scale pattern on helmet (more extensive)
        for i in range(3):
            for j in range(3):
                scale_x = head_x + 5 + i * 5
                scale_y = head_y + 5 + j * 3
                pygame.draw.ellipse(surface, helmet_detail, (scale_x, scale_y, 3, 2))
                pygame.draw.ellipse(surface, helmet_highlight, (scale_x + 1, scale_y + 1, 1, 1))
        
        # Eyes (glowing through visor)
        pygame.draw.circle(surface, (255, 255, 0), (head_x + 6, head_y + 6), 2)
        pygame.draw.circle(surface, (255, 255, 0), (head_x + 10, head_y + 6), 2)
        pygame.draw.circle(surface, (255, 255, 255), (head_x + 5, head_y + 5), 1)
        pygame.draw.circle(surface, (255, 255, 255), (head_x + 9, head_y + 5), 1)
        
        # Dragon Knight arms with armor
        arm_color = (160, 160, 180)
        arm_highlight = (200, 200, 220)
        arm_shadow = (120, 120, 140)
        
        # Left arm
        pygame.draw.rect(surface, arm_color, (guard_x + 2, guard_y + 20, 6, 12))
        pygame.draw.rect(surface, arm_highlight, (guard_x + 3, guard_y + 21, 4, 6))
        pygame.draw.rect(surface, arm_shadow, (guard_x + 2, guard_y + 20, 2, 12))
        
        # Right arm
        pygame.draw.rect(surface, arm_color, (guard_x + guard_w - 8, guard_y + 20, 6, 12))
        pygame.draw.rect(surface, arm_highlight, (guard_x + guard_w - 9, guard_y + 21, 4, 6))
        pygame.draw.rect(surface, arm_shadow, (guard_x + guard_w - 8, guard_y + 20, 2, 12))
        
        # Dragon Knight legs with armor
        leg_color = (160, 160, 180)
        leg_highlight = (200, 200, 220)
        leg_shadow = (120, 120, 140)
        
        # Left leg
        pygame.draw.rect(surface, leg_color, (guard_x + 6, guard_y + 32, 8, 12))
        pygame.draw.rect(surface, leg_highlight, (guard_x + 7, guard_y + 33, 6, 6))
        pygame.draw.rect(surface, leg_shadow, (guard_x + 6, guard_y + 32, 2, 12))
        
        # Right leg
        pygame.draw.rect(surface, leg_color, (guard_x + guard_w - 14, guard_y + 32, 8, 12))
        pygame.draw.rect(surface, leg_highlight, (guard_x + guard_w - 15, guard_y + 33, 6, 6))
        pygame.draw.rect(surface, leg_shadow, (guard_x + guard_w - 14, guard_y + 32, 2, 12))
        
        # Dragon Knight shield (detailed)
        shield_x = guard_x - 25
        shield_y = guard_y + 15
        shield_color = (140, 140, 160)
        shield_highlight = (180, 180, 200)
        shield_shadow = (100, 100, 120)
        shield_detail = (80, 80, 100)
        
        # Shield base
        pygame.draw.ellipse(surface, shield_color, (shield_x, shield_y, 20, 30))
        # Shield highlight
        pygame.draw.ellipse(surface, shield_highlight, (shield_x + 2, shield_y + 2, 16, 26))
        # Shield shadow
        pygame.draw.ellipse(surface, shield_shadow, (shield_x, shield_y, 8, 30))
        
        # Shield border
        pygame.draw.ellipse(surface, shield_detail, (shield_x, shield_y, 20, 30), 2)
        
        # Dragon emblem on shield
        dragon_center_x = shield_x + 10
        dragon_center_y = shield_y + 15
        # Dragon head
        pygame.draw.circle(surface, shield_detail, (dragon_center_x, dragon_center_y - 5), 3)
        # Dragon body
        pygame.draw.ellipse(surface, shield_detail, (dragon_center_x - 2, dragon_center_y, 4, 8))
        # Dragon wings
        pygame.draw.polygon(surface, shield_detail, 
                          [(dragon_center_x - 2, dragon_center_y + 2), (dragon_center_x - 6, dragon_center_y - 2), (dragon_center_x - 4, dragon_center_y + 4)])
        pygame.draw.polygon(surface, shield_detail, 
                          [(dragon_center_x + 2, dragon_center_y + 2), (dragon_center_x + 6, dragon_center_y - 2), (dragon_center_x + 4, dragon_center_y + 4)])
        
        # Shield handle
        pygame.draw.rect(surface, (80, 60, 40), (shield_x + 8, shield_y + 12, 4, 6))
        
        # Dragon Knight sword (silver with dragon hilt)
        sword_x = guard_x + guard_w + 5
        sword_y = guard_y + guard_h//2
        
        # Sword handle (dragon-themed)
        handle_color = (120, 80, 40)
        handle_highlight = (160, 120, 80)
        pygame.draw.rect(surface, handle_color, (sword_x, sword_y - 2, 6, 8))
        pygame.draw.rect(surface, handle_highlight, (sword_x + 1, sword_y - 1, 4, 6))
        
        # Dragon hilt detail
        pygame.draw.circle(surface, (100, 60, 20), (sword_x + 3, sword_y + 2), 2)
        pygame.draw.circle(surface, (140, 100, 60), (sword_x + 3, sword_y + 2), 1)
        
        # Sword blade (silver)
        blade_color = (220, 220, 240)
        blade_highlight = (255, 255, 255)
        blade_shadow = (180, 180, 200)
        
        pygame.draw.rect(surface, blade_color, (sword_x + 6, sword_y - 3, 25, 6))
        pygame.draw.rect(surface, blade_highlight, (sword_x + 7, sword_y - 2, 23, 4))
        pygame.draw.rect(surface, blade_shadow, (sword_x + 6, sword_y - 3, 2, 6))
        
        # Sword tip
        pygame.draw.polygon(surface, blade_color, 
                          [(sword_x + 31, sword_y - 3), (sword_x + 35, sword_y), (sword_x + 31, sword_y + 3)])
        pygame.draw.polygon(surface, blade_highlight, 
                          [(sword_x + 31, sword_y - 3), (sword_x + 33, sword_y - 1), (sword_x + 31, sword_y + 1)])
        
        # Sword guard (dragon wings)
        guard_color = (160, 120, 80)
        guard_highlight = (200, 160, 120)
        
        # Left wing of guard
        pygame.draw.polygon(surface, guard_color, 
                          [(sword_x + 4, sword_y - 4), (sword_x, sword_y - 6), (sword_x + 2, sword_y - 2)])
        pygame.draw.polygon(surface, guard_highlight, 
                          [(sword_x + 4, sword_y - 4), (sword_x + 1, sword_y - 5), (sword_x + 3, sword_y - 3)])
        
        # Right wing of guard
        pygame.draw.polygon(surface, guard_color, 
                          [(sword_x + 4, sword_y + 4), (sword_x, sword_y + 6), (sword_x + 2, sword_y + 2)])
        pygame.draw.polygon(surface, guard_highlight, 
                          [(sword_x + 4, sword_y + 4), (sword_x + 1, sword_y + 5), (sword_x + 3, sword_y + 3)])
    
    def draw_dialogue(self, surface):
        """
        Draw the guard's dialogue box
        
        Args:
            surface (pygame.Surface): The surface to draw on
        """
        # Dialogue box background
        box_x = 200
        box_y = 500
        box_w = 600
        box_h = 100
        
        # Box shadow
        pygame.draw.rect(surface, (20, 20, 20), (box_x + 3, box_y + 3, box_w, box_h))
        # Box base
        pygame.draw.rect(surface, (40, 40, 60), (box_x, box_y, box_w, box_h))
        pygame.draw.rect(surface, (80, 80, 120), (box_x, box_y, box_w, box_h), 3)
        
        # Dialogue text
        try:
            dialogue = self.dialogue[self.current_dialogue]
            text = font_small.render(dialogue, True, (255, 255, 255))
            text_rect = text.get_rect(center=(box_x + box_w//2, box_y + box_h//2))
            surface.blit(text, text_rect)
        except:
            # Fallback if font not available
            pass
        
        # Dragon Knight name
        try:
            name_text = font_tiny.render("Sir Marcus - Dragon Knight", True, (255, 215, 0))
            name_rect = name_text.get_rect(center=(box_x + box_w//2, box_y + 20))
            surface.blit(name_text, name_rect)
        except:
            pass
        
        # Draw "Press SPACE to continue" prompt
        if self.dialogue_timer > 60:
            try:
                prompt_text = font_tiny.render("Press SPACE to continue", True, (200, 200, 200))
                prompt_rect = prompt_text.get_rect(center=(500, 620))
                surface.blit(prompt_text, prompt_rect)
            except:
                pass
    
    def next_dialogue(self):
        """Advance to the next dialogue line"""
        self.current_dialogue = (self.current_dialogue + 1) % len(self.dialogue)
        self.dialogue_timer = 0
    
    def update_dialogue(self):
        """Update dialogue timer"""
        self.dialogue_timer += 1 