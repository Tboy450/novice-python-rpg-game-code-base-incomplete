"""
DRAGON'S LAIR RPG - Game UI Module
================================

This module contains UI drawing functions and helpers extracted from the Game class.
It handles all visual elements, overlays, and UI components for different game states.

The module provides:
- UI drawing functions for all game states
- Overlay and transition effects
- Android virtual control rendering
- UI element positioning and styling
"""

import pygame
import math
from ui.button import Button
from config.constants import *
from utils.android_utils import is_android


# Main menu and character select buttons
start_button = Button(SCREEN_WIDTH//2 - 120, 500, 240, 60, "START QUEST", UI_BORDER)
quit_button = Button(SCREEN_WIDTH//2 - 120, 580, 240, 60, "QUIT", UI_BORDER)
back_button = Button(20, 20, 100, 40, "BACK")
warrior_button = Button(SCREEN_WIDTH//2 - 300, 300, 200, 150, "WARRIOR", (0, 255, 0))
mage_button = Button(SCREEN_WIDTH//2 - 50, 300, 200, 150, "MAGE", (0, 200, 255))
rogue_button = Button(SCREEN_WIDTH//2 + 200, 300, 200, 150, "ROGUE", (255, 100, 0))


def draw_start_menu(game, screen):
    """
    Draw the start menu with title, dragon, and buttons.
    
    Args:
        game: The main Game instance
        screen: The pygame display surface
    """
    # Update button text if needed
    if game.start_button.text != "START QUEST":
        game.start_button.text = "START QUEST"
        game.start_button.text_surf = font_medium.render(game.start_button.text, True, TEXT_COLOR)
        game.start_button.text_rect = game.start_button.text_surf.get_rect(center=game.start_button.rect.center)
    
    # Draw title
    title = font_large.render("DRAGON'S LAIR", True, (255, 50, 50))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
    
    # Draw subtitle
    subtitle = font_medium.render("A RETRO RPG ADVENTURE", True, TEXT_COLOR)
    screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 140))
    
    # Draw animated dragon
    game.dragon.draw(screen)
    
    # Draw buttons
    game.start_button.draw(screen)
    game.quit_button.draw(screen)
    
    # Draw instructions
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
        text = font_tiny.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 350 + i*25))


def draw_character_select(game, screen):
    """
    Draw the character selection screen with class descriptions.
    
    Args:
        game: The main Game instance
        screen: The pygame display surface
    """
    # Draw title
    title = font_large.render("CHOOSE YOUR HERO", True, TEXT_COLOR)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
    
    # Character descriptions
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
    
    # Draw descriptions
    y_pos = 480
    for line in warrior_desc:
        text = font_tiny.render(line, True, (0, 255, 0))
        screen.blit(text, (SCREEN_WIDTH//2 - 300, y_pos))
        y_pos += 25
    
    y_pos = 480
    for line in mage_desc:
        text = font_tiny.render(line, True, (0, 200, 255))
        screen.blit(text, (SCREEN_WIDTH//2 - 50, y_pos))
        y_pos += 25
    
    y_pos = 480
    for line in rogue_desc:
        text = font_tiny.render(line, True, (255, 100, 0))
        screen.blit(text, (SCREEN_WIDTH//2 + 200, y_pos))
        y_pos += 25
    
    # Draw buttons
    game.warrior_button.draw(screen)
    game.mage_button.draw(screen)
    game.rogue_button.draw(screen)
    game.back_button.draw(screen)


def draw_overworld_ui(game, screen):
    """
    Draw the overworld UI including player stats, score, and controls.
    
    Args:
        game: The main Game instance
        screen: The pygame display surface
    """
    # Debug output
    if not game.player:
        print("❌ ERROR: game.player is None!")
        return
    
    # Draw UI panel
    pygame.draw.rect(screen, UI_BG, (10, 10, 280, 150), border_radius=8)
    pygame.draw.rect(screen, UI_BORDER, (10, 10, 280, 150), 3, border_radius=8)
    
    # Draw player stats
    game.player.draw_stats(screen, 20, 20)
    
    # Draw score and other info
    score_text = font_medium.render(f"SCORE: {game.score}", True, TEXT_COLOR)
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 20, 20))
    
    time_text = font_small.render(f"TIME: {game.game_time//FPS}s", True, TEXT_COLOR)
    screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 20, 60))
    
    kills_text = font_small.render(f"KILLS: {game.player.kills}", True, TEXT_COLOR)
    screen.blit(kills_text, (SCREEN_WIDTH - kills_text.get_width() - 20, 90))
    
    # Draw area information
    current_area = game.world_map.get_current_area()
    if current_area:
        area_text = font_small.render(f"AREA: {current_area.area_type.upper()}", True, TEXT_COLOR)
        screen.blit(area_text, (SCREEN_WIDTH - area_text.get_width() - 20, 120))
        
        # Area descriptions
        area_descriptions = {
            "plains": "Peaceful grasslands",
            "forest": "Dense woodland",
            "mountain": "Rocky peaks",
            "desert": "Harsh wasteland",
            "swamp": "Misty wetlands",
            "beach": "Sandy shores",
            "volcano": "Fiery depths",
            "ice": "Frozen wastes",
            "castle": "Ancient fortress",
            "cave": "Dark caverns"
        }
        
        desc = area_descriptions.get(current_area.area_type, "")
        if desc:
            desc_text = font_tiny.render(desc, True, (180, 180, 200))
            screen.blit(desc_text, (SCREEN_WIDTH - desc_text.get_width() - 20, 145))
        
        # Draw mini-map
        draw_mini_map(game, screen, current_area)
    
    # Draw position info
    local_x = game.player.x % AREA_WIDTH
    local_y = game.player.y % AREA_HEIGHT
    grid_pos_x = local_x // GRID_SIZE
    grid_pos_y = local_y // GRID_SIZE
    pos_text = font_tiny.render(f"POS: ({grid_pos_x}, {grid_pos_y})", True, (255, 255, 0))
    screen.blit(pos_text, (20, SCREEN_HEIGHT - 180))
    
    # Draw controls info
    controls = [
        "CONTROLS:",
        "ARROWS/WASD - MOVE",
        "ENTER - SELECT",
        "M - WORLD MAP",
        "ESC - MENU"
    ]
    
    for i, line in enumerate(controls):
        text = font_tiny.render(line, True, (180, 180, 200))
        screen.blit(text, (20, SCREEN_HEIGHT - 140 + i * 25))


def draw_mini_map(game, screen, current_area):
    """
    Draw the mini-map showing visited areas.
    
    Args:
        game: The main Game instance
        screen: The pygame display surface
        current_area: The current world area
    """
    mini_map_size = 80
    mini_map_x = SCREEN_WIDTH - mini_map_size - 20
    mini_map_y = 160
    
    # Draw mini-map background
    pygame.draw.rect(screen, UI_BG, (mini_map_x, mini_map_y, mini_map_size, mini_map_size), border_radius=4)
    pygame.draw.rect(screen, UI_BORDER, (mini_map_x, mini_map_y, mini_map_size, mini_map_size), 2, border_radius=4)
    
    # Draw visited areas
    cell_size = mini_map_size // 3
    for y in range(3):
        for x in range(3):
            area = game.world_map.areas.get((x, y))
            if area and area.visited:
                color = (100, 200, 100) if area == current_area else (50, 100, 50)
                pygame.draw.rect(screen, color, 
                               (mini_map_x + x * cell_size, mini_map_y + y * cell_size, 
                                cell_size, cell_size))
                pygame.draw.rect(screen, UI_BORDER, 
                               (mini_map_x + x * cell_size, mini_map_y + y * cell_size, 
                                cell_size, cell_size), 1)


def draw_world_map_overlay(game, screen):
    """
    Draw the world map overlay when M is pressed.
    
    Args:
        game: The main Game instance
        screen: The pygame display surface
    """
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Draw world map grid
    map_size = 300
    map_x = (SCREEN_WIDTH - map_size) // 2
    map_y = (SCREEN_HEIGHT - map_size) // 2
    cell_size = map_size // 3
    
    # Draw background
    pygame.draw.rect(screen, UI_BG, (map_x, map_y, map_size, map_size), border_radius=8)
    pygame.draw.rect(screen, UI_BORDER, (map_x, map_y, map_size, map_size), 3, border_radius=8)
    
    # Draw areas
    for y in range(3):
        for x in range(3):
            area = game.world_map.areas.get((x, y))
            if area:
                cell_x = map_x + x * cell_size
                cell_y = map_y + y * cell_size
                
                # Color based on area type and visited status
                if area == game.world_map.get_current_area():
                    color = (100, 255, 100)  # Current area - bright green
                elif area.visited:
                    color = (50, 150, 50)    # Visited area - dark green
                else:
                    color = (50, 50, 50)     # Unvisited area - dark gray
                
                pygame.draw.rect(screen, color, (cell_x + 2, cell_y + 2, cell_size - 4, cell_size - 4))
                pygame.draw.rect(screen, UI_BORDER, (cell_x, cell_y, cell_size, cell_size), 1)
                
                # Draw area name
                name_text = font_tiny.render(area.area_type[:3].upper(), True, TEXT_COLOR)
                text_x = cell_x + (cell_size - name_text.get_width()) // 2
                text_y = cell_y + (cell_size - name_text.get_height()) // 2
                screen.blit(name_text, (text_x, text_y))
    
    # Draw player position
    player_world_x, player_world_y = game.player.x, game.player.y
    player_area_x = player_world_x // AREA_WIDTH
    player_area_y = player_world_y // AREA_HEIGHT
    player_cell_x = map_x + player_area_x * cell_size + cell_size // 2
    player_cell_y = map_y + player_area_y * cell_size + cell_size // 2
    pygame.draw.circle(screen, (255, 255, 0), (player_cell_x, player_cell_y), 4)
    
    # Draw title
    title = font_medium.render("WORLD MAP", True, TEXT_COLOR)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, map_y - 40))
    
    # Draw instructions
    instructions = font_tiny.render("Press M to close", True, (180, 180, 200))
    screen.blit(instructions, (SCREEN_WIDTH//2 - instructions.get_width()//2, map_y + map_size + 10))


def draw_game_over_screen(game, screen):
    """
    Draw the game over screen with stats and options.
    
    Args:
        game: The main Game instance
        screen: The pygame display surface
    """
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    title = font_large.render("GAME OVER", True, (255, 50, 50))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
    
    stats = [
        f"HERO: {game.player.type}",
        f"LEVEL: {game.player.level}",
        f"SCORE: {game.score}",
        f"KILLS: {game.player.kills}",
        f"ITEMS: {game.player.items_collected}",
        f"TIME: {game.game_time//FPS} SECONDS"
    ]
    
    y_pos = 220
    for stat in stats:
        text = font_medium.render(stat, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y_pos))
        y_pos += 40
        
    # Play again button
    game.start_button.text = "PLAY AGAIN"
    game.start_button.rect = pygame.Rect(SCREEN_WIDTH//2 - 120, y_pos + 20, 240, 60)
    game.start_button.text_surf = font_medium.render(game.start_button.text, True, TEXT_COLOR)
    game.start_button.text_rect = game.start_button.text_surf.get_rect(center=game.start_button.rect.center)
    game.start_button.draw(screen)
    
    # Back to menu button
    game.back_button.text = "BACK TO MENU"
    game.back_button.rect = pygame.Rect(SCREEN_WIDTH//2 - 120, y_pos + 100, 240, 60)
    game.back_button.text_surf = font_medium.render(game.back_button.text, True, TEXT_COLOR)
    game.back_button.text_rect = game.back_button.text_surf.get_rect(center=game.back_button.rect.center)
    game.back_button.draw(screen)


def draw_victory_screen(game, screen):
    """
    Draw the victory screen with stats and congratulations.
    
    Args:
        game: The main Game instance
        screen: The pygame display surface
    """
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 220))
    screen.blit(overlay, (0, 0))
    
    title = font_large.render("YOU WIN!", True, (255, 255, 0))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
    
    stats = [
        f"HERO: {game.player.type}",
        f"LEVEL: {game.player.level}",
        f"SCORE: {game.score}",
        f"KILLS: {game.player.kills}",
        f"ITEMS: {game.player.items_collected}",
        f"TIME: {game.game_time//FPS} SECONDS"
    ]
    
    y_pos = 240
    for stat in stats:
        text = font_medium.render(stat, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y_pos))
        y_pos += 40
    
    win_text = font_medium.render("Congratulations! You defeated Malakor!", True, (255, 215, 0))
    screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, y_pos + 40))
    
    # Play again button
    game.start_button.text = "PLAY AGAIN"
    game.start_button.rect = pygame.Rect(SCREEN_WIDTH//2 - 120, y_pos + 80, 240, 60)
    game.start_button.text_surf = font_medium.render(game.start_button.text, True, TEXT_COLOR)
    game.start_button.text_rect = game.start_button.text_surf.get_rect(center=game.start_button.rect.center)
    game.start_button.draw(screen)
    
    # Back to menu button
    game.back_button.text = "BACK TO MENU"
    game.back_button.rect = pygame.Rect(SCREEN_WIDTH//2 - 120, y_pos + 160, 240, 60)
    game.back_button.text_surf = font_medium.render(game.back_button.text, True, TEXT_COLOR)
    game.back_button.text_rect = game.back_button.text_surf.get_rect(center=game.back_button.rect.center)
    game.back_button.draw(screen)


def draw_transition_overlay(game, screen):
    """
    Draw transition overlay for screen transitions.
    
    Args:
        game: The main Game instance
        screen: The pygame display surface
    """
    if game.transition_state != "none":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, game.transition_alpha))
        screen.blit(overlay, (0, 0))


def draw_android_controls(game, screen):
    """
    Draw Android virtual controls if on Android platform.
    
    Args:
        game: The main Game instance
        screen: The pygame display surface
    """
    if is_android() and game.android_buttons:
        # D-pad
        pygame.draw.rect(screen, (200,200,200), game.android_buttons['up'], border_radius=20)
        pygame.draw.polygon(screen, (100,100,100), [
            (game.android_buttons['up'].centerx, game.android_buttons['up'].top+15),
            (game.android_buttons['up'].left+15, game.android_buttons['up'].bottom-15),
            (game.android_buttons['up'].right-15, game.android_buttons['up'].bottom-15)
        ])
        pygame.draw.rect(screen, (200,200,200), game.android_buttons['down'], border_radius=20)
        pygame.draw.polygon(screen, (100,100,100), [
            (game.android_buttons['down'].centerx, game.android_buttons['down'].bottom-15),
            (game.android_buttons['down'].left+15, game.android_buttons['down'].top+15),
            (game.android_buttons['down'].right-15, game.android_buttons['down'].top+15)
        ])
        pygame.draw.rect(screen, (200,200,200), game.android_buttons['left'], border_radius=20)
        pygame.draw.polygon(screen, (100,100,100), [
            (game.android_buttons['left'].left+15, game.android_buttons['left'].centery),
            (game.android_buttons['left'].right-15, game.android_buttons['left'].top+15),
            (game.android_buttons['left'].right-15, game.android_buttons['left'].bottom-15)
        ])
        pygame.draw.rect(screen, (200,200,200), game.android_buttons['right'], border_radius=20)
        pygame.draw.polygon(screen, (100,100,100), [
            (game.android_buttons['right'].right-15, game.android_buttons['right'].centery),
            (game.android_buttons['right'].left+15, game.android_buttons['right'].top+15),
            (game.android_buttons['right'].left+15, game.android_buttons['right'].bottom-15)
        ])
        
        # Enter
        pygame.draw.rect(screen, (255,215,0), game.android_buttons['enter'], border_radius=20)
        enter_text = font_small.render('ENT', True, (0,0,0))
        screen.blit(enter_text, enter_text.get_rect(center=game.android_buttons['enter'].center))
        
        # Space
        pygame.draw.rect(screen, (0,255,255), game.android_buttons['space'], border_radius=20)
        space_text = font_small.render('SPC', True, (0,0,0))
        screen.blit(space_text, space_text.get_rect(center=game.android_buttons['space'].center)) 