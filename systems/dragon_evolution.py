"""
DRAGON'S LAIR RPG - Dragon Evolution System
==========================================

This module contains the DragonEvolutionSystem class that handles all dragon
evolution mechanics, including boss dragon progression, color evolution,
stat scaling, and visual effects.

The module provides:
- Progressive boss dragon evolution based on player level
- Color scheme evolution for different boss tiers
- Stat scaling and difficulty progression
- Visual effects and animations for evolved dragons
- Evolution tracking and history

RESOURCE: This module provides dragon evolution mechanics for the game.
"""

import pygame
import random
import math
from config.constants import *


class DragonEvolutionSystem:
    """
    Dragon Evolution System - Manages boss dragon evolution mechanics
    
    This class handles all dragon evolution logic including:
    - Boss dragon progression and scaling
    - Color evolution based on player level
    - Stat scaling and difficulty progression
    - Visual effects for evolved dragons
    - Evolution tracking and history
    
    Attributes:
        evolution_tier (int): Current evolution tier (0-9)
        evolution_history (list): History of dragon evolutions
        color_progression (list): Color progression for each tier
        stat_scaling (dict): Stat scaling factors for each tier
    """
    
    def __init__(self):
        """Initialize the dragon evolution system"""
        self.evolution_tier = 0
        self.evolution_history = []
        self.color_progression = DRAGON_BOSS_COLORS
        self.stat_scaling = {
            0: {"health_mult": 1.0, "strength_mult": 1.0, "speed_mult": 1.0},
            1: {"health_mult": 1.2, "strength_mult": 1.1, "speed_mult": 1.05},
            2: {"health_mult": 1.4, "strength_mult": 1.2, "speed_mult": 1.1},
            3: {"health_mult": 1.6, "strength_mult": 1.3, "speed_mult": 1.15},
            4: {"health_mult": 1.8, "strength_mult": 1.4, "speed_mult": 1.2},
            5: {"health_mult": 2.0, "strength_mult": 1.5, "speed_mult": 1.25},
            6: {"health_mult": 2.2, "strength_mult": 1.6, "speed_mult": 1.3},
            7: {"health_mult": 2.4, "strength_mult": 1.7, "speed_mult": 1.35},
            8: {"health_mult": 2.6, "strength_mult": 1.8, "speed_mult": 1.4},
            9: {"health_mult": 3.0, "strength_mult": 2.0, "speed_mult": 1.5}
        }
    
    def get_evolution_tier(self, player_level):
        """
        Get the current evolution tier based on player level
        
        Args:
            player_level (int): Current player level
            
        Returns:
            int: Evolution tier (0-9)
        """
        if player_level >= 10:
            return 9  # Final boss tier
        elif player_level >= 2:
            return min(player_level - 2, 8)  # Progressive tiers
        else:
            return 0  # Starting tier
    
    def get_evolved_dragon_stats(self, base_stats, player_level):
        """
        Get evolved dragon stats based on player level
        
        Args:
            base_stats (dict): Base dragon stats
            player_level (int): Current player level
            
        Returns:
            dict: Evolved dragon stats
        """
        tier = self.get_evolution_tier(player_level)
        scaling = self.stat_scaling[tier]
        
        evolved_stats = {
            "health": int(base_stats["health"] * scaling["health_mult"]),
            "strength": int(base_stats["strength"] * scaling["strength_mult"]),
            "speed": int(base_stats["speed"] * scaling["speed_mult"]),
            "tier": tier,
            "color_scheme": self.color_progression[tier]
        }
        
        return evolved_stats
    
    def get_evolution_name(self, tier):
        """
        Get the evolution name for a given tier
        
        Args:
            tier (int): Evolution tier
            
        Returns:
            str: Evolution name
        """
        evolution_names = [
            "Young Dragon",
            "Adolescent Dragon", 
            "Adult Dragon",
            "Veteran Dragon",
            "Elite Dragon",
            "Champion Dragon",
            "Legendary Dragon",
            "Ancient Dragon",
            "Elder Dragon",
            "Malakor, the Dragon Lord"
        ]
        
        return evolution_names[min(tier, len(evolution_names) - 1)]
    
    def get_evolution_effects(self, tier):
        """
        Get visual effects for a given evolution tier
        
        Args:
            tier (int): Evolution tier
            
        Returns:
            dict: Visual effects configuration
        """
        effects = {
            "aura_intensity": min(0.3 + tier * 0.1, 1.0),
            "fire_breath_size": min(1.0 + tier * 0.2, 2.5),
            "particle_count": min(20 + tier * 5, 60),
            "glow_effect": tier >= 5,
            "wing_animation_speed": 1.0 + tier * 0.2,
            "eye_glow_color": (255, 255, 255) if tier < 5 else (255, 0, 0) if tier < 8 else (255, 215, 0)
        }
        
        return effects
    
    def record_evolution(self, player_level, dragon_type, tier):
        """
        Record a dragon evolution event
        
        Args:
            player_level (int): Player level when evolution occurred
            dragon_type (str): Type of dragon that evolved
            tier (int): Evolution tier
        """
        evolution_event = {
            "player_level": player_level,
            "dragon_type": dragon_type,
            "tier": tier,
            "evolution_name": self.get_evolution_name(tier),
            "timestamp": pygame.time.get_ticks()
        }
        
        self.evolution_history.append(evolution_event)
        self.evolution_tier = max(self.evolution_tier, tier)
    
    def get_evolution_summary(self):
        """
        Get a summary of all dragon evolutions
        
        Returns:
            dict: Evolution summary statistics
        """
        if not self.evolution_history:
            return {"total_evolutions": 0, "highest_tier": 0, "evolution_count": 0}
        
        total_evolutions = len(self.evolution_history)
        highest_tier = max(event["tier"] for event in self.evolution_history)
        evolution_count = len(set(event["dragon_type"] for event in self.evolution_history))
        
        return {
            "total_evolutions": total_evolutions,
            "highest_tier": highest_tier,
            "evolution_count": evolution_count,
            "recent_evolution": self.evolution_history[-1] if self.evolution_history else None
        }
    
    def should_trigger_evolution(self, player_level, current_tier):
        """
        Check if a dragon evolution should be triggered
        
        Args:
            player_level (int): Current player level
            current_tier (int): Current evolution tier
            
        Returns:
            bool: True if evolution should be triggered
        """
        new_tier = self.get_evolution_tier(player_level)
        return new_tier > current_tier
    
    def get_evolution_animation(self, tier):
        """
        Get special animation effects for evolution
        
        Args:
            tier (int): Evolution tier
            
        Returns:
            dict: Animation configuration
        """
        animations = {
            "evolution_flash": True,
            "color_transition_duration": 60 + tier * 10,
            "particle_burst_count": 50 + tier * 10,
            "screen_shake_intensity": 3 + tier,
            "evolution_sound": True
        }
        
        return animations
    
    def reset_evolution_state(self):
        """Reset evolution system state for new game"""
        self.evolution_tier = 0
        self.evolution_history = []
    
    def get_evolution_progress(self, player_level):
        """
        Get evolution progress information
        
        Args:
            player_level (int): Current player level
            
        Returns:
            dict: Evolution progress information
        """
        current_tier = self.get_evolution_tier(player_level)
        max_tier = 9  # Maximum evolution tier
        
        progress = {
            "current_tier": current_tier,
            "max_tier": max_tier,
            "progress_percentage": (current_tier / max_tier) * 100,
            "next_evolution_level": self.get_level_for_tier(current_tier + 1),
            "evolution_name": self.get_evolution_name(current_tier)
        }
        
        return progress
    
    def get_level_for_tier(self, tier):
        """
        Get the player level required for a given evolution tier
        
        Args:
            tier (int): Evolution tier
            
        Returns:
            int: Required player level
        """
        if tier >= 9:
            return 10  # Final boss
        else:
            return tier + 2  # Progressive evolution 