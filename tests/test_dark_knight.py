"""
Dark Knight Test Script
=======================

This script demonstrates the DarkKnight entity functionality.
It creates a simple window showing the dark knight with dialogue.

RESOURCE: This demonstrates the entities.dark_knight.DarkKnight class.
"""

import pygame
import sys
from entities.dark_knight import DarkKnight
from config.constants import *

def test_dark_knight():
    """Test the DarkKnight entity"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Dark Knight Test")
    clock = pygame.time.Clock()
    
    # Create dark knight
    dark_knight = DarkKnight(400, 300)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dark_knight.next_dialogue()
        
        # Update dark knight
        dark_knight.update()
        dark_knight.update_dialogue()
        
        # Draw
        screen.fill((20, 20, 40))  # Dark background
        
        # Draw dark knight
        dark_knight.draw(screen)
        
        # Draw dialogue
        dark_knight.draw_dialogue(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    test_dark_knight() 