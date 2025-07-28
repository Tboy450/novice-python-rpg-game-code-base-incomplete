"""
DRAGON'S LAIR RPG - Start Screen Module
=======================================

This module contains the start screen with animated dragon graphics.
It handles the title screen, dragon animations, and start menu UI.

RESOURCE FLOW EXPLANATION:
=========================
1. BACKGROUND RENDERING:
   - Game class fills background with config.constants.BACKGROUND (dark blue)
   - Game class draws animated starfield and flying dragons
   - StartScreen draws UI content on top (no background fill)
   - This ensures proper layering with animated background

2. DRAGON GRAPHICS:
   - Uses entities.dragon.Dragon class for animated dragon
   - Dragon is positioned at screen center with fire breathing effects
   - Graphics are procedurally generated (no external image files)

3. UI ELEMENTS:
   - Uses ui.button.Button class for interactive buttons
   - Button colors from config.constants (UI_BORDER, TEXT_COLOR)
   - Fonts from config.constants (font_large, font_medium, font_tiny)

4. ANIMATION SYSTEM:
   - Title glow effect using sine wave animation
   - Dragon fire breathing with random timing
   - Button hover effects with color transitions

5. STATE MANAGEMENT:
   - Returns state transitions to Game class
   - Handles mouse input and button clicks
   - Manages character selection flow

6. AUDIO INTEGRATION:
   - Music system handled by Game class
   - Sound effects triggered by button clicks
   - Procedural chiptune music from audio.music_system

DEPENDENCIES:
=============
- config.constants: Colors, fonts, screen dimensions
- entities.dragon: Animated dragon graphics
- ui.button: Interactive button components
- pygame: Graphics and input handling
"""

import pygame
import random
import math
from entities.dragon import Dragon
from ui.button import Button
from config.constants import *


class StartScreen:
    """
    Start screen with animated dragon and menu system.
    Handles the title screen, character selection, and transitions.
    
    RESOURCE USAGE:
    ===============
    - Dragon graphics: entities.dragon.Dragon class
    - Button UI: ui.button.Button class  
    - Colors: config.constants (BACKGROUND, UI_BORDER, TEXT_COLOR)
    - Fonts: config.constants (font_large, font_medium, font_tiny)
    - Screen dimensions: config.constants (SCREEN_WIDTH, SCREEN_HEIGHT)
    """

    def __init__(self):
        """Initialize the start screen with dragon and UI elements"""
        # Dragon will be provided by Game class
        self.dragon = None

        # Create UI buttons using ui.button.Button class
        # RESOURCE: Button colors from config.constants.UI_BORDER
        self.start_button = Button(SCREEN_WIDTH//2 - 120, 500, 240, 60, "START QUEST", UI_BORDER)
        self.quit_button = Button(SCREEN_WIDTH//2 - 120, 580, 240, 60, "QUIT", UI_BORDER)

        # Character selection buttons with class-specific colors
        # RESOURCE: Colors represent character classes (Warrior=Green, Mage=Blue, Rogue=Orange)
        self.warrior_button = Button(SCREEN_WIDTH//2 - 300, 300, 200, 60, "WARRIOR", (0, 255, 0))
        self.mage_button = Button(SCREEN_WIDTH//2 - 50, 300, 200, 60, "MAGE", (0, 200, 255))
        self.rogue_button = Button(SCREEN_WIDTH//2 + 200, 300, 200, 60, "ROGUE", (255, 100, 0))
        self.back_button = Button(SCREEN_WIDTH//2 - 120, 580, 240, 60, "BACK", UI_BORDER)

        # Animation state for title glow effect
        # RESOURCE: Procedural animation using sine wave
        self.title_glow = 0
        self.glow_direction = 1

    def update(self):
        """
        Update start screen animations and state.
        
        RESOURCE USAGE:
        ===============
        - Dragon animation: Handled by Game class
        - Fire breathing: Handled by Game class
        - Title glow: Sine wave animation for pulsing effect
        
        Returns:
            str or None: State to transition to, or None to stay in current state
        """
        # Dragon animation is handled by Game class

        # Update title glow effect using sine wave animation
        # RESOURCE: Procedural animation creates pulsing title effect
        self.title_glow += 0.1 * self.glow_direction
        if self.title_glow > 1.0:
            self.title_glow = 1.0
            self.glow_direction = -1
        elif self.title_glow < 0.0:
            self.title_glow = 0.0
            self.glow_direction = 1

        return None

    def draw_start_menu(self, screen):
        """
        Draw the main start menu with animated dragon and title.
        
        RESOURCE USAGE:
        ===============
        - Background: Handled by Game class (starfield + flying dragons)
        - Title font: config.constants.font_large
        - Subtitle font: config.constants.font_medium  
        - Text color: config.constants.TEXT_COLOR (cyan)
        - Dragon graphics: entities.dragon.Dragon.draw()
        - Button UI: ui.button.Button.draw()
        - Instructions font: config.constants.font_tiny
        
        Args:
            screen: Pygame surface to draw on
        """
        # NOTE: Background is filled by Game class before calling this method
        # RESOURCE: Game class handles starfield and flying dragons background
        
        # Update button text if needed
        if self.start_button.text != "START QUEST":
            self.start_button.text = "START QUEST"
            # RESOURCE: font_medium from config.constants for button text
            self.start_button.text_surf = font_medium.render(self.start_button.text, True, TEXT_COLOR)
            self.start_button.text_rect = self.start_button.text_surf.get_rect(center=self.start_button.rect.center)
        
        # Draw animated title with glow effect
        # RESOURCE: font_large from config.constants, glow effect from sine wave animation
        glow_intensity = int(50 + 30 * self.title_glow)
        title_color = (255, 50 + glow_intensity, 50)  # Red with glow effect
        title = font_large.render("DRAGON'S LAIR", True, title_color)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        
        # Draw subtitle using font_medium from config.constants
        subtitle = font_medium.render("A RETRO RPG ADVENTURE", True, TEXT_COLOR)
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 140))
        
        # Draw animated dragon from Game class
        # RESOURCE: Dragon graphics are procedurally generated
        # Note: Dragon is managed by Game class, not StartScreen
        
        # Draw UI buttons from ui.button.Button class
        # RESOURCE: Button colors and hover effects from Button class
        self.start_button.draw(screen)
        self.quit_button.draw(screen)
        
        # Draw instructions using font_tiny from config.constants
        instructions = [
            "SELECT YOUR HERO AND EMBARK ON A QUEST",
            "DEFEAT THE DRAGON'S MINIONS AND SURVIVE!",
            "",
            "CONTROLS:",
            "ARROWS/WASD - MOVE",
            "ENTER - SELECT",
            "ESC - QUIT"
        ]
        
        for i, line in enumerate(instructions):
            # RESOURCE: font_tiny from config.constants for instruction text
            text = font_tiny.render(line, True, TEXT_COLOR)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 350 + i*25))

    def draw_character_select(self, screen):
        """
        Draw the character selection screen.
        
        RESOURCE USAGE:
        ===============
        - Background: Handled by Game class (starfield + flying dragons)
        - Title font: config.constants.font_large
        - Description font: config.constants.font_tiny
        - Character colors: Green (Warrior), Blue (Mage), Orange (Rogue)
        - Button UI: ui.button.Button.draw()
        
        Args:
            screen: Pygame surface to draw on
        """
        # NOTE: Background is filled by Game class before calling this method
        # RESOURCE: Game class handles starfield and flying dragons background
        
        # Draw title using font_large from config.constants
        title = font_large.render("CHOOSE YOUR HERO", True, TEXT_COLOR)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        # Character descriptions with class-specific colors
        # RESOURCE: Colors represent character class themes
        warrior_desc = [
            "THE WARRIOR",
            "- HIGH HEALTH",
            "- STRONG ATTACKS",
            "- GOOD DEFENSE",
            "- MEDIUM SPEED"
        ]
        
        mage_desc = [
            "THE MAGE",
            "- HIGH MANA",
            "- MAGIC ATTACKS",
            "- LOW DEFENSE",
            "- MEDIUM SPEED"
        ]
        
        rogue_desc = [
            "THE ROGUE",
            "- BALANCED STATS",
            "- QUICK ATTACKS",
            "- AVERAGE DEFENSE",
            "- HIGH SPEED"
        ]
        
        # Draw warrior description in green
        y_pos = 480
        for line in warrior_desc:
            # RESOURCE: font_tiny from config.constants, green color for Warrior
            text = font_tiny.render(line, True, (0, 255, 0))
            screen.blit(text, (SCREEN_WIDTH//2 - 300, y_pos))
            y_pos += 25
        
        # Draw mage description in blue
        y_pos = 480
        for line in mage_desc:
            # RESOURCE: font_tiny from config.constants, blue color for Mage
            text = font_tiny.render(line, True, (0, 200, 255))
            screen.blit(text, (SCREEN_WIDTH//2 - 50, y_pos))
            y_pos += 25
        
        # Draw rogue description in orange
        y_pos = 480
        for line in rogue_desc:
            # RESOURCE: font_tiny from config.constants, orange color for Rogue
            text = font_tiny.render(line, True, (255, 100, 0))
            screen.blit(text, (SCREEN_WIDTH//2 + 200, y_pos))
            y_pos += 25
        
        # Draw character buttons from ui.button.Button class
        # RESOURCE: Button colors match character class themes
        self.warrior_button.draw(screen)
        self.mage_button.draw(screen)
        self.rogue_button.draw(screen)
        self.back_button.draw(screen)

    def handle_start_menu_clicks(self, mouse_pos, mouse_click):
        """
        Handle button clicks in the start menu.
        
        RESOURCE USAGE:
        ===============
        - Button detection: ui.button.Button.is_clicked()
        - State transitions: Returns strings for Game class state management
        
        Args:
            mouse_pos: Current mouse position
            mouse_click: Whether mouse was clicked
            
        Returns:
            str or None: State to transition to, or None to stay in current state
        """
        if mouse_click:
            # RESOURCE: Button click detection from ui.button.Button class
            if self.start_button.is_clicked(mouse_pos, mouse_click):
                return "opening_cutscene"
            elif self.quit_button.is_clicked(mouse_pos, mouse_click):
                return "quit"
        return None
        
    def handle_character_select_clicks(self, mouse_pos, mouse_click):
        """
        Handle button clicks in the character selection screen.
        
        RESOURCE USAGE:
        ===============
        - Button detection: ui.button.Button.is_clicked()
        - Character creation: Returns character type for Game class
        - State transitions: Returns tuples for Game class state management
        
        Args:
            mouse_pos: Current mouse position
            mouse_click: Whether mouse was clicked
            
        Returns:
            tuple or None: (state, character_type) or None to stay in current state
        """
        if mouse_click:
            # RESOURCE: Button click detection from ui.button.Button class
            if self.warrior_button.is_clicked(mouse_pos, mouse_click):
                return ("overworld", "Warrior")
            elif self.mage_button.is_clicked(mouse_pos, mouse_click):
                return ("overworld", "Mage")
            elif self.rogue_button.is_clicked(mouse_pos, mouse_click):
                return ("overworld", "Rogue")
            elif self.back_button.is_clicked(mouse_pos, mouse_click):
                return ("start_menu", None)
        return None
        
    def update_buttons(self, mouse_pos):
        """
        Update button hover states.
        
        RESOURCE USAGE:
        ===============
        - Button hover effects: ui.button.Button.update()
        
        Args:
            mouse_pos: Current mouse position
        """
        # RESOURCE: Button hover effects from ui.button.Button class
        self.start_button.update(mouse_pos)
        self.quit_button.update(mouse_pos)
        self.warrior_button.update(mouse_pos)
        self.mage_button.update(mouse_pos)
        self.rogue_button.update(mouse_pos)
        self.back_button.update(mouse_pos) 