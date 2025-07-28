"""
Guard Entities Test Script
=========================

This script demonstrates both the Guard and DarkKnight entities side by side.
It creates a simple window showing both entities with their dialogue systems.

RESOURCE: This demonstrates the entities.guard.Guard and entities.dark_knight.DarkKnight classes.
"""

import pygame
import sys
from entities.guard import Guard
from entities.dark_knight import DarkKnight
from config.constants import *

def test_guard_entities():
    """Test both Guard and DarkKnight entities"""
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Guard Entities Test")
    clock = pygame.time.Clock()
    
    # Create both entities
    guard = Guard(200, 300)  # Left side
    dark_knight = DarkKnight(600, 300)  # Right side
    
    # Track which entity is speaking
    current_speaker = "guard"
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_speaker == "guard":
                        guard.next_dialogue()
                        current_speaker = "dark_knight"
                    else:
                        dark_knight.next_dialogue()
                        current_speaker = "guard"
                elif event.key == pygame.K_1:
                    current_speaker = "guard"
                elif event.key == pygame.K_2:
                    current_speaker = "dark_knight"
        
        # Update entities
        guard.update()
        guard.update_dialogue()
        dark_knight.update()
        dark_knight.update_dialogue()
        
        # Draw
        screen.fill((40, 40, 60))  # Dark background
        
        # Draw title
        try:
            title_font = pygame.font.Font(None, 36)
            title_text = title_font.render("Guard Entities Test - Press SPACE to advance dialogue", True, (255, 255, 255))
            screen.blit(title_text, (50, 50))
            
            subtitle_text = title_font.render("Press 1 for Guard, 2 for Dark Knight", True, (200, 200, 200))
            screen.blit(subtitle_text, (50, 80))
        except:
            pass
        
        # Draw guard
        guard.draw(screen)
        
        # Draw dark knight
        dark_knight.draw(screen)
        
        # Draw dialogue for current speaker
        if current_speaker == "guard":
            guard.draw_dialogue(screen)
        else:
            dark_knight.draw_dialogue(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    test_guard_entities() 