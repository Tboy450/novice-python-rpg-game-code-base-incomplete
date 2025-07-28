"""
DRAGON'S LAIR RPG - Button Module
=================================

This module contains the Button class for UI elements.
"""

import pygame
from config.constants import *

class Button:
    """
    Interactive button for menus and UI elements.
    Handles hover effects and click detection.
    """
    def __init__(self, x, y, width, height, text, color=UI_BORDER, hover_color=(255, 215, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.text_surf = font_medium.render(text, True, TEXT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.glow = 0
        self.glow_dir = 1
        self.selected = False
        
    def draw(self, surface):
        """Draw the button with glow effects and selection state"""
        if self.glow > 0 or self.selected:
            glow_radius = max(self.glow, 8 if self.selected else 0)
            glow_surf = pygame.Surface((self.rect.width + glow_radius*2, self.rect.height + glow_radius*2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*self.current_color[:3], 50), glow_surf.get_rect(), border_radius=12)
            surface.blit(glow_surf, (self.rect.x - glow_radius, self.rect.y - glow_radius))
        
        pygame.draw.rect(surface, UI_BG, self.rect, border_radius=8)
        
        border_color = (255, 215, 0) if self.selected else self.current_color
        border_width = 4 if self.selected else 3
        pygame.draw.rect(surface, border_color, self.rect, border_width, border_radius=8)
        
        surface.blit(self.text_surf, self.text_rect)
        
    def update(self, mouse_pos):
        """Update button hover state and glow effects"""
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
            self.glow = min(self.glow + 2, 10)
            return True
        else:
            self.current_color = self.color
            self.glow = max(self.glow - 1, 0)
        return False
        
    def is_clicked(self, mouse_pos, mouse_click):
        """Check if button was clicked"""
        return self.rect.collidepoint(mouse_pos) and mouse_click 