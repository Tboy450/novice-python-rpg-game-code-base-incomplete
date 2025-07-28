"""
DRAGON'S LAIR RPG - Opening Cutscene Module
===========================================

This module contains the OpeningCutscene class for the story introduction sequence.
It handles multiple scenes with text progression, animations, and transitions.

The OpeningCutscene features:
- Three distinct scenes (intro, dragon, story)
- Animated text appearance/disappearance
- Particle effects and visual transitions
- Scrollable story text
- Skip functionality
"""

import pygame
import random
import math
from config.constants import *
from systems.particle_system import ParticleSystem


class OpeningCutscene:
    """
    Story introduction sequence with multiple scenes and text progression.
    Sets up the game's narrative and world background.
    
    This class handles:
    - Three distinct story scenes with different visual styles
    - Animated text transitions and effects
    - Particle systems for visual enhancement
    - Scene transitions and timing
    - Skip functionality for user convenience
    """
    
    def __init__(self):
        """
        Initialize the opening cutscene with default state and timing.
        """
        self.state = "intro"
        self.timer = 0
        self.scene_duration = 300  # 5 seconds per scene at 60 FPS
        self.scene_index = 0
        self.transition_alpha = 0
        self.transition_speed = 5
        self.text_alpha = 0
        self.text_appear_speed = 3
        self.text_disappear_speed = 2
        self.particle_system = ParticleSystem()
        self.scroll_y = SCREEN_HEIGHT
        self.scroll_speed = 1
        self.transition_state = "none"  # Initialize transition_state
        
    def update(self):
        """
        Update the cutscene state, animations, and timing.
        
        Returns:
            str or None: "character_select" when cutscene ends, None otherwise
        """
        self.timer += 1
        self.particle_system.update()
        
        # Update text alpha for fade in/out effects
        if self.timer < 120:  # First 2 seconds: text appears
            self.text_alpha = min(255, self.text_alpha + self.text_appear_speed)
        elif self.timer > 180:  # Last 2 seconds: text disappears
            self.text_alpha = max(0, self.text_alpha - self.text_disappear_speed)
        
        # Scene transitions
        if self.timer >= self.scene_duration:
            self.timer = 0
            self.scene_index += 1
            self.text_alpha = 0
            self.transition_alpha = 0
            self.transition_state = "in"
            
        # Add particles for scene 2 (dragon scene)
        if self.scene_index == 1 and self.timer % 5 == 0:
            self.particle_system.add_particle(
                random.randint(0, SCREEN_WIDTH),
                -10,
                random.choice(FIRE_COLORS),
                (random.uniform(-0.5, 0.5), random.uniform(1, 3)),
                random.randint(3, 7),
                random.randint(40, 80)
            )
        
        # Scroll text for scene 3 (story scene)
        if self.scene_index == 2:
            self.scroll_y -= self.scroll_speed
            if self.scroll_y < -600:
                self.scroll_y = SCREEN_HEIGHT
        
        # Transition animation
        if self.timer > self.scene_duration - 60:  # Last second of scene
            self.transition_alpha = min(255, self.transition_alpha + self.transition_speed)
        
        # End of cutscene
        if self.scene_index >= 3:
            return "character_select"
            
        return None
    
    def draw(self, screen):
        """
        Draw the current cutscene scene with all visual elements.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Draw scene based on index
        if self.scene_index == 0:
            self.draw_intro_scene(screen)
        elif self.scene_index == 1:
            self.draw_dragon_scene(screen)
        elif self.scene_index == 2:
            self.draw_story_scene(screen)
        
        # Draw transition overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.transition_alpha))
        screen.blit(overlay, (0, 0))
        
        # Draw particles
        self.particle_system.draw(screen)
        
        # Draw skip prompt
        if pygame.time.get_ticks() % 1000 < 500:  # Blinking text
            skip_text = font_small.render("Press any key to skip...", True, (200, 200, 200))
            screen.blit(skip_text, (SCREEN_WIDTH - skip_text.get_width() - 20, SCREEN_HEIGHT - 40))
    
    def draw_intro_scene(self, screen):
        """
        Draw the intro scene with starfield background and title.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Draw starfield background
        screen.fill(BACKGROUND)
        for i in range(100):
            x = i * 10
            y = math.sin(pygame.time.get_ticks() * 0.001 + i) * 50 + SCREEN_HEIGHT//2
            pygame.draw.circle(screen, (200, 200, 255), (x, int(y)), 1)
        
        # Draw title with shadow effect
        title = font_large.render("DRAGON'S LAIR", True, (255, 50, 50))
        title_shadow = font_large.render("DRAGON'S LAIR", True, (150, 0, 0))
        screen.blit(title_shadow, (SCREEN_WIDTH//2 - title.get_width()//2 + 3, 103))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        # Draw subtitle with shadow effect
        subtitle = font_medium.render("A RETRO RPG ADVENTURE", True, TEXT_COLOR)
        subtitle_shadow = font_medium.render("A RETRO RPG ADVENTURE", True, (0, 100, 100))
        screen.blit(subtitle_shadow, (SCREEN_WIDTH//2 - subtitle.get_width()//2 + 2, 162))
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 160))
        
        # Draw intro text with fade effect
        intro_text = [
            "LONG AGO, IN THE KINGDOM OF PIXELONIA,",
            "AN ANCIENT EVIL AWOKE FROM ITS SLUMBER.",
            "THE DRAGON MALAKOR, RULER OF SHADOWS,",
            "THREATENED TO PLUNGE THE WORLD INTO DARKNESS."
        ]
        
        y_pos = 250
        for line in intro_text:
            text = font_cinematic.render(line, True, TEXT_COLOR)
            text.set_alpha(self.text_alpha)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_pos))
            screen.blit(text, text_rect)
            y_pos += 50
    
    def draw_dragon_scene(self, screen):
        """
        Draw the dragon scene with animated dragon and fire effects.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Draw dark background
        screen.fill((10, 5, 20))
        
        # Draw mountains silhouette
        for i in range(10):
            height = 150 + random.randint(0, 50)
            pygame.draw.polygon(screen, (30, 30, 60), [
                (i * 100, SCREEN_HEIGHT),
                (i * 100 + 50, SCREEN_HEIGHT - height),
                (i * 100 + 100, SCREEN_HEIGHT)
            ])
        
        # Draw dragon silhouette
        dragon_x = SCREEN_WIDTH//2 - 100
        dragon_y = SCREEN_HEIGHT//2 - 50
        
        # Dragon body
        pygame.draw.ellipse(screen, (60, 20, 20), (dragon_x, dragon_y, 200, 80))
        
        # Dragon head
        pygame.draw.circle(screen, (60, 20, 20), (dragon_x + 200, dragon_y + 40), 40)
        
        # Animated wings
        wing_offset = math.sin(pygame.time.get_ticks() * 0.005) * 10
        pygame.draw.polygon(screen, (80, 30, 30), [
            (dragon_x + 50, dragon_y + 40),
            (dragon_x - 50, dragon_y - 50 - wing_offset),
            (dragon_x + 50, dragon_y - 30 - wing_offset)
        ])
        pygame.draw.polygon(screen, (80, 30, 30), [
            (dragon_x + 50, dragon_y + 40),
            (dragon_x - 50, dragon_y + 130 + wing_offset),
            (dragon_x + 50, dragon_y + 110 + wing_offset)
        ])
        
        # Draw animated fire breath
        for i in range(20):
            x = dragon_x + 230 + i * 10
            y = dragon_y + 40 + math.sin(pygame.time.get_ticks() * 0.01 + i) * 10
            size = 10 - i * 0.4
            if size > 0:
                pygame.draw.circle(screen, (255, 150, 0), (x, y), int(size))
        
        # Draw scene text with fade effect
        scene_text = [
            "THE DRAGON MALAKOR RAVAGED THE LAND,",
            "BURNING VILLAGES AND TERRIFYING THE PEOPLE.",
            "THE KING CALLED FOR HEROES TO RISE UP",
            "AND CHALLENGE THE ANCIENT EVIL."
        ]
        
        y_pos = 100
        for line in scene_text:
            text = font_cinematic.render(line, True, (255, 200, 100))
            text.set_alpha(self.text_alpha)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_pos))
            screen.blit(text, text_rect)
            y_pos += 50
    
    def draw_story_scene(self, screen):
        """
        Draw the story scene with parchment background and scrolling text.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Draw parchment background
        screen.fill((200, 180, 120))
        pygame.draw.rect(screen, (180, 150, 100), (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
        pygame.draw.rect(screen, (150, 120, 80), (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100), 3)
        
        # Draw story text (scrolling)
        story = [
            "YOUR QUEST BEGINS...",
            "",
            "THE KINGDOM OF PIXELONIA NEEDS A HERO.",
            "MALAKOR THE TERRIBLE HAS RETURNED,",
            "AND ONLY YOU CAN STOP HIM.",
            "",
            "TRAVEL THROUGH PERILOUS LANDS,",
            "BATTLE FIERCE MONSTERS,",
            "AND GATHER POWERFUL ARTIFACTS.",
            "",
            "YOUR JOURNEY LEADS TO THE DRAGON'S LAIR,",
            "WHERE THE FINAL CONFRONTATION AWAITS.",
            "",
            "CHOOSE YOUR HERO WISELY,",
            "FOR THE FATE OF THE KINGDOM RESTS IN YOUR HANDS."
        ]
        
        y_pos = self.scroll_y
        for line in story:
            text = font_cinematic.render(line, True, (60, 40, 20))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_pos))
            screen.blit(text, text_rect)
            y_pos += 50
        
        # Draw decorative elements
        pygame.draw.line(screen, (100, 80, 60), (100, 100), (100, SCREEN_HEIGHT - 100), 2)
        pygame.draw.line(screen, (100, 80, 60), (SCREEN_WIDTH - 100, 100), (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100), 2)
        
        # Draw scroll top and bottom
        pygame.draw.rect(screen, (150, 120, 80), (40, 40, SCREEN_WIDTH - 80, 20))
        pygame.draw.rect(screen, (150, 120, 80), (40, SCREEN_HEIGHT - 60, SCREEN_WIDTH - 80, 20))
        
        # Draw continue prompt
        if self.timer > 180 and pygame.time.get_ticks() % 1000 < 500:
            prompt = font_medium.render("PRESS ENTER TO CONTINUE", True, (100, 60, 30))
            screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, SCREEN_HEIGHT - 80))
    
    def skip(self):
        """
        Skip to the end of the cutscene.
        """
        self.scene_index = 3 