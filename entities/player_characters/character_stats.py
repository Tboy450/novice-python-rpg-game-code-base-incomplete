# Character stats, leveling, and progression for player characters
from config.constants import *

# These methods implement the CharacterBase interface and are called by battle/UI modules.
def gain_exp(self, amount):
    """Add experience and check for level up (called by game/UI)."""
    self.exp += amount
    if self.exp >= self.exp_to_level:
        self.level_up()

def level_up(self):
    """Increase level and stats, reset health/mana (called by game/UI)."""
    self.level += 1
    self.exp -= self.exp_to_level
    self.exp_to_level = int(self.exp_to_level * 1.5)
    self.max_health += 20
    self.max_mana += 15
    self.strength += 3
    self.defense += 2
    self.speed += 1
    self.health = self.max_health
    self.mana = self.max_mana
    self.just_leveled_up = True
    self.boss_cooldown = False  # Reset cooldown on level up 