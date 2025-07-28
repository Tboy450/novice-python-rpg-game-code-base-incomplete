"""
DRAGON'S LAIR RPG - Player Character Main Class
==============================================

This module contains the Character factory class for player characters.
Depending on char_type, it instantiates Warrior, Mage, or Rogue.
All logic for actions, animation, and stats is split into separate modules in this package.

Interface Note:
---------------
CharacterBase defines the required interface for animation and action methods.
Battle and UI modules (e.g., battle_screen, battle_actions, battle_effects) will call these methods to trigger or update character animations.
"""

import pygame
import math
import random
from config.constants import *
from abc import ABC, abstractmethod
# Import character animation module for battle-specific animations only
from . import character_animation

class CharacterBase(ABC):
    """
    Abstract base class for all player character types.
    Provides the interface for animation and action methods used by battle/UI modules.
    """
    @abstractmethod
    def start_attack_animation(self):
        """Trigger the character's attack animation (called by battle modules)."""
        pass

    @abstractmethod
    def start_hit_animation(self):
        """Trigger the character's hit animation (called by battle modules)."""
        pass

    @abstractmethod
    def update_animation(self):
        """Update the character's animation state (called every frame)."""
        pass

    @abstractmethod
    def draw(self, surface):
        """Draw the character sprite (called by UI/battle modules)."""
        pass

    @abstractmethod
    def draw_stats(self, surface, x, y):
        """Draw the character's stats (HP, MP, EXP, etc.) on the given surface."""
        pass

class Character:
    """
    Character factory/wrapper. Instantiates the correct subclass (Warrior, Mage, Rogue) based on char_type.
    Implements the CharacterBase interface for use in battle/UI modules.
    """
    def __new__(cls, char_type="Warrior"):
        if char_type == "Warrior":
            from .warrior import Warrior
            return Warrior()
        elif char_type == "Mage":
            from .mage import Mage
            return Mage()
        else:
            from .rogue import Rogue
            return Rogue() 