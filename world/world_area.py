"""
WORLD AREA MODULE - Individual Areas in the 3x3 World Grid
========================================================

This module contains the WorldArea class that represents individual areas
in the game world. Each area has its own terrain type, enemies, items,
and visual style.

Area Types: forest, desert, mountain, swamp, volcano, town, ice, castle, cave, beach
"""

import pygame
import random
import math
from config.constants import *

class WorldArea:
    """
    Represents a single area in the 3x3 world grid.
    Each area has its own terrain type, enemies, items, and visual style.
    
    Area Types: forest, desert, mountain, swamp, volcano, town, ice, castle, cave, beach
    """
    def __init__(self, area_x, area_y, area_type="forest"):
        self.area_x = area_x  # Grid position (0-2)
        self.area_y = area_y  # Grid position (0-2)
        self.area_type = area_type
        self.enemies = []
        self.items = []
        self.visited = False
        
        # ========================================
        # AREA-SPECIFIC VISUAL PROPERTIES
        # ========================================
        # Each area type has unique colors and visual characteristics
        if area_type == "forest":
            self.background_color = (20, 40, 20)  # Dark green forest
            self.grid_color = (40, 60, 40)
        elif area_type == "desert":
            self.background_color = (80, 70, 40)  # Sandy yellow desert
            self.grid_color = (100, 90, 60)
        elif area_type == "mountain":
            self.background_color = (50, 50, 60)  # Gray-blue mountains
            self.grid_color = (70, 70, 80)
        elif area_type == "swamp":
            self.background_color = (25, 35, 25)  # Dark swamp green
            self.grid_color = (45, 55, 45)
        elif area_type == "volcano":
            self.background_color = (60, 25, 25)  # Dark red volcanic
            self.grid_color = (80, 45, 45)
        elif area_type == "ice":
            self.background_color = (35, 45, 65)  # Ice blue
            self.grid_color = (55, 65, 85)
        elif area_type == "castle":
            self.background_color = (45, 35, 45)  # Purple-gray
            self.grid_color = (65, 55, 65)
        elif area_type == "cave":
            self.background_color = (15, 15, 25)  # Very dark blue
            self.grid_color = (35, 35, 45)
        elif area_type == "beach":
            self.background_color = (75, 65, 45)  # Sandy brown
            self.grid_color = (95, 85, 65)
        elif area_type == "town":
            self.background_color = (80, 120, 60)  # Grass green for town
            self.grid_color = (100, 140, 80)
            # Town-specific buildings and structures
            self.buildings = []
            self.town_boundaries = []
            self.decorations = []
            self._generate_town_layout()
        
        # Area-specific particle effects
        self.particle_timer = 0
        self.particle_interval = 30  # Frames between particle spawns (faster)
        
        # Initialize cutscene attributes for all areas
        self.entrance_cutscene_triggered = False
        self.guard = None
        self.cutscene_active = False
        self.cutscene_timer = 0
        self.cutscene_phase = 0
        
        # Town-specific particle effects
        if area_type == "town":
            self.particle_interval = 15  # More frequent particles for town
            self.smoke_sources = [
                {"x": 150, "y": 430},  # Shop chimney
                {"x": 850, "y": 430},  # Inn chimney
                {"x": 180, "y": 570},  # Blacksmith chimney
                {"x": 820, "y": 570},  # Library chimney
            ]
            # Create town guard for cutscene
            self._create_town_guard()
    
    def get_world_position(self):
        """Convert area grid position to world pixel position"""
        return (self.area_x * AREA_WIDTH, self.area_y * AREA_HEIGHT)
    
    def is_point_in_area(self, world_x, world_y):
        """Check if a world position is within this area"""
        area_world_x, area_world_y = self.get_world_position()
        return (area_world_x <= world_x < area_world_x + AREA_WIDTH and 
                area_world_y <= world_y < area_world_y + AREA_HEIGHT)
    
    def get_local_position(self, world_x, world_y):
        """Convert world position to local area position"""
        area_world_x, area_world_y = self.get_world_position()
        return (world_x - area_world_x, world_y - area_world_y)
    
    def _generate_town_layout(self):
        """Generate detailed town layout with buildings, boundaries, and decorations"""
        if self.area_type != "town":
            return
            
        # Create town boundaries (walls/gates at the top)
        self.town_boundaries = [
            # Main gate at the top center (moved down 2 squares)
            {"type": "gate", "x": 450, "y": 200, "width": 100, "height": 60},
            # Left wall section
            {"type": "wall", "x": 0, "y": 200, "width": 450, "height": 20},
            # Right wall section  
            {"type": "wall", "x": 550, "y": 200, "width": 450, "height": 20},
            # Decorative towers
            {"type": "tower", "x": 400, "y": 180, "width": 40, "height": 80},
            {"type": "tower", "x": 560, "y": 180, "width": 40, "height": 80},
        ]
        
        # Create main buildings with better spacing and reduced clustering
        self.buildings = [
            # Town Hall (center, grand and surreal) - physical building
            {"type": "town_hall", "x": 400, "y": 380, "width": 200, "height": 140, "color": (200, 180, 160), "style": "grand", "collision": True},
            # Shop (left side, colorful and inviting) - physical building
            {"type": "shop", "x": 60, "y": 430, "width": 140, "height": 90, "color": (180, 160, 200), "style": "magical", "collision": True},
            # Inn (right side, cozy and warm) - physical building
            {"type": "inn", "x": 800, "y": 430, "width": 140, "height": 90, "color": (200, 160, 140), "style": "cozy", "collision": True},
            # Blacksmith (bottom left, industrial) - physical building
            {"type": "blacksmith", "x": 100, "y": 570, "width": 120, "height": 80, "color": (140, 120, 100), "style": "industrial", "collision": True},
            # Library (bottom right, mystical) - physical building
            {"type": "library", "x": 780, "y": 570, "width": 120, "height": 80, "color": (160, 180, 200), "style": "mystical", "collision": True},
            # House (single residential building, asymmetrical placement in grass)
            {"type": "house", "x": 750, "y": 340, "width": 70, "height": 60, "color": (150, 130, 110), "style": "cottage", "collision": True},
            # Market stall (reduced from 2 to 1) - physical object
            {"type": "stall", "x": 450, "y": 530, "width": 100, "height": 50, "color": (170, 150, 130), "style": "market", "collision": True},
        ]
        
        # Create decorative elements (no collision)
        self.decorations = [
            # Street lamps (decorative only)
            {"type": "lamp", "x": 150, "y": 300, "width": 20, "height": 60},
            {"type": "lamp", "x": 850, "y": 300, "width": 20, "height": 60},
            {"type": "lamp", "x": 150, "y": 650, "width": 20, "height": 60},
            {"type": "lamp", "x": 850, "y": 650, "width": 20, "height": 60},
            # Trees and plants (decorative only)
            {"type": "tree", "x": 50, "y": 250, "width": 30, "height": 50},
            {"type": "tree", "x": 920, "y": 250, "width": 30, "height": 50},
            {"type": "tree", "x": 50, "y": 700, "width": 30, "height": 50},
            {"type": "tree", "x": 920, "y": 700, "width": 30, "height": 50},
            # Flower beds (decorative only)
            {"type": "flowers", "x": 200, "y": 270, "width": 40, "height": 20},
            {"type": "flowers", "x": 760, "y": 270, "width": 40, "height": 20},
            {"type": "flowers", "x": 200, "y": 730, "width": 40, "height": 20},
            {"type": "flowers", "x": 760, "y": 730, "width": 40, "height": 20},
        ]
        
        # Create smoke sources for buildings
        self.smoke_sources = [
            {"x": 150, "y": 430},  # Shop chimney
            {"x": 850, "y": 430},  # Inn chimney
            {"x": 180, "y": 570},  # Blacksmith chimney
            {"x": 820, "y": 570},  # Library chimney
        ]
    
    def _draw_scenic_background(self, surface):
        """Draw scenic background with massive fantasy castle and sunset"""
        # Sunset sky gradient
        for y in range(200):
            # Create sunset colors from orange to purple to blue
            if y < 60:
                # Orange to red sunset
                sky_color = (
                    min(255, 200 + y * 2),
                    max(100, 150 - y),
                    max(50, 100 - y * 2)
                )
            elif y < 120:
                # Purple transition
                sky_color = (
                    max(150, 200 - (y - 60) * 2),
                    max(50, 100 - (y - 60) * 2),
                    min(200, 150 + (y - 60) * 2)
                )
            else:
                # Blue night sky
                sky_color = (
                    max(50, 100 - (y - 120) * 2),
                    max(50, 100 - (y - 120) * 2),
                    min(255, 150 + (y - 120) * 2)
                )
            pygame.draw.line(surface, sky_color, (0, y), (1000, y))
        
        # Massive fantasy castle filling half the sky
        castle_base_y = 50
        castle_height = 150
        
        # Main castle structure (orange/purple/blue gradient)
        for i in range(castle_height):
            # Create gradient from orange to purple to blue
            if i < 50:
                # Orange section
                castle_color = (
                    min(255, 200 + i * 2),
                    max(100, 150 - i),
                    max(50, 100 - i * 2)
                )
            elif i < 100:
                # Purple section
                castle_color = (
                    max(150, 200 - (i - 50) * 2),
                    max(50, 100 - (i - 50) * 2),
                    min(200, 150 + (i - 50) * 2)
                )
            else:
                # Blue section
                castle_color = (
                    max(50, 100 - (i - 100) * 2),
                    max(50, 100 - (i - 100) * 2),
                    min(255, 150 + (i - 100) * 2)
                )
            
            # Draw castle base with gradient
            pygame.draw.rect(surface, castle_color, (0, castle_base_y + i, 1000, 1))
        
        # Castle towers and spiral staircases (reduced from 10 to 6)
        tower_positions = [
            (100, castle_base_y), (250, castle_base_y), (350, castle_base_y),
            (650, castle_base_y), (750, castle_base_y), (900, castle_base_y)
        ]
        
        for tower_x, tower_y in tower_positions:
            # Main tower
            tower_width = 40
            tower_height = 120
            
            # Tower base (orange)
            pygame.draw.rect(surface, (255, 150, 50), (tower_x, tower_y + 30, tower_width, tower_height - 30))
            pygame.draw.rect(surface, (200, 100, 30), (tower_x, tower_y + 30, tower_width, tower_height - 30), 2)
            
            # Tower top (purple)
            pygame.draw.rect(surface, (150, 50, 200), (tower_x, tower_y, tower_width, 30))
            pygame.draw.rect(surface, (100, 30, 150), (tower_x, tower_y, tower_width, 30), 2)
            
            # Spiral staircase (blue)
            for step in range(8):
                step_x = tower_x + 5 + (step % 3) * 10
                step_y = tower_y + 35 + step * 10
                pygame.draw.rect(surface, (50, 100, 255), (step_x, step_y, 8, 6))
                pygame.draw.rect(surface, (30, 70, 200), (step_x, step_y, 8, 6), 1)
            
            # Tower windows (glowing)
            for window_y in [tower_y + 15, tower_y + 45, tower_y + 75]:
                pygame.draw.rect(surface, (255, 255, 200), (tower_x + 8, window_y, 12, 15))
                pygame.draw.rect(surface, (255, 255, 100), (tower_x + 8, window_y, 12, 15), 1)
            
            # Tower flags
            flag_x = tower_x + tower_width // 2
            flag_y = tower_y - 10
            pygame.draw.line(surface, (100, 100, 100), (flag_x, flag_y), (flag_x, flag_y + 15), 2)
            flag_colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
            flag_color = flag_colors[tower_positions.index((tower_x, tower_y)) % len(flag_colors)]
            pygame.draw.rect(surface, flag_color, (flag_x + 2, flag_y + 2, 12, 8))
            pygame.draw.rect(surface, (255, 255, 255), (flag_x + 2, flag_y + 2, 12, 8), 1)
        
        # Central castle keep (larger structure)
        keep_x = 400
        keep_y = castle_base_y + 20
        keep_width = 200
        keep_height = 100
        
        # Keep base (orange gradient)
        for i in range(keep_height // 2):
            keep_color = (
                min(255, 200 + i * 2),
                max(100, 150 - i),
                max(50, 100 - i * 2)
            )
            pygame.draw.rect(surface, keep_color, (keep_x, keep_y + i, keep_width, 1))
        
        # Keep top (purple gradient)
        for i in range(keep_height // 2):
            keep_color = (
                max(150, 200 - i * 2),
                max(50, 100 - i * 2),
                min(200, 150 + i * 2)
            )
            pygame.draw.rect(surface, keep_color, (keep_x, keep_y + keep_height // 2 + i, keep_width, 1))
        
        # Keep border
        pygame.draw.rect(surface, (100, 50, 150), (keep_x, keep_y, keep_width, keep_height), 3)
        
        # Keep windows
        for window_x in [keep_x + 30, keep_x + 80, keep_x + 130, keep_x + 180]:
            for window_y in [keep_y + 20, keep_y + 50, keep_y + 80]:
                pygame.draw.rect(surface, (255, 255, 200), (window_x, window_y, 20, 25))
                pygame.draw.rect(surface, (255, 255, 100), (window_x, window_y, 20, 25), 1)
        
        # Keep roof (blue)
        roof_points = [(keep_x - 20, keep_y), (keep_x + keep_width // 2, keep_y - 30), (keep_x + keep_width + 20, keep_y)]
        pygame.draw.polygon(surface, (50, 100, 255), roof_points)
        pygame.draw.polygon(surface, (30, 70, 200), roof_points, 2)
        
        # Castle walls connecting towers (updated for 6 towers)
        for i in range(len(tower_positions) - 1):
            wall_x1 = tower_positions[i][0] + 20
            wall_x2 = tower_positions[i + 1][0] + 20
            wall_y = castle_base_y + 140
            wall_height = 20
            
            # Wall gradient
            for j in range(wall_height):
                wall_color = (
                    max(150, 200 - j * 2),
                    max(50, 100 - j * 2),
                    min(200, 150 + j * 2)
                )
                pygame.draw.line(surface, wall_color, (wall_x1, wall_y + j), (wall_x2, wall_y + j))
        
        # Distant mountains (behind castle)
        mountain_points = [
            (0, 200), (200, 160), (400, 180), (600, 150), (800, 170), (1000, 190), (1000, 250), (0, 250)
        ]
        pygame.draw.polygon(surface, (40, 60, 80), mountain_points)
        
        # Mountain details
        for i in range(3):
            peak_x = 200 + i * 300
            peak_y = 160 + (i % 2) * 20
            pygame.draw.circle(surface, (20, 40, 60), (peak_x, peak_y), 20)
        
        # Fill ground with solid base color
        pygame.draw.rect(surface, self.background_color, (0, 250, 1000, 450))
        
        # Scattered dirt/earth spots for texture (static, not moving)
        # Use fixed seed for consistent positioning
        random.seed(42)  # Fixed seed for town ground texture
        for _ in range(50):  # Just a few scattered spots
            dirt_x = random.randint(0, 1000)
            dirt_y = random.randint(250, 700)
            dirt_color = (100 + random.randint(0, 30), 60 + random.randint(0, 20), 40 + random.randint(0, 15))
            pygame.draw.circle(surface, dirt_color, (dirt_x, dirt_y), random.randint(1, 3))
        
        # Grass texture overlay (solid grass appearance) - STATIC positions
        for x in range(0, 1000, 10):  # More frequent grass
            for y in range(250, 700, 8):  # More frequent grass
                if random.random() < 0.6:  # Higher density
                    grass_color = (60 + random.randint(0, 40), 100 + random.randint(0, 40), 40 + random.randint(0, 20))
                    # Fixed positions for grass (no random offset)
                    pygame.draw.circle(surface, grass_color, (x, y), 3)  # Larger grass, fixed position
    
    def _draw_town_paths(self, surface):
        """Draw red dirt paths connecting buildings"""
        # Main path from gate to town center
        path_points = [(500, 260), (500, 350), (500, 400)]
        for i in range(len(path_points) - 1):
            x1, y1 = path_points[i]
            x2, y2 = path_points[i + 1]
            pygame.draw.line(surface, (120, 80, 60), (x1, y1), (x2, y2), 8)
        
        # Side paths to buildings (updated for better spacing)
        side_paths = [
            [(500, 400), (200, 475)],  # To shop
            [(500, 400), (870, 475)],  # To inn
            [(500, 400), (160, 610)],  # To blacksmith
            [(500, 400), (840, 610)],  # To library
            [(500, 400), (500, 555)],  # To market stall
            [(500, 400), (785, 370)],  # To house
        ]
        
        for path in side_paths:
            x1, y1 = path[0]
            x2, y2 = path[1]
            pygame.draw.line(surface, (110, 70, 50), (x1, y1), (x2, y2), 6)
        
        # Path texture (dirt spots)
        for path in side_paths + [[(500, 260), (500, 400)]]:
            x1, y1 = path[0]
            x2, y2 = path[1]
            for i in range(0, int(abs(x2-x1) + abs(y2-y1)), 10):
                t = i / max(abs(x2-x1) + abs(y2-y1), 1)
                px = x1 + (x2-x1) * t
                py = y1 + (y2-y1) * t
                if random.random() < 0.4:
                    pygame.draw.circle(surface, (100, 60, 40), (int(px), int(py)), 2)
    
    def draw_town(self, surface):
        """Draw the scenic town with unique building styles and red dirt paths"""
        if self.area_type != "town":
            return
            
        # Draw scenic background first
        self._draw_scenic_background(surface)
        
        # Draw red dirt paths
        self._draw_town_paths(surface)
        
        # Draw town boundaries first (walls and gates) - 3D style
        for boundary in self.town_boundaries:
            if boundary["type"] == "gate":
                # Draw main gate with 3D arch effect
                gate_x, gate_y = boundary["x"], boundary["y"]
                gate_w, gate_h = boundary["width"], boundary["height"]
                
                # Gate base (3D effect with shadow)
                pygame.draw.rect(surface, (60, 40, 20), (gate_x + 3, gate_y + 3, gate_w, gate_h))
                pygame.draw.rect(surface, (80, 60, 40), (gate_x, gate_y, gate_w, gate_h))
                pygame.draw.rect(surface, (40, 20, 10), (gate_x, gate_y, gate_w, gate_h), 3)
                
                # Gate arch (3D effect)
                arch_points = [
                    (gate_x + 10, gate_y), (gate_x + gate_w//2, gate_y - 25), (gate_x + gate_w - 10, gate_y)
                ]
                pygame.draw.polygon(surface, (70, 50, 30), [(p[0] + 2, p[1] + 2) for p in arch_points])
                pygame.draw.polygon(surface, (100, 80, 60), arch_points)
                pygame.draw.polygon(surface, (50, 30, 10), arch_points, 2)
                
                # Gate door (3D effect)
                door_x = gate_x + 20
                door_y = gate_y + 10
                door_w = gate_w - 40
                door_h = gate_h - 20
                pygame.draw.rect(surface, (30, 15, 5), (door_x + 2, door_y + 2, door_w, door_h))
                pygame.draw.rect(surface, (50, 25, 10), (door_x, door_y, door_w, door_h))
                pygame.draw.rect(surface, (20, 10, 5), (door_x, door_y, door_w, door_h), 2)
                
            elif boundary["type"] == "wall":
                # Draw wall sections with 3D effect
                wall_x, wall_y = boundary["x"], boundary["y"]
                wall_w, wall_h = boundary["width"], boundary["height"]
                
                # Wall shadow
                pygame.draw.rect(surface, (50, 30, 10), (wall_x + 3, wall_y + 3, wall_w, wall_h))
                # Wall base
                pygame.draw.rect(surface, (70, 50, 30), (wall_x, wall_y, wall_w, wall_h))
                pygame.draw.rect(surface, (50, 30, 10), (wall_x, wall_y, wall_w, wall_h), 2)
                
                # Wall texture (3D bricks)
                for i in range(0, wall_w, 15):
                    for j in range(0, wall_h, 8):
                        brick_x = wall_x + i
                        brick_y = wall_y + j
                        pygame.draw.rect(surface, (60, 40, 20), (brick_x + 1, brick_y + 1, 13, 6))
                        pygame.draw.rect(surface, (80, 60, 40), (brick_x, brick_y, 13, 6), 1)
                    
            elif boundary["type"] == "tower":
                # Draw decorative towers with 3D effect
                tower_x, tower_y = boundary["x"], boundary["y"]
                tower_w, tower_h = boundary["width"], boundary["height"]
                
                # Tower shadow
                pygame.draw.rect(surface, (70, 50, 30), (tower_x + 3, tower_y + 3, tower_w, tower_h))
                # Tower base
                pygame.draw.rect(surface, (90, 70, 50), (tower_x, tower_y, tower_w, tower_h))
                pygame.draw.rect(surface, (70, 50, 30), (tower_x, tower_y, tower_w, tower_h), 2)
                
                # Tower top (3D cone)
                top_points = [
                    (tower_x, tower_y), (tower_x + tower_w//2, tower_y - 15), (tower_x + tower_w, tower_y)
                ]
                pygame.draw.polygon(surface, (80, 60, 40), [(p[0] + 2, p[1] + 2) for p in top_points])
                pygame.draw.polygon(surface, (110, 90, 70), top_points)
                pygame.draw.polygon(surface, (60, 40, 20), top_points, 2)
                
                # Tower windows (3D effect)
                window1 = (tower_x + 5, tower_y + 20, 10, 15)
                window2 = (tower_x + 25, tower_y + 20, 10, 15)
                for wx, wy, ww, wh in [window1, window2]:
                    pygame.draw.rect(surface, (20, 10, 5), (wx + 1, wy + 1, ww, wh))
                    pygame.draw.rect(surface, (40, 20, 10), (wx, wy, ww, wh))
                    pygame.draw.rect(surface, (10, 5, 0), (wx, wy, ww, wh), 1)
        
        # Draw main buildings with 3D pop-up style
        for building in self.buildings:
            color = building["color"]
            x, y, w, h = building["x"], building["y"], building["width"], building["height"]
            
            if building["type"] == "town_hall":
                # Draw town hall with 3D columns and roof
                # Building shadow
                pygame.draw.rect(surface, (color[0]-60, color[1]-60, color[2]-60), (x + 4, y + 4, w, h))
                # Building base
                pygame.draw.rect(surface, color, (x, y, w, h))
                pygame.draw.rect(surface, (color[0]-40, color[1]-40, color[2]-40), (x, y, w, h), 3)
                
                # 3D Columns
                for i in range(4):
                    col_x = x + 20 + i * 45
                    col_y = y + 10
                    col_w, col_h = 15, h - 20
                    # Column shadow
                    pygame.draw.rect(surface, (color[0]-40, color[1]-40, color[2]-40), (col_x + 2, col_y + 2, col_w, col_h))
                    # Column base
                    pygame.draw.rect(surface, (color[0]-20, color[1]-20, color[2]-20), (col_x, col_y, col_w, col_h))
                    pygame.draw.rect(surface, (color[0]-40, color[1]-40, color[2]-40), (col_x, col_y, col_w, col_h), 1)
                
                # 3D Roof
                roof_points = [(x - 10, y), (x + w//2, y - 35), (x + w + 10, y)]
                pygame.draw.polygon(surface, (color[0]-50, color[1]-50, color[2]-50), [(p[0] + 3, p[1] + 3) for p in roof_points])
                pygame.draw.polygon(surface, (color[0]-30, color[1]-30, color[2]-30), roof_points)
                pygame.draw.polygon(surface, (color[0]-60, color[1]-60, color[2]-60), roof_points, 2)
                
                # 3D Bell tower
                bell_x = x + w//2 - 10
                bell_y = y - 55
                bell_w, bell_h = 20, 30
                pygame.draw.rect(surface, (color[0]-30, color[1]-30, color[2]-30), (bell_x + 2, bell_y + 2, bell_w, bell_h))
                pygame.draw.rect(surface, (color[0]-10, color[1]-10, color[2]-10), (bell_x, bell_y, bell_w, bell_h))
                pygame.draw.rect(surface, (color[0]-50, color[1]-50, color[2]-50), (bell_x, bell_y, bell_w, bell_h), 2)
                
                # 3D Bell
                bell_center_x = x + w//2
                bell_center_y = y - 40
                pygame.draw.circle(surface, (180, 180, 0), (bell_center_x + 1, bell_center_y + 1), 8)
                pygame.draw.circle(surface, (220, 220, 0), (bell_center_x, bell_center_y), 8)
                pygame.draw.circle(surface, (160, 160, 0), (bell_center_x, bell_center_y), 8, 2)
                
            elif building["type"] == "shop":
                # Draw shop with 3D sign and details
                # Building shadow
                pygame.draw.rect(surface, (color[0]-60, color[1]-60, color[2]-60), (x + 3, y + 3, w, h))
                # Building base
                pygame.draw.rect(surface, color, (x, y, w, h))
                pygame.draw.rect(surface, (color[0]-40, color[1]-40, color[2]-40), (x, y, w, h), 3)
                
                # 3D Shop sign
                sign_x = x + w//2 - 15
                sign_y = y - 25
                sign_w, sign_h = 30, 15
                pygame.draw.rect(surface, (120, 80, 40), (sign_x + 2, sign_y + 2, sign_w, sign_h))
                pygame.draw.rect(surface, (150, 100, 50), (sign_x, sign_y, sign_w, sign_h))
                pygame.draw.rect(surface, (100, 50, 0), (sign_x, sign_y, sign_w, sign_h), 2)
                
                # 3D Door
                door_x = x + w//2 - 15
                door_y = y + h - 35
                door_w, door_h = 30, 30
                pygame.draw.rect(surface, (60, 40, 20), (door_x + 2, door_y + 2, door_w, door_h))
                pygame.draw.rect(surface, (80, 60, 40), (door_x, door_y, door_w, door_h))
                pygame.draw.rect(surface, (40, 20, 10), (door_x, door_y, door_w, door_h), 2)
                
                # 3D Windows
                for wx, wy in [(x + 10, y + 15), (x + w - 30, y + 15)]:
                    pygame.draw.rect(surface, (80, 120, 200), (wx + 1, wy + 1, 20, 20))
                    pygame.draw.rect(surface, (100, 150, 255), (wx, wy, 20, 20))
                    pygame.draw.rect(surface, (60, 100, 180), (wx, wy, 20, 20), 2)
                
            elif building["type"] == "inn":
                # Draw inn with 3D thatched roof
                # Building shadow
                pygame.draw.rect(surface, (color[0]-60, color[1]-60, color[2]-60), (x + 3, y + 3, w, h))
                # Building base
                pygame.draw.rect(surface, color, (x, y, w, h))
                pygame.draw.rect(surface, (color[0]-40, color[1]-40, color[2]-40), (x, y, w, h), 3)
                
                # 3D Thatched roof
                roof_points = [(x - 5, y), (x + w//2, y - 30), (x + w + 5, y)]
                pygame.draw.polygon(surface, (100, 80, 40), [(p[0] + 2, p[1] + 2) for p in roof_points])
                pygame.draw.polygon(surface, (120, 100, 60), roof_points)
                pygame.draw.polygon(surface, (80, 60, 20), roof_points, 2)
                
                # 3D Door
                door_x = x + w//2 - 15
                door_y = y + h - 35
                door_w, door_h = 30, 30
                pygame.draw.rect(surface, (60, 40, 20), (door_x + 2, door_y + 2, door_w, door_h))
                pygame.draw.rect(surface, (80, 60, 40), (door_x, door_y, door_w, door_h))
                pygame.draw.rect(surface, (40, 20, 10), (door_x, door_y, door_w, door_h), 2)
                
                # 3D Windows
                for wx, wy in [(x + 15, y + 15), (x + w - 40, y + 15)]:
                    pygame.draw.rect(surface, (220, 220, 180), (wx + 1, wy + 1, 25, 25))
                    pygame.draw.rect(surface, (255, 255, 200), (wx, wy, 25, 25))
                    pygame.draw.rect(surface, (180, 180, 150), (wx, wy, 25, 25), 2)
                
            elif building["type"] == "blacksmith":
                # Draw blacksmith with 3D chimney and smoke
                # Building shadow
                pygame.draw.rect(surface, (color[0]-60, color[1]-60, color[2]-60), (x + 3, y + 3, w, h))
                # Building base
                pygame.draw.rect(surface, color, (x, y, w, h))
                pygame.draw.rect(surface, (color[0]-40, color[1]-40, color[2]-40), (x, y, w, h), 3)
                
                # 3D Chimney
                chimney_x = x + w - 25
                chimney_y = y - 25
                chimney_w, chimney_h = 15, 20
                pygame.draw.rect(surface, (color[0]-40, color[1]-40, color[2]-40), (chimney_x + 2, chimney_y + 2, chimney_w, chimney_h))
                pygame.draw.rect(surface, (color[0]-20, color[1]-20, color[2]-20), (chimney_x, chimney_y, chimney_w, chimney_h))
                pygame.draw.rect(surface, (color[0]-60, color[1]-60, color[2]-60), (chimney_x, chimney_y, chimney_w, chimney_h), 2)
                
                # 3D Smoke effect
                smoke_x = x + w - 17
                smoke_y = y - 30
                pygame.draw.circle(surface, (80, 80, 80), (smoke_x + 1, smoke_y + 1), 5)
                pygame.draw.circle(surface, (100, 100, 100), (smoke_x, smoke_y), 5)
                pygame.draw.circle(surface, (60, 60, 60), (smoke_x, smoke_y), 5, 1)
                
                # 3D Door
                door_x = x + w//2 - 15
                door_y = y + h - 30
                door_w, door_h = 30, 25
                pygame.draw.rect(surface, (40, 20, 10), (door_x + 2, door_y + 2, door_w, door_h))
                pygame.draw.rect(surface, (60, 40, 20), (door_x, door_y, door_w, door_h))
                pygame.draw.rect(surface, (20, 10, 5), (door_x, door_y, door_w, door_h), 2)
                
            elif building["type"] == "library":
                # Draw library with 3D columns
                # Building shadow
                pygame.draw.rect(surface, (color[0]-60, color[1]-60, color[2]-60), (x + 3, y + 3, w, h))
                # Building base
                pygame.draw.rect(surface, color, (x, y, w, h))
                pygame.draw.rect(surface, (color[0]-40, color[1]-40, color[2]-40), (x, y, w, h), 3)
                
                # 3D Columns
                for col_x, col_y in [(x + 10, y + 10), (x + w - 18, y + 10)]:
                    col_w, col_h = 8, h - 20
                    pygame.draw.rect(surface, (color[0]-40, color[1]-40, color[2]-40), (col_x + 1, col_y + 1, col_w, col_h))
                    pygame.draw.rect(surface, (color[0]-20, color[1]-20, color[2]-20), (col_x, col_y, col_w, col_h))
                    pygame.draw.rect(surface, (color[0]-60, color[1]-60, color[2]-60), (col_x, col_y, col_w, col_h), 1)
                
                # 3D Door
                door_x = x + w//2 - 12
                door_y = y + h - 30
                door_w, door_h = 24, 25
                pygame.draw.rect(surface, (60, 40, 20), (door_x + 2, door_y + 2, door_w, door_h))
                pygame.draw.rect(surface, (80, 60, 40), (door_x, door_y, door_w, door_h))
                pygame.draw.rect(surface, (40, 20, 10), (door_x, door_y, door_w, door_h), 2)
                
                # 3D Windows
                for wx, wy in [(x + 25, y + 15), (x + w - 45, y + 15)]:
                    pygame.draw.rect(surface, (180, 180, 220), (wx + 1, wy + 1, 20, 20))
                    pygame.draw.rect(surface, (200, 200, 255), (wx, wy, 20, 20))
                    pygame.draw.rect(surface, (140, 140, 200), (wx, wy, 20, 20), 2)
                
            elif building["type"] == "house":
                # Draw houses with 3D roofs
                # Building shadow
                pygame.draw.rect(surface, (color[0]-60, color[1]-60, color[2]-60), (x + 3, y + 3, w, h))
                # Building base
                pygame.draw.rect(surface, color, (x, y, w, h))
                pygame.draw.rect(surface, (color[0]-40, color[1]-40, color[2]-40), (x, y, w, h), 3)
                
                # 3D Roof
                roof_points = [(x - 3, y), (x + w//2, y - 20), (x + w + 3, y)]
                pygame.draw.polygon(surface, (color[0]-50, color[1]-50, color[2]-50), [(p[0] + 2, p[1] + 2) for p in roof_points])
                pygame.draw.polygon(surface, (color[0]-30, color[1]-30, color[2]-30), roof_points)
                pygame.draw.polygon(surface, (color[0]-70, color[1]-70, color[2]-70), roof_points, 2)
                
                # 3D Door
                door_x = x + w//2 - 8
                door_y = y + h - 25
                door_w, door_h = 16, 20
                pygame.draw.rect(surface, (40, 20, 10), (door_x + 1, door_y + 1, door_w, door_h))
                pygame.draw.rect(surface, (60, 40, 20), (door_x, door_y, door_w, door_h))
                pygame.draw.rect(surface, (20, 10, 5), (door_x, door_y, door_w, door_h), 2)
                
                # 3D Window
                window_x = x + w//2 - 6
                window_y = y + 10
                window_w, window_h = 12, 12
                pygame.draw.rect(surface, (180, 180, 220), (window_x + 1, window_y + 1, window_w, window_h))
                pygame.draw.rect(surface, (200, 200, 255), (window_x, window_y, window_w, window_h))
                pygame.draw.rect(surface, (140, 140, 200), (window_x, window_y, window_w, window_h), 2)
                
            elif building["type"] == "stall":
                # Draw market stalls with 3D effect
                # Building shadow
                pygame.draw.rect(surface, (color[0]-60, color[1]-60, color[2]-60), (x + 2, y + 2, w, h))
                # Building base
                pygame.draw.rect(surface, color, (x, y, w, h))
                pygame.draw.rect(surface, (color[0]-40, color[1]-40, color[2]-40), (x, y, w, h), 2)
                
                # 3D Stall roof
                roof_points = [(x - 2, y), (x + w//2, y - 12), (x + w + 2, y)]
                pygame.draw.polygon(surface, (color[0]-30, color[1]-30, color[2]-30), [(p[0] + 1, p[1] + 1) for p in roof_points])
                pygame.draw.polygon(surface, (color[0]-20, color[1]-20, color[2]-20), roof_points)
                pygame.draw.polygon(surface, (color[0]-50, color[1]-50, color[2]-50), roof_points, 1)
                
                # 3D Stall counter
                counter_x = x + 5
                counter_y = y + h - 20
                counter_w, counter_h = w - 10, 10
                pygame.draw.rect(surface, (color[0]-20, color[1]-20, color[2]-20), (counter_x + 1, counter_y + 1, counter_w, counter_h))
                pygame.draw.rect(surface, (color[0]-10, color[1]-10, color[2]-10), (counter_x, counter_y, counter_w, counter_h))
                pygame.draw.rect(surface, (color[0]-40, color[1]-40, color[2]-40), (counter_x, counter_y, counter_w, counter_h), 1)
        
        # Draw decorative elements with 3D effect
        for decoration in self.decorations:
            x, y, w, h = decoration["x"], decoration["y"], decoration["width"], decoration["height"]
            
            if decoration["type"] == "lamp":
                # Draw 3D street lamps
                # Lamp post shadow
                pygame.draw.rect(surface, (40, 20, 10), (x + w//2 - 2, y + h - 18, 6, 20))
                # Lamp post
                pygame.draw.rect(surface, (60, 40, 20), (x + w//2 - 3, y + h - 20, 6, 20))
                pygame.draw.rect(surface, (40, 20, 10), (x + w//2 - 3, y + h - 20, 6, 20), 1)
                
                # 3D Lamp top
                lamp_x = x + w//2
                lamp_y = y + h - 25
                pygame.draw.circle(surface, (180, 180, 80), (lamp_x + 1, lamp_y + 1), 8)
                pygame.draw.circle(surface, (200, 200, 100), (lamp_x, lamp_y), 8)
                pygame.draw.circle(surface, (160, 160, 60), (lamp_x, lamp_y), 8, 2)
                
                # 3D Light glow
                pygame.draw.circle(surface, (255, 255, 200), (lamp_x, lamp_y), 12, 1)
                
            elif decoration["type"] == "tree":
                # Draw 3D trees
                # Tree trunk shadow
                pygame.draw.rect(surface, (60, 40, 20), (x + w//2 - 2, y + h - 12, 6, 15))
                # Tree trunk
                pygame.draw.rect(surface, (80, 60, 40), (x + w//2 - 3, y + h - 15, 6, 15))
                pygame.draw.rect(surface, (60, 40, 20), (x + w//2 - 3, y + h - 15, 6, 15), 1)
                
                # 3D Tree foliage
                tree_center_x = x + w//2
                tree_center_y = y + h - 20
                pygame.draw.circle(surface, (30, 60, 30), (tree_center_x + 2, tree_center_y + 2), 15)
                pygame.draw.circle(surface, (40, 80, 40), (tree_center_x, tree_center_y), 15)
                pygame.draw.circle(surface, (20, 40, 20), (tree_center_x, tree_center_y), 15, 2)
                
                # 3D Tree details
                for detail_x, detail_y in [(tree_center_x - 8, tree_center_y - 5), (tree_center_x + 8, tree_center_y - 5)]:
                    pygame.draw.circle(surface, (50, 80, 50), (detail_x + 1, detail_y + 1), 8)
                    pygame.draw.circle(surface, (60, 100, 60), (detail_x, detail_y), 8)
                    pygame.draw.circle(surface, (40, 60, 40), (detail_x, detail_y), 8, 1)
                
            elif decoration["type"] == "flowers":
                # Draw 3D flower beds
                # Flower bed shadow
                pygame.draw.rect(surface, (30, 60, 30), (x + 1, y + 1, w, h))
                # Flower bed base
                pygame.draw.rect(surface, (40, 80, 40), (x, y, w, h))
                pygame.draw.rect(surface, (20, 40, 20), (x, y, w, h), 1)
                
                # 3D Flowers
                for i in range(6):
                    flower_x = x + 5 + i * 5
                    flower_y = y + 5 + (i % 2) * 8
                    color_choices = [(255, 100, 100), (255, 200, 100), (200, 100, 255), (100, 200, 255)]
                    flower_color = color_choices[i % len(color_choices)]
                    
                    # Flower shadow
                    pygame.draw.circle(surface, (flower_color[0]-50, flower_color[1]-50, flower_color[2]-50), (flower_x + 1, flower_y + 1), 3)
                    # Flower base
                    pygame.draw.circle(surface, flower_color, (flower_x, flower_y), 3)
                    pygame.draw.circle(surface, (255, 255, 255), (flower_x, flower_y), 1)
    
    def generate_town_particles(self, particle_system):
        """Generate town-specific particle effects"""
        if self.area_type != "town":
            return
            
        # Generate smoke from chimneys
        for smoke_source in self.smoke_sources:
            if random.random() < 0.3:  # 30% chance each frame
                particle_system.add_particle(
                    smoke_source["x"], smoke_source["y"],
                    (100, 100, 100),
                    (random.uniform(-0.2, 0.2), random.uniform(-1, -0.5)),
                    4, 60
                )
        
        # Generate fountain particles (if near town center)
        if random.random() < 0.2:  # 20% chance each frame
            particle_system.add_particle(
                500, 450,  # Town center
                (150, 200, 255),
                (random.uniform(-0.3, 0.3), random.uniform(-0.5, -0.2)),
                3, 40
            )
        
        # Generate leaf particles from trees
        if random.random() < 0.1:  # 10% chance each frame
            tree_positions = [(50, 250), (920, 250), (50, 700), (920, 700)]
            tree_x, tree_y = random.choice(tree_positions)
            particle_system.add_particle(
                tree_x, tree_y,
                (100, 150, 50),
                (random.uniform(-0.2, 0.2), random.uniform(0.2, 0.5)),
                3, 50
            )
    
    def is_player_near_building(self, player_x, player_y, building_type=None):
        """Check if player is near a specific building type"""
        if self.area_type != "town":
            return False
            
        for building in self.buildings:
            if building_type and building["type"] != building_type:
                continue
                
            # Check if player is within 50 pixels of building
            building_center_x = building["x"] + building["width"] // 2
            building_center_y = building["y"] + building["height"] // 2
            
            distance = math.sqrt((player_x - building_center_x)**2 + (player_y - building_center_y)**2)
            if distance < 50:
                return True
        return False
    
    def check_building_collision(self, player_x, player_y):
        """Check if player collides with any building"""
        if self.area_type != "town":
            return False
            
        player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
        
        for building in self.buildings:
            if building.get("collision", False):
                building_rect = pygame.Rect(building["x"], building["y"], 
                                          building["width"], building["height"])
                if player_rect.colliderect(building_rect):
                    return True
        return False
    
    def _create_town_guard(self):
        """Create the town guard NPC for the entrance cutscene"""
        if self.area_type != "town":
            return
            
        # Create guard at the town entrance (near the gate)
        self.guard = {
            "x": 300,  # Moved 200 pixels left from center gate
            "y": 270,  # Just inside the gate (moved down 2 squares)
            "width": 40,
            "height": 60,
            "color": (100, 150, 200),  # Blue uniform
            "animation_offset": 0,
            "animation_timer": 0,
            "dialogue": [
                "Halt! Welcome to our fair town, traveler.",
                "I am Captain Marcus, keeper of the peace.",
                "You may enter freely, but mind our laws.",
                "If you need assistance, seek me out.",
                "Safe travels, adventurer!"
            ],
            "current_dialogue": 0,
            "dialogue_timer": 0,
            "visible": True
        }
    
    def check_entrance_cutscene(self, player_x, player_y):
        """Check if player should trigger the entrance cutscene"""
        if self.area_type != "town" or self.entrance_cutscene_triggered:
            return False
            
        # Convert world coordinates to local area coordinates
        area_world_x, area_world_y = self.get_world_position()
        local_x = player_x - area_world_x
        local_y = player_y - area_world_y
        
        # Check if player is near the entrance area (adjusted for new gate position)
        if 450 <= local_x <= 550 and 250 <= local_y <= 300:
            self.entrance_cutscene_triggered = True
            self.cutscene_active = True
            self.cutscene_timer = 0
            self.cutscene_phase = 0
            return True
        return False
    
    def update_cutscene(self):
        """Update the entrance cutscene"""
        if not self.cutscene_active or not self.guard:
            return
            
        self.cutscene_timer += 1
        
        # Update guard animation
        self.guard["animation_timer"] += 1
        if self.guard["animation_timer"] >= 10:
            self.guard["animation_timer"] = 0
            self.guard["animation_offset"] = 2 if self.guard["animation_offset"] == 0 else 0
        
        # Cutscene phases
        if self.cutscene_phase == 0:  # Guard approaches
            if self.cutscene_timer > 5:  # Much faster spawn (reduced from 15 to 5)
                self.cutscene_phase = 1
                self.cutscene_timer = 0
                # Reset dialogue to first line
                if self.guard:
                    self.guard["current_dialogue"] = 0
        elif self.cutscene_phase == 1:  # Guard speaks
            # Dialogue progression is now handled by SPACE key input
            # Only auto-advance to phase 2 if player reaches the last dialogue
            pass
        elif self.cutscene_phase == 2:  # Cutscene ends
            if self.cutscene_timer > 60:  # 1 second
                self.cutscene_active = False
                # Hide the guard after cutscene
                if self.guard:
                    self.guard["visible"] = False
    
    def draw_cutscene(self, surface):
        """Draw the entrance cutscene"""
        if not self.cutscene_active or not self.guard or self.cutscene_phase >= 2:
            return
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface((1000, 700), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        surface.blit(overlay, (0, 0))
        
        # Draw Dragon Knight Guard
        if not self.guard.get("visible", True):
            return
            
        guard_x = self.guard["x"]
        guard_y = self.guard["y"] + self.guard["animation_offset"]
        guard_w = self.guard["width"]
        guard_h = self.guard["height"]
        
        # Dragon Knight shadow
        pygame.draw.ellipse(surface, (0, 0, 0), (guard_x + 2, guard_y + 62, guard_w - 4, 8))
        
        # Silver armor with detailed shading
        # Armor base (dark silver)
        pygame.draw.rect(surface, (120, 120, 140), (guard_x, guard_y, guard_w, guard_h))
        pygame.draw.rect(surface, (100, 100, 120), (guard_x, guard_y, guard_w, guard_h), 2)
        
        # Armor highlights (light silver)
        pygame.draw.rect(surface, (180, 180, 200), (guard_x + 2, guard_y + 2, guard_w - 4, 10))
        pygame.draw.rect(surface, (160, 160, 180), (guard_x + 2, guard_y + 15, guard_w - 4, 8))
        
        # Helmet (3D effect)
        helmet_y = guard_y - 15
        pygame.draw.rect(surface, (140, 140, 160), (guard_x + 5, helmet_y, guard_w - 10, 15))
        pygame.draw.rect(surface, (100, 100, 120), (guard_x + 5, helmet_y, guard_w - 10, 15), 2)
        pygame.draw.rect(surface, (180, 180, 200), (guard_x + 8, helmet_y + 2, guard_w - 16, 8))
        
        # Visor (dark)
        pygame.draw.rect(surface, (40, 40, 60), (guard_x + 8, helmet_y + 5, guard_w - 16, 4))
        
        # Dragon Knight Helmet Flares (silver dragon wings)
        # Left flare
        left_flare_points = [
            (guard_x + 2, helmet_y + 3),
            (guard_x - 8, helmet_y + 1),
            (guard_x - 12, helmet_y + 5),
            (guard_x - 10, helmet_y + 8),
            (guard_x - 5, helmet_y + 10),
            (guard_x + 2, helmet_y + 8)
        ]
        pygame.draw.polygon(surface, (160, 160, 180), left_flare_points)
        pygame.draw.polygon(surface, (120, 120, 140), left_flare_points, 2)
        pygame.draw.polygon(surface, (200, 200, 220), [
            (guard_x + 2, helmet_y + 3),
            (guard_x - 6, helmet_y + 2),
            (guard_x - 8, helmet_y + 4),
            (guard_x - 4, helmet_y + 6),
            (guard_x + 2, helmet_y + 5)
        ])
        
        # Right flare
        right_flare_points = [
            (guard_x + guard_w - 2, helmet_y + 3),
            (guard_x + guard_w + 8, helmet_y + 1),
            (guard_x + guard_w + 12, helmet_y + 5),
            (guard_x + guard_w + 10, helmet_y + 8),
            (guard_x + guard_w + 5, helmet_y + 10),
            (guard_x + guard_w - 2, helmet_y + 8)
        ]
        pygame.draw.polygon(surface, (160, 160, 180), right_flare_points)
        pygame.draw.polygon(surface, (120, 120, 140), right_flare_points, 2)
        pygame.draw.polygon(surface, (200, 200, 220), [
            (guard_x + guard_w - 2, helmet_y + 3),
            (guard_x + guard_w + 6, helmet_y + 2),
            (guard_x + guard_w + 8, helmet_y + 4),
            (guard_x + guard_w + 4, helmet_y + 6),
            (guard_x + guard_w - 2, helmet_y + 5)
        ])
        
        # Helmet crest (dragon spine)
        crest_points = [
            (guard_x + guard_w//2 - 2, helmet_y - 8),
            (guard_x + guard_w//2, helmet_y - 15),
            (guard_x + guard_w//2 + 2, helmet_y - 8),
            (guard_x + guard_w//2 + 1, helmet_y - 5),
            (guard_x + guard_w//2 - 1, helmet_y - 5)
        ]
        pygame.draw.polygon(surface, (180, 180, 200), crest_points)
        pygame.draw.polygon(surface, (140, 140, 160), crest_points, 2)
        pygame.draw.line(surface, (200, 200, 220), 
                        (guard_x + guard_w//2, helmet_y - 15), 
                        (guard_x + guard_w//2, helmet_y - 8), 2)
        
        # Shoulder plates
        pygame.draw.rect(surface, (160, 160, 180), (guard_x - 5, guard_y + 5, 8, 12))
        pygame.draw.rect(surface, (160, 160, 180), (guard_x + guard_w - 3, guard_y + 5, 8, 12))
        
        # Chest plate (detailed)
        chest_x = guard_x + 5
        chest_y = guard_y + 12
        chest_w = guard_w - 10
        chest_h = 20
        pygame.draw.rect(surface, (140, 140, 160), (chest_x, chest_y, chest_w, chest_h))
        pygame.draw.rect(surface, (100, 100, 120), (chest_x, chest_y, chest_w, chest_h), 2)
        pygame.draw.rect(surface, (180, 180, 200), (chest_x + 2, chest_y + 2, chest_w - 4, 6))
        
        # Belt
        pygame.draw.rect(surface, (80, 80, 100), (guard_x + 3, guard_y + 35, guard_w - 6, 4))
        
        # Legs
        pygame.draw.rect(surface, (120, 120, 140), (guard_x + 5, guard_y + 40, 8, 20))
        pygame.draw.rect(surface, (120, 120, 140), (guard_x + guard_w - 13, guard_y + 40, 8, 20))
        
        # Boots
        pygame.draw.rect(surface, (60, 60, 80), (guard_x + 3, guard_y + 60, 10, 8))
        pygame.draw.rect(surface, (60, 60, 80), (guard_x + guard_w - 13, guard_y + 60, 10, 8))
        
        # Sword (silver)
        sword_x = guard_x + guard_w + 5
        sword_y = guard_y + 20
        pygame.draw.rect(surface, (180, 180, 200), (sword_x, sword_y, 4, 25))
        pygame.draw.rect(surface, (160, 160, 180), (sword_x, sword_y, 4, 25), 1)
        pygame.draw.rect(surface, (200, 200, 220), (sword_x + 1, sword_y + 1, 2, 8))
        
        # Sword handle
        pygame.draw.rect(surface, (100, 80, 60), (sword_x - 2, sword_y + 25, 8, 6))
        pygame.draw.rect(surface, (80, 60, 40), (sword_x - 2, sword_y + 25, 8, 6), 1)
        
        # Shield (round)
        shield_x = guard_x - 15
        shield_y = guard_y + 15
        pygame.draw.circle(surface, (140, 140, 160), (shield_x, shield_y), 12)
        pygame.draw.circle(surface, (100, 100, 120), (shield_x, shield_y), 12, 2)
        pygame.draw.circle(surface, (180, 180, 200), (shield_x, shield_y), 8)
        pygame.draw.circle(surface, (160, 160, 180), (shield_x, shield_y), 8, 1)
        
        # Dialogue box
        dialogue_box = pygame.Surface((800, 150))
        dialogue_box.fill(UI_BG)
        pygame.draw.rect(dialogue_box, UI_BORDER, (0, 0, 800, 150), 3)
        
        # Draw dialogue text
        current_text = self.guard["dialogue"][self.guard["current_dialogue"]]
        text_surface = font_cinematic.render(current_text, True, TEXT_COLOR)
        dialogue_box.blit(text_surface, (120, 60))
        
        # Draw continue indicator
        if self.cutscene_timer % 60 < 30:
            continue_text = font_small.render("Press SPACE to continue", True, (150, 150, 150))
            dialogue_box.blit(continue_text, (120, 120))
        
        # Position dialogue box at bottom of screen
        surface.blit(dialogue_box, (100, SCREEN_HEIGHT - 200))
    
    def draw(self, surface, world_map=None):
        """Draw the area based on its type"""
        if self.area_type == "town":
            self.draw_town(surface)
        else:
            # Draw regular area background
            surface.fill(self.background_color)
            
            # Draw grid overlay
            for x in range(0, SCREEN_WIDTH, GRID_SIZE):
                pygame.draw.line(surface, self.grid_color, (x, 0), (x, SCREEN_HEIGHT), 1)
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
                pygame.draw.line(surface, self.grid_color, (0, y), (SCREEN_WIDTH, y), 1)
            
            # Draw area-specific decorations
            if self.area_type == "forest":
                # Draw trees
                for i in range(5):
                    x = random.randint(50, SCREEN_WIDTH - 50)
                    y = random.randint(50, SCREEN_HEIGHT - 50)
                    pygame.draw.circle(surface, (50, 100, 50), (x, y), 30)
            elif self.area_type == "desert":
                # Draw sand dunes
                for i in range(3):
                    x = random.randint(100, SCREEN_WIDTH - 100)
                    y = random.randint(100, SCREEN_HEIGHT - 100)
                    pygame.draw.ellipse(surface, (120, 110, 80), (x, y, 80, 40))
            elif self.area_type == "mountain":
                # Draw mountain peaks
                points = [(0, SCREEN_HEIGHT), (200, SCREEN_HEIGHT - 100), 
                         (400, SCREEN_HEIGHT - 150), (600, SCREEN_HEIGHT - 120),
                         (800, SCREEN_HEIGHT - 130), (SCREEN_WIDTH, SCREEN_HEIGHT)]
                pygame.draw.polygon(surface, (80, 80, 100), points)
        
        # Draw town cutscene if active
        if self.cutscene_active:
            self.draw_cutscene(surface) 