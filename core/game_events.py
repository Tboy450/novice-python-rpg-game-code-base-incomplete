"""
DRAGON'S LAIR RPG - Game Events Module
=====================================

This module contains all event handling logic extracted from the Game class.
It manages user input, mouse interactions, and Android virtual controls.

The module handles:
- Keyboard input for all game states
- Mouse interactions and button clicks
- Android virtual control mapping
- Event processing and state transitions
"""

import pygame
from core.game_state import *
from utils.android_utils import is_android


def handle_events(game, screen):
    """
    Main event handling function that processes all pygame events.
    
    Args:
        game: The main Game instance
        screen: The pygame display surface
        
    Returns:
        tuple: (running, mouse_pos, mouse_click) where running is a boolean
    """
    running = True
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True
            # Android virtual controls
            if hasattr(game, 'android_buttons') and game.android_buttons:
                mx, my = event.pos
                for name, rect in game.android_buttons.items():
                    if rect.collidepoint(mx, my):
                        if name == 'up':
                            fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
                            pygame.event.post(fake_event)
                        elif name == 'down':
                            fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
                            pygame.event.post(fake_event)
                        elif name == 'left':
                            fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
                            pygame.event.post(fake_event)
                        elif name == 'right':
                            fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
                            pygame.event.post(fake_event)
                        elif name == 'enter':
                            fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
                            pygame.event.post(fake_event)
                        elif name == 'space':
                            fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                            pygame.event.post(fake_event)
        
        if event.type == pygame.KEYDOWN:
            handle_keydown_event(game, event)
            
        # Pass input to battle screen if in battle state
        if game.state == "battle" and game.battle_screen:
            game.battle_screen.handle_input(event, game)
    
    return running, mouse_pos, mouse_click


def handle_keydown_event(game, event):
    """
    Handle keyboard input events for different game states.
    
    Args:
        game: The main Game instance
        event: The pygame KEYDOWN event
    """
    if event.key == pygame.K_ESCAPE:
        handle_escape_key(game)
    
    # Handle skip for cutscene
    if game.state == "opening_cutscene":
        game.opening_cutscene.skip()
    
    # Handle world map toggle
    if game.state == "overworld" and event.key == pygame.K_m:
        game.show_world_map = not game.show_world_map
    
    # Handle movement in overworld
    if game.state == "overworld" and game.player and game.movement_cooldown <= 0:
        handle_movement_input(game, event)
    
    # Handle town cutscene dialogue advancement
    if game.state == "overworld" and event.key == pygame.K_SPACE:
        handle_town_cutscene_input(game)


def handle_escape_key(game):
    """
    Handle ESC key presses for different game states.
    
    Args:
        game: The main Game instance
    """
    if game.state == "overworld":
        game.state = "game_over"
    elif game.state == "game_over":
        game.state = "start_menu"
    elif game.state == "character_select":
        game.state = "start_menu"
    elif game.state == "opening_cutscene":
        game.opening_cutscene.skip()


def handle_movement_input(game, event):
    """
    Handle movement input in the overworld state.
    
    Args:
        game: The main Game instance
        event: The pygame KEYDOWN event
    """
    # Store original position for collision detection
    original_x = game.player.x
    original_y = game.player.y
    
    if event.key in [pygame.K_UP, pygame.K_w]:
        if game.SFX_ARROW: 
            game.SFX_ARROW.play()
        game.player.move(0, -1)
        check_movement_collision(game, original_x, original_y)
    elif event.key in [pygame.K_DOWN, pygame.K_s]:
        if game.SFX_ARROW: 
            game.SFX_ARROW.play()
        game.player.move(0, 1)
        check_movement_collision(game, original_x, original_y)
    elif event.key in [pygame.K_LEFT, pygame.K_a]:
        if game.SFX_ARROW: 
            game.SFX_ARROW.play()
        game.player.move(-1, 0)
        check_movement_collision(game, original_x, original_y)
    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
        if game.SFX_ARROW: 
            game.SFX_ARROW.play()
        game.player.move(1, 0)
        check_movement_collision(game, original_x, original_y)


def check_movement_collision(game, original_x, original_y):
    """
    Check for building collisions and revert movement if needed.
    
    Args:
        game: The main Game instance
        original_x: Original player X position
        original_y: Original player Y position
    """
    current_area = game.world_map.get_current_area()
    if current_area and current_area.check_building_collision(game.player.x, game.player.y):
        game.player.x = original_x
        game.player.y = original_y
    else:
        game.player_moved = True
        game.movement_cooldown = game.movement_delay


def handle_town_cutscene_input(game):
    """
    Handle input during town cutscene dialogue.
    
    Args:
        game: The main Game instance
    """
    current_area = game.world_map.get_current_area()
    if current_area and current_area.cutscene_active and current_area.guard:
        # Advance dialogue
        current_area.guard["current_dialogue"] += 1
        current_area.cutscene_timer = 0
        
        # Check if we've reached the end of dialogue
        if current_area.guard["current_dialogue"] >= len(current_area.guard["dialogue"]):
            current_area.cutscene_phase = 2  # End cutscene


def handle_button_clicks(game, mouse_pos, mouse_click):
    """
    Handle button clicks for different game states.
    
    Args:
        game: The main Game instance
        mouse_pos: Current mouse position
        mouse_click: Boolean indicating if mouse was clicked
    """
    if game.state == "start_menu":
        handle_start_menu_clicks(game, mouse_pos, mouse_click)
    elif game.state == "character_select":
        handle_character_select_clicks(game, mouse_pos, mouse_click)
    elif game.state == "overworld":
        pass  # No button clicks in overworld
    elif game.state == "battle":
        handle_battle_state(game)
    elif game.state == "game_over":
        handle_game_over_clicks(game, mouse_pos, mouse_click)
    elif game.state == "victory":
        handle_victory_clicks(game, mouse_pos, mouse_click)


def handle_start_menu_clicks(game, mouse_pos, mouse_click):
    """
    Handle button clicks in the start menu state.
    
    Args:
        game: The main Game instance
        mouse_pos: Current mouse position
        mouse_click: Boolean indicating if mouse was clicked
    """
    # Update button hover states
    game.start_screen.update_buttons(mouse_pos)
    
    # Handle clicks using StartScreen module
    result = game.start_screen.handle_start_menu_clicks(mouse_pos, mouse_click)
    if result:
        if game.SFX_CLICK: 
            game.SFX_CLICK.play()
        if result == "quit":
            return False  # Signal to quit
        else:
            game.state = result
            if result == "opening_cutscene":
                game.opening_cutscene = game.opening_cutscene.__class__()  # Reset cutscene
    return True


def handle_character_select_clicks(game, mouse_pos, mouse_click):
    """
    Handle button clicks in the character select state.
    
    Args:
        game: The main Game instance
        mouse_pos: Current mouse position
        mouse_click: Boolean indicating if mouse was clicked
    """
    # Update button hover states
    game.start_screen.update_buttons(mouse_pos)
    
    # Handle clicks using StartScreen module
    result = game.start_screen.handle_character_select_clicks(mouse_pos, mouse_click)
    if result:
        if game.SFX_CLICK: 
            game.SFX_CLICK.play()
        if isinstance(result, tuple):
            game.state, character_type = result
            if character_type:
                # Import Character class and create new instance
                from entities.player_characters.character import Character
                game.player = Character(character_type)
                game.start_game()
        else:
            game.state = result


def handle_game_over_clicks(game, mouse_pos, mouse_click):
    """
    Handle button clicks in the game over state.
    
    Args:
        game: The main Game instance
        mouse_pos: Current mouse position
        mouse_click: Boolean indicating if mouse was clicked
    """
    game.start_button.update(mouse_pos)
    game.back_button.update(mouse_pos)
    
    if game.start_button.is_clicked(mouse_pos, mouse_click):
        if game.SFX_CLICK: 
            game.SFX_CLICK.play()
        game.state = "character_select"
        
    if game.back_button.is_clicked(mouse_pos, mouse_click):
        if game.SFX_CLICK: 
            game.SFX_CLICK.play()
        game.state = "start_menu"


def handle_victory_clicks(game, mouse_pos, mouse_click):
    """
    Handle button clicks in the victory state.
    
    Args:
        game: The main Game instance
        mouse_pos: Current mouse position
        mouse_click: Boolean indicating if mouse was clicked
    """
    game.start_button.update(mouse_pos)
    game.back_button.update(mouse_pos)
    
    if game.start_button.is_clicked(mouse_pos, mouse_click):
        if game.SFX_CLICK: 
            game.SFX_CLICK.play()
        game.state = "character_select"
        
    if game.back_button.is_clicked(mouse_pos, mouse_click):
        if game.SFX_CLICK: 
            game.SFX_CLICK.play()
        game.state = "start_menu" 


def handle_battle_state(game):
    """
    Handle battle state updates and transitions.
    
    Args:
        game: The main Game instance
    """
    if game.battle_screen:
        battle_ended = game.battle_screen.update()
        
        if battle_ended:
            # Boss battle win/lose/escape
            if game.boss_system.is_boss_battle(game.battle_screen):
                if game.battle_screen.result == "win":
                    game.boss_system.handle_boss_battle_win(game.player, game.battle_screen.enemy, game)
                    game.battle_screen = None
                    game.music.update(game.state, False)  # Explicitly reset music state
                    return
                elif game.battle_screen.result == "lose":
                    game.boss_system.handle_boss_battle_lose(game)
                    game.battle_screen = None
                    game.music.update(game.state, False)  # Explicitly reset music state
                    return
                elif game.battle_screen.result == "escape":
                    game.boss_system.handle_boss_battle_escape(game.player, game)
                    game.battle_screen = None
                    game.music.update(game.state, False)  # Explicitly reset music state
                    return
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
                    return 