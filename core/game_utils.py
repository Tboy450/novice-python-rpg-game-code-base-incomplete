"""
DRAGON'S LAIR RPG - Game Utilities Module
=======================================

This module contains utility functions extracted from the Game class.
It handles game mechanics, spawning, and helper functions.

The module provides:
- Enemy and item spawning logic
- Game state management utilities
- Helper functions for game mechanics
- Area-specific logic and calculations
"""

import random
import math
from entities.enemy import Enemy, DragonBoss, BossDragon
from entities.item import Item
from world.world_area import AREA_WIDTH, AREA_HEIGHT
from config.constants import *


# Removed old spawn_enemy function - now using the improved version in core/game.py


def spawn_item(game):
    """
    Spawn an item in the current area.
    
    Args:
        game: The main Game instance
    """
    current_area = game.world_map.get_current_area()
    if current_area and len(current_area.items) < 2:
        # Spawn item in current area
        item = Item()
        # Position item randomly within the current area
        area_world_x, area_world_y = current_area.get_world_position()
        item.x = area_world_x + random.randint(100, AREA_WIDTH - 100)
        item.y = area_world_y + random.randint(100, AREA_HEIGHT - 100)
        current_area.items.append(item)
        game.items.append(item)


def check_battle_collision(game):
    """
    Check for battle collisions between player and enemies.
    
    Args:
        game: The main Game instance
        
    Returns:
        bool: True if battle was triggered, False otherwise
    """
    for enemy in game.enemies[:]:
        if game.player:  # Ensure player exists
            player_rect = pygame.Rect(game.player.x, game.player.y, PLAYER_SIZE, PLAYER_SIZE)
            enemy_rect = pygame.Rect(enemy.x, enemy.y, ENEMY_SIZE, ENEMY_SIZE)
            if player_rect.colliderect(enemy_rect):
                game.battle_screen = game.battle_screen.__class__(game.player, enemy)
                game.battle_screen.start_transition()
                game.state = "battle"
                # Remove enemy from both lists
                game.enemies.remove(enemy)
                current_area = game.world_map.get_current_area()
                if current_area and enemy in current_area.enemies:
                    current_area.enemies.remove(enemy)
                game.player_moved = False
                return True
    return False


def check_item_collision(game):
    """
    Check for item collisions and handle item collection.
    
    Args:
        game: The main Game instance
    """
    for item in game.items[:]:
        if game.player:  # Ensure player exists
            item_rect = pygame.Rect(item.x, item.y, ITEM_SIZE, ITEM_SIZE)
            player_rect = pygame.Rect(game.player.x, game.player.y, PLAYER_SIZE, PLAYER_SIZE)
            if player_rect.colliderect(item_rect):
                if item.type == "health":
                    game.player.health = min(game.player.max_health, game.player.health + 30)
                    for _ in range(15):
                        x = random.randint(game.player.x, game.player.x + PLAYER_SIZE)
                        y = random.randint(game.player.y, game.player.y + PLAYER_SIZE)
                        game.particle_system.add_particle(
                            x, y, HEALTH_COLOR,
                            (random.uniform(-0.5, 0.5), random.uniform(-1, -0.5)),
                            3, 30
                        )
                else:
                    game.player.mana = min(game.player.max_mana, game.player.mana + 40)
                    for _ in range(15):
                        x = random.randint(game.player.x, game.player.x + PLAYER_SIZE)
                        y = random.randint(game.player.y, game.player.y + PLAYER_SIZE)
                        game.particle_system.add_particle(
                            x, y, MANA_COLOR,
                            (random.uniform(-0.5, 0.5), random.uniform(-1, -0.5)),
                            3, 30
                        )
                game.player.items_collected += 1
                # Remove item from both lists
                if item in game.items:
                    game.items.remove(item)
                current_area = game.world_map.get_current_area()
                if current_area and item in current_area.items:
                    current_area.items.remove(item)


def handle_battle_result(game):
    """
    Handle the result of a battle and update game state accordingly.
    
    Args:
        game: The main Game instance
        
    Returns:
        bool: True if game should continue, False if state changed
    """
    battle_ended = game.battle_screen.update()
    
    if battle_ended:
        # Boss battle win
        if hasattr(game.battle_screen.enemy, 'enemy_type') and "boss_dragon" in game.battle_screen.enemy.enemy_type:
            if game.battle_screen.result == "win":
                game.player.just_leveled_up = False
                game.player.kills += 1
                game.player.gain_exp(45)  # Boss gives more exp than regular enemies (25)
                game.score += 25  # Boss gives more score too
                game.player.boss_cooldown = True  # Set cooldown after boss battle
                game.player.last_boss_level = game.player.level  # Set after the fight
                if game.battle_screen.enemy.enemy_type == "boss_dragon":
                    game.boss_defeated = True
                    game.state = "victory"
                    game.battle_screen = None
                    game.music.update(game.state, False)  # Explicitly reset music state
                else:
                    print(f"Boss battle ended - transitioning to overworld")
                    game.state = "overworld"
                    game.battle_screen = None
                    game.music.update(game.state, False)  # Explicitly reset music state
                return False
            elif game.battle_screen.result == "lose":
                game.state = "game_over"
                game.battle_screen = None
                game.music.update(game.state, False)  # Explicitly reset music state
                return False
            elif game.battle_screen.result == "escape":
                game.player.exp = 0
                game.player.just_leveled_up = False
                game.player.boss_cooldown = True  # Set cooldown after boss battle
                game.player.last_boss_level = game.player.level  # Set after the fight
                print(f"Boss battle escaped - transitioning to overworld")
                game.state = "overworld"
                game.battle_screen = None
                game.music.update(game.state, False)  # Explicitly reset music state
                return False
        else:
            if game.battle_screen.result == "win":
                game.player.kills += 1
                game.player.gain_exp(25)
                game.score += 10
                game.start_transition()
                print(f"Battle ended - transitioning to overworld")
                game.state = "overworld"
                game.battle_screen = None
                game.music.update(game.state, False)  # Explicitly reset music state
            elif game.battle_screen.result == "lose":
                game.state = "game_over"
                game.battle_screen = None
                game.music.update(game.state, False)  # Explicitly reset music state
            elif game.battle_screen.result == "escape":
                game.player.exp = 0
                game.player.just_leveled_up = False
                print(f"Battle escaped - transitioning to overworld")
                game.state = "overworld"
                game.battle_screen = None
                game.music.update(game.state, False)  # Explicitly reset music state
                return False
    return True


def generate_area_particles(game, current_area):
    """
    Generate area-specific particle effects.
    
    Args:
        game: The main Game instance
        current_area: The current world area
    """
    if current_area:
        current_area.particle_timer += 1
        if current_area.particle_timer >= current_area.particle_interval:
            current_area.particle_timer = 0
            
            # Spawn area-specific particles
            area_world_x, area_world_y = current_area.get_world_position()
            if current_area.area_type == "volcano":
                # Lava particles
                for _ in range(5):
                    x = area_world_x + random.randint(0, AREA_WIDTH)
                    y = area_world_y + random.randint(0, AREA_HEIGHT)
                    game.particle_system.add_particle(
                        x, y, (255, 100, 0),
                        (random.uniform(-0.5, 0.5), random.uniform(-2, -0.5)),
                        6, 40
                    )
            elif current_area.area_type == "ice":
                # Snow particles
                for _ in range(4):
                    x = area_world_x + random.randint(0, AREA_WIDTH)
                    y = area_world_y + random.randint(0, AREA_HEIGHT)
                    game.particle_system.add_particle(
                        x, y, (200, 220, 255),
                        (random.uniform(-0.3, 0.3), random.uniform(0.5, 1.5)),
                        4, 50
                    )
            elif current_area.area_type == "swamp":
                # Mist particles
                for _ in range(3):
                    x = area_world_x + random.randint(0, AREA_WIDTH)
                    y = area_world_y + random.randint(0, AREA_HEIGHT)
                    game.particle_system.add_particle(
                        x, y, (150, 180, 150),
                        (random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)),
                        5, 60
                    )
            elif current_area.area_type == "forest":
                # Leaf particles
                for _ in range(4):
                    x = area_world_x + random.randint(0, AREA_WIDTH)
                    y = area_world_y + random.randint(0, AREA_HEIGHT)
                    game.particle_system.add_particle(
                        x, y, (100, 150, 50),
                        (random.uniform(-0.3, 0.3), random.uniform(-0.5, -0.1)),
                        5, 45
                    )
            elif current_area.area_type == "desert":
                # Sand particles
                for _ in range(6):
                    x = area_world_x + random.randint(0, AREA_WIDTH)
                    y = area_world_y + random.randint(0, AREA_HEIGHT)
                    game.particle_system.add_particle(
                        x, y, (200, 180, 120),
                        (random.uniform(-1, 1), random.uniform(-0.5, 0.5)),
                        4, 35
                    )
            elif current_area.area_type == "mountain":
                # Wind particles
                for _ in range(3):
                    x = area_world_x + random.randint(0, AREA_WIDTH)
                    y = area_world_y + random.randint(0, AREA_HEIGHT)
                    game.particle_system.add_particle(
                        x, y, (180, 180, 200),
                        (random.uniform(-0.8, 0.8), random.uniform(-0.3, 0.3)),
                        4, 40
                    )
            elif current_area.area_type == "beach":
                # Sea foam particles
                for _ in range(4):
                    x = area_world_x + random.randint(0, AREA_WIDTH)
                    y = area_world_y + random.randint(0, AREA_HEIGHT)
                    game.particle_system.add_particle(
                        x, y, (220, 240, 255),
                        (random.uniform(-0.4, 0.4), random.uniform(-0.2, 0.2)),
                        5, 55
                    )
            elif current_area.area_type == "castle":
                # Magic sparkles
                for _ in range(3):
                    x = area_world_x + random.randint(0, AREA_WIDTH)
                    y = area_world_y + random.randint(0, AREA_HEIGHT)
                    game.particle_system.add_particle(
                        x, y, (255, 215, 0),
                        (random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)),
                        4, 50
                    )
            elif current_area.area_type == "cave":
                # Dust particles
                for _ in range(2):
                    x = area_world_x + random.randint(0, AREA_WIDTH)
                    y = area_world_y + random.randint(0, AREA_HEIGHT)
                    game.particle_system.add_particle(
                        x, y, (100, 100, 120),
                        (random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)),
                        3, 70
                    )
            elif current_area.area_type == "town":
                # Town-specific particles (smoke, fountain, leaves)
                current_area.generate_town_particles(game.particle_system)


def reset_game_state(game):
    """
    Reset the game state for a new game.
    
    Args:
        game: The main Game instance
    """
    game.enemies = []
    game.items = []
    game.score = 0
    game.game_time = 0
    game.spawn_timer = 0
    game.item_timer = 0
    game.player_moved = False
    game.movement_cooldown = 0
    game.boss_battle_triggered = False
    game.boss_defeated = False
    
    # Reset world map
    game.world_map = game.world_map.__class__()
    
    # Position player in center area (1,1) at center position
    if game.player:
        game.player.x = AREA_WIDTH + (AREA_WIDTH // 2)
        game.player.y = AREA_HEIGHT + (AREA_HEIGHT // 2)
    
    # Spawn initial enemies and items using the improved spawn methods
    # The spawn_enemy() method in core/game.py will handle spawning across all areas
    for _ in range(3):
        game.spawn_enemy()
    for _ in range(2):
        game.spawn_item() 