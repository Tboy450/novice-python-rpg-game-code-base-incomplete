"""
DRAGON'S LAIR RPG - World Map Module
====================================

This module contains the WorldMap class that manages the entire 3x3 world grid,
camera positioning, and area transitions.
"""

import pygame
from config.constants import *
from world.world_area import WorldArea

class WorldMap:
    """
    Manages the entire 3x3 world grid, camera positioning, and area transitions.
    Handles coordinate conversion between world and screen space.
    """
    def __init__(self):
        self.areas = {}
        self.current_area_x = 1  # Start in center area
        self.current_area_y = 1
        self.camera_x = 0
        self.camera_y = 0
        self.area_transition_alpha = 0
        self.transitioning = False
        
        # Initialize all areas
        area_types = [
            ["mountain", "forest", "desert"],
            ["swamp", "beach", "volcano"],
            ["ice", "town", "cave"]
        ]
        
        for y in range(WORLD_SIZE):
            for x in range(WORLD_SIZE):
                area_type = area_types[y][x]
                self.areas[(x, y)] = WorldArea(x, y, area_type)
        
        # Mark starting area as visited
        self.areas[(1, 1)].visited = True
    
    def get_current_area(self):
        """Get the current area the player is in"""
        return self.areas.get((self.current_area_x, self.current_area_y))
    
    def get_area_at_world_pos(self, world_x, world_y):
        """Get area at world position"""
        area_x = world_x // AREA_WIDTH
        area_y = world_y // AREA_HEIGHT
        return self.areas.get((area_x, area_y))
    
    def update_camera(self, player_world_x, player_world_y):
        """Update camera to follow player - now screen-based"""
        # Calculate which area the player is in
        area_x = player_world_x // AREA_WIDTH
        area_y = player_world_y // AREA_HEIGHT
        
        # Clamp area coordinates to valid range (0-2)
        area_x = max(0, min(2, area_x))
        area_y = max(0, min(2, area_y))
        
        # Set camera to show the current area
        self.camera_x = area_x * AREA_WIDTH
        self.camera_y = area_y * AREA_HEIGHT
    
    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates"""
        return (world_x - self.camera_x, world_y - self.camera_y)
    
    def screen_to_world(self, screen_x, screen_y):
        """Convert screen coordinates to world coordinates"""
        return (screen_x + self.camera_x, screen_y + self.camera_y)
    
    def check_area_transition(self, player_world_x, player_world_y):
        """Check if player should transition to a new area"""
        # Clamp player position to world bounds
        player_world_x = max(0, min(WORLD_WIDTH - 1, player_world_x))
        player_world_y = max(0, min(WORLD_HEIGHT - 1, player_world_y))
        
        current_area = self.get_area_at_world_pos(player_world_x, player_world_y)
        if current_area:
            new_area_x, new_area_y = current_area.area_x, current_area.area_y
            if new_area_x != self.current_area_x or new_area_y != self.current_area_y:
                self.current_area_x = new_area_x
                self.current_area_y = new_area_y
                current_area.visited = True
                self.transitioning = True
                self.area_transition_alpha = 255
                return True
        return False
    
    def update_transition(self):
        """Update area transition effect"""
        if self.transitioning:
            self.area_transition_alpha = max(0, self.area_transition_alpha - 15)
            if self.area_transition_alpha <= 0:
                self.transitioning = False
    
    def draw_world_map(self, surface):
        """Draw the world map view"""
        surface.fill(BACKGROUND)
        
        # Draw title
        title_text = font_large.render("WORLD MAP", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 50))
        surface.blit(title_text, title_rect)
        
        # Calculate area size for map display
        map_area_size = 150
        map_start_x = (SCREEN_WIDTH - WORLD_SIZE * map_area_size) // 2
        map_start_y = 150
        
        # Draw each area
        for y in range(WORLD_SIZE):
            for x in range(WORLD_SIZE):
                area = self.areas.get((x, y))
                if area:
                    # Calculate position
                    area_x = map_start_x + x * map_area_size
                    area_y = map_start_y + y * map_area_size
                    
                    # Draw area background
                    pygame.draw.rect(surface, area.background_color, 
                                   (area_x, area_y, map_area_size, map_area_size))
                    
                    # Draw border
                    border_color = UI_BORDER if (x, y) == (self.current_area_x, self.current_area_y) else GRID_COLOR
                    pygame.draw.rect(surface, border_color, 
                                   (area_x, area_y, map_area_size, map_area_size), 3)
                    
                    # Draw area name
                    area_name = area.area_type.upper()
                    name_text = font_small.render(area_name, True, TEXT_COLOR)
                    name_rect = name_text.get_rect(center=(area_x + map_area_size//2, area_y + map_area_size//2))
                    surface.blit(name_text, name_rect)
                    
                    # Draw visited indicator
                    if area.visited:
                        visited_text = font_tiny.render("VISITED", True, (0, 255, 0))
                        visited_rect = visited_text.get_rect(center=(area_x + map_area_size//2, area_y + map_area_size - 20))
                        surface.blit(visited_text, visited_rect)
        
        # Draw player position indicator
        player_area_x = map_start_x + self.current_area_x * map_area_size + map_area_size//2
        player_area_y = map_start_y + self.current_area_y * map_area_size + map_area_size//2
        pygame.draw.circle(surface, PLAYER_COLOR, (player_area_x, player_area_y), 10)
        
        # Draw instructions
        instructions_text = font_small.render("Press M to return to game", True, (150, 150, 150))
        instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        surface.blit(instructions_text, instructions_rect) 