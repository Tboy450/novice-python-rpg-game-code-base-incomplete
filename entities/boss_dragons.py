"""
DRAGON'S LAIR RPG - Boss Dragons Module
======================================

This module contains the boss dragon classes for the game.
It includes progressive boss dragons and the final boss.

The module provides:
- DragonBoss: Progressive boss dragons that scale with player level
- BossDragon: Final boss (Malakor) with unique abilities
- Advanced dragon graphics and animations
- Fire breathing effects and special attacks
- Evolution system integration with visual effects
"""

import pygame
import random
import math
from entities.enemy import Enemy
from config.constants import *


class DragonBoss(Enemy):
    """
    Progressive boss dragon that scales with player level.
    Appears as a boss battle after leveling up.
    Now includes evolution system integration.
    """
    
    def __init__(self, boss_level):
        super().__init__(player_level=5 + boss_level * 2)
        self.size = 120
        self.x = 700
        self.y = 180
        self.enemy_type = f"boss_dragon_{boss_level}"
        self.name = f"Dragon Boss Lv.{boss_level}"
        
        # Stat scaling based on boss level
        self.health = self.max_health = 200 + boss_level * 60
        self.strength = 18 + boss_level * 4
        self.speed = 6 + boss_level // 2
        
        # Color cycling for different boss levels
        color_idx = (boss_level - 1) % len(DRAGON_BOSS_COLORS)
        self.dragon_color, self.fire_color = DRAGON_BOSS_COLORS[color_idx]
        self.color = self.dragon_color
        
        # Animation and movement properties
        self.movement_cooldown = 0
        self.movement_delay = 40
        self.animation_offset = 0
        self.attack_animation = 0
        self.hit_animation = 0
        self.fire_breathing = False
        self.fire_breath_timer = 0
        
        # Evolution system properties
        self.evolution_tier = 0
        self.evolution_effects = {}
        self.evolution_name = "Young Dragon"
        self.evolution_flash_timer = 0
    
    def start_attack_animation(self):
        """Start the fire breathing attack animation"""
        self.attack_animation = 20
        self.fire_breathing = True
        self.fire_breath_timer = 20
    
    def update_animation(self):
        """Update dragon boss animations and effects"""
        # Floating animation
        self.animation_offset = math.sin(pygame.time.get_ticks() * 0.005) * 2
        
        # Attack animation
        if self.attack_animation > 0:
            self.attack_animation -= 1
            
        # Hit animation
        if self.hit_animation > 0:
            self.hit_animation -= 1
            
        # Fire breathing timer
        if self.fire_breathing:
            self.fire_breath_timer -= 1
            if self.fire_breath_timer <= 0:
                self.fire_breathing = False
        
        # Evolution flash timer
        if self.evolution_flash_timer > 0:
            self.evolution_flash_timer -= 1
    
    def draw(self, surface):
        """Draw the dragon boss with detailed graphics and evolution effects"""
        # Calculate animation offsets
        offset_x = 0
        offset_y = self.animation_offset
        
        if self.attack_animation > 0:
            offset_x = 10 * math.sin(self.attack_animation * 0.2)
        if self.hit_animation > 0:
            offset_x = random.randint(-4, 4)
            offset_y = random.randint(-4, 4)
            
        x = self.x + offset_x
        y = self.y + offset_y
        
        # Draw evolution aura effect
        if hasattr(self, 'evolution_effects') and self.evolution_effects:
            aura_intensity = self.evolution_effects.get('aura_intensity', 0.3)
            if aura_intensity > 0:
                aura_alpha = int(50 * aura_intensity)
                aura_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
                pygame.draw.circle(aura_surf, (*self.dragon_color, aura_alpha), (100, 100), 80)
                surface.blit(aura_surf, (x - 20, y - 20))
        
        # Evolution flash effect
        if self.evolution_flash_timer > 0:
            flash_alpha = int(100 * (self.evolution_flash_timer / 30))
            flash_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
            pygame.draw.circle(flash_surf, (255, 255, 255, flash_alpha), (100, 100), 90)
            surface.blit(flash_surf, (x - 20, y - 20))
        
        # --- Draw a detailed dragon-like boss, facing left ---
        
        # Main body
        pygame.draw.ellipse(surface, self.dragon_color, (x, y + 60, 180, 60))
        
        # Tail with spikes
        pygame.draw.polygon(surface, (200, 50, 50), [
            (x + 180, y + 90), (x + 240, y + 80), (x + 180, y + 110)
        ])
        
        # Legs with claws
        pygame.draw.rect(surface, (120, 40, 20), (x + 120, y + 110, 18, 30), border_radius=8)
        pygame.draw.rect(surface, (120, 40, 20), (x + 40, y + 110, 18, 30), border_radius=8)
        
        # Claws
        pygame.draw.polygon(surface, (255, 255, 255), [
            (x + 120, y + 140), (x + 118, y + 150), (x + 124, y + 150)
        ])
        pygame.draw.polygon(surface, (255, 255, 255), [
            (x + 40, y + 140), (x + 38, y + 150), (x + 44, y + 150)
        ])
        
        # Wings (bat-like, animated with evolution speed)
        wing_y = y + 60
        wing_speed = self.evolution_effects.get('wing_animation_speed', 1.0) if hasattr(self, 'evolution_effects') else 1.0
        wing_offset = math.sin(pygame.time.get_ticks() * 0.01 * wing_speed) * 5
        pygame.draw.polygon(surface, (180, 50, 50), [
            (x + 120, wing_y), (x + 170, wing_y - 60 + wing_offset), 
            (x + 60, wing_y - 80 + wing_offset), (x + 10, wing_y - 40), (x + 60, wing_y)
        ])
        pygame.draw.polygon(surface, (180, 50, 50), [
            (x + 60, wing_y), (x + 10, wing_y - 60 - wing_offset), 
            (x, wing_y - 20), (x + 20, wing_y + 10)
        ])
        
        # Head with detailed features
        head_x = x - 40
        head_y = y + 70
        pygame.draw.ellipse(surface, self.dragon_color, (head_x, head_y, 60, 40))
        
        # Jaw (open during attack)
        if self.fire_breathing:
            pygame.draw.polygon(surface, (200, 50, 50), [
                (head_x + 20, head_y + 30), (head_x, head_y + 50), 
                (head_x + 5, head_y + 35), (head_x + 10, head_y + 30)
            ])
            
            # Teeth
            for i in range(3):
                pygame.draw.polygon(surface, (255, 255, 255), [
                    (head_x + 12 + i*6, head_y + 38), 
                    (head_x + 10 + i*6, head_y + 45), 
                    (head_x + 14 + i*6, head_y + 38)
                ])
        
        # Horns
        pygame.draw.polygon(surface, (220, 220, 220), [
            (head_x + 50, head_y + 5), (head_x + 60, head_y - 25), (head_x + 45, head_y + 5)
        ])
        pygame.draw.polygon(surface, (220, 220, 220), [
            (head_x + 10, head_y + 5), (head_x, head_y - 25), (head_x + 15, head_y + 5)
        ])
        
        # Nostrils
        pygame.draw.circle(surface, (80, 0, 0), (head_x + 15, head_y + 25), 3)
        pygame.draw.circle(surface, (80, 0, 0), (head_x + 25, head_y + 28), 3)
        
        # Eye with evolution-based glow effect
        eye_glow = math.sin(pygame.time.get_ticks() * 0.02) * 0.3 + 0.7
        if hasattr(self, 'evolution_effects') and self.evolution_effects.get('glow_effect', False):
            glow_color = self.evolution_effects.get('eye_glow_color', (255, 255, 255))
        else:
            glow_color = (int(255 * eye_glow), int(255 * eye_glow), 255)
        
        pygame.draw.circle(surface, glow_color, (head_x + 15, head_y + 15), 7)
        pygame.draw.circle(surface, (0, 0, 0), (head_x + 13, head_y + 15), 3)
        
        # Fire breath animation with evolution scaling
        if self.fire_breathing:
            mouth_x = head_x - 10
            mouth_y = head_y + 40
            player_x = 200 + 25
            player_y = 300 + 25
            
            # Evolution-based fire breath size
            fire_size_mult = self.evolution_effects.get('fire_breath_size', 1.0) if hasattr(self, 'evolution_effects') else 1.0
            particle_count = self.evolution_effects.get('particle_count', 30) if hasattr(self, 'evolution_effects') else 30
            
            for i in range(particle_count):
                t = i / particle_count
                fx = int(mouth_x * (1-t) + player_x * t + random.randint(-10, 10))
                fy = int(mouth_y * (1-t) + player_y * t + random.randint(-10, 10))
                size = int(10 * (1-t) + 40 * t * fire_size_mult)
                color = (255, 140 + random.randint(0, 100), 0, max(0, 200 - i * 6))
                
                fire_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(fire_surf, color, (size, size), size)
                surface.blit(fire_surf, (fx - size, fy - size))
        
        # Health bar with boss styling
        bar_width = 120
        bar_x = x + 60
        bar_y = y + 20
        pygame.draw.rect(surface, (20, 20, 30), (bar_x, bar_y, bar_width, 16), border_radius=2)
        health_width = (bar_width - 2) * (self.health / self.max_health)
        pygame.draw.rect(surface, HEALTH_COLOR, (bar_x + 1, bar_y + 1, health_width, 14), border_radius=2)
        
        # HP numbers
        hp_text = font_small.render(f"{self.health}/{self.max_health}", True, (255, 255, 255))
        hp_rect = hp_text.get_rect(center=(bar_x + bar_width//2, bar_y + 8))
        surface.blit(hp_text, hp_rect)
        
        # Boss name with evolution tier
        name_text = font_medium.render(self.evolution_name, True, (255, 215, 0))
        name_rect = name_text.get_rect(midtop=(x + 120, y - 10))
        surface.blit(name_text, name_rect)


class BossDragon(Enemy):
    """
    Final boss enemy (Malakor) with the most powerful abilities and unique visual design.
    Represents the ultimate challenge in the game.
    Now includes enhanced evolution effects.
    """
    
    def __init__(self):
        super().__init__(player_level=10)
        self.size = 120
        self.x = 700
        self.y = 180
        self.enemy_type = "boss_dragon"
        self.name = "Malakor, the Dragon"
        
        # Final boss stats
        self.health = 400
        self.max_health = 400
        self.strength = 35
        self.speed = 10
        self.color = (255, 69, 0)
        
        # Animation and movement properties
        self.movement_cooldown = 0
        self.movement_delay = 40
        self.animation_offset = 0
        self.attack_animation = 0
        self.hit_animation = 0
        self.fire_breathing = False
        self.fire_breath_timer = 0
        
        # Special final boss effects
        self.aura_timer = 0
        self.aura_color = (255, 215, 0)
        
        # Evolution system properties for final boss
        self.evolution_tier = 9
        self.evolution_effects = {
            "aura_intensity": 1.0,
            "fire_breath_size": 2.5,
            "particle_count": 60,
            "glow_effect": True,
            "wing_animation_speed": 2.0,
            "eye_glow_color": (255, 215, 0)
        }
        self.evolution_name = "Malakor, the Dragon Lord"
        self.evolution_flash_timer = 0
    
    def start_attack_animation(self):
        """Start the devastating fire breathing attack animation"""
        self.attack_animation = 20
        self.fire_breathing = True
        self.fire_breath_timer = 20
    
    def update_animation(self):
        """Update final boss animations and special effects"""
        # Enhanced floating animation
        self.animation_offset = math.sin(pygame.time.get_ticks() * 0.005) * 3
        
        # Attack animation
        if self.attack_animation > 0:
            self.attack_animation -= 1
            
        # Hit animation
        if self.hit_animation > 0:
            self.hit_animation -= 1
            
        # Fire breathing timer
        if self.fire_breathing:
            self.fire_breath_timer -= 1
            if self.fire_breath_timer <= 0:
                self.fire_breathing = False
        
        # Aura effect timer
        self.aura_timer += 1
        
        # Evolution flash timer
        if self.evolution_flash_timer > 0:
            self.evolution_flash_timer -= 1
    
    def draw(self, surface):
        """Draw the final boss dragon with enhanced graphics and evolution effects"""
        # Calculate animation offsets
        offset_x = 0
        offset_y = self.animation_offset
        
        if self.attack_animation > 0:
            offset_x = 10 * math.sin(self.attack_animation * 0.2)
        if self.hit_animation > 0:
            offset_x = random.randint(-4, 4)
            offset_y = random.randint(-4, 4)
            
        x = self.x + offset_x
        y = self.y + offset_y
        
        # Draw enhanced aura effect for final boss
        aura_alpha = int(50 + 30 * math.sin(self.aura_timer * 0.1))
        aura_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.circle(aura_surf, (*self.aura_color, aura_alpha), (100, 100), 80)
        surface.blit(aura_surf, (x - 20, y - 20))
        
        # Evolution flash effect
        if self.evolution_flash_timer > 0:
            flash_alpha = int(150 * (self.evolution_flash_timer / 30))
            flash_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
            pygame.draw.circle(flash_surf, (255, 215, 0, flash_alpha), (100, 100), 90)
            surface.blit(flash_surf, (x - 20, y - 20))
        
        # --- Draw the ultimate dragon boss, facing left ---
        
        # Main body with enhanced detail
        pygame.draw.ellipse(surface, DRAGON_COLOR, (x, y + 60, 180, 60))
        
        # Tail with enhanced spikes
        pygame.draw.polygon(surface, (200, 50, 50), [
            (x + 180, y + 90), (x + 240, y + 80), (x + 180, y + 110)
        ])
        
        # Enhanced legs with claws
        pygame.draw.rect(surface, (120, 40, 20), (x + 120, y + 110, 18, 30), border_radius=8)
        pygame.draw.rect(surface, (120, 40, 20), (x + 40, y + 110, 18, 30), border_radius=8)
        
        # Sharp claws
        pygame.draw.polygon(surface, (255, 255, 255), [
            (x + 120, y + 140), (x + 118, y + 150), (x + 124, y + 150)
        ])
        pygame.draw.polygon(surface, (255, 255, 255), [
            (x + 40, y + 140), (x + 38, y + 150), (x + 44, y + 150)
        ])
        
        # Enhanced wings with more detail
        wing_y = y + 60
        wing_offset = math.sin(pygame.time.get_ticks() * 0.01 * 2.0) * 5
        pygame.draw.polygon(surface, (180, 50, 50), [
            (x + 120, wing_y), (x + 170, wing_y - 60 + wing_offset), 
            (x + 60, wing_y - 80 + wing_offset), (x + 10, wing_y - 40), (x + 60, wing_y)
        ])
        pygame.draw.polygon(surface, (180, 50, 50), [
            (x + 60, wing_y), (x + 10, wing_y - 60 - wing_offset), 
            (x, wing_y - 20), (x + 20, wing_y + 10)
        ])
        
        # Enhanced head with more detail
        head_x = x - 40
        head_y = y + 70
        pygame.draw.ellipse(surface, DRAGON_COLOR, (head_x, head_y, 60, 40))
        
        # Jaw (open during attack)
        if self.fire_breathing:
            pygame.draw.polygon(surface, (200, 50, 50), [
                (head_x + 20, head_y + 30), (head_x, head_y + 50), 
                (head_x + 5, head_y + 35), (head_x + 10, head_y + 30)
            ])
            
            # Sharp teeth
            for i in range(3):
                pygame.draw.polygon(surface, (255, 255, 255), [
                    (head_x + 12 + i*6, head_y + 38), 
                    (head_x + 10 + i*6, head_y + 45), 
                    (head_x + 14 + i*6, head_y + 38)
                ])
        
        # Enhanced horns
        pygame.draw.polygon(surface, (220, 220, 220), [
            (head_x + 50, head_y + 5), (head_x + 60, head_y - 25), (head_x + 45, head_y + 5)
        ])
        pygame.draw.polygon(surface, (220, 220, 220), [
            (head_x + 10, head_y + 5), (head_x, head_y - 25), (head_x + 15, head_y + 5)
        ])
        
        # Nostrils
        pygame.draw.circle(surface, (80, 0, 0), (head_x + 15, head_y + 25), 3)
        pygame.draw.circle(surface, (80, 0, 0), (head_x + 25, head_y + 28), 3)
        
        # Enhanced eye with evil glow
        eye_glow = math.sin(pygame.time.get_ticks() * 0.02) * 0.3 + 0.7
        glow_color = (255, 215, 0)  # Golden evil glow for final boss
        pygame.draw.circle(surface, glow_color, (head_x + 15, head_y + 15), 7)
        pygame.draw.circle(surface, (0, 0, 0), (head_x + 13, head_y + 15), 3)
        
        # Devastating fire breath animation with maximum evolution effects
        if self.fire_breathing:
            mouth_x = head_x - 10
            mouth_y = head_y + 40
            player_x = 200 + 25
            player_y = 300 + 25
            
            for i in range(60):  # Maximum particle count
                t = i / 60
                fx = int(mouth_x * (1-t) + player_x * t + random.randint(-10, 10))
                fy = int(mouth_y * (1-t) + player_y * t + random.randint(-10, 10))
                size = int(10 * (1-t) + 40 * t * 2.5)  # Maximum fire breath size
                color = (255, 140 + random.randint(0, 100), 0, max(0, 200 - i * 6))
                
                fire_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(fire_surf, color, (size, size), size)
                surface.blit(fire_surf, (fx - size, fy - size))
        
        # Enhanced health bar for final boss
        bar_width = 120
        bar_x = x + 60
        bar_y = y + 20
        pygame.draw.rect(surface, (20, 20, 30), (bar_x, bar_y, bar_width, 16), border_radius=2)
        health_width = (bar_width - 2) * (self.health / self.max_health)
        pygame.draw.rect(surface, HEALTH_COLOR, (bar_x + 1, bar_y + 1, health_width, 14), border_radius=2)
        
        # HP numbers
        hp_text = font_small.render(f"{self.health}/{self.max_health}", True, (255, 255, 255))
        hp_rect = hp_text.get_rect(center=(bar_x + bar_width//2, bar_y + 8))
        surface.blit(hp_text, hp_rect)
        
        # Final boss name with special styling
        name_text = font_medium.render(self.evolution_name, True, (255, 215, 0))
        name_rect = name_text.get_rect(midtop=(x + 120, y - 10))
        surface.blit(name_text, name_rect) 