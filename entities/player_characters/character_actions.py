# Character actions and interactions for player characters
from config.constants import *

# These methods implement the CharacterBase interface and are called by battle/UI modules.
def move(self, dx, dy):
    """Move the character by (dx, dy) grid units. Called by game logic/UI."""
    new_x = self.x + dx * GRID_SIZE
    new_y = self.y + dy * GRID_SIZE
    # Keep character within world bounds
    if 0 <= new_x < WORLD_WIDTH:
        self.x = new_x
    if 0 <= new_y < WORLD_HEIGHT:
        self.y = new_y

def start_attack_animation(self):
    """Trigger the character's attack animation (called by battle/UI modules)."""
    self.attack_animation = 10

def start_hit_animation(self):
    """Trigger the character's hit animation (called by battle/UI modules)."""
    self.hit_animation = 5

def take_damage(self, damage):
    """Apply damage and trigger hit animation (called by battle/UI modules)."""
    actual_damage = max(1, damage - self.defense // 3)
    self.health -= actual_damage
    self.start_hit_animation()
    return actual_damage 