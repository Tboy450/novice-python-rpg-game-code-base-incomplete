"""
📜 LEGACY FILE - Original Monolithic Version
===========================================

⚠️  IMPORTANT: This is the OLD version of the game (5523 lines in one file!)
   The NEW version is organized into separate modules in the other folders.

🎯 WHAT THIS FILE IS:
- This is the original "messy" version before we organized it
- It contains ALL the game code in one giant file (5523 lines!)
- It's kept for reference and comparison
- The NEW organized version is much easier to understand and modify

📁 NEW ORGANIZED VERSION:
- main.py - Starts the game
- config/ - Game settings and constants
- core/ - Main game logic
- world/ - World and areas
- entities/ - Characters and objects
- ui/ - User interface
- audio/ - Music and sound
- systems/ - Special effects
- utils/ - Helper functions

🔍 FOR NOVICE CODERS:
This file shows what the code looked like BEFORE organization.
It's like having all your clothes in one giant pile vs. organizing them
into drawers by type (shirts, pants, socks, etc.).

The new organized version is much easier to:
- Find specific code
- Make changes
- Understand what each part does
- Work on with other people

🎮 GAME FEATURES (Same in both versions):
- 3x3 world map with different area types
- Turn-based combat system with multiple character classes
- Procedurally generated chiptune music
- Particle effects and visual effects
- Opening cutscene and story elements
- Boss battles and progression system

CONTROLS:
- Arrow Keys/WASD: Movement in overworld
- Enter/Space: Confirm actions
- Escape: Menu navigation
- M: Toggle world map view
"""

import os
os.environ['SDL_AUDIODRIVER'] = 'directsound'  # or 'winmm' or 'waveout'
import pygame
import sys
import random
import math
from pygame import gfxdraw
import numpy as np
import tempfile
import wave
import io

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

# ============================================================================
# GAME CONSTANTS AND CONFIGURATION
# ============================================================================

# Display and Performance Settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
PLAYER_SIZE = 50
ENEMY_SIZE = 40
ITEM_SIZE = 30
FPS = 60

# Visual Design - Retro 80s Color Palette
# =======================================
# Core UI Colors
BACKGROUND = (10, 10, 30)        # Dark blue background
UI_BG = (20, 15, 40)             # UI panel background
UI_BORDER = (255, 105, 180)      # Hot pink borders
TEXT_COLOR = (0, 255, 255)       # Cyan text
GRID_COLOR = (50, 50, 80)        # Grid lines

# Character and Entity Colors
PLAYER_COLOR = (0, 255, 0)       # Green player
ENEMY_COLOR = (255, 0, 0)        # Red enemies
DRAGON_COLOR = (255, 69, 0)      # Red-orange dragons
ITEM_COLOR = (255, 215, 0)       # Gold items

# Status Bar Colors
HEALTH_COLOR = (255, 105, 180)   # Hot pink health
MANA_COLOR = (0, 255, 255)       # Cyan mana
EXP_COLOR = (255, 255, 0)        # Yellow experience

# Special Effect Color Palettes
# =============================
# Fire effect gradient (orange to yellow)
FIRE_COLORS = [(255, 100, 0), (255, 150, 0), (255, 200, 50)]
# Ice effect gradient (light blue to white)
ICE_COLORS = [(100, 200, 255), (150, 220, 255), (200, 240, 255)]
# Shadow effect gradient (dark blue to purple)
SHADOW_COLORS = [(40, 40, 80), (70, 70, 120), (100, 100, 150)]
# Magic effect gradient (purple to pink)
MAGIC_COLORS = [(150, 0, 255), (200, 50, 255), (255, 100, 255)]

# ============================================================================
# PYGAME INITIALIZATION AND SETUP
# ============================================================================

# Create the main game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dragon's Lair RPG")
clock = pygame.time.Clock()

# Font System Setup
# =================
# Try to load custom fonts, fall back to system fonts if not available
try:
    font_large = pygame.font.Font("freesansbold.ttf", 48)      # Main titles
    font_medium = pygame.font.Font("freesansbold.ttf", 32)     # UI headers
    font_small = pygame.font.Font("freesansbold.ttf", 24)      # Regular text
    font_tiny = pygame.font.Font("freesansbold.ttf", 18)       # Small labels
    font_cinematic = pygame.font.Font("freesansbold.ttf", 28)  # Cutscene text
except:
    # Fallback to system fonts if custom fonts not found
    font_large = pygame.font.SysFont("Courier", 48, bold=True)
    font_medium = pygame.font.SysFont("Courier", 32, bold=True)
    font_small = pygame.font.SysFont("Courier", 24, bold=True)
    font_tiny = pygame.font.SysFont("Courier", 18, bold=True)
    font_cinematic = pygame.font.SysFont("Courier", 28, bold=True)

# ============================================================================
# WORLD AND GRID SYSTEM CONFIGURATION
# ============================================================================

# Grid System (for movement and collision detection)
GRID_SIZE = 50                    # Size of each grid square
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE   # Number of grid columns
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE # Number of grid rows

# World Map System (3x3 grid of areas)
WORLD_SIZE = 3                    # 3x3 world grid
AREA_WIDTH = SCREEN_WIDTH         # Each area is full screen width
AREA_HEIGHT = SCREEN_HEIGHT       # Each area is full screen height
WORLD_WIDTH = WORLD_SIZE * AREA_WIDTH    # Total world width
WORLD_HEIGHT = WORLD_SIZE * AREA_HEIGHT  # Total world height

# ============================================================================
# WORLD AREA CLASS - Manages individual areas in the 3x3 world grid
# ============================================================================
class WorldArea:
    """
    Represents a single area in the 3x3 world grid.
    Each area has its own terrain type, enemies, items, and visual style.
    
    Area Types: forest, desert, mountain, swamp, volcano, town
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
            (100, castle_base_y), (250, castle_base_y), (400, castle_base_y),
            (600, castle_base_y), (750, castle_base_y), (900, castle_base_y)
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
        
        # Grass texture overlay (moved much lower)
        for x in range(0, 1000, 20):
            for y in range(250, 700, 15):
                if random.random() < 0.3:
                    grass_color = (60 + random.randint(0, 40), 100 + random.randint(0, 40), 40 + random.randint(0, 20))
                    pygame.draw.circle(surface, grass_color, (x + random.randint(0, 20), y + random.randint(0, 15)), 2)
    
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
                smoke_x = smoke_source["x"] + random.randint(-5, 5)
                smoke_y = smoke_source["y"] - 10
                velocity = (random.uniform(-0.5, 0.5), random.uniform(-1, -0.5))
                color = (100 + random.randint(0, 50), 100 + random.randint(0, 50), 100 + random.randint(0, 50))
                particle_system.add_particle(smoke_x, smoke_y, color, velocity, random.randint(3, 8), random.randint(30, 60))
        
        # Generate floating leaves
        if random.random() < 0.2:  # 20% chance each frame
            leaf_x = random.randint(50, 950)
            leaf_y = random.randint(220, 320)
            velocity = (random.uniform(-0.2, 0.2), random.uniform(0.1, 0.3))
            color = (100 + random.randint(0, 50), 150 + random.randint(0, 50), 50 + random.randint(0, 30))
            particle_system.add_particle(leaf_x, leaf_y, color, velocity, random.randint(2, 5), random.randint(40, 80))
    
    def is_player_near_building(self, player_x, player_y, building_type=None):
        """Check if player is near a specific building type for interaction"""
        if self.area_type != "town":
            return False, None
            
        # Convert world coordinates to local area coordinates
        area_world_x, area_world_y = self.get_world_position()
        local_x = player_x - area_world_x
        local_y = player_y - area_world_y
        
        # Check distance to buildings
        for building in self.buildings:
            if building_type and building["type"] != building_type:
                continue
                
            building_center_x = building["x"] + building["width"] // 2
            building_center_y = building["y"] + building["height"] // 2
            
            distance = math.sqrt((local_x - building_center_x)**2 + (local_y - building_center_y)**2)
            if distance < 80:  # Interaction range
                return True, building["type"]
        
        return False, None

    def check_building_collision(self, player_x, player_y):
        """Check if player is colliding with any buildings (allows 1 square inside)"""
        if self.area_type != "town":
            return False
            
        # Convert world coordinates to local area coordinates
        area_world_x, area_world_y = self.get_world_position()
        local_x = player_x - area_world_x
        local_y = player_y - area_world_y
        
        # Check collision with buildings (allowing 1 square inside horizontally, full collision vertically)
        for building in self.buildings:
            if building.get("collision", False):
                # Allow 1 square (60 pixels) inside horizontally, but full collision vertically
                if (local_x < building["x"] + building["width"] - 60 and 
                    local_x + 40 > building["x"] + 60 and 
                    local_y < building["y"] + building["height"] and 
                    local_y + 40 > building["y"]):
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
        armor_base = (180, 180, 200)  # Silver base
        armor_highlight = (220, 220, 240)  # Bright silver
        armor_shadow = (140, 140, 160)  # Dark silver
        armor_detail = (100, 100, 120)  # Darker detail lines
        
        # Main armor body
        pygame.draw.rect(surface, armor_base, (guard_x + 2, guard_y + 12, guard_w - 4, guard_h - 12))
        # Armor highlight
        pygame.draw.rect(surface, armor_highlight, (guard_x + 4, guard_y + 14, guard_w - 8, 8))
        # Armor shadow
        pygame.draw.rect(surface, armor_shadow, (guard_x + 2, guard_y + 12, 4, guard_h - 12))
        
        # Dragon scale pattern on chest
        for i in range(3):
            for j in range(2):
                scale_x = guard_x + 8 + i * 8
                scale_y = guard_y + 20 + j * 8
                pygame.draw.ellipse(surface, armor_detail, (scale_x, scale_y, 6, 4))
                pygame.draw.ellipse(surface, armor_highlight, (scale_x + 1, scale_y + 1, 4, 2))
        
        # Dragon Knight head with detailed helmet
        head_x = guard_x + guard_w//2 - 10
        head_y = guard_y - 15
        
        # Head shadow
        pygame.draw.circle(surface, (180, 140, 100), (head_x + 10 + 1, head_y + 10 + 1), 10)
        # Head base
        pygame.draw.circle(surface, (240, 200, 150), (head_x + 10, head_y + 10), 10)
        # Head highlight
        pygame.draw.circle(surface, (255, 220, 180), (head_x + 8, head_y + 8), 4)
        # Head outline
        pygame.draw.circle(surface, (200, 150, 100), (head_x + 10, head_y + 10), 10, 1)
        
        # Dragon Knight full helmet with flares
        helmet_color = (160, 160, 180)
        helmet_highlight = (200, 200, 220)
        helmet_shadow = (120, 120, 140)
        helmet_detail = (100, 100, 120)
        
        # Helmet base (full coverage)
        helmet_base_points = [
            (head_x + 2, head_y), (head_x + 18, head_y),  # Top
            (head_x + 20, head_y + 2), (head_x + 20, head_y + 8),  # Right side
            (head_x + 18, head_y + 12), (head_x + 2, head_y + 12),  # Bottom
            (head_x, head_y + 8), (head_x, head_y + 2)  # Left side
        ]
        pygame.draw.polygon(surface, helmet_color, helmet_base_points)
        pygame.draw.polygon(surface, helmet_highlight, [
            (head_x + 4, head_y + 1), (head_x + 16, head_y + 1),
            (head_x + 18, head_y + 3), (head_x + 18, head_y + 7),
            (head_x + 16, head_y + 10), (head_x + 4, head_y + 10),
            (head_x + 2, head_y + 7), (head_x + 2, head_y + 3)
        ])
        pygame.draw.polygon(surface, helmet_shadow, [
            (head_x + 2, head_y), (head_x, head_y + 2), (head_x, head_y + 8),
            (head_x + 2, head_y + 12), (head_x + 4, head_y + 12)
        ])
        
        # Helmet crown with dragon motifs
        crown_points = [
            (head_x + 2, head_y), (head_x + 18, head_y),
            (head_x + 16, head_y - 2), (head_x + 14, head_y - 4),
            (head_x + 12, head_y - 6), (head_x + 8, head_y - 6),
            (head_x + 6, head_y - 4), (head_x + 4, head_y - 2)
        ]
        pygame.draw.polygon(surface, helmet_color, crown_points)
        pygame.draw.polygon(surface, helmet_highlight, [
            (head_x + 4, head_y - 1), (head_x + 16, head_y - 1),
            (head_x + 14, head_y - 3), (head_x + 12, head_y - 5),
            (head_x + 8, head_y - 5), (head_x + 6, head_y - 3)
        ])
        
        # Dragon horns on helmet (larger and more detailed)
        horn_color = (140, 140, 160)
        horn_highlight = (180, 180, 200)
        
        # Left horn (curved)
        left_horn_points = [
            (head_x + 4, head_y), (head_x + 2, head_y - 2), (head_x + 1, head_y - 6),
            (head_x + 2, head_y - 10), (head_x + 4, head_y - 12), (head_x + 6, head_y - 10),
            (head_x + 7, head_y - 6), (head_x + 6, head_y - 2)
        ]
        pygame.draw.polygon(surface, horn_color, left_horn_points)
        pygame.draw.polygon(surface, horn_highlight, [
            (head_x + 4, head_y), (head_x + 3, head_y - 2), (head_x + 2, head_y - 6),
            (head_x + 3, head_y - 10), (head_x + 5, head_y - 10), (head_x + 6, head_y - 6),
            (head_x + 5, head_y - 2)
        ])
        
        # Right horn (curved)
        right_horn_points = [
            (head_x + 12, head_y), (head_x + 14, head_y - 2), (head_x + 15, head_y - 6),
            (head_x + 14, head_y - 10), (head_x + 12, head_y - 12), (head_x + 10, head_y - 10),
            (head_x + 9, head_y - 6), (head_x + 10, head_y - 2)
        ]
        pygame.draw.polygon(surface, horn_color, right_horn_points)
        pygame.draw.polygon(surface, horn_highlight, [
            (head_x + 12, head_y), (head_x + 13, head_y - 2), (head_x + 14, head_y - 6),
            (head_x + 13, head_y - 10), (head_x + 11, head_y - 10), (head_x + 10, head_y - 6),
            (head_x + 11, head_y - 2)
        ])
        
        # Helmet visor (full face coverage with multiple slits)
        visor_points = [
            (head_x + 3, head_y + 3), (head_x + 17, head_y + 3),
            (head_x + 18, head_y + 5), (head_x + 18, head_y + 9),
            (head_x + 17, head_y + 11), (head_x + 3, head_y + 11),
            (head_x + 2, head_y + 9), (head_x + 2, head_y + 5)
        ]
        pygame.draw.polygon(surface, (80, 80, 100), visor_points)
        pygame.draw.polygon(surface, (120, 120, 140), [
            (head_x + 4, head_y + 4), (head_x + 16, head_y + 4),
            (head_x + 17, head_y + 6), (head_x + 17, head_y + 8),
            (head_x + 16, head_y + 10), (head_x + 4, head_y + 10),
            (head_x + 3, head_y + 8), (head_x + 3, head_y + 6)
        ])
        
        # Multiple visor slits for better visibility
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 4, head_y + 4, 2, 2))
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 7, head_y + 4, 2, 2))
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 10, head_y + 4, 2, 2))
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 13, head_y + 4, 2, 2))
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 4, head_y + 7, 2, 2))
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 7, head_y + 7, 2, 2))
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 10, head_y + 7, 2, 2))
        pygame.draw.rect(surface, (40, 40, 60), (head_x + 13, head_y + 7, 2, 2))
        
        # Chin guard (full face and chin coverage)
        chin_guard_points = [
            (head_x + 2, head_y + 11), (head_x + 18, head_y + 11),  # Top
            (head_x + 20, head_y + 13), (head_x + 20, head_y + 18),  # Right side
            (head_x + 18, head_y + 20), (head_x + 2, head_y + 20),   # Bottom
            (head_x, head_y + 18), (head_x, head_y + 13)             # Left side
        ]
        pygame.draw.polygon(surface, helmet_color, chin_guard_points)
        pygame.draw.polygon(surface, helmet_highlight, [
            (head_x + 4, head_y + 12), (head_x + 16, head_y + 12),
            (head_x + 18, head_y + 14), (head_x + 18, head_y + 17),
            (head_x + 16, head_y + 19), (head_x + 4, head_y + 19),
            (head_x + 2, head_y + 17), (head_x + 2, head_y + 14)
        ])
        pygame.draw.polygon(surface, helmet_shadow, [
            (head_x + 2, head_y + 11), (head_x, head_y + 13), (head_x, head_y + 18),
            (head_x + 2, head_y + 20), (head_x + 4, head_y + 20)
        ])
        
        # Chin guard breathing holes
        pygame.draw.circle(surface, (60, 60, 80), (head_x + 6, head_y + 15), 1)
        pygame.draw.circle(surface, (60, 60, 80), (head_x + 14, head_y + 15), 1)
        pygame.draw.circle(surface, (60, 60, 80), (head_x + 6, head_y + 17), 1)
        pygame.draw.circle(surface, (60, 60, 80), (head_x + 14, head_y + 17), 1)
        
        # Helmet flares (larger decorative metal pieces)
        flare_color = (180, 180, 200)
        flare_highlight = (220, 220, 240)
        
        # Left flare (larger)
        left_flare_points = [
            (head_x, head_y + 4), (head_x - 6, head_y + 1), (head_x - 8, head_y + 4),
            (head_x - 6, head_y + 7), (head_x, head_y + 10)
        ]
        pygame.draw.polygon(surface, flare_color, left_flare_points)
        pygame.draw.polygon(surface, flare_highlight, [
            (head_x, head_y + 4), (head_x - 3, head_y + 2), (head_x - 6, head_y + 4),
            (head_x - 3, head_y + 7), (head_x, head_y + 9)
        ])
        
        # Right flare (larger)
        right_flare_points = [
            (head_x + 20, head_y + 4), (head_x + 26, head_y + 1), (head_x + 28, head_y + 4),
            (head_x + 26, head_y + 7), (head_x + 20, head_y + 10)
        ]
        pygame.draw.polygon(surface, flare_color, right_flare_points)
        pygame.draw.polygon(surface, flare_highlight, [
            (head_x + 20, head_y + 4), (head_x + 23, head_y + 2), (head_x + 26, head_y + 4),
            (head_x + 23, head_y + 7), (head_x + 20, head_y + 9)
        ])
        
        # Helmet details (extensive rivets and engravings)
        for i in range(5):
            rivet_x = head_x + 3 + i * 4
            rivet_y = head_y + 2
            pygame.draw.circle(surface, helmet_detail, (rivet_x, rivet_y), 1)
            pygame.draw.circle(surface, helmet_highlight, (rivet_x, rivet_y), 1, 1)
        
        # Additional rivets on sides
        for i in range(3):
            rivet_x = head_x + 2
            rivet_y = head_y + 4 + i * 4
            pygame.draw.circle(surface, helmet_detail, (rivet_x, rivet_y), 1)
            pygame.draw.circle(surface, helmet_highlight, (rivet_x, rivet_y), 1, 1)
            
            rivet_x = head_x + 18
            pygame.draw.circle(surface, helmet_detail, (rivet_x, rivet_y), 1)
            pygame.draw.circle(surface, helmet_highlight, (rivet_x, rivet_y), 1, 1)
        
        # Dragon scale pattern on helmet (more extensive)
        for i in range(3):
            for j in range(3):
                scale_x = head_x + 5 + i * 5
                scale_y = head_y + 5 + j * 3
                pygame.draw.ellipse(surface, helmet_detail, (scale_x, scale_y, 3, 2))
                pygame.draw.ellipse(surface, helmet_highlight, (scale_x + 1, scale_y + 1, 1, 1))
        
        # Eyes (glowing through visor)
        pygame.draw.circle(surface, (255, 255, 0), (head_x + 6, head_y + 6), 2)
        pygame.draw.circle(surface, (255, 255, 0), (head_x + 10, head_y + 6), 2)
        pygame.draw.circle(surface, (255, 255, 255), (head_x + 5, head_y + 5), 1)
        pygame.draw.circle(surface, (255, 255, 255), (head_x + 9, head_y + 5), 1)
        
        # Dragon Knight arms with armor
        arm_color = (160, 160, 180)
        arm_highlight = (200, 200, 220)
        arm_shadow = (120, 120, 140)
        
        # Left arm
        pygame.draw.rect(surface, arm_color, (guard_x + 2, guard_y + 20, 6, 12))
        pygame.draw.rect(surface, arm_highlight, (guard_x + 3, guard_y + 21, 4, 6))
        pygame.draw.rect(surface, arm_shadow, (guard_x + 2, guard_y + 20, 2, 12))
        
        # Right arm
        pygame.draw.rect(surface, arm_color, (guard_x + guard_w - 8, guard_y + 20, 6, 12))
        pygame.draw.rect(surface, arm_highlight, (guard_x + guard_w - 9, guard_y + 21, 4, 6))
        pygame.draw.rect(surface, arm_shadow, (guard_x + guard_w - 8, guard_y + 20, 2, 12))
        
        # Dragon Knight legs with armor
        leg_color = (160, 160, 180)
        leg_highlight = (200, 200, 220)
        leg_shadow = (120, 120, 140)
        
        # Left leg
        pygame.draw.rect(surface, leg_color, (guard_x + 6, guard_y + 32, 8, 12))
        pygame.draw.rect(surface, leg_highlight, (guard_x + 7, guard_y + 33, 6, 6))
        pygame.draw.rect(surface, leg_shadow, (guard_x + 6, guard_y + 32, 2, 12))
        
        # Right leg
        pygame.draw.rect(surface, leg_color, (guard_x + guard_w - 14, guard_y + 32, 8, 12))
        pygame.draw.rect(surface, leg_highlight, (guard_x + guard_w - 15, guard_y + 33, 6, 6))
        pygame.draw.rect(surface, leg_shadow, (guard_x + guard_w - 14, guard_y + 32, 2, 12))
        
        # Dragon Knight shield (detailed)
        shield_x = guard_x - 25
        shield_y = guard_y + 15
        shield_color = (140, 140, 160)
        shield_highlight = (180, 180, 200)
        shield_shadow = (100, 100, 120)
        shield_detail = (80, 80, 100)
        
        # Shield base
        pygame.draw.ellipse(surface, shield_color, (shield_x, shield_y, 20, 30))
        # Shield highlight
        pygame.draw.ellipse(surface, shield_highlight, (shield_x + 2, shield_y + 2, 16, 26))
        # Shield shadow
        pygame.draw.ellipse(surface, shield_shadow, (shield_x, shield_y, 8, 30))
        
        # Shield border
        pygame.draw.ellipse(surface, shield_detail, (shield_x, shield_y, 20, 30), 2)
        
        # Dragon emblem on shield
        dragon_center_x = shield_x + 10
        dragon_center_y = shield_y + 15
        # Dragon head
        pygame.draw.circle(surface, shield_detail, (dragon_center_x, dragon_center_y - 5), 3)
        # Dragon body
        pygame.draw.ellipse(surface, shield_detail, (dragon_center_x - 2, dragon_center_y, 4, 8))
        # Dragon wings
        pygame.draw.polygon(surface, shield_detail, 
                          [(dragon_center_x - 2, dragon_center_y + 2), (dragon_center_x - 6, dragon_center_y - 2), (dragon_center_x - 4, dragon_center_y + 4)])
        pygame.draw.polygon(surface, shield_detail, 
                          [(dragon_center_x + 2, dragon_center_y + 2), (dragon_center_x + 6, dragon_center_y - 2), (dragon_center_x + 4, dragon_center_y + 4)])
        
        # Shield handle
        pygame.draw.rect(surface, (80, 60, 40), (shield_x + 8, shield_y + 12, 4, 6))
        
        # Dragon Knight sword (silver with dragon hilt)
        sword_x = guard_x + guard_w + 5
        sword_y = guard_y + guard_h//2
        
        # Sword handle (dragon-themed)
        handle_color = (120, 80, 40)
        handle_highlight = (160, 120, 80)
        pygame.draw.rect(surface, handle_color, (sword_x, sword_y - 2, 6, 8))
        pygame.draw.rect(surface, handle_highlight, (sword_x + 1, sword_y - 1, 4, 6))
        
        # Dragon hilt detail
        pygame.draw.circle(surface, (100, 60, 20), (sword_x + 3, sword_y + 2), 2)
        pygame.draw.circle(surface, (140, 100, 60), (sword_x + 3, sword_y + 2), 1)
        
        # Sword blade (silver)
        blade_color = (220, 220, 240)
        blade_highlight = (255, 255, 255)
        blade_shadow = (180, 180, 200)
        
        pygame.draw.rect(surface, blade_color, (sword_x + 6, sword_y - 3, 25, 6))
        pygame.draw.rect(surface, blade_highlight, (sword_x + 7, sword_y - 2, 23, 4))
        pygame.draw.rect(surface, blade_shadow, (sword_x + 6, sword_y - 3, 2, 6))
        
        # Sword tip
        pygame.draw.polygon(surface, blade_color, 
                          [(sword_x + 31, sword_y - 3), (sword_x + 35, sword_y), (sword_x + 31, sword_y + 3)])
        pygame.draw.polygon(surface, blade_highlight, 
                          [(sword_x + 31, sword_y - 3), (sword_x + 33, sword_y - 1), (sword_x + 31, sword_y + 1)])
        
        # Sword guard (dragon wings)
        guard_color = (160, 120, 80)
        guard_highlight = (200, 160, 120)
        
        # Left wing of guard
        pygame.draw.polygon(surface, guard_color, 
                          [(sword_x + 4, sword_y - 4), (sword_x, sword_y - 6), (sword_x + 2, sword_y - 2)])
        pygame.draw.polygon(surface, guard_highlight, 
                          [(sword_x + 4, sword_y - 4), (sword_x + 1, sword_y - 5), (sword_x + 3, sword_y - 3)])
        
        # Right wing of guard
        pygame.draw.polygon(surface, guard_color, 
                          [(sword_x + 4, sword_y + 4), (sword_x, sword_y + 6), (sword_x + 2, sword_y + 2)])
        pygame.draw.polygon(surface, guard_highlight, 
                          [(sword_x + 4, sword_y + 4), (sword_x + 1, sword_y + 5), (sword_x + 3, sword_y + 3)])
        
        # Draw dialogue box
        if self.cutscene_phase == 1:
            # Safety check to prevent index out of bounds
            dialogue_index = min(self.guard["current_dialogue"], len(self.guard["dialogue"]) - 1)
            dialogue = self.guard["dialogue"][dialogue_index]
            
            # Dialogue box background
            box_x = 200
            box_y = 500
            box_w = 600
            box_h = 100
            
            # Box shadow
            pygame.draw.rect(surface, (20, 20, 20), (box_x + 3, box_y + 3, box_w, box_h))
            # Box base
            pygame.draw.rect(surface, (40, 40, 60), (box_x, box_y, box_w, box_h))
            pygame.draw.rect(surface, (80, 80, 120), (box_x, box_y, box_w, box_h), 3)
            
            # Dialogue text
            try:
                text = font_small.render(dialogue, True, (255, 255, 255))
                text_rect = text.get_rect(center=(box_x + box_w//2, box_y + box_h//2))
                surface.blit(text, text_rect)
            except:
                # Fallback if font not available
                pass
            
            # Dragon Knight name
            try:
                name_text = font_tiny.render("Sir Marcus - Dragon Knight", True, (255, 215, 0))
                name_rect = name_text.get_rect(center=(box_x + box_w//2, box_y + 20))
                surface.blit(name_text, name_rect)
            except:
                pass
        
        # Draw "Press SPACE to continue" prompt
        if self.cutscene_phase == 1 and self.cutscene_timer > 60:
            try:
                prompt_text = font_tiny.render("Press SPACE to continue", True, (200, 200, 200))
                prompt_rect = prompt_text.get_rect(center=(500, 620))
                surface.blit(prompt_text, prompt_rect)
            except:
                pass

# ============================================================================
# WORLD MAP CLASS - Manages the 3x3 world grid and camera system
# ============================================================================
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

# ============================================================================
# PARTICLE SYSTEM CLASSES - Visual effects and particle management
# ============================================================================
class Particle:
    """
    Individual particle for visual effects like explosions, magic, and environmental effects.
    """
    def __init__(self, x, y, color, velocity, size, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.size = size
        self.lifetime = lifetime
        self.age = 0
        
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.age += 1
        return self.age >= self.lifetime
        
    def draw(self, surface):
        alpha = 255 * (1 - self.age/self.lifetime)
        color = (*self.color[:3], int(alpha))
        radius = int(self.size * (1 - self.age/self.lifetime))
        if radius > 0:
            # Use regular pygame circle drawing instead of gfxdraw
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), radius)

class ParticleSystem:
    """
    Manages all particles in the game, including explosions, magic effects, and environmental particles.
    Provides methods for creating various types of particle effects.
    """
    def __init__(self):
        self.particles = []
        
    def add_particle(self, x, y, color, velocity, size, lifetime):
        self.particles.append(Particle(x, y, color, velocity, size, lifetime))
        
    def add_explosion(self, x, y, color, count=20, size_range=(2, 5), speed_range=(1, 3), lifetime_range=(20, 40)):
        for _ in range(count):
            angle = random.uniform(0, math.pi*2)
            speed = random.uniform(*speed_range)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            size = random.uniform(*size_range)
            lifetime = random.randint(*lifetime_range)
            self.add_particle(x, y, color, velocity, size, lifetime)
            
    def add_beam(self, x1, y1, x2, y2, color, width=3, particle_count=10, speed=2):
        dx = x2 - x1
        dy = y2 - y1
        distance = math.sqrt(dx*dx + dy*dy)
        steps = max(1, int(distance / 5))
        
        for i in range(steps):
            px = x1 + (dx * i/steps)
            py = y1 + (dy * i/steps)
            for _ in range(particle_count):
                angle = random.uniform(0, math.pi*2)
                velocity = (math.cos(angle) * 0.2, math.sin(angle) * 0.2)
                self.add_particle(px, py, color, velocity, width, 15)
    
    def update(self):
        self.particles = [p for p in self.particles if not p.update()]
        
    def draw(self, surface, world_map=None):
        for particle in self.particles:
            if world_map:
                # Convert world coordinates to screen coordinates
                screen_x, screen_y = world_map.world_to_screen(particle.x, particle.y)
                # Temporarily set particle position for drawing
                original_x, original_y = particle.x, particle.y
                particle.x, particle.y = screen_x, screen_y
                particle.draw(surface)
                particle.x, particle.y = original_x, original_y
            else:
                particle.draw(surface)

# ============================================================================
# UI COMPONENTS - User interface elements
# ============================================================================
class Button:
    """
    Interactive button for menus and UI elements.
    Handles hover effects and click detection.
    """
    def __init__(self, x, y, width, height, text, color=UI_BORDER, hover_color=(255, 215, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.text_surf = font_medium.render(text, True, TEXT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.glow = 0
        self.glow_dir = 1
        self.selected = False
        
    def draw(self, surface):
        if self.glow > 0 or self.selected:
            glow_radius = max(self.glow, 8 if self.selected else 0)
            glow_surf = pygame.Surface((self.rect.width + glow_radius*2, self.rect.height + glow_radius*2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*self.current_color[:3], 50), glow_surf.get_rect(), border_radius=12)
            surface.blit(glow_surf, (self.rect.x - glow_radius, self.rect.y - glow_radius))
        
        pygame.draw.rect(surface, UI_BG, self.rect, border_radius=8)
        
        border_color = (255, 215, 0) if self.selected else self.current_color
        border_width = 4 if self.selected else 3
        pygame.draw.rect(surface, border_color, self.rect, border_width, border_radius=8)
        
        surface.blit(self.text_surf, self.text_rect)
        
    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
            self.glow = min(self.glow + 2, 10)
            return True
        else:
            self.current_color = self.color
            self.glow = max(self.glow - 1, 0)
        return False
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

# ============================================================================
# CHARACTER SYSTEM - Player character with stats, abilities, and progression
# ============================================================================
class Character:
    """
    Player character with RPG stats, abilities, and progression system.
    Supports multiple character classes: Warrior, Mage, Rogue
    """
    def __init__(self, char_type="Warrior"):
        self.type = char_type
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        
        if char_type == "Warrior":
            self.max_health = 120
            self.max_mana = 50
            self.strength = 15
            self.defense = 10
            self.speed = 7
        elif char_type == "Mage":
            self.max_health = 80
            self.max_mana = 120
            self.strength = 8
            self.defense = 6
            self.speed = 8
        else:  # Rogue
            self.max_health = 100
            self.max_mana = 70
            self.strength = 12
            self.defense = 8
            self.speed = 12
            
        self.health = self.max_health
        self.mana = self.max_mana
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.attack_cooldown = 0
        self.kills = 0
        self.items_collected = 0
        self.animation_offset = 0
        self.attack_animation = 0
        self.hit_animation = 0
        self.last_boss_level = 0  # Track the last boss level encountered
        self.just_leveled_up = False
        self.boss_cooldown = False  # Prevent boss battles during cooldown
        
    def move(self, dx, dy):
        new_x = self.x + dx * GRID_SIZE
        new_y = self.y + dy * GRID_SIZE
        
        # Check world boundaries (0 to WORLD_WIDTH/HEIGHT)
        if 0 <= new_x < WORLD_WIDTH:
            self.x = new_x
        if 0 <= new_y < WORLD_HEIGHT:
            self.y = new_y
            
    def update_animation(self):
        self.animation_offset = math.sin(pygame.time.get_ticks() * 0.005) * 2
        
        if self.attack_animation > 0:
            self.attack_animation -= 1
            
        if self.hit_animation > 0:
            self.hit_animation -= 1
            
    def draw(self, surface):
        offset_x = self.animation_offset
        offset_y = self.animation_offset
        
        if self.attack_animation > 0:
            if self.type == "Warrior":
                offset_x = 5 * math.sin(self.attack_animation * 0.2)
            elif self.type == "Mage":
                offset_y -= 5 * (1 - self.attack_animation / 10)
            else:  # Rogue
                offset_x = -5 * math.sin(self.attack_animation * 0.2)
                
        if self.hit_animation > 0:
            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)
        
        x = self.x + offset_x
        y = self.y + offset_y
        
        if self.type == "Warrior":
            # Draw shadow first
            pygame.draw.ellipse(surface, (0, 0, 0), (x + 2, y + 45, PLAYER_SIZE - 4, 8))
            
            # Paladin - Noble and righteous
            # Torso (armored and noble)
            torso_color = (192, 192, 192)  # Silver armor
            torso_highlight = (220, 220, 220)  # Bright silver
            torso_shadow = (160, 160, 160)  # Dark silver
            
            # Main torso (armored)
            torso_points = [
                (x + 6, y + 10), (x + PLAYER_SIZE - 6, y + 10),  # Top
                (x + PLAYER_SIZE - 4, y + 18), (x + PLAYER_SIZE - 2, y + 30),  # Right curve
                (x + PLAYER_SIZE - 4, y + 38), (x + 4, y + 38),  # Bottom
                (x + 2, y + 30), (x + 4, y + 18)  # Left curve
            ]
            pygame.draw.polygon(surface, torso_color, torso_points)
            pygame.draw.polygon(surface, torso_highlight, [
                (x + 8, y + 12), (x + PLAYER_SIZE - 8, y + 12),
                (x + PLAYER_SIZE - 10, y + 20), (x + 10, y + 20)
            ])
            pygame.draw.polygon(surface, torso_shadow, [
                (x + 6, y + 10), (x + 4, y + 18), (x + 2, y + 30),
                (x + 4, y + 38), (x + 6, y + 38)
            ])
            
            # Armor plates and details
            # Chest plate
            pygame.draw.ellipse(surface, (160, 160, 160), (x + 10, y + 14, PLAYER_SIZE - 20, 12))
            pygame.draw.ellipse(surface, (180, 180, 180), (x + 11, y + 15, PLAYER_SIZE - 22, 10))
            # Armor trim
            pygame.draw.ellipse(surface, (139, 69, 19), (x + 8, y + 8, PLAYER_SIZE - 16, 8))
            pygame.draw.ellipse(surface, (160, 82, 45), (x + 10, y + 9, PLAYER_SIZE - 20, 6))
            # Belt
            pygame.draw.ellipse(surface, (139, 69, 19), (x + 6, y + 32, PLAYER_SIZE - 12, 6))
            pygame.draw.ellipse(surface, (160, 82, 45), (x + 8, y + 33, PLAYER_SIZE - 16, 4))
            
            # Head (noble and righteous)
            head_center_x = x + PLAYER_SIZE // 2
            head_center_y = y + 8
            # Head shadow
            pygame.draw.circle(surface, (180, 140, 100), (head_center_x + 1, head_center_y + 1), 10)
            # Head base (noble)
            pygame.draw.ellipse(surface, (240, 200, 150), (head_center_x - 10, head_center_y - 8, 20, 22))
            # Head highlight
            pygame.draw.ellipse(surface, (255, 220, 180), (head_center_x - 8, head_center_y - 6, 16, 18))
            # Head outline
            pygame.draw.ellipse(surface, (200, 150, 100), (head_center_x - 10, head_center_y - 8, 20, 22), 1)
            
            # Noble hair (flowing and well-groomed)
            hair_color = (139, 69, 19)  # Brown
            hair_highlight = (160, 82, 45)
            # Hair base
            pygame.draw.ellipse(surface, hair_color, (head_center_x - 8, head_center_y - 6, 16, 8))
            pygame.draw.ellipse(surface, hair_highlight, (head_center_x - 6, head_center_y - 5, 12, 6))
            # Flowing hair strands
            hair_strands = [
                (head_center_x - 6, head_center_y - 6), (head_center_x - 4, head_center_y - 10),
                (head_center_x - 2, head_center_y - 8), (head_center_x, head_center_y - 12),
                (head_center_x + 2, head_center_y - 10), (head_center_x + 4, head_center_y - 12),
                (head_center_x + 6, head_center_y - 8)
            ]
            for i in range(len(hair_strands) - 1):
                pygame.draw.line(surface, hair_color, hair_strands[i], hair_strands[i+1], 2)
            
            # Noble eyes (determined and righteous)
            pygame.draw.ellipse(surface, (50, 50, 50), (head_center_x - 6, head_center_y - 2, 4, 3))
            pygame.draw.ellipse(surface, (50, 50, 50), (head_center_x + 2, head_center_y - 2, 4, 3))
            pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x - 5, head_center_y - 3, 2, 2))
            pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x + 3, head_center_y - 3, 2, 2))
            pygame.draw.circle(surface, (0, 150, 255), (head_center_x - 4, head_center_y - 1), 1)  # Blue eyes
            pygame.draw.circle(surface, (0, 150, 255), (head_center_x + 4, head_center_y - 1), 1)
            
            # Noble features
            pygame.draw.ellipse(surface, (220, 180, 140), (head_center_x - 1, head_center_y + 1, 2, 3))  # Nose
            
            # Noble beard (well-groomed)
            beard_points = [
                (head_center_x - 4, head_center_y + 4), (head_center_x - 6, head_center_y + 8),
                (head_center_x - 4, head_center_y + 12), (head_center_x, head_center_y + 14),
                (head_center_x + 4, head_center_y + 12), (head_center_x + 6, head_center_y + 8),
                (head_center_x + 4, head_center_y + 4)
            ]
            pygame.draw.polygon(surface, hair_color, beard_points)
            pygame.draw.polygon(surface, hair_highlight, [
                (head_center_x - 2, head_center_y + 6), (head_center_x - 4, head_center_y + 10),
                (head_center_x, head_center_y + 12), (head_center_x + 4, head_center_y + 10),
                (head_center_x + 2, head_center_y + 6)
            ])
            
            # Arms (armored)
            arm_color = (192, 192, 192)  # Silver armor
            arm_highlight = (220, 220, 220)  # Bright silver
            arm_shadow = (160, 160, 160)  # Dark silver
            
            # Left arm (armored)
            left_arm_points = [
                (x + 2, y + 16), (x + 10, y + 16), (x + 12, y + 20), (x + 10, y + 32), (x + 2, y + 32)
            ]
            pygame.draw.polygon(surface, arm_color, left_arm_points)
            pygame.draw.polygon(surface, arm_highlight, [(x + 3, y + 17), (x + 9, y + 17), (x + 10, y + 20), (x + 9, y + 30), (x + 3, y + 30)])
            # Armor details
            pygame.draw.ellipse(surface, (160, 160, 160), (x + 3, y + 20, 8, 6))
            pygame.draw.ellipse(surface, (180, 180, 180), (x + 4, y + 21, 6, 4))
            
            # Right arm (armored)
            right_arm_points = [
                (x + PLAYER_SIZE - 2, y + 16), (x + PLAYER_SIZE - 10, y + 16), 
                (x + PLAYER_SIZE - 12, y + 20), (x + PLAYER_SIZE - 10, y + 32), (x + PLAYER_SIZE - 2, y + 32)
            ]
            pygame.draw.polygon(surface, arm_color, right_arm_points)
            pygame.draw.polygon(surface, arm_highlight, [(x + PLAYER_SIZE - 3, y + 17), (x + PLAYER_SIZE - 9, y + 17), (x + PLAYER_SIZE - 10, y + 20), (x + PLAYER_SIZE - 9, y + 30), (x + PLAYER_SIZE - 3, y + 30)])
            # Armor details
            pygame.draw.ellipse(surface, (160, 160, 160), (x + PLAYER_SIZE - 11, y + 20, 8, 6))
            pygame.draw.ellipse(surface, (180, 180, 180), (x + PLAYER_SIZE - 12, y + 21, 6, 4))
            
            # Holy Sword (noble and righteous)
            sword_offset = 0
            if self.attack_animation > 0:
                sword_offset = -12 * (1 - self.attack_animation / 10)
            
            # Sword handle (ornate)
            pygame.draw.rect(surface, (139, 69, 19), (x + 32 + sword_offset, y + 16, 4, 10))
            pygame.draw.rect(surface, (160, 82, 45), (x + 33 + sword_offset, y + 17, 2, 8))
            # Handle grip
            pygame.draw.rect(surface, (101, 67, 33), (x + 33 + sword_offset, y + 20, 2, 4))
            pygame.draw.rect(surface, (139, 69, 19), (x + 33 + sword_offset, y + 21, 2, 2))
            
            # Sword guard (ornate cross)
            guard_points = [
                (x + 28 + sword_offset, y + 18), (x + 40 + sword_offset, y + 18),
                (x + 39 + sword_offset, y + 20), (x + 29 + sword_offset, y + 20)
            ]
            pygame.draw.polygon(surface, (192, 192, 192), guard_points)
            pygame.draw.polygon(surface, (220, 220, 220), [
                (x + 29 + sword_offset, y + 18), (x + 39 + sword_offset, y + 18),
                (x + 38 + sword_offset, y + 19), (x + 30 + sword_offset, y + 19)
            ])
            # Cross detail
            pygame.draw.rect(surface, (160, 160, 160), (x + 32 + sword_offset, y + 16, 4, 4))
            pygame.draw.rect(surface, (180, 180, 180), (x + 33 + sword_offset, y + 17, 2, 2))
            
            # Sword blade (holy and gleaming)
            blade_points = [
                (x + 30 + sword_offset, y + 12), (x + 34 + sword_offset, y + 12),
                (x + 35 + sword_offset, y + 18), (x + 34 + sword_offset, y + 24),
                (x + 30 + sword_offset, y + 24)
            ]
            pygame.draw.polygon(surface, (220, 220, 240), blade_points)
            pygame.draw.polygon(surface, (180, 180, 200), blade_points, 1)
            # Blade edge
            pygame.draw.line(surface, (255, 255, 255), (x + 30 + sword_offset, y + 12), (x + 34 + sword_offset, y + 12), 2)
            
            # Sword tip (pointed)
            pygame.draw.polygon(surface, (200, 200, 220), [
                (x + 30 + sword_offset, y + 12), (x + 36 + sword_offset, y + 6),
                (x + 32 + sword_offset, y + 12)
            ])
            pygame.draw.polygon(surface, (220, 220, 240), [
                (x + 30 + sword_offset, y + 12), (x + 34 + sword_offset, y + 8),
                (x + 32 + sword_offset, y + 12)
            ])
            
            # Holy glow effect
            glow_points = [
                (x + 32 + sword_offset, y + 8), (x + 34 + sword_offset, y + 8),
                (x + 35 + sword_offset, y + 10), (x + 34 + sword_offset, y + 12),
                (x + 32 + sword_offset, y + 12)
            ]
            pygame.draw.polygon(surface, (255, 255, 200), glow_points)
            pygame.draw.polygon(surface, (255, 255, 255), [
                (x + 32 + sword_offset, y + 9), (x + 34 + sword_offset, y + 9),
                (x + 34 + sword_offset, y + 11), (x + 32 + sword_offset, y + 11)
            ])
            
            # Legs (armored)
            leg_color = (192, 192, 192)  # Silver armor
            leg_highlight = (220, 220, 220)  # Bright silver
            leg_shadow = (160, 160, 160)  # Dark silver
            
            # Left leg (armored)
            left_leg_points = [
                (x + 6, y + 38), (x + 16, y + 38), (x + 17, y + 42), (x + 16, y + 50), (x + 6, y + 50)
            ]
            pygame.draw.polygon(surface, leg_color, left_leg_points)
            pygame.draw.polygon(surface, leg_highlight, [(x + 7, y + 39), (x + 15, y + 39), (x + 16, y + 42), (x + 15, y + 48), (x + 7, y + 48)])
            # Armor details
            pygame.draw.ellipse(surface, (160, 160, 160), (x + 7, y + 44, 10, 6))
            pygame.draw.ellipse(surface, (180, 180, 180), (x + 8, y + 45, 8, 4))
            
            # Right leg (armored)
            right_leg_points = [
                (x + PLAYER_SIZE - 6, y + 38), (x + PLAYER_SIZE - 16, y + 38), 
                (x + PLAYER_SIZE - 17, y + 42), (x + PLAYER_SIZE - 16, y + 50), (x + PLAYER_SIZE - 6, y + 50)
            ]
            pygame.draw.polygon(surface, leg_color, right_leg_points)
            pygame.draw.polygon(surface, leg_highlight, [(x + PLAYER_SIZE - 7, y + 39), (x + PLAYER_SIZE - 15, y + 39), (x + PLAYER_SIZE - 16, y + 42), (x + PLAYER_SIZE - 15, y + 48), (x + PLAYER_SIZE - 7, y + 48)])
            # Armor details
            pygame.draw.ellipse(surface, (160, 160, 160), (x + PLAYER_SIZE - 17, y + 44, 10, 6))
            pygame.draw.ellipse(surface, (180, 180, 180), (x + PLAYER_SIZE - 18, y + 45, 8, 4))
            
        elif self.type == "Mage":
            # Draw shadow first
            pygame.draw.ellipse(surface, (0, 0, 0), (x + 2, y + 50, PLAYER_SIZE - 4, 8))
            
            # Mystical Elementalist - Ethereal and otherworldly
            # Robe (flowing and ethereal)
            robe_color = (75, 0, 130)  # Deep purple
            robe_highlight = (138, 43, 226)  # Bright purple
            robe_shadow = (47, 0, 82)  # Dark purple
            robe_detail = (147, 112, 219)  # Medium purple
            
            # Main robe (flowing and mystical)
            robe_points = [
                (x + 4, y + 16), (x + PLAYER_SIZE - 4, y + 16),  # Top
                (x + PLAYER_SIZE - 2, y + 20), (x + PLAYER_SIZE, y + 28),  # Right curve
                (x + PLAYER_SIZE - 2, y + 36), (x + 2, y + 36),  # Bottom
                (x, y + 28), (x + 2, y + 20)  # Left curve
            ]
            pygame.draw.polygon(surface, robe_color, robe_points)
            pygame.draw.polygon(surface, robe_highlight, [
                (x + 6, y + 18), (x + PLAYER_SIZE - 6, y + 18),
                (x + PLAYER_SIZE - 8, y + 24), (x + 8, y + 24)
            ])
            pygame.draw.polygon(surface, robe_shadow, [
                (x + 4, y + 16), (x + 2, y + 20), (x, y + 28),
                (x + 2, y + 36), (x + 4, y + 36)
            ])
            
            # Mystical symbols and runes
            for i in range(4):
                rune_x = x + 10 + i * 6
                rune_y = y + 22
                # Star symbols
                star_points = [
                    (rune_x, rune_y - 2), (rune_x + 1, rune_y), (rune_x + 2, rune_y - 2),
                    (rune_x, rune_y + 2), (rune_x - 1, rune_y), (rune_x - 2, rune_y + 2)
                ]
                pygame.draw.polygon(surface, robe_detail, star_points)
                pygame.draw.polygon(surface, robe_highlight, [
                    (rune_x, rune_y - 1), (rune_x + 1, rune_y), (rune_x + 1, rune_y - 1),
                    (rune_x, rune_y + 1), (rune_x - 1, rune_y), (rune_x - 1, rune_y + 1)
                ])
            
            # Head (ethereal and mystical)
            head_center_x = x + PLAYER_SIZE // 2
            head_center_y = y + 10
            # Head shadow
            pygame.draw.circle(surface, (180, 140, 100), (head_center_x + 1, head_center_y + 1), 9)
            # Head base (slightly smaller, more ethereal)
            pygame.draw.ellipse(surface, (240, 200, 150), (head_center_x - 8, head_center_y - 6, 16, 18))
            # Head highlight
            pygame.draw.ellipse(surface, (255, 220, 180), (head_center_x - 6, head_center_y - 4, 12, 14))
            # Head outline
            pygame.draw.ellipse(surface, (200, 150, 100), (head_center_x - 8, head_center_y - 6, 16, 18), 1)
            
            # Mystical eyes (glowing)
            pygame.draw.ellipse(surface, (50, 50, 50), (head_center_x - 5, head_center_y - 2, 4, 3))
            pygame.draw.ellipse(surface, (50, 50, 50), (head_center_x + 1, head_center_y - 2, 4, 3))
            pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x - 4, head_center_y - 3, 2, 2))
            pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x + 2, head_center_y - 3, 2, 2))
            pygame.draw.circle(surface, (138, 43, 226), (head_center_x - 3, head_center_y - 1), 1)  # Purple eyes
            pygame.draw.circle(surface, (138, 43, 226), (head_center_x + 3, head_center_y - 1), 1)
            
            # Mystical hood (flowing)
            hood_color = (47, 0, 82)  # Dark purple
            hood_highlight = (75, 0, 130)
            hood_points = [
                (head_center_x - 8, head_center_y - 6), (head_center_x + 8, head_center_y - 6),
                (head_center_x + 10, head_center_y - 8), (head_center_x + 8, head_center_y - 12),
                (head_center_x + 4, head_center_y - 16), (head_center_x, head_center_y - 18),
                (head_center_x - 4, head_center_y - 16), (head_center_x - 8, head_center_y - 12),
                (head_center_x - 10, head_center_y - 8)
            ]
            pygame.draw.polygon(surface, hood_color, hood_points)
            pygame.draw.polygon(surface, hood_highlight, [
                (head_center_x - 6, head_center_y - 8), (head_center_x + 6, head_center_y - 8),
                (head_center_x + 8, head_center_y - 10), (head_center_x + 6, head_center_y - 14),
                (head_center_x + 2, head_center_y - 16), (head_center_x - 2, head_center_y - 16),
                (head_center_x - 6, head_center_y - 14), (head_center_x - 8, head_center_y - 10)
            ])
            
            # Mystical beard (ethereal wisps)
            beard_wisps = [
                (head_center_x - 4, head_center_y + 4), (head_center_x - 6, head_center_y + 8),
                (head_center_x - 4, head_center_y + 12), (head_center_x - 2, head_center_y + 16),
                (head_center_x + 2, head_center_y + 16), (head_center_x + 4, head_center_y + 12),
                (head_center_x + 6, head_center_y + 8), (head_center_x + 4, head_center_y + 4)
            ]
            # Draw individual wisps
            for i in range(len(beard_wisps) - 1):
                pygame.draw.line(surface, (147, 112, 219), beard_wisps[i], beard_wisps[i+1], 2)
            # Beard base
            pygame.draw.ellipse(surface, (138, 43, 226), (head_center_x - 4, head_center_y + 4, 8, 8))
            pygame.draw.ellipse(surface, (147, 112, 219), (head_center_x - 3, head_center_y + 5, 6, 6))
            
            # Arms with flowing sleeves
            hat_offset = 0
            if self.attack_animation > 0:
                hat_offset = -5 * (1 - self.attack_animation / 10)
            
            hat_color = (80, 40, 160)
            hat_highlight = (120, 60, 200)
            hat_shadow = (60, 30, 120)
            hat_detail = (100, 50, 180)
            
            # Hat base (curved)
            hat_base_points = [
                (head_center_x - 12, head_center_y - 5 + hat_offset),
                (head_center_x + 12, head_center_y - 5 + hat_offset),
                (head_center_x + 10, head_center_y - 2 + hat_offset),
                (head_center_x - 10, head_center_y - 2 + hat_offset)
            ]
            pygame.draw.polygon(surface, hat_color, hat_base_points)
            pygame.draw.polygon(surface, hat_highlight, [
                (head_center_x - 10, head_center_y - 4 + hat_offset),
                (head_center_x + 10, head_center_y - 4 + hat_offset),
                (head_center_x + 8, head_center_y - 2 + hat_offset),
                (head_center_x - 8, head_center_y - 2 + hat_offset)
            ])
            
            # Hat point (curved)
            hat_point_points = [
                (head_center_x, head_center_y - 15 + hat_offset),
                (head_center_x - 8, head_center_y - 5 + hat_offset),
                (head_center_x - 6, head_center_y - 8 + hat_offset),
                (head_center_x, head_center_y - 12 + hat_offset),
                (head_center_x + 6, head_center_y - 8 + hat_offset),
                (head_center_x + 8, head_center_y - 5 + hat_offset)
            ]
            pygame.draw.polygon(surface, hat_color, hat_point_points)
            pygame.draw.polygon(surface, hat_highlight, [
                (head_center_x, head_center_y - 15 + hat_offset),
                (head_center_x - 4, head_center_y - 8 + hat_offset),
                (head_center_x, head_center_y - 11 + hat_offset),
                (head_center_x + 4, head_center_y - 8 + hat_offset)
            ])
            
            # Hat details (stars)
            for i in range(3):
                star_x = head_center_x - 8 + i * 8
                star_y = head_center_y - 3 + hat_offset
                pygame.draw.circle(surface, hat_detail, (star_x, star_y), 1)
            
            # Staff with enhanced magical glow
            staff_top_offset = 0
            if self.attack_animation > 0:
                staff_top_offset = -10 * (1 - self.attack_animation / 10)
            
            # Staff shaft (curved)
            staff_points = [
                (x + 12, y + 12), (x + 14, y + 20), (x + 12, y + 28), (x + 10, y + 36), (x + 12, y + PLAYER_SIZE)
            ]
            for i in range(len(staff_points) - 1):
                pygame.draw.line(surface, (120, 80, 40), staff_points[i], staff_points[i + 1], 4)
            
            # Staff orb with enhanced glow effect
            orb_x = x + 12
            orb_y = y + 12 + staff_top_offset
            # Outer glow
            pygame.draw.circle(surface, (80, 80, 255), (orb_x, orb_y), 10)
            # Main orb
            pygame.draw.circle(surface, (100, 100, 255), (orb_x, orb_y), 8)
            pygame.draw.circle(surface, (150, 150, 255), (orb_x, orb_y), 5)
            pygame.draw.circle(surface, (200, 200, 255), (orb_x, orb_y), 2)
            # Orb highlight
            pygame.draw.circle(surface, (255, 255, 255), (orb_x - 2, orb_y - 2), 1)
            
            # Arms with flowing sleeves (mystical)
            arm_color = (75, 0, 130)  # Deep purple
            arm_highlight = (138, 43, 226)  # Bright purple
            arm_shadow = (47, 0, 82)  # Dark purple
            
            # Left arm (flowing sleeves)
            left_arm_points = [
                (x + 2, y + 20), (x + 10, y + 20), (x + 12, y + 24), (x + 10, y + 32), (x + 2, y + 32)
            ]
            pygame.draw.polygon(surface, arm_color, left_arm_points)
            pygame.draw.polygon(surface, arm_highlight, [(x + 3, y + 21), (x + 9, y + 21), (x + 10, y + 24), (x + 9, y + 30), (x + 3, y + 30)])
            # Sleeve details
            pygame.draw.ellipse(surface, robe_detail, (x + 3, y + 24, 8, 6))
            pygame.draw.ellipse(surface, robe_highlight, (x + 4, y + 25, 6, 4))
            
            # Right arm (flowing sleeves)
            right_arm_points = [
                (x + PLAYER_SIZE - 2, y + 20), (x + PLAYER_SIZE - 10, y + 20),
                (x + PLAYER_SIZE - 12, y + 24), (x + PLAYER_SIZE - 10, y + 32), (x + PLAYER_SIZE - 2, y + 32)
            ]
            pygame.draw.polygon(surface, arm_color, right_arm_points)
            pygame.draw.polygon(surface, arm_highlight, [(x + PLAYER_SIZE - 3, y + 21), (x + PLAYER_SIZE - 9, y + 21), (x + PLAYER_SIZE - 10, y + 24), (x + PLAYER_SIZE - 9, y + 30), (x + PLAYER_SIZE - 3, y + 30)])
            # Sleeve details
            pygame.draw.ellipse(surface, robe_detail, (x + PLAYER_SIZE - 11, y + 24, 8, 6))
            pygame.draw.ellipse(surface, robe_highlight, (x + PLAYER_SIZE - 12, y + 25, 6, 4))
            
            # Mystical Staff (ethereal)
            staff_offset = 0
            if self.attack_animation > 0:
                staff_offset = -15 * (1 - self.attack_animation / 10)
            
            # Staff shaft (mystical wood)
            staff_color = (139, 69, 19)  # Brown
            staff_highlight = (160, 82, 45)
            pygame.draw.rect(surface, staff_color, (x + 14 + staff_offset, y + 16, 4, 20))
            pygame.draw.rect(surface, staff_highlight, (x + 15 + staff_offset, y + 17, 2, 18))
            
            # Staff orb (mystical crystal)
            orb_x = x + 16 + staff_offset
            orb_y = y + 12
            # Outer glow
            pygame.draw.circle(surface, (138, 43, 226), (orb_x, orb_y), 8)
            # Main orb
            pygame.draw.circle(surface, (147, 112, 219), (orb_x, orb_y), 6)
            pygame.draw.circle(surface, (186, 85, 211), (orb_x, orb_y), 4)
            pygame.draw.circle(surface, (221, 160, 221), (orb_x, orb_y), 2)
            # Orb highlight
            pygame.draw.circle(surface, (255, 255, 255), (orb_x - 1, orb_y - 1), 1)
            
            # Mystical energy around orb
            for i in range(4):
                angle = i * 90
                energy_x = orb_x + int(6 * math.cos(math.radians(angle)))
                energy_y = orb_y + int(6 * math.sin(math.radians(angle)))
                pygame.draw.circle(surface, (138, 43, 226), (energy_x, energy_y), 2)
                pygame.draw.circle(surface, (147, 112, 219), (energy_x, energy_y), 1)
            
            # Legs with flowing robes
            leg_color = (75, 0, 130)  # Deep purple
            leg_highlight = (138, 43, 226)  # Bright purple
            leg_shadow = (47, 0, 82)  # Dark purple
            
            # Left leg (flowing robe)
            left_leg_points = [
                (x + 6, y + 36), (x + 14, y + 36), (x + 15, y + 40), (x + 14, y + 48), (x + 6, y + 48)
            ]
            pygame.draw.polygon(surface, leg_color, left_leg_points)
            pygame.draw.polygon(surface, leg_highlight, [(x + 7, y + 37), (x + 13, y + 37), (x + 14, y + 40), (x + 13, y + 46), (x + 7, y + 46)])
            # Robe hem details
            pygame.draw.ellipse(surface, robe_detail, (x + 7, y + 44, 8, 6))
            pygame.draw.ellipse(surface, robe_highlight, (x + 8, y + 45, 6, 4))
            
            # Right leg (flowing robe)
            right_leg_points = [
                (x + PLAYER_SIZE - 6, y + 36), (x + PLAYER_SIZE - 14, y + 36),
                (x + PLAYER_SIZE - 15, y + 40), (x + PLAYER_SIZE - 14, y + 48), (x + PLAYER_SIZE - 6, y + 48)
            ]
            pygame.draw.polygon(surface, leg_color, right_leg_points)
            pygame.draw.polygon(surface, leg_highlight, [(x + PLAYER_SIZE - 7, y + 37), (x + PLAYER_SIZE - 13, y + 37), (x + PLAYER_SIZE - 14, y + 40), (x + PLAYER_SIZE - 13, y + 46), (x + PLAYER_SIZE - 7, y + 46)])
            # Robe hem details
            pygame.draw.ellipse(surface, robe_detail, (x + PLAYER_SIZE - 15, y + 44, 8, 6))
            pygame.draw.ellipse(surface, robe_highlight, (x + PLAYER_SIZE - 16, y + 45, 6, 4))
            
        else:  # Rogue
            # Draw shadow first
            pygame.draw.ellipse(surface, (0, 0, 0), (x + 2, y + 50, PLAYER_SIZE - 4, 8))
            
            # Stealthy Assassin - Dark and mysterious
            # Leather armor (dark and sleek)
            armor_color = (40, 40, 40)  # Dark gray
            armor_highlight = (80, 80, 80)  # Light gray
            armor_shadow = (20, 20, 20)  # Very dark gray
            armor_detail = (60, 60, 60)  # Medium gray
            
            # Main armor (sleek and form-fitting)
            armor_points = [
                (x + 4, y + 16), (x + PLAYER_SIZE - 4, y + 16),  # Top
                (x + PLAYER_SIZE - 2, y + 20), (x + PLAYER_SIZE, y + 28),  # Right curve
                (x + PLAYER_SIZE - 2, y + 36), (x + 2, y + 36),  # Bottom
                (x, y + 28), (x + 2, y + 20)  # Left curve
            ]
            pygame.draw.polygon(surface, armor_color, armor_points)
            pygame.draw.polygon(surface, armor_highlight, [
                (x + 6, y + 18), (x + PLAYER_SIZE - 6, y + 18),
                (x + PLAYER_SIZE - 8, y + 24), (x + 8, y + 24)
            ])
            pygame.draw.polygon(surface, armor_shadow, [
                (x + 4, y + 16), (x + 2, y + 20), (x, y + 28),
                (x + 2, y + 36), (x + 4, y + 36)
            ])
            
            # Armor details (straps and buckles)
            for i in range(3):
                strap_x = x + 8 + i * 8
                strap_y = y + 22
                pygame.draw.rect(surface, armor_detail, (strap_x, strap_y, 4, 2))
                pygame.draw.rect(surface, armor_highlight, (strap_x + 1, strap_y + 1, 2, 1))
                # Buckles
                pygame.draw.rect(surface, (139, 69, 19), (strap_x + 1, strap_y - 1, 2, 4))
                pygame.draw.rect(surface, (160, 82, 45), (strap_x + 1, strap_y, 2, 2))
            
            # Leather straps and buckles
            for i in range(2):
                strap_x = x + 10 + i * 12
                strap_y = y + 22
                pygame.draw.rect(surface, armor_detail, (strap_x, strap_y, 8, 2))
                pygame.draw.rect(surface, (60, 60, 60), (strap_x + 2, strap_y, 4, 2))
            
            # Head (hidden and mysterious)
            head_center_x = x + PLAYER_SIZE // 2
            head_center_y = y + 10
            # Head shadow
            pygame.draw.circle(surface, (180, 140, 100), (head_center_x + 1, head_center_y + 1), 8)
            # Head base (smaller, more hidden)
            pygame.draw.ellipse(surface, (240, 200, 150), (head_center_x - 7, head_center_y - 5, 14, 16))
            # Head highlight
            pygame.draw.ellipse(surface, (255, 220, 180), (head_center_x - 5, head_center_y - 3, 10, 12))
            # Head outline
            pygame.draw.ellipse(surface, (200, 150, 100), (head_center_x - 7, head_center_y - 5, 14, 16), 1)
            
            # Dark hood (mysterious)
            hood_color = (20, 20, 20)  # Very dark
            hood_highlight = (40, 40, 40)
            hood_points = [
                (head_center_x - 8, head_center_y - 5), (head_center_x + 8, head_center_y - 5),
                (head_center_x + 10, head_center_y - 7), (head_center_x + 8, head_center_y - 11),
                (head_center_x + 4, head_center_y - 15), (head_center_x, head_center_y - 17),
                (head_center_x - 4, head_center_y - 15), (head_center_x - 8, head_center_y - 11),
                (head_center_x - 10, head_center_y - 7)
            ]
            pygame.draw.polygon(surface, hood_color, hood_points)
            pygame.draw.polygon(surface, hood_highlight, [
                (head_center_x - 6, head_center_y - 7), (head_center_x + 6, head_center_y - 7),
                (head_center_x + 8, head_center_y - 9), (head_center_x + 6, head_center_y - 13),
                (head_center_x + 2, head_center_y - 15), (head_center_x - 2, head_center_y - 15),
                (head_center_x - 6, head_center_y - 13), (head_center_x - 8, head_center_y - 9)
            ])
            
            # Hood stitching (stealth details)
            for i in range(3):
                stitch_x = head_center_x - 5 + i * 5
                stitch_y = head_center_y - 9
                pygame.draw.line(surface, (10, 10, 10), (stitch_x, stitch_y), (stitch_x, stitch_y + 2), 1)
            
            # Eyes (hidden in shadow, mysterious)
            pygame.draw.ellipse(surface, (10, 10, 10), (head_center_x - 4, head_center_y - 2, 5, 3))
            pygame.draw.ellipse(surface, (10, 10, 10), (head_center_x - 1, head_center_y - 2, 5, 3))
            pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x - 3, head_center_y - 3, 2, 2))
            pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x, head_center_y - 3, 2, 2))
            pygame.draw.circle(surface, (0, 255, 0), (head_center_x - 2, head_center_y - 1), 1)  # Green eyes
            pygame.draw.circle(surface, (0, 255, 0), (head_center_x + 1, head_center_y - 1), 1)
            pygame.draw.ellipse(surface, (255, 255, 0), (head_center_x - 1, head_center_y - 2, 4, 3))
            pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x - 2, head_center_y - 3, 2, 2))
            pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x, head_center_y - 3, 2, 2))
            pygame.draw.circle(surface, (0, 0, 0), (head_center_x - 1, head_center_y - 1), 1)
            pygame.draw.circle(surface, (0, 0, 0), (head_center_x + 1, head_center_y - 1), 1)
            
            # Daggers with enhanced detail
            dagger_offset = 0
            if self.attack_animation > 0:
                dagger_offset = -15 * (1 - self.attack_animation / 10)
            
            # Left dagger (curved blade)
            left_dagger_points = [
                (x + 18 + dagger_offset, y + 22), (x + 22 + dagger_offset, y + 18),
                (x + 25 + dagger_offset, y + 20), (x + 26 + dagger_offset, y + 22),
                (x + 25 + dagger_offset, y + 24), (x + 22 + dagger_offset, y + 22)
            ]
            pygame.draw.polygon(surface, (200, 200, 220), left_dagger_points)
            pygame.draw.polygon(surface, (180, 180, 200), left_dagger_points, 1)
            # Dagger handle (wrapped)
            pygame.draw.rect(surface, (120, 80, 40), (x + 20 + dagger_offset, y + 22, 4, 6))
            for i in range(2):
                pygame.draw.line(surface, (100, 60, 20), (x + 20 + dagger_offset, y + 24 + i*2), (x + 24 + dagger_offset, y + 24 + i*2), 1)
            
            # Right dagger (curved blade)
            right_dagger_points = [
                (x + PLAYER_SIZE - 18 - dagger_offset, y + 22), (x + PLAYER_SIZE - 22 - dagger_offset, y + 18),
                (x + PLAYER_SIZE - 25 - dagger_offset, y + 20), (x + PLAYER_SIZE - 26 - dagger_offset, y + 22),
                (x + PLAYER_SIZE - 25 - dagger_offset, y + 24), (x + PLAYER_SIZE - 22 - dagger_offset, y + 22)
            ]
            pygame.draw.polygon(surface, (200, 200, 220), right_dagger_points)
            pygame.draw.polygon(surface, (180, 180, 200), right_dagger_points, 1)
            # Dagger handle (wrapped)
            pygame.draw.rect(surface, (120, 80, 40), (x + PLAYER_SIZE - 24 - dagger_offset, y + 22, 4, 6))
            for i in range(2):
                pygame.draw.line(surface, (100, 60, 20), (x + PLAYER_SIZE - 24 - dagger_offset, y + 24 + i*2), (x + PLAYER_SIZE - 20 - dagger_offset, y + 24 + i*2), 1)
            
            # Arms with organic shape
            arm_color = (100, 0, 0)
            arm_highlight = (140, 0, 0)
            arm_shadow = (80, 0, 0)
            
            # Left arm (curved)
            left_arm_points = [
                (x + 2, y + 25), (x + 8, y + 25), (x + 10, y + 28), (x + 8, y + 35), (x + 2, y + 35)
            ]
            pygame.draw.polygon(surface, arm_color, left_arm_points)
            pygame.draw.polygon(surface, arm_highlight, [(x + 3, y + 26), (x + 7, y + 26), (x + 9, y + 28), (x + 7, y + 33), (x + 3, y + 33)])
            
            # Right arm (curved)
            right_arm_points = [
                (x + PLAYER_SIZE - 2, y + 25), (x + PLAYER_SIZE - 8, y + 25),
                (x + PLAYER_SIZE - 10, y + 28), (x + PLAYER_SIZE - 8, y + 35), (x + PLAYER_SIZE - 2, y + 35)
            ]
            pygame.draw.polygon(surface, arm_color, right_arm_points)
            pygame.draw.polygon(surface, arm_highlight, [(x + PLAYER_SIZE - 3, y + 26), (x + PLAYER_SIZE - 7, y + 26), (x + PLAYER_SIZE - 9, y + 28), (x + PLAYER_SIZE - 7, y + 33), (x + PLAYER_SIZE - 3, y + 33)])
            
            # Legs with organic shape
            leg_color = (80, 0, 0)
            leg_highlight = (120, 0, 0)
            leg_shadow = (60, 0, 0)
            
            # Left leg (curved)
            left_leg_points = [
                (x + 6, y + 35), (x + 14, y + 35), (x + 15, y + 38), (x + 14, y + 45), (x + 6, y + 45)
            ]
            pygame.draw.polygon(surface, leg_color, left_leg_points)
            pygame.draw.polygon(surface, leg_highlight, [(x + 7, y + 36), (x + 13, y + 36), (x + 14, y + 38), (x + 13, y + 43), (x + 7, y + 43)])
            
            # Right leg (curved)
            right_leg_points = [
                (x + PLAYER_SIZE - 14, y + 35), (x + PLAYER_SIZE - 6, y + 35),
                (x + PLAYER_SIZE - 5, y + 38), (x + PLAYER_SIZE - 6, y + 45), (x + PLAYER_SIZE - 14, y + 45)
            ]
            pygame.draw.polygon(surface, leg_color, right_leg_points)
            pygame.draw.polygon(surface, leg_highlight, [(x + PLAYER_SIZE - 13, y + 36), (x + PLAYER_SIZE - 7, y + 36), (x + PLAYER_SIZE - 6, y + 38), (x + PLAYER_SIZE - 7, y + 43), (x + PLAYER_SIZE - 13, y + 43)])
            
            # Belt with buckle
            pygame.draw.rect(surface, (40, 40, 40), (x + 2, y + 35, PLAYER_SIZE - 4, 3))
            # Belt buckle
            buckle_x = x + PLAYER_SIZE // 2 - 3
            buckle_y = y + 35
            pygame.draw.rect(surface, (80, 80, 80), (buckle_x, buckle_y, 6, 3))
            pygame.draw.rect(surface, (120, 120, 120), (buckle_x + 1, buckle_y + 1, 4, 1))
    
    def start_attack_animation(self):
        self.attack_animation = 10
        
    def start_hit_animation(self):
        self.hit_animation = 5
        
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense // 3)
        self.health -= actual_damage
        self.start_hit_animation()
        return actual_damage
    
    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_level:
            self.level_up()
            
    def level_up(self):
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
    
    def draw_stats(self, surface, x, y):
        pygame.draw.rect(surface, (20, 20, 30), (x, y, 200, 25), border_radius=3)
        health_width = 196 * (self.health / self.max_health)
        pygame.draw.rect(surface, HEALTH_COLOR, (x + 2, y + 2, health_width, 21), border_radius=3)
        health_text = font_small.render(f"HP: {self.health}/{self.max_health}", True, TEXT_COLOR)
        surface.blit(health_text, (x + 205, y + 4))
        
        pygame.draw.rect(surface, (20, 20, 30), (x, y + 30, 200, 20), border_radius=3)
        mana_width = 196 * (self.mana / self.max_mana)
        pygame.draw.rect(surface, MANA_COLOR, (x + 2, y + 32, mana_width, 16), border_radius=3)
        mana_text = font_small.render(f"MP: {self.mana}/{self.max_mana}", True, TEXT_COLOR)
        surface.blit(mana_text, (x + 205, y + 32))
        
        pygame.draw.rect(surface, (20, 20, 30), (x, y + 55, 200, 15), border_radius=3)
        exp_width = 196 * (self.exp / self.exp_to_level)
        pygame.draw.rect(surface, EXP_COLOR, (x + 2, y + 57, exp_width, 11), border_radius=3)
        exp_text = font_small.render(f"Level: {self.level}  Exp: {self.exp}/{self.exp_to_level}", True, TEXT_COLOR)
        surface.blit(exp_text, (x, y + 75))
        
        stats_text = font_small.render(f"Str: {self.strength}  Def: {self.defense}  Spd: {self.speed}", True, TEXT_COLOR)
        surface.blit(stats_text, (x, y + 100))

# ============================================================================
# ENEMY SYSTEM - Various enemy types with AI and combat abilities
# ============================================================================
class Enemy:
    """
    Base enemy class with AI behavior, combat abilities, and progression scaling.
    Different enemy types have unique abilities and visual appearances.
    """
    def __init__(self, player_level):
        self.size = ENEMY_SIZE
        # Enemies will be positioned by the spawn system
        self.x = 0
        self.y = 0
        self.enemy_type = random.choice(["fiery", "shadow", "ice"])
        
        # Generate enemy name based on type
        if self.enemy_type == "fiery":
            names = ["Fire Imp", "Lava Sprite", "Magma Beast", "Inferno Hound", "Blaze Fiend"]
        elif self.enemy_type == "shadow":
            names = ["Dark Shade", "Night Phantom", "Void Walker", "Gloom Stalker", "Shadow Fiend"]
        else:  # ice
            names = ["Frost Sprite", "Ice Golem", "Blizzard Elemental", "Frozen Wraith", "Chill Specter"]
        self.name = random.choice(names)
        
        self.health = random.randint(20, 30) + player_level * 5
        self.max_health = self.health
        self.strength = random.randint(5, 10) + player_level * 2
        self.speed = random.randint(3, 6) + player_level // 2
        self.color = ENEMY_COLOR
        self.movement_cooldown = 0
        self.movement_delay = 60
        self.animation_offset = 0
        self.attack_animation = 0
        self.hit_animation = 0
        
    def update_animation(self):
        self.animation_offset = math.sin(pygame.time.get_ticks() * 0.005) * 2
        
        if self.attack_animation > 0:
            self.attack_animation -= 1
            
        if self.hit_animation > 0:
            self.hit_animation -= 1
            
    def start_attack_animation(self):
        self.attack_animation = 10
        
    def start_hit_animation(self):
        self.hit_animation = 5
        
    def draw(self, surface):
        offset_x = 0
        offset_y = self.animation_offset
        
        if self.attack_animation > 0:
            offset_x = 5 * math.sin(self.attack_animation * 0.2)
            
        if self.hit_animation > 0:
            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)
        
        x = self.x + offset_x
        y = self.y + offset_y
        
        if self.enemy_type == "fiery":
            pygame.draw.ellipse(surface, (200, 50, 0), (x, y, self.size, self.size))
            flame_size = 15
            if self.attack_animation > 0:
                flame_size = 20 * (1 - self.attack_animation / 10)
            for i in range(8):
                angle = i * math.pi / 4
                flame_x = x + self.size//2 + math.cos(angle) * flame_size
                flame_y = y + self.size//2 + math.sin(angle) * flame_size
                pygame.draw.polygon(surface, (255, 150, 0), 
                                  [(x + self.size//2, y + self.size//2),
                                   (flame_x, flame_y),
                                   (flame_x + math.cos(angle+0.3)*5, flame_y + math.sin(angle+0.3)*5)])
            pygame.draw.circle(surface, (255, 255, 0), (x + 15, y + 15), 4)
            pygame.draw.circle(surface, (255, 255, 0), (x + self.size - 15, y + 15), 4)
            pygame.draw.arc(surface, (255, 100, 0), (x + 10, y + 20, self.size - 20, 15), 0, math.pi, 2)
            
        elif self.enemy_type == "shadow":
            pygame.draw.ellipse(surface, (40, 40, 80), (x, y, self.size, self.size))
            smoke_count = 6
            if self.attack_animation > 0:
                smoke_count = 12 * (1 - self.attack_animation / 10)
            for i in range(int(smoke_count)):
                offset_x = random.randint(-5, 5)
                offset_y = random.randint(-5, 5)
                pygame.draw.circle(surface, (70, 70, 120), 
                                 (x + self.size//2 + offset_x, y + self.size//2 + offset_y), 
                                 random.randint(3, 8))
            pygame.draw.circle(surface, (0, 255, 255), (x + 20, y + 20), 5)
            pygame.draw.circle(surface, (0, 255, 255), (x + self.size - 20, y + 20), 5)
            claw_length = 10
            if self.attack_animation > 0:
                claw_length = 15 * (1 - self.attack_animation / 10)
            pygame.draw.line(surface, (0, 200, 200), (x, y + self.size), (x - claw_length, y + self.size + claw_length), 2)
            pygame.draw.line(surface, (0, 200, 200), (x + self.size, y + self.size), (x + self.size + claw_length, y + self.size + claw_length), 2)
            
        else:  # Ice enemy
            pygame.draw.ellipse(surface, (150, 220, 255), (x, y, self.size, self.size))
            shard_length = 20
            if self.attack_animation > 0:
                shard_length = 30 * (1 - self.attack_animation / 10)
            for i in range(8):
                angle = i * math.pi / 4
                shard_x = x + self.size//2 + math.cos(angle) * shard_length
                shard_y = y + self.size//2 + math.sin(angle) * shard_length
                pygame.draw.line(surface, (200, 240, 255), 
                               (x + self.size//2, y + self.size//2),
                               (shard_x, shard_y), 2)
            pygame.draw.circle(surface, (0, 100, 200), (x + 15, y + 15), 4)
            pygame.draw.circle(surface, (0, 100, 200), (x + self.size - 15, y + 15), 4)
            breath_width = 10
            if self.attack_animation > 0:
                breath_width = 20 * (1 - self.attack_animation / 10)
            pygame.draw.arc(surface, (100, 200, 255), (x + 10, y + 25, self.size - 20, breath_width), 0, math.pi, 2)
            
        bar_width = 40
        pygame.draw.rect(surface, (20, 20, 30), (x - 5, y - 15, bar_width, 8), border_radius=2)
        health_width = (bar_width - 2) * (self.health / self.max_health)
        pygame.draw.rect(surface, HEALTH_COLOR, (x - 4, y - 14, health_width, 6), border_radius=2)
        
        # Draw enemy name
        name_text = font_tiny.render(self.name, True, TEXT_COLOR)
        name_rect = name_text.get_rect(midtop=(x + self.size//2, y - 30))
        surface.blit(name_text, name_rect)
        
    def update(self, player_x, player_y):
        self.update_animation()
        self.movement_cooldown -= 1
        if self.movement_cooldown <= 0:
            self.movement_cooldown = self.movement_delay
            
            dx, dy = random.choice([(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)])
            new_x = self.x + dx * GRID_SIZE
            new_y = self.y + dy * GRID_SIZE
            
            # Check world boundaries
            if 0 <= new_x < WORLD_WIDTH:
                self.x = new_x
            if 0 <= new_y < WORLD_HEIGHT:
                self.y = new_y

# ============================================================================
# ITEM SYSTEM - Collectible items and power-ups
# ============================================================================
class Item:
    """
    Collectible items that provide healing, mana restoration, or other benefits.
    Items spawn randomly in the world and can be collected by the player.
    """
    def __init__(self):
        self.size = ITEM_SIZE
        # Items will be positioned by the spawn system
        self.x = 0
        self.y = 0
        self.type = random.choice(["health", "mana"])
        self.color = ITEM_COLOR if self.type == "health" else MANA_COLOR
        self.pulse = 0
        self.float_offset = 0
        
    def update(self):
        self.pulse += 0.1
        self.float_offset = math.sin(pygame.time.get_ticks() * 0.003) * 3
        
    def draw(self, surface):
        pulse_size = self.size//2 + math.sin(self.pulse) * 3
        y_pos = self.y + self.float_offset
        
        pygame.draw.circle(surface, self.color, (self.x + self.size//2, y_pos + self.size//2), pulse_size)
        
        if self.type == "health":
            pygame.draw.rect(surface, (255, 255, 255), (self.x + 10, y_pos + 8, 10, 14), border_radius=2)
        else:
            pygame.draw.polygon(surface, (255, 255, 255), 
                              [(self.x + 15, y_pos + 8),
                               (self.x + 8, y_pos + 22),
                               (self.x + 22, y_pos + 22)])

# ============================================================================
# DECORATIVE DRAGON - Animated background element for title screen
# ============================================================================
class Dragon:
    """
    Decorative dragon for the title screen with fire breathing animation.
    This is a visual element, not a combat enemy.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_frame = 0
        self.fire_frame = 0
        self.fire_active = False
        self.flap_direction = 1
        self.flap_speed = 0.1
        
    def draw(self, surface):
        pygame.draw.ellipse(surface, DRAGON_COLOR, (self.x, self.y + 30, 180, 70))
        pygame.draw.circle(surface, DRAGON_COLOR, (self.x + 180, self.y + 50), 35)
        pygame.draw.circle(surface, (255, 255, 255), (self.x + 195, self.y + 45), 10)
        pygame.draw.circle(surface, (0, 0, 0), (self.x + 195, self.y + 45), 5)
        pygame.draw.polygon(surface, (200, 100, 50), [
            (self.x + 180, self.y + 25),
            (self.x + 190, self.y + 10),
            (self.x + 195, self.y + 20)
        ])
        pygame.draw.polygon(surface, (200, 100, 50), [
            (self.x + 205, self.y + 25),
            (self.x + 215, self.y + 10),
            (self.x + 210, self.y + 20)
        ])
        
        wing_y_offset = math.sin(self.animation_frame) * 12
        pygame.draw.polygon(surface, (200, 50, 50), [
            (self.x + 40, self.y + 50),
            (self.x, self.y + 15 + wing_y_offset),
            (self.x + 50, self.y + 30)
        ])
        pygame.draw.polygon(surface, (200, 50, 50), [
            (self.x + 40, self.y + 50),
            (self.x, self.y + 85 - wing_y_offset),
            (self.x + 50, self.y + 70)
        ])
        
        pygame.draw.polygon(surface, DRAGON_COLOR, [
            (self.x, self.y + 50),
            (self.x - 50, self.y + 20),
            (self.x - 50, self.y + 80)
        ])
        
        for i in range(3):
            offset = i * 15
            pygame.draw.polygon(surface, (200, 50, 50), [
                (self.x - 50 + offset, self.y + 50 - offset//2),
                (self.x - 55 + offset, self.y + 40 - offset//2),
                (self.x - 45 + offset, self.y + 40 - offset//2)
            ])
        
        if self.fire_active:
            for i in range(15):
                fire_size = 5 + i * 1.5
                alpha = max(0, 200 - i * 10)
                fire_color = (255, 215, 0, alpha)
                
                fire_surf = pygame.Surface((fire_size*2, fire_size*2), pygame.SRCALPHA)
                pygame.draw.circle(fire_surf, fire_color, (fire_size, fire_size), fire_size)
                surface.blit(
                    fire_surf, 
                    (
                        self.x + 180 + 35 + i*15 + self.fire_frame*2, 
                        self.y + 40
                    )
                )
        
        self.animation_frame += self.flap_speed
        
    def breathe_fire(self):
        self.fire_active = True
        self.fire_frame = 0
        
    def update(self):
        if self.fire_active:
            self.fire_frame += 1
            if self.fire_frame > 30:
                self.fire_active = False

# ============================================================================
# BATTLE SYSTEM - Turn-based combat interface and mechanics
# ============================================================================
class BattleScreen:
    """
    Turn-based combat system with attack, magic, item, and run options.
    Handles battle animations, damage calculations, and victory/defeat conditions.
    """
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.state = "player_turn"
        self.battle_log = ["Battle started!", "It's your turn!"]
        self.buttons = [
            Button(50, 525, 180, 50, "ATTACK"),
            Button(250, 525, 180, 50, "MAGIC"),
            Button(450, 525, 180, 50, "ITEM"),
            Button(650, 525, 180, 50, "RUN")
        ]
        self.selected_option = 0
        self.battle_ended = False
        self.result = None
        self.transition_alpha = 0
        self.transition_state = "in"
        self.transition_speed = 8
        self.show_summary = False
        self.damage_effect_timer = 0
        self.damage_target = None
        self.damage_amount = 0
        self.action_cooldown = 0
        self.action_delay = 30
        self.log_page = 0
        self.log_lines_per_page = 3
        self.waiting_for_continue = False
        self.action_steps = []
        self.particle_system = ParticleSystem()
        self.screen_shake = 0
        self.attack_effect_timer = 0
        self.magic_effect = {
            'active': False,
            'x': 0, 'y': 0,
            'radius': 0,
            'max_radius': 50,
            'color': MAGIC_COLORS[0]
        }
        self.is_boss = hasattr(self.enemy, 'enemy_type') and "boss_dragon" in self.enemy.enemy_type
        self.pending_elemental_effect = None
        self.elemental_effect_timer = 0
        
    def start_transition(self):
        self.transition_state = "in"
        self.transition_alpha = 0
        
    def add_screen_shake(self, intensity=5, duration=10):
        self.screen_shake = duration
        self.shake_intensity = intensity
        
    def draw(self, surface):
        shake_offset_x = 0
        shake_offset_y = 0
        if self.screen_shake > 0:
            shake_offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            shake_offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            self.screen_shake -= 1
        
        temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        temp_surface.fill((20, 10, 40))
        
        # Draw player and enemy avatars
        player_x, player_y = 200 + shake_offset_x, 350 + shake_offset_y
        enemy_x, enemy_y = 700 + shake_offset_x, 250 + shake_offset_y
        
        # Draw player using the same character drawing method as overworld
        # Temporarily set the player's position for battle drawing
        original_x, original_y = self.player.x, self.player.y
        self.player.x, self.player.y = player_x, player_y
        
        # Draw the player directly to the battle surface
        self.player.draw(temp_surface)
        
        # Restore original position
        self.player.x, self.player.y = original_x, original_y
        
        # Draw enemy
        if hasattr(self.enemy, 'enemy_type') and "boss_dragon" in self.enemy.enemy_type:
            # Draw the boss using its own draw method, at the correct position
            boss_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            self.enemy.x = enemy_x
            self.enemy.y = enemy_y
            self.enemy.draw(boss_surf)
            temp_surface.blit(boss_surf, (0, 0))
        elif self.enemy.enemy_type == "fiery":
            pygame.draw.ellipse(temp_surface, (220, 80, 0), (enemy_x, enemy_y, 60, 60))
            for i in range(12):
                angle = i * math.pi / 6
                flame_length = random.randint(10, 20)
                flame_x = enemy_x + 30 + math.cos(angle) * flame_length
                flame_y = enemy_y + 30 + math.sin(angle) * flame_length
                flame_color = random.choice(FIRE_COLORS)
                pygame.draw.line(temp_surface, flame_color, 
                               (enemy_x + 30, enemy_y + 30),
                               (flame_x, flame_y), 3)
            pygame.draw.circle(temp_surface, (255, 255, 0), (enemy_x + 20, enemy_y + 25), 6)
            pygame.draw.circle(temp_surface, (255, 255, 0), (enemy_x + 40, enemy_y + 25), 6)
        elif self.enemy.enemy_type == "shadow":
            pygame.draw.ellipse(temp_surface, (30, 30, 60), (enemy_x, enemy_y, 60, 60))
            for i in range(10):
                offset_x = random.randint(-10, 10)
                offset_y = random.randint(-10, 10)
                size = random.randint(5, 15)
                alpha = random.randint(50, 150)
                smoke_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(smoke_surf, (70, 70, 120, alpha), (size, size), size)
                temp_surface.blit(smoke_surf, (enemy_x + 30 - size + offset_x, enemy_y + 30 - size + offset_y))
            pygame.draw.circle(temp_surface, (0, 255, 255), (enemy_x + 20, enemy_y + 25), 7)
            pygame.draw.circle(temp_surface, (0, 255, 255), (enemy_x + 40, enemy_y + 25), 7)
        else:  # Ice enemy
            pygame.draw.ellipse(temp_surface, (180, 230, 255), (enemy_x, enemy_y, 60, 60))
            for i in range(8):
                angle = i * math.pi / 4
                crystal_length = random.randint(10, 20)
                crystal_x = enemy_x + 30 + math.cos(angle) * crystal_length
                crystal_y = enemy_y + 30 + math.sin(angle) * crystal_length
                pygame.draw.line(temp_surface, (220, 240, 255), 
                               (enemy_x + 30, enemy_y + 30),
                               (crystal_x, crystal_y), 3)
            pygame.draw.circle(temp_surface, (0, 100, 200), (enemy_x + 20, enemy_y + 25), 6)
            pygame.draw.circle(temp_surface, (0, 100, 200), (enemy_x + 40, enemy_y + 25), 6)
        
        # Draw character-specific attack effects
        if self.attack_effect_timer > 0:
            if self.player.type == "Warrior":
                # Holy slash effect for Warrior/Paladin
                effect_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                
                # Multiple holy slashes with different angles and colors
                slash_angles = [0, 15, -15, 30, -30]
                for i, angle in enumerate(slash_angles):
                    # Calculate slash start and end points
                    start_x = player_x + 25
                    start_y = player_y + 15
                    end_x = start_x + math.cos(math.radians(angle)) * 80
                    end_y = start_y + math.sin(math.radians(angle)) * 80
                    
                    # Holy slash colors (gold, white, light blue)
                    slash_colors = [(255, 215, 0, 200), (255, 255, 255, 180), (173, 216, 230, 160)]
                    color = slash_colors[i % len(slash_colors)]
                    
                    # Draw the slash with glow effect
                    for width in range(8, 2, -2):
                        alpha = color[3] - (8 - width) * 20
                        glow_color = (*color[:3], max(0, alpha))
                        pygame.draw.line(effect_surf, glow_color, (start_x, start_y), (end_x, end_y), width)
                
                # Add enemy-side slash effect
                enemy_slash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                
                # Draw impact slashes on enemy
                impact_angles = [0, 20, -20, 40, -40]
                for i, angle in enumerate(impact_angles):
                    # Calculate impact slash points
                    center_x = enemy_x + 30
                    center_y = enemy_y + 30
                    start_x = center_x - math.cos(math.radians(angle)) * 25
                    start_y = center_y - math.sin(math.radians(angle)) * 25
                    end_x = center_x + math.cos(math.radians(angle)) * 25
                    end_y = center_y + math.sin(math.radians(angle)) * 25
                    
                    # Impact slash colors (brighter versions)
                    impact_colors = [(255, 255, 100, 250), (255, 255, 255, 220), (200, 230, 255, 200)]
                    color = impact_colors[i % len(impact_colors)]
                    
                    # Draw impact slash with glow
                    for width in range(10, 3, -2):
                        alpha = color[3] - (10 - width) * 25
                        glow_color = (*color[:3], max(0, alpha))
                        pygame.draw.line(enemy_slash_surf, glow_color, (start_x, start_y), (end_x, end_y), width)
                
                temp_surface.blit(effect_surf, (0, 0))
                temp_surface.blit(enemy_slash_surf, (0, 0))
            
            self.attack_effect_timer -= 1
        
        # Draw magic effect
        if self.magic_effect['active']:
            radius = self.magic_effect['radius']
            max_radius = self.magic_effect['max_radius']
            
            for i in range(3, 0, -1):
                r = radius * (i/3)
                alpha = 150 * (1 - r/max_radius)
                color = (*self.magic_effect['color'][:3], int(alpha))
                pygame.draw.circle(temp_surface, color, 
                                 (self.magic_effect['x'], self.magic_effect['y']), 
                                 int(r), 2)
            
            pygame.draw.circle(temp_surface, self.magic_effect['color'], 
                             (self.magic_effect['x'], self.magic_effect['y']), 8)
        
        # Draw fireball projectile
        if hasattr(self, 'fireball_projectile') and self.fireball_projectile['active'] and not self.fireball_projectile.get('hit', False):
            # Draw fireball with glow effect
            x, y = int(self.fireball_projectile['x']), int(self.fireball_projectile['y'])
            size = self.fireball_projectile['size']
            color = self.fireball_projectile['color']
            
            # Outer glow
            for i in range(3, 0, -1):
                glow_size = size + i * 3
                glow_alpha = 100 - i * 30
                glow_color = (*color[:3], glow_alpha)
                glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, glow_color, (glow_size, glow_size), glow_size)
                temp_surface.blit(glow_surf, (x - glow_size, y - glow_size))
            
            # Main fireball
            pygame.draw.circle(temp_surface, color, (x, y), size)
            pygame.draw.circle(temp_surface, (255, 255, 200), (x, y), size // 2)
        
        # Draw knife projectile
        if hasattr(self, 'knife_projectile') and self.knife_projectile['active'] and not self.knife_projectile.get('hit', False):
            x, y = int(self.knife_projectile['x']), int(self.knife_projectile['y'])
            size = self.knife_projectile['size']
            rotation = self.knife_projectile['rotation']
            color = self.knife_projectile['color']
            
            # Create knife surface for rotation
            knife_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            
            # Draw knife blade (pointed oval) - scaled for larger size
            blade_points = [
                (size, 0),  # Tip
                (size - 4, size // 2),  # Top edge
                (size - 2, size),  # Bottom edge
                (size + 2, size),  # Bottom edge
                (size + 4, size // 2),  # Top edge
            ]
            pygame.draw.polygon(knife_surf, color, blade_points)
            
            # Draw knife handle - scaled for larger size
            handle_rect = pygame.Rect(size - 2, size, 4, size // 2)
            pygame.draw.rect(knife_surf, (139, 69, 19), handle_rect)  # Brown handle
            
            # Add metallic shine to blade
            shine_points = [
                (size, 2),  # Tip shine
                (size - 2, size // 2 - 2),  # Top shine
                (size + 2, size // 2 - 2),  # Top shine
            ]
            pygame.draw.polygon(knife_surf, (200, 200, 200), shine_points)
            
            # Rotate and draw
            rotated_knife = pygame.transform.rotate(knife_surf, rotation)
            knife_rect = rotated_knife.get_rect(center=(x, y))
            temp_surface.blit(rotated_knife, knife_rect)
        
        # Draw health bars
        player_health_width = 150 * (self.player.health / max(1, self.player.max_health))
        pygame.draw.rect(temp_surface, (30, 30, 50), (180, 410, 160, 20))
        pygame.draw.rect(temp_surface, HEALTH_COLOR, (182, 412, player_health_width, 16))
        player_text = font_small.render(f"{self.player.health}/{self.player.max_health}", True, TEXT_COLOR)
        text_rect = player_text.get_rect(center=(180 + 80, 410 + 10))
        temp_surface.blit(player_text, text_rect)
        # Only draw enemy health bar and name if not a boss dragon
        if not (hasattr(self.enemy, 'enemy_type') and "boss_dragon" in self.enemy.enemy_type):
            enemy_health_width = 150 * (self.enemy.health / max(1, self.enemy.max_health))
            pygame.draw.rect(temp_surface, (30, 30, 50), (680, 310, 160, 20))
            pygame.draw.rect(temp_surface, HEALTH_COLOR, (682, 312, enemy_health_width, 16))
            enemy_text = font_small.render(f"{self.enemy.health}/{self.enemy.max_health}", True, TEXT_COLOR)
            text_rect = enemy_text.get_rect(center=(680 + 80, 310 + 10))
            temp_surface.blit(enemy_text, text_rect)
        # Draw enemy name (not for boss)
        if not (hasattr(self.enemy, 'enemy_type') and "boss_dragon" in self.enemy.enemy_type):
            enemy_name = font_small.render(self.enemy.name, True, (255, 215, 0))
            name_rect = enemy_name.get_rect(midtop=(enemy_x + 30, enemy_y - 25))
            temp_surface.blit(enemy_name, name_rect)
        
        # Draw battle log
        pygame.draw.rect(temp_surface, UI_BG, (100, 50, 800, 100), border_radius=8)
        pygame.draw.rect(temp_surface, UI_BORDER, (100, 50, 800, 100), 3, border_radius=8)
        
        start_idx = max(0, len(self.battle_log) - self.log_lines_per_page)
        end_idx = min(len(self.battle_log), start_idx + self.log_lines_per_page)
        
        for i, log in enumerate(self.battle_log[start_idx:end_idx]):
            log_text = font_small.render(log, True, TEXT_COLOR)
            temp_surface.blit(log_text, (120, 70 + i * 30))
        
        if self.waiting_for_continue:
            continue_text = font_small.render("(Press ENTER to continue...)", True, (255, 215, 0))
            temp_surface.blit(continue_text, (120, 70 + self.log_lines_per_page * 30))
        
        # Draw buttons
        if self.state == "player_turn" and not self.waiting_for_continue:
            for i, button in enumerate(self.buttons):
                button.selected = (i == self.selected_option)
                button.draw(temp_surface)
        
        # Draw damage effect
        if self.damage_effect_timer > 0:
            effect_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            if self.damage_target == "player":
                pygame.draw.rect(effect_surf, (255, 0, 0, 100), (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))
            elif self.damage_target == "enemy":
                pygame.draw.rect(effect_surf, (255, 0, 0, 100), (enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE))
            
            damage_text = font_medium.render(f"-{self.damage_amount}", True, (255, 50, 50))
            if self.damage_target == "player":
                temp_surface.blit(damage_text, (player_x + 20, player_y - 30))
            elif self.damage_target == "enemy":
                temp_surface.blit(damage_text, (enemy_x + 20, enemy_y - 30))
                
            temp_surface.blit(effect_surf, (0, 0))
            self.damage_effect_timer -= 1
        
        # Draw particles
        self.particle_system.draw(temp_surface)
        
        # Draw transition overlay if active
        if self.transition_state != "none":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self.transition_alpha))
            temp_surface.blit(overlay, (0, 0))
            
        # Show summary after battle
        if self.battle_ended and self.show_summary:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            temp_surface.blit(overlay, (0, 0))
            
            if self.result == "win":
                summary = [
                    "VICTORY!",
                    f"EXP GAINED: 25",
                    f"KILLS: {self.player.kills}",
                    "Press ENTER to continue..."
                ]
            elif self.result == "lose":
                summary = [
                    "DEFEAT...",
                    "Press ENTER to continue..."
                ]
            elif self.result == "escape":
                summary = [
                    "You Escaped!",
                    "Press ENTER to continue..."
                ]
                
            for i, line in enumerate(summary):
                text = font_large.render(line, True, TEXT_COLOR)
                temp_surface.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 250 + i*60))
        
        # Draw the temporary surface to the screen
        surface.blit(temp_surface, (0, 0))

    def update(self):
        self.player.update_animation()
        self.enemy.update_animation()
        self.particle_system.update()
        
        # Update magic effect
        if self.magic_effect['active']:
            self.magic_effect['radius'] += 3
            if self.magic_effect['radius'] > self.magic_effect['max_radius']:
                self.magic_effect['active'] = False
                self.magic_effect['radius'] = 0
        
        # Update fireball projectile
        if hasattr(self, 'fireball_projectile') and self.fireball_projectile['active']:
            # Update timer
            self.fireball_projectile['timer'] += 1
            
            if self.fireball_projectile['timer'] < self.fireball_projectile['max_timer']:
                # Calculate direction to target
                dx = self.fireball_projectile['target_x'] - self.fireball_projectile['x']
                dy = self.fireball_projectile['target_y'] - self.fireball_projectile['y']
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 0:
                    # Move fireball towards target
                    self.fireball_projectile['x'] += (dx / distance) * self.fireball_projectile['speed']
                    self.fireball_projectile['y'] += (dy / distance) * self.fireball_projectile['speed']
                
                # Add trail particles
                for _ in range(2):
                    angle = random.uniform(0, math.pi*2)
                    dist = random.uniform(0, 6)
                    px = self.fireball_projectile['x'] + math.cos(angle) * dist
                    py = self.fireball_projectile['y'] + math.sin(angle) * dist
                    self.particle_system.add_particle(
                        px, py, self.fireball_projectile['color'],
                        (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)),
                        2, 15
                    )
            else:
                # Timer expired - fireball hits target and explodes
                self.particle_system.add_explosion(
                    700 + 30, 250 + 30,  # Enemy center position
                    self.fireball_projectile['color'], count=30, size_range=(3, 8), 
                    speed_range=(2, 6), lifetime_range=(20, 35)
                )
                self.fireball_projectile['active'] = False
                self.fireball_projectile['hit'] = True  # Mark as hit
                # Add a small delay to ensure projectile is removed before next frame
                self.action_cooldown = 2
        
        # Clean up hit projectiles
        if hasattr(self, 'fireball_projectile') and self.fireball_projectile.get('hit', False):
            delattr(self, 'fireball_projectile')
        if hasattr(self, 'knife_projectile') and self.knife_projectile.get('hit', False):
            delattr(self, 'knife_projectile')
        
        # Update knife projectile
        if hasattr(self, 'knife_projectile') and self.knife_projectile['active']:
            # Update timer
            self.knife_projectile['timer'] += 1
            
            if self.knife_projectile['timer'] < self.knife_projectile['max_timer']:
                # Calculate direction to target
                dx = self.knife_projectile['target_x'] - self.knife_projectile['x']
                dy = self.knife_projectile['target_y'] - self.knife_projectile['y']
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 0:
                    # Move knife towards target
                    self.knife_projectile['x'] += (dx / distance) * self.knife_projectile['speed']
                    self.knife_projectile['y'] += (dy / distance) * self.knife_projectile['speed']
                    self.knife_projectile['rotation'] += 60  # Spin the knife faster (4x speed)
                
                # Add trail particles
                for _ in range(1):
                    angle = random.uniform(0, math.pi*2)
                    dist = random.uniform(0, 4)
                    px = self.knife_projectile['x'] + math.cos(angle) * dist
                    py = self.knife_projectile['y'] + math.sin(angle) * dist
                    self.particle_system.add_particle(
                        px, py, (120, 120, 120),
                        (random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3)),
                        1, 10
                    )
            else:
                # Timer expired - knife hits target and explodes
                self.particle_system.add_explosion(
                    700 + 30, 250 + 30,  # Enemy center position
                    (80, 80, 80), count=20, size_range=(2, 6), 
                    speed_range=(1, 4), lifetime_range=(15, 25)
                )
                self.knife_projectile['active'] = False
                self.knife_projectile['hit'] = True  # Mark as hit
                # Add a small delay to ensure projectile is removed before next frame
                self.action_cooldown = 2
        
        if self.transition_state == "in":
            self.transition_alpha += self.transition_speed
            if self.transition_alpha >= 255:
                self.transition_alpha = 255
                self.transition_state = "out"
        elif self.transition_state == "out":
            self.transition_alpha -= self.transition_speed
            if self.transition_alpha <= 0:
                self.transition_alpha = 0
                self.transition_state = "none"
                
        if self.action_cooldown > 0:
            self.action_cooldown -= 1
            return False
        
        # Check for battle end conditions
        if self.enemy.health <= 0:
            self.battle_ended = True
            self.result = "win"
            self.add_log("You defeated the enemy!")
            self.show_summary = True
            return True
        elif self.player.health <= 0:
            self.battle_ended = True
            self.result = "lose"
            self.add_log("You were defeated...")
            self.show_summary = True
            return True
        
        # Update elemental effect
        if self.elemental_effect_timer > 0:
            self.elemental_effect_timer -= 1
            if self.elemental_effect_timer == 0:
                self.pending_elemental_effect = None
        
        # Process current action steps
        if self.action_steps:
            step = self.action_steps.pop(0)
            step()
            return False
            
        # Handle enemy turn if no actions are queued
        if self.state == "enemy_turn" and not self.battle_ended and not self.waiting_for_continue:
            damage = max(1, self.enemy.strength - self.player.defense // 3)
            self.player.health -= damage
            self.add_log(f"{self.enemy.name} attacks for {damage} damage!")
            self.damage_target = "player"
            self.damage_amount = damage
            self.damage_effect_timer = 20
            self.enemy.start_attack_animation()
            self.player.start_hit_animation()
            self.add_screen_shake(3, 5)
            # Elemental effect after dialog
            self.pending_elemental_effect = self.enemy.enemy_type
            self.elemental_effect_timer = 20
            self.state = "player_turn"
            self.add_log("It's your turn!")
            self.action_cooldown = self.action_delay
            
        return False
    
    def add_log(self, message):
        self.battle_log.append(message)
        self.waiting_for_continue = True
    
    def handle_input(self, event, game=None):
        if self.waiting_for_continue:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                self.waiting_for_continue = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.waiting_for_continue = False
            return
            
        if self.battle_ended and self.show_summary:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                if self.result == "escape" and game:
                    self.show_summary = False
                    game.state = "overworld"
                    game.battle_screen = None
                else:
                    self.show_summary = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.result == "escape" and game:
                    self.show_summary = False
                    game.state = "overworld"
                    game.battle_screen = None
                else:
                    self.show_summary = False
        elif self.state == "player_turn" and not self.battle_ended and self.action_cooldown == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.selected_option = (self.selected_option + 1) % 4
                    if game and hasattr(game, 'SFX_ARROW') and game.SFX_ARROW: game.SFX_ARROW.play()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.selected_option = (self.selected_option - 1) % 4
                    if game and hasattr(game, 'SFX_ARROW') and game.SFX_ARROW: game.SFX_ARROW.play()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_option = (self.selected_option - 2) % 4
                    if game and hasattr(game, 'SFX_ARROW') and game.SFX_ARROW: game.SFX_ARROW.play()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_option = (self.selected_option + 2) % 4
                    if game and hasattr(game, 'SFX_ARROW') and game.SFX_ARROW: game.SFX_ARROW.play()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if game and hasattr(game, 'SFX_ENTER') and game.SFX_ENTER: game.SFX_ENTER.play()
                    self.handle_action(game)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    if button.rect.collidepoint(mouse_pos):
                        self.selected_option = i
                        if game and hasattr(game, 'SFX_ENTER') and game.SFX_ENTER: game.SFX_ENTER.play()
                        self.handle_action(game)
    
    def handle_action(self, game=None):
        if self.state != "player_turn" or self.battle_ended or self.action_cooldown > 0:
            return
        if self.selected_option == 0:  # Attack
            if game and hasattr(game, 'SFX_ATTACK') and game.SFX_ATTACK: game.SFX_ATTACK.play()
            self.action_steps = [
                lambda: self.add_log("You attack!"),
                lambda: self.start_attack_animation(),
                lambda: self.execute_attack()
            ]
        elif self.selected_option == 1:  # Magic
            if self.player.mana >= 20:
                if game and hasattr(game, 'SFX_MAGIC') and game.SFX_MAGIC: game.SFX_MAGIC.play()
                self.action_steps = [
                    lambda: self.add_log("You cast a fireball!"),
                    lambda: self.start_magic_animation(),
                    lambda: self.execute_magic()
                ]
            else:
                if game and hasattr(game, 'SFX_CLICK') and game.SFX_CLICK: game.SFX_CLICK.play()
                self.add_log("Not enough mana!")
        elif self.selected_option == 2:  # Item
            if game and hasattr(game, 'SFX_ITEM') and game.SFX_ITEM: game.SFX_ITEM.play()
            self.action_steps = [
                lambda: self.add_log("You used a health potion!"),
                lambda: self.execute_item()
            ]
        elif self.selected_option == 3:  # Run
            if game and hasattr(game, 'SFX_CLICK') and game.SFX_CLICK: game.SFX_CLICK.play()
            self.action_steps = [
                lambda: self.add_log("You attempt to escape..."),
                lambda: self.execute_run()
            ]
    

    
    def start_attack_animation(self):
        self.player.start_attack_animation()
        self.attack_effect_timer = 20
        
        # Clear any existing projectiles to prevent stacking
        if hasattr(self, 'fireball_projectile'):
            delattr(self, 'fireball_projectile')
        if hasattr(self, 'knife_projectile'):
            delattr(self, 'knife_projectile')
        
        # Character-specific attack animations
        if self.player.type == "Mage":
            # Fireball attack animation
            self.fireball_projectile = {
                'active': True,
                'x': 200 + 25,  # Player center
                'y': 350 + 15,  # Player center
                'target_x': 700 + 30,  # Enemy center
                'target_y': 250 + 30,  # Enemy center
                'speed': 56,  # Slightly faster than knife
                'size': 12,
                'color': random.choice(FIRE_COLORS),
                'trail_particles': [],
                'timer': 0,  # Timer for 0.8 seconds
                'max_timer': 48  # 0.8 seconds at 60 FPS
            }
            
            # Create fireball trail particles
            for _ in range(10):
                angle = random.uniform(0, math.pi*2)
                dist = random.uniform(0, 8)
                px = self.fireball_projectile['x'] + math.cos(angle) * dist
                py = self.fireball_projectile['y'] + math.sin(angle) * dist
                self.particle_system.add_particle(
                    px, py, self.fireball_projectile['color'],
                    (math.cos(angle) * 0.3, math.sin(angle) * 0.3),
                    2, 20
                )
                
        elif self.player.type == "Rogue":
            # Knife throw attack animation
            self.knife_projectile = {
                'active': True,
                'x': 200 + 25,  # Player center
                'y': 350 + 15,  # Player center
                'target_x': 700 + 30,  # Enemy center
                'target_y': 250 + 30,  # Enemy center
                'speed': 48,  # 4 times faster (12 * 4)
                'size': 16,  # 2 times bigger (8 * 2)
                'rotation': 0,
                'color': (100, 100, 100),  # Steel gray
                'trail_particles': [],
                'timer': 0,  # Timer for 0.6 seconds
                'max_timer': 36  # 0.6 seconds at 60 FPS
            }
            
            # Create knife throw particles
            for _ in range(8):
                angle = random.uniform(0, math.pi*2)
                dist = random.uniform(0, 6)
                px = self.knife_projectile['x'] + math.cos(angle) * dist
                py = self.knife_projectile['y'] + math.sin(angle) * dist
                self.particle_system.add_particle(
                    px, py, (150, 150, 150),
                    (math.cos(angle) * 0.4, math.sin(angle) * 0.4),
                    1, 15
                )
                
        else:
            # Warrior/Paladin holy attack animation
            # Create holy energy particles around the player
            for _ in range(12):
                angle = random.uniform(0, math.pi*2)
                dist = random.uniform(0, 15)
                px = 200 + 25 + math.cos(angle) * dist
                py = 350 + 15 + math.sin(angle) * dist
                # Holy particle colors (gold, white, light blue)
                holy_colors = [(255, 215, 0), (255, 255, 255), (173, 216, 230)]
                particle_color = random.choice(holy_colors)
                self.particle_system.add_particle(
                    px, py, 
                    particle_color,
                    (math.cos(angle) * 0.8, math.sin(angle) * 0.8),
                    4, 25
                )
    
    def start_magic_animation(self):
        self.player.start_attack_animation()
        self.magic_effect = {
            'active': True,
            'x': 700 + 30,  # Enemy center x (where magic hits)
            'y': 250 + 30,  # Enemy center y (where magic hits)
            'radius': 0,
            'max_radius': 100,
            'color': random.choice(MAGIC_COLORS)
        }
        
        for _ in range(20):
            angle = random.uniform(0, math.pi*2)
            dist = random.uniform(0, 10)
            px = self.magic_effect['x'] + math.cos(angle) * dist
            py = self.magic_effect['y'] + math.sin(angle) * dist
            self.particle_system.add_particle(
                px, py, self.magic_effect['color'],
                (math.cos(angle) * 0.5, math.sin(angle) * 0.5),
                3, 30
            )
    
    def execute_attack(self):
        damage = self.player.strength
        self.enemy.health -= damage
        
        # Character-specific attack messages and effects
        if self.player.type == "Mage":
            self.add_log(f"Fireball dealt {damage} damage to {self.enemy.name}!")
            # Fireball explosion happens when projectile hits in update method
        elif self.player.type == "Rogue":
            self.add_log(f"Knife throw dealt {damage} damage to {self.enemy.name}!")
            # Knife explosion happens when projectile hits in update method
        else:
            # Warrior/Paladin attack
            self.add_log(f"You dealt {damage} damage to {self.enemy.name}!")
            # Default enemy-type based explosion
            if self.enemy.enemy_type == "fiery":
                self.particle_system.add_explosion(
                    700 + 30, 250 + 30, FIRE_COLORS[0], 
                    count=30, size_range=(2, 6), speed_range=(1, 4), lifetime_range=(15, 30)
                )
            elif self.enemy.enemy_type == "shadow":
                self.particle_system.add_explosion(
                    700 + 30, 250 + 30, SHADOW_COLORS[1], 
                    count=20, size_range=(3, 8), speed_range=(0.5, 2), lifetime_range=(20, 40)
                )
            else:  # Ice
                self.particle_system.add_explosion(
                    700 + 30, 250 + 30, ICE_COLORS[2], 
                    count=25, size_range=(2, 5), speed_range=(1, 3), lifetime_range=(15, 25)
                )
        
        self.damage_target = "enemy"
        self.damage_amount = damage
        self.damage_effect_timer = 20
        self.enemy.start_hit_animation()
        self.add_screen_shake(5, 8)
        
        self.state = "enemy_turn"
        self.action_cooldown = self.action_delay
    
    def execute_magic(self):
        damage = self.player.strength * 2
        self.enemy.health -= damage
        self.player.mana -= 20
        self.add_log(f"Fireball dealt {damage} damage to {self.enemy.name}!")
        self.damage_target = "enemy"
        self.damage_amount = damage
        self.damage_effect_timer = 20
        self.enemy.start_hit_animation()
        self.add_screen_shake(8, 10)
        
        self.particle_system.add_beam(
            200 + 25, 350 + 15,  # Staff top (adjusted for new player position)
            700 + 30, 250 + 30,  # Enemy center (adjusted for new enemy position)
            self.magic_effect['color'], width=5, particle_count=15, speed=3
        )
        
        self.particle_system.add_explosion(
            700 + 30, 250 + 30, self.magic_effect['color'],
            count=40, size_range=(3, 7), speed_range=(1, 5), lifetime_range=(15, 30)
        )
        
        self.state = "enemy_turn"
        self.action_cooldown = self.action_delay
    
    def execute_item(self):
        heal_amount = 30
        self.player.health = min(self.player.max_health, self.player.health + heal_amount)
        self.add_log(f"Restored {heal_amount} HP!")
        
        for _ in range(20):
            x = random.randint(200, 200 + PLAYER_SIZE)
            y = random.randint(300, 300 + PLAYER_SIZE)
            self.particle_system.add_particle(
                x, y, HEALTH_COLOR,
                (random.uniform(-0.5, 0.5), random.uniform(-1, -0.5)),
                3, 30
            )
        
        self.state = "enemy_turn"
        self.action_cooldown = self.action_delay
    
    def execute_run(self):
        if random.random() < 0.7:  # 70% chance to escape
            self.add_log("You successfully escaped!")
            self.battle_ended = True
            self.result = "escape"
            self.show_summary = True
        else:
            self.add_log("Escape failed! The enemy attacks!")
            self.state = "enemy_turn"
            self.action_cooldown = self.action_delay

# ============================================================================
# STORY SYSTEM - Opening cutscene and narrative elements
# ============================================================================
class OpeningCutscene:
    """
    Story introduction sequence with multiple scenes and text progression.
    Sets up the game's narrative and world background.
    """
    def __init__(self):
        self.state = "intro"
        self.timer = 0
        self.scene_duration = 300  # 5 seconds per scene at 60 FPS
        self.scene_index = 0
        self.transition_alpha = 0
        self.transition_speed = 5
        self.text_alpha = 0
        self.text_appear_speed = 3
        self.text_disappear_speed = 2
        self.particle_system = ParticleSystem()
        self.scroll_y = SCREEN_HEIGHT
        self.scroll_speed = 1
        self.transition_state = "none"  # Initialize transition_state
        
    def update(self):
        self.timer += 1
        self.particle_system.update()
        
        # Update text alpha
        if self.timer < 120:  # First 2 seconds: text appears
            self.text_alpha = min(255, self.text_alpha + self.text_appear_speed)
        elif self.timer > 180:  # Last 2 seconds: text disappears
            self.text_alpha = max(0, self.text_alpha - self.text_disappear_speed)
        
        # Scene transitions
        if self.timer >= self.scene_duration:
            self.timer = 0
            self.scene_index += 1
            self.text_alpha = 0
            self.transition_alpha = 0
            self.transition_state = "in"
            
        # Add particles for scene 2
        if self.scene_index == 1 and self.timer % 5 == 0:
            self.particle_system.add_particle(
                random.randint(0, SCREEN_WIDTH),
                -10,
                random.choice(FIRE_COLORS),
                (random.uniform(-0.5, 0.5), random.uniform(1, 3)),
                random.randint(3, 7),
                random.randint(40, 80)
            )
        
        # Scroll text for scene 3
        if self.scene_index == 2:
            self.scroll_y -= self.scroll_speed
            if self.scroll_y < -600:
                self.scroll_y = SCREEN_HEIGHT
        
        # Transition animation
        if self.timer > self.scene_duration - 60:  # Last second of scene
            self.transition_alpha = min(255, self.transition_alpha + self.transition_speed)
        
        # End of cutscene
        if self.scene_index >= 3:
            return "character_select"
            
        return None
    
    def draw(self, screen):
        # Draw scene based on index
        if self.scene_index == 0:
            self.draw_intro_scene(screen)
        elif self.scene_index == 1:
            self.draw_dragon_scene(screen)
        elif self.scene_index == 2:
            self.draw_story_scene(screen)
        
        # Draw transition overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.transition_alpha))
        screen.blit(overlay, (0, 0))
        
        # Draw particles
        self.particle_system.draw(screen)
        
        # Draw skip prompt
        if pygame.time.get_ticks() % 1000 < 500:  # Blinking text
            skip_text = font_small.render("Press any key to skip...", True, (200, 200, 200))
            screen.blit(skip_text, (SCREEN_WIDTH - skip_text.get_width() - 20, SCREEN_HEIGHT - 40))
    
    def draw_intro_scene(self, screen):
        # Draw starfield background
        screen.fill(BACKGROUND)
        for i in range(100):
            x = i * 10
            y = math.sin(pygame.time.get_ticks() * 0.001 + i) * 50 + SCREEN_HEIGHT//2
            pygame.draw.circle(screen, (200, 200, 255), (x, int(y)), 1)
        
        # Draw title
        title = font_large.render("DRAGON'S LAIR", True, (255, 50, 50))
        title_shadow = font_large.render("DRAGON'S LAIR", True, (150, 0, 0))
        screen.blit(title_shadow, (SCREEN_WIDTH//2 - title.get_width()//2 + 3, 103))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        # Draw subtitle
        subtitle = font_medium.render("A RETRO RPG ADVENTURE", True, TEXT_COLOR)
        subtitle_shadow = font_medium.render("A RETRO RPG ADVENTURE", True, (0, 100, 100))
        screen.blit(subtitle_shadow, (SCREEN_WIDTH//2 - subtitle.get_width()//2 + 2, 162))
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 160))
        
        # Draw intro text
        intro_text = [
            "LONG AGO, IN THE KINGDOM OF PIXELONIA,",
            "AN ANCIENT EVIL AWOKE FROM ITS SLUMBER.",
            "THE DRAGON MALAKOR, RULER OF SHADOWS,",
            "THREATENED TO PLUNGE THE WORLD INTO DARKNESS."
        ]
        
        y_pos = 250
        for line in intro_text:
            text = font_cinematic.render(line, True, TEXT_COLOR)
            text.set_alpha(self.text_alpha)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_pos))
            screen.blit(text, text_rect)
            y_pos += 50
    
    def draw_dragon_scene(self, screen):
        # Draw dark background
        screen.fill((10, 5, 20))
        
        # Draw mountains
        for i in range(10):
            height = 150 + random.randint(0, 50)
            pygame.draw.polygon(screen, (30, 30, 60), [
                (i * 100, SCREEN_HEIGHT),
                (i * 100 + 50, SCREEN_HEIGHT - height),
                (i * 100 + 100, SCREEN_HEIGHT)
            ])
        
        # Draw dragon silhouette
        dragon_x = SCREEN_WIDTH//2 - 100
        dragon_y = SCREEN_HEIGHT//2 - 50
        
        # Body
        pygame.draw.ellipse(screen, (60, 20, 20), (dragon_x, dragon_y, 200, 80))
        # Head
        pygame.draw.circle(screen, (60, 20, 20), (dragon_x + 200, dragon_y + 40), 40)
        # Wings
        wing_offset = math.sin(pygame.time.get_ticks() * 0.005) * 10
        pygame.draw.polygon(screen, (80, 30, 30), [
            (dragon_x + 50, dragon_y + 40),
            (dragon_x - 50, dragon_y - 50 - wing_offset),
            (dragon_x + 50, dragon_y - 30 - wing_offset)
        ])
        pygame.draw.polygon(screen, (80, 30, 30), [
            (dragon_x + 50, dragon_y + 40),
            (dragon_x - 50, dragon_y + 130 + wing_offset),
            (dragon_x + 50, dragon_y + 110 + wing_offset)
        ])
        
        # Draw fire breath
        for i in range(20):
            x = dragon_x + 230 + i * 10
            y = dragon_y + 40 + math.sin(pygame.time.get_ticks() * 0.01 + i) * 10
            size = 10 - i * 0.4
            if size > 0:
                pygame.draw.circle(screen, (255, 150, 0), (x, y), int(size))
        
        # Draw scene text
        scene_text = [
            "THE DRAGON MALAKOR RAVAGED THE LAND,",
            "BURNING VILLAGES AND TERRIFYING THE PEOPLE.",
            "THE KING CALLED FOR HEROES TO RISE UP",
            "AND CHALLENGE THE ANCIENT EVIL."
        ]
        
        y_pos = 100
        for line in scene_text:
            text = font_cinematic.render(line, True, (255, 200, 100))
            text.set_alpha(self.text_alpha)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_pos))
            screen.blit(text, text_rect)
            y_pos += 50
    
    def draw_story_scene(self, screen):
        # Draw parchment background
        screen.fill((200, 180, 120))
        pygame.draw.rect(screen, (180, 150, 100), (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
        pygame.draw.rect(screen, (150, 120, 80), (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100), 3)
        
        # Draw story text (scrolling)
        story = [
            "YOUR QUEST BEGINS...",
            "",
            "THE KINGDOM OF PIXELONIA NEEDS A HERO.",
            "MALAKOR THE TERRIBLE HAS RETURNED,",
            "AND ONLY YOU CAN STOP HIM.",
            "",
            "TRAVEL THROUGH PERILOUS LANDS,",
            "BATTLE FIERCE MONSTERS,",
            "AND GATHER POWERFUL ARTIFACTS.",
            "",
            "YOUR JOURNEY LEADS TO THE DRAGON'S LAIR,",
            "WHERE THE FINAL CONFRONTATION AWAITS.",
            "",
            "CHOOSE YOUR HERO WISELY,",
            "FOR THE FATE OF THE KINGDOM RESTS IN YOUR HANDS."
        ]
        
        y_pos = self.scroll_y
        for line in story:
            text = font_cinematic.render(line, True, (60, 40, 20))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_pos))
            screen.blit(text, text_rect)
            y_pos += 50
        
        # Draw decorative elements
        pygame.draw.line(screen, (100, 80, 60), (100, 100), (100, SCREEN_HEIGHT - 100), 2)
        pygame.draw.line(screen, (100, 80, 60), (SCREEN_WIDTH - 100, 100), (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100), 2)
        
        # Draw scroll top and bottom
        pygame.draw.rect(screen, (150, 120, 80), (40, 40, SCREEN_WIDTH - 80, 20))
        pygame.draw.rect(screen, (150, 120, 80), (40, SCREEN_HEIGHT - 60, SCREEN_WIDTH - 80, 20))
        
        # Draw continue prompt
        if self.timer > 180 and pygame.time.get_ticks() % 1000 < 500:
            prompt = font_medium.render("PRESS ENTER TO CONTINUE", True, (100, 60, 30))
            screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, SCREEN_HEIGHT - 80))
    
    def skip(self):
        # Skip to the end of the cutscene
        self.scene_index = 3

# ============================================================================
# PLATFORM DETECTION - Cross-platform compatibility
# ============================================================================
def is_android():
    """
    Detects if the game is running on Android platform.
    Used for enabling touch controls and platform-specific features.
    """
    return (
        sys.platform.startswith("android") or
        "ANDROID_ARGUMENT" in os.environ
    )

# ============================================================================
# MAIN GAME CLASS - Central game controller and state manager
# ============================================================================
class Game:
    """
    Main game controller that manages all game states, systems, and user input.
    Handles the complete game loop from start menu to game over.
    
    Game States:
    - start_menu: Title screen with start/quit options
    - opening_cutscene: Story introduction sequence
    - character_select: Choose character class
    - overworld: Main gameplay area with movement and exploration
    - battle: Turn-based combat system
    - game_over: End game screen
    """
    def __init__(self):
        self.state = "start_menu"
        self.player = None
        self.world_map = WorldMap()
        self.enemies = []
        self.items = []
        self.score = 0
        self.game_time = 0
        self.spawn_timer = 0
        self.item_timer = 0
        self.starfield = []
        self.dragon = Dragon(SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 - 120)
        self.fire_timer = 0
        self.battle_screen = None
        self.transition_alpha = 0
        self.transition_state = "none"
        self.transition_speed = 10
        self.player_moved = False
        self.movement_cooldown = 0
        self.movement_delay = 10
        self.particle_system = ParticleSystem()
        self.opening_cutscene = OpeningCutscene()
        self.boss_battle_triggered = False
        self.boss_defeated = False
        self.show_world_map = False
        
        # Initialize starfield
        for _ in range(150):
            self.starfield.append([
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                random.random() * 2 + 0.5
            ])
        
        # Add flying dragons
        self.flying_dragons = []
        for _ in range(5):
            self.flying_dragons.append({
                'x': random.randint(-200, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.5, 2.0),
                'size': random.randint(2, 5),
                'flap': random.random() * 2 * math.pi
            })
        
        # UI Elements
        self.start_button = Button(SCREEN_WIDTH//2 - 120, 500, 240, 60, "START QUEST", UI_BORDER)
        self.quit_button = Button(SCREEN_WIDTH//2 - 120, 580, 240, 60, "QUIT", UI_BORDER)
        self.back_button = Button(20, 20, 100, 40, "BACK")
        
        # Character buttons
        self.warrior_button = Button(SCREEN_WIDTH//2 - 300, 300, 200, 150, "WARRIOR", (0, 255, 0))
        self.mage_button = Button(SCREEN_WIDTH//2 - 50, 300, 200, 150, "MAGE", (0, 200, 255))
        self.rogue_button = Button(SCREEN_WIDTH//2 + 200, 300, 200, 150, "ROGUE", (255, 100, 0))
        
        # ========================================
        # AUDIO SYSTEM - Procedurally Generated Sound Effects
        # ========================================
        # Generate retro-style sound effects using mathematical waveforms
        def generate_tone(frequency=440, duration_ms=100, volume=0.5, sample_rate=44100, waveform='sine'):
            t = np.linspace(0, duration_ms / 1000, int(sample_rate * duration_ms / 1000), False)
            if waveform == 'sine':
                wave = np.sin(frequency * 2 * np.pi * t)
            elif waveform == 'square':
                wave = np.sign(np.sin(frequency * 2 * np.pi * t))
            elif waveform == 'sawtooth':
                wave = 2 * (t * frequency - np.floor(t * frequency + 0.5))
            elif waveform == 'noise':
                wave = np.random.uniform(-1, 1, t.shape)
            else:
                wave = np.sin(frequency * 2 * np.pi * t)
            audio = (wave * volume * 32767).astype(np.int16)
            # Make it stereo by duplicating the mono channel
            audio_stereo = np.column_stack((audio, audio))
            return pygame.sndarray.make_sound(audio_stereo)
        try:
            pygame.mixer.init()
            self.SFX_CLICK = generate_tone(frequency=800, duration_ms=60, volume=0.5, waveform='square')
            self.SFX_ATTACK = generate_tone(frequency=200, duration_ms=120, volume=0.5, waveform='square')
            self.SFX_MAGIC = generate_tone(frequency=1200, duration_ms=200, volume=0.5, waveform='sine')
            self.SFX_ITEM = generate_tone(frequency=1000, duration_ms=80, volume=0.5, waveform='sine')
            self.SFX_LEVELUP = generate_tone(frequency=1500, duration_ms=300, volume=0.5, waveform='sine')
            self.SFX_GAMEOVER = generate_tone(frequency=100, duration_ms=400, volume=0.5, waveform='sine')
            self.SFX_VICTORY = generate_tone(frequency=900, duration_ms=500, volume=0.5, waveform='sine')
            self.SFX_ARROW = generate_tone(frequency=600, duration_ms=40, volume=0.4, waveform='square')
            self.SFX_ENTER = generate_tone(frequency=1200, duration_ms=80, volume=0.5, waveform='sine')
        except Exception as e:
            print("[WARNING] Could not generate sound effects:", e)
            self.SFX_CLICK = self.SFX_ATTACK = self.SFX_MAGIC = self.SFX_ITEM = self.SFX_LEVELUP = self.SFX_GAMEOVER = self.SFX_VICTORY = None
        
        # ========================================
        # MUSIC SYSTEM - Procedural Chiptune Generation
        # ========================================
        # Dynamic music that changes based on game state and area
        self.music = MusicSystem()
        
        # Virtual button setup for Android
        self.android_buttons = {}
        if is_android():
            button_size = 80
            button_margin = 20
            screen_w, screen_h = SCREEN_WIDTH, SCREEN_HEIGHT
            # D-pad
            self.android_buttons['up'] = pygame.Rect(button_margin + button_size, screen_h - 3*button_size, button_size, button_size)
            self.android_buttons['down'] = pygame.Rect(button_margin + button_size, screen_h - button_size, button_size, button_size)
            self.android_buttons['left'] = pygame.Rect(button_margin, screen_h - 2*button_size, button_size, button_size)
            self.android_buttons['right'] = pygame.Rect(button_margin + 2*button_size, screen_h - 2*button_size, button_size, button_size)
            # Enter/Space
            self.android_buttons['enter'] = pygame.Rect(screen_w - button_margin - button_size, screen_h - 2*button_size, button_size, button_size)
            self.android_buttons['space'] = pygame.Rect(screen_w - button_margin - 2*button_size, screen_h - 2*button_size, button_size, button_size)
    
    def spawn_enemy(self):
        current_area = self.world_map.get_current_area()
        # Don't spawn enemies in town areas
        if current_area and current_area.area_type != "town" and len(current_area.enemies) < 3:
            # Spawn enemy in current area
            enemy = Enemy(self.player.level if self.player else 1)
            
            # Area-specific enemy types
            area_enemy_types = {
                "plains": ["fiery", "shadow", "ice"],
                "forest": ["shadow", "ice"],
                "mountain": ["fiery", "ice"],
                "desert": ["fiery"],
                "swamp": ["shadow", "ice"],
                "volcano": ["fiery"],
                "ice": ["ice"],
                "castle": ["shadow", "fiery"],
                "cave": ["shadow", "ice"]
            }
            
            # Set enemy type based on area
            available_types = area_enemy_types.get(current_area.area_type, ["fiery", "shadow", "ice"])
            enemy.enemy_type = random.choice(available_types)
            
            # Position enemy randomly within the current area
            area_world_x, area_world_y = current_area.get_world_position()
            enemy.x = area_world_x + random.randint(100, AREA_WIDTH - 100)
            enemy.y = area_world_y + random.randint(100, AREA_HEIGHT - 100)
            current_area.enemies.append(enemy)
            self.enemies.append(enemy)
    
    def spawn_item(self):
        current_area = self.world_map.get_current_area()
        if current_area and len(current_area.items) < 2:
            # Spawn item in current area
            item = Item()
            # Position item randomly within the current area
            area_world_x, area_world_y = current_area.get_world_position()
            item.x = area_world_x + random.randint(100, AREA_WIDTH - 100)
            item.y = area_world_y + random.randint(100, AREA_HEIGHT - 100)
            current_area.items.append(item)
            self.items.append(item)
    
    def start_transition(self):
        self.transition_state = "in"
        self.transition_alpha = 0
    
    def update(self):
        """
        Main game update loop - called every frame to update all game systems.
        Handles different update logic based on current game state.
        """
        # ========================================
        # VISUAL EFFECTS UPDATES
        # ========================================
        # Update starfield animation
        for star in self.starfield:
            star[0] -= star[2]
            if star[0] < 0:
                star[0] = SCREEN_WIDTH
                star[1] = random.randint(0, SCREEN_HEIGHT)
        
        # Update flying dragons
        for dragon in self.flying_dragons:
            dragon['x'] += dragon['speed']
            dragon['flap'] += 0.05
            if dragon['x'] > SCREEN_WIDTH + 50:
                dragon['x'] = -50
                dragon['y'] = random.randint(0, SCREEN_HEIGHT)
                dragon['speed'] = random.uniform(0.5, 2.0)
        
        # ========================================
        # SYSTEM UPDATES
        # ========================================
        # Update particle effects
        self.particle_system.update()
        
        # Update dynamic music system based on game state
        is_boss_battle = (
            self.state == "battle" and 
            self.battle_screen and 
            hasattr(self.battle_screen.enemy, 'enemy_type') and 
            "boss_dragon" in self.battle_screen.enemy.enemy_type
        )
        current_area = self.world_map.get_current_area() if hasattr(self, 'world_map') else None
        self.music.update(self.state, is_boss_battle, current_area)
        
        # ========================================
        # TRANSITION EFFECTS
        # ========================================
        # Handle screen transition animations (fade in/out)
        if self.transition_state == "in":
            self.transition_alpha += self.transition_speed
            if self.transition_alpha >= 255:
                self.transition_alpha = 255
                self.transition_state = "out"
        elif self.transition_state == "out":
            self.transition_alpha -= self.transition_speed
            if self.transition_alpha <= 0:
                self.transition_alpha = 0
                self.transition_state = "none"
        
        # ========================================
        # GAME STATE-SPECIFIC UPDATES
        # ========================================
        if self.state == "start_menu":
            # Title screen with animated dragon
            self.dragon.update()
            self.fire_timer += 1
            if self.fire_timer > 120:
                self.dragon.breathe_fire()
                self.fire_timer = 0
                
        elif self.state == "opening_cutscene":
            # Story introduction sequence
            next_state = self.opening_cutscene.update()
            if next_state:
                self.state = next_state
                
        elif self.state == "character_select":
            # Character selection screen (no updates needed)
            pass
                
        elif self.state == "overworld" and self.player:
            # Main gameplay area with movement and exploration
            self.game_time += 1
            self.spawn_timer += 1
            self.item_timer += 1
            self.movement_cooldown = max(0, self.movement_cooldown - 1)
            self.player.update_animation()
            
            # Update camera to follow player
            self.world_map.update_camera(self.player.x, self.player.y)
            
            # Update area transition effect
            self.world_map.update_transition()
            
            # Check for area transition
            if self.world_map.check_area_transition(self.player.x, self.player.y):
                # Area changed, update enemy and item lists
                current_area = self.world_map.get_current_area()
                self.enemies = current_area.enemies
                self.items = current_area.items
                
                # If entering town area, position player at the gate (4 squares lower)
                if current_area and current_area.area_type == "town":
                    area_world_x, area_world_y = current_area.get_world_position()
                    # Position at gate (center horizontally, 4 squares lower)
                    self.player.x = area_world_x + (AREA_WIDTH // 2)  # Center horizontally
                    self.player.y = area_world_y + 260  # 4 squares lower from top (200 + 60 = 260)
            
            # Add area-specific particle effects
            current_area = self.world_map.get_current_area()
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
                            self.particle_system.add_particle(
                                x, y, (255, 100, 0),
                                (random.uniform(-0.5, 0.5), random.uniform(-2, -0.5)),
                                6, 40
                            )
                    elif current_area.area_type == "ice":
                        # Snow particles
                        for _ in range(4):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (200, 220, 255),
                                (random.uniform(-0.3, 0.3), random.uniform(0.5, 1.5)),
                                4, 50
                            )
                    elif current_area.area_type == "swamp":
                        # Mist particles
                        for _ in range(3):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (150, 180, 150),
                                (random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)),
                                5, 60
                            )
                    elif current_area.area_type == "forest":
                        # Leaf particles
                        for _ in range(4):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (100, 150, 50),
                                (random.uniform(-0.3, 0.3), random.uniform(-0.5, -0.1)),
                                5, 45
                            )
                    elif current_area.area_type == "desert":
                        # Sand particles
                        for _ in range(6):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (200, 180, 120),
                                (random.uniform(-1, 1), random.uniform(-0.5, 0.5)),
                                4, 35
                            )
                    elif current_area.area_type == "mountain":
                        # Wind particles
                        for _ in range(3):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (180, 180, 200),
                                (random.uniform(-0.8, 0.8), random.uniform(-0.3, 0.3)),
                                4, 40
                            )
                    elif current_area.area_type == "beach":
                        # Sea foam particles
                        for _ in range(4):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (220, 240, 255),
                                (random.uniform(-0.4, 0.4), random.uniform(-0.2, 0.2)),
                                5, 55
                            )
                    elif current_area.area_type == "castle":
                        # Magic sparkles
                        for _ in range(3):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (255, 215, 0),
                                (random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)),
                                4, 50
                            )
                    elif current_area.area_type == "cave":
                        # Dust particles
                        for _ in range(2):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (100, 100, 120),
                                (random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)),
                                3, 70
                            )
                    elif current_area.area_type == "town":
                        # Town-specific particles (smoke, fountain, leaves)
                        current_area.generate_town_particles(self.particle_system)
                        
                        # Check for town entrance cutscene
                        if current_area.check_entrance_cutscene(self.player.x, self.player.y):
                            print("Town entrance cutscene triggered!")
                        
                        # Update town cutscene if active
                        current_area.update_cutscene()
            
            for item in self.items:
                item.update()
            if self.spawn_timer >= 300:
                self.spawn_enemy()
                self.spawn_timer = 0
            if self.item_timer >= 600:
                self.spawn_item()
                self.item_timer = 0
            for enemy in self.enemies:
                enemy.update(self.player.x, self.player.y)
                enemy.update_animation()
            # --- Check for boss battle after level up ---
            if (
                self.player.just_leveled_up and
                self.player.level > 1 and
                not self.player.boss_cooldown and
                self.player.level > self.player.last_boss_level
            ):
                # At level 10, spawn Malakor, else progressive boss
                if self.player.level == 10:
                    self.battle_screen = BattleScreen(self.player, BossDragon())
                else:
                    self.battle_screen = BattleScreen(self.player, DragonBoss(self.player.level))
                self.battle_screen.start_transition()
                self.state = "battle"
                self.player.boss_cooldown = True  # Prevent immediate retrigger
                self.player.just_leveled_up = False
                return
            for enemy in self.enemies[:]:
                if self.player:  # Ensure player exists
                    player_rect = pygame.Rect(self.player.x, self.player.y, PLAYER_SIZE, PLAYER_SIZE)
                    enemy_rect = pygame.Rect(enemy.x, enemy.y, ENEMY_SIZE, ENEMY_SIZE)
                    if player_rect.colliderect(enemy_rect):
                        self.battle_screen = BattleScreen(self.player, enemy)
                        self.battle_screen.start_transition()
                        self.state = "battle"
                        # Remove enemy from both lists
                        self.enemies.remove(enemy)
                        current_area = self.world_map.get_current_area()
                        if current_area and enemy in current_area.enemies:
                            current_area.enemies.remove(enemy)
                        self.player_moved = False
                        break
            for item in self.items[:]:
                if self.player:  # Ensure player exists
                    item_rect = pygame.Rect(item.x, item.y, ITEM_SIZE, ITEM_SIZE)
                    player_rect = pygame.Rect(self.player.x, self.player.y, PLAYER_SIZE, PLAYER_SIZE)
                    if player_rect.colliderect(item_rect):
                        if item.type == "health":
                            self.player.health = min(self.player.max_health, self.player.health + 30)
                            for _ in range(15):
                                x = random.randint(self.player.x, self.player.x + PLAYER_SIZE)
                                y = random.randint(self.player.y, self.player.y + PLAYER_SIZE)
                                self.particle_system.add_particle(
                                    x, y, HEALTH_COLOR,
                                    (random.uniform(-0.5, 0.5), random.uniform(-1, -0.5)),
                                    3, 30
                                )
                        else:
                            self.player.mana = min(self.player.max_mana, self.player.mana + 40)
                            for _ in range(15):
                                x = random.randint(self.player.x, self.player.x + PLAYER_SIZE)
                                y = random.randint(self.player.y, self.player.y + PLAYER_SIZE)
                                self.particle_system.add_particle(
                                    x, y, MANA_COLOR,
                                    (random.uniform(-0.5, 0.5), random.uniform(-1, -0.5)),
                                    3, 30
                                )
                        self.player.items_collected += 1
                        # Remove item from both lists
                        if item in self.items:
                            self.items.remove(item)
                        current_area = self.world_map.get_current_area()
                        if current_area and item in current_area.items:
                            current_area.items.remove(item)
    
    def draw(self, screen):
        screen.fill(BACKGROUND)
        
        # Draw starfield background
        for x, y, speed in self.starfield:
            alpha = min(255, int(speed * 100))
            pygame.draw.circle(screen, (200, 200, 255, alpha), (int(x), int(y)), 1)
        
        # Draw flying dragons
        for dragon in self.flying_dragons:
            wing_offset = math.sin(dragon['flap']) * dragon['size']
            color = (200, 200, 255, min(255, int(dragon['size'] * 40)))
            
            pygame.draw.line(
                screen, color,
                (dragon['x'], dragon['y']),
                (dragon['x'] + 5 * dragon['size'], dragon['y']),
                max(1, dragon['size'] // 2)
            )
            
            pygame.draw.line(
                screen, color,
                (dragon['x'] + 2 * dragon['size'], dragon['y']),
                (dragon['x'] + dragon['size'], dragon['y'] - 3 * dragon['size'] - wing_offset),
                max(1, dragon['size'] // 2)
            )
            pygame.draw.line(
                screen, color,
                (dragon['x'] + 2 * dragon['size'], dragon['y']),
                (dragon['x'] + dragon['size'], dragon['y'] + 3 * dragon['size'] + wing_offset),
                max(1, dragon['size'] // 2)
            )
            
            pygame.draw.line(
                screen, color,
                (dragon['x'] + 5 * dragon['size'], dragon['y']),
                (dragon['x'] + 7 * dragon['size'], dragon['y'] - dragon['size']),
                max(1, dragon['size'] // 2)
            )
            
            pygame.draw.line(
                screen, color,
                (dragon['x'], dragon['y']),
                (dragon['x'] - 2 * dragon['size'], dragon['y'] + dragon['size']),
                max(1, dragon['size'] // 2)
            )
        
        if self.state == "start_menu":
            if self.start_button.text != "START QUEST":
                self.start_button.text = "START QUEST"
                self.start_button.text_surf = font_medium.render(self.start_button.text, True, TEXT_COLOR)
                self.start_button.text_rect = self.start_button.text_surf.get_rect(center=self.start_button.rect.center)
            
            title = font_large.render("DRAGON'S LAIR", True, (255, 50, 50))
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
            
            subtitle = font_medium.render("A RETRO RPG ADVENTURE", True, TEXT_COLOR)
            screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 140))
            
            self.dragon.draw(screen)
            
            self.start_button.draw(screen)
            self.quit_button.draw(screen)
            
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
            
        elif self.state == "opening_cutscene":
            # Draw the opening cutscene
            self.opening_cutscene.draw(screen)
            
        elif self.state == "character_select":
            title = font_large.render("CHOOSE YOUR HERO", True, TEXT_COLOR)
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
            
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
            
            self.warrior_button.draw(screen)
            self.mage_button.draw(screen)
            self.rogue_button.draw(screen)
            self.back_button.draw(screen)
            
        elif self.state == "overworld" and self.player:
            # Draw world background
            current_area = self.world_map.get_current_area()
            if current_area:
                screen.fill(current_area.background_color)
                # Draw town if this is a town area
                if current_area.area_type == "town":
                    current_area.draw_town(screen)
            else:
                screen.fill(BACKGROUND)
            
            # Draw grid for current area
            for x in range(0, SCREEN_WIDTH, GRID_SIZE):
                pygame.draw.line(screen, current_area.grid_color if current_area else GRID_COLOR, 
                               (x, 0), (x, SCREEN_HEIGHT), 2)
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
                pygame.draw.line(screen, current_area.grid_color if current_area else GRID_COLOR, 
                               (0, y), (SCREEN_WIDTH, y), 2)
            
            # Draw area boundaries more prominently
            pygame.draw.rect(screen, (255, 255, 255), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 3)
            
            # Draw items (convert world coordinates to screen coordinates)
            for item in self.items:
                screen_x, screen_y = self.world_map.world_to_screen(item.x, item.y)
                if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
                    # Temporarily set item position for drawing
                    original_x, original_y = item.x, item.y
                    item.x, item.y = screen_x, screen_y
                    item.draw(screen)
                    item.x, item.y = original_x, original_y
                
            # Draw enemies (convert world coordinates to screen coordinates)
            for enemy in self.enemies:
                screen_x, screen_y = self.world_map.world_to_screen(enemy.x, enemy.y)
                if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
                    # Temporarily set enemy position for drawing
                    original_x, original_y = enemy.x, enemy.y
                    enemy.x, enemy.y = screen_x, screen_y
                    enemy.draw(screen)
                    enemy.x, enemy.y = original_x, original_y
            
            # Draw player (convert world coordinates to screen coordinates)
            screen_x, screen_y = self.world_map.world_to_screen(self.player.x, self.player.y)
            original_x, original_y = self.player.x, self.player.y
            self.player.x, self.player.y = screen_x, screen_y
            self.player.draw(screen)
            self.player.x, self.player.y = original_x, original_y
            
            # Draw player position indicator
            grid_x = (screen_x // GRID_SIZE) * GRID_SIZE
            grid_y = (screen_y // GRID_SIZE) * GRID_SIZE
            pygame.draw.rect(screen, (255, 255, 0), (grid_x, grid_y, GRID_SIZE, GRID_SIZE), 2)
            
            # Draw particles
            self.particle_system.draw(screen, self.world_map)
            
            # Draw area transition effect
            if self.world_map.transitioning:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, self.world_map.area_transition_alpha))
                screen.blit(overlay, (0, 0))
            
            # Draw world map overlay
            if self.show_world_map:
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
                        area = self.world_map.areas.get((x, y))
                        if area:
                            cell_x = map_x + x * cell_size
                            cell_y = map_y + y * cell_size
                            
                            # Color based on area type and visited status
                            if area == self.world_map.get_current_area():
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
                player_world_x, player_world_y = self.player.x, self.player.y
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
            
            # Draw UI panel
            pygame.draw.rect(screen, UI_BG, (10, 10, 250, 130), border_radius=8)
            pygame.draw.rect(screen, UI_BORDER, (10, 10, 250, 130), 3, border_radius=8)
            
            # Draw player stats
            self.player.draw_stats(screen, 20, 20)
            
            # Draw score and other info
            score_text = font_medium.render(f"SCORE: {self.score}", True, TEXT_COLOR)
            screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 20, 20))
            
            time_text = font_small.render(f"TIME: {self.game_time//FPS}s", True, TEXT_COLOR)
            screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 20, 60))
            
            kills_text = font_small.render(f"KILLS: {self.player.kills}", True, TEXT_COLOR)
            screen.blit(kills_text, (SCREEN_WIDTH - kills_text.get_width() - 20, 90))
            
            # Draw area information
            current_area = self.world_map.get_current_area()
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
                        area = self.world_map.areas.get((x, y))
                        if area and area.visited:
                            color = (100, 200, 100) if area == current_area else (50, 100, 50)
                            pygame.draw.rect(screen, color, 
                                           (mini_map_x + x * cell_size, mini_map_y + y * cell_size, 
                                            cell_size, cell_size))
                            pygame.draw.rect(screen, UI_BORDER, 
                                           (mini_map_x + x * cell_size, mini_map_y + y * cell_size, 
                                            cell_size, cell_size), 1)
            
            # Draw position info
            local_x = self.player.x % AREA_WIDTH
            local_y = self.player.y % AREA_HEIGHT
            grid_pos_x = local_x // GRID_SIZE
            grid_pos_y = local_y // GRID_SIZE
            pos_text = font_tiny.render(f"POS: ({grid_pos_x}, {grid_pos_y})", True, (255, 255, 0))
            screen.blit(pos_text, (20, SCREEN_HEIGHT - 180))
            
            # Draw town entrance cutscene if active
            current_area = self.world_map.get_current_area()
            if current_area and current_area.cutscene_active:
                current_area.draw_cutscene(screen)
            
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
            
        elif self.state == "battle" and self.battle_screen:
            self.battle_screen.draw(screen)
            
        elif self.state == "game_over" and self.player:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            
            title = font_large.render("GAME OVER", True, (255, 50, 50))
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
            
            stats = [
                f"HERO: {self.player.type}",
                f"LEVEL: {self.player.level}",
                f"SCORE: {self.score}",
                f"KILLS: {self.player.kills}",
                f"ITEMS: {self.player.items_collected}",
                f"TIME: {self.game_time//FPS} SECONDS"
            ]
            
            y_pos = 220
            for stat in stats:
                text = font_medium.render(stat, True, TEXT_COLOR)
                screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y_pos))
                y_pos += 40
                
            # Play again button
            self.start_button.text = "PLAY AGAIN"
            self.start_button.rect = pygame.Rect(SCREEN_WIDTH//2 - 120, y_pos + 20, 240, 60)
            self.start_button.text_surf = font_medium.render(self.start_button.text, True, TEXT_COLOR)
            self.start_button.text_rect = self.start_button.text_surf.get_rect(center=self.start_button.rect.center)
            self.start_button.draw(screen)
            
            # Back to menu button
            self.back_button.text = "BACK TO MENU"
            self.back_button.rect = pygame.Rect(SCREEN_WIDTH//2 - 120, y_pos + 100, 240, 60)
            self.back_button.text_surf = font_medium.render(self.back_button.text, True, TEXT_COLOR)
            self.back_button.text_rect = self.back_button.text_surf.get_rect(center=self.back_button.rect.center)
            self.back_button.draw(screen)
            
        if self.state in ["character_select", "game_over"]:
            self.back_button.draw(screen)
            
        if self.transition_state != "none":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self.transition_alpha))
            screen.blit(overlay, (0, 0))
            
        # Draw Android virtual controls if on Android
        if is_android() and self.android_buttons:
            # D-pad
            pygame.draw.rect(screen, (200,200,200), self.android_buttons['up'], border_radius=20)
            pygame.draw.polygon(screen, (100,100,100), [
                (self.android_buttons['up'].centerx, self.android_buttons['up'].top+15),
                (self.android_buttons['up'].left+15, self.android_buttons['up'].bottom-15),
                (self.android_buttons['up'].right-15, self.android_buttons['up'].bottom-15)
            ])
            pygame.draw.rect(screen, (200,200,200), self.android_buttons['down'], border_radius=20)
            pygame.draw.polygon(screen, (100,100,100), [
                (self.android_buttons['down'].centerx, self.android_buttons['down'].bottom-15),
                (self.android_buttons['down'].left+15, self.android_buttons['down'].top+15),
                (self.android_buttons['down'].right-15, self.android_buttons['down'].top+15)
            ])
            pygame.draw.rect(screen, (200,200,200), self.android_buttons['left'], border_radius=20)
            pygame.draw.polygon(screen, (100,100,100), [
                (self.android_buttons['left'].left+15, self.android_buttons['left'].centery),
                (self.android_buttons['left'].right-15, self.android_buttons['left'].top+15),
                (self.android_buttons['left'].right-15, self.android_buttons['left'].bottom-15)
            ])
            pygame.draw.rect(screen, (200,200,200), self.android_buttons['right'], border_radius=20)
            pygame.draw.polygon(screen, (100,100,100), [
                (self.android_buttons['right'].right-15, self.android_buttons['right'].centery),
                (self.android_buttons['right'].left+15, self.android_buttons['right'].top+15),
                (self.android_buttons['right'].left+15, self.android_buttons['right'].bottom-15)
            ])
            # Enter
            pygame.draw.rect(screen, (255,215,0), self.android_buttons['enter'], border_radius=20)
            enter_text = font_small.render('ENT', True, (0,0,0))
            screen.blit(enter_text, enter_text.get_rect(center=self.android_buttons['enter'].center))
            # Space
            pygame.draw.rect(screen, (0,255,255), self.android_buttons['space'], border_radius=20)
            space_text = font_small.render('SPC', True, (0,0,0))
            screen.blit(space_text, space_text.get_rect(center=self.android_buttons['space'].center))
        
        if self.state == "victory" and self.player:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 220))
            screen.blit(overlay, (0, 0))
            title = font_large.render("YOU WIN!", True, (255, 255, 0))
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
            stats = [
                f"HERO: {self.player.type}",
                f"LEVEL: {self.player.level}",
                f"SCORE: {self.score}",
                f"KILLS: {self.player.kills}",
                f"ITEMS: {self.player.items_collected}",
                f"TIME: {self.game_time//FPS} SECONDS"
            ]
            y_pos = 240
            for stat in stats:
                text = font_medium.render(stat, True, TEXT_COLOR)
                screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y_pos))
                y_pos += 40
            win_text = font_medium.render("Congratulations! You defeated Malakor!", True, (255, 215, 0))
            screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, y_pos + 40))
            
            # Play again button
            self.start_button.text = "PLAY AGAIN"
            self.start_button.rect = pygame.Rect(SCREEN_WIDTH//2 - 120, y_pos + 80, 240, 60)
            self.start_button.text_surf = font_medium.render(self.start_button.text, True, TEXT_COLOR)
            self.start_button.text_rect = self.start_button.text_surf.get_rect(center=self.start_button.rect.center)
            self.start_button.draw(screen)
            
            # Back to menu button
            self.back_button.text = "BACK TO MENU"
            self.back_button.rect = pygame.Rect(SCREEN_WIDTH//2 - 120, y_pos + 160, 240, 60)
            self.back_button.text_surf = font_medium.render(self.back_button.text, True, TEXT_COLOR)
            self.back_button.text_rect = self.back_button.text_surf.get_rect(center=self.back_button.rect.center)
            self.back_button.draw(screen)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True
                    # Android virtual controls
                    if is_android() and self.android_buttons:
                        mx, my = event.pos
                        for name, rect in self.android_buttons.items():
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
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "overworld":
                            self.state = "game_over"
                        elif self.state == "game_over":
                            self.state = "start_menu"
                        elif self.state == "character_select":
                            self.state = "start_menu"
                        elif self.state == "opening_cutscene":
                            self.opening_cutscene.skip()
                    
                    # Handle skip for cutscene
                    if self.state == "opening_cutscene":
                        self.opening_cutscene.skip()
                    
                    # Handle world map toggle
                    if self.state == "overworld" and event.key == pygame.K_m:
                        self.show_world_map = not self.show_world_map
                    
                    # Handle movement in overworld
                    if self.state == "overworld" and self.player and self.movement_cooldown <= 0:
                        # Store original position for collision detection
                        original_x = self.player.x
                        original_y = self.player.y
                        
                        if event.key in [pygame.K_UP, pygame.K_w]:
                            if self.SFX_ARROW: self.SFX_ARROW.play()
                            self.player.move(0, -1)
                            # Check collision and revert if needed
                            current_area = self.world_map.get_current_area()
                            if current_area and current_area.check_building_collision(self.player.x, self.player.y):
                                self.player.x = original_x
                                self.player.y = original_y
                            else:
                                self.player_moved = True
                                self.movement_cooldown = self.movement_delay
                        elif event.key in [pygame.K_DOWN, pygame.K_s]:
                            if self.SFX_ARROW: self.SFX_ARROW.play()
                            self.player.move(0, 1)
                            # Check collision and revert if needed
                            current_area = self.world_map.get_current_area()
                            if current_area and current_area.check_building_collision(self.player.x, self.player.y):
                                self.player.x = original_x
                                self.player.y = original_y
                            else:
                                self.player_moved = True
                                self.movement_cooldown = self.movement_delay
                        elif event.key in [pygame.K_LEFT, pygame.K_a]:
                            if self.SFX_ARROW: self.SFX_ARROW.play()
                            self.player.move(-1, 0)
                            # Check collision and revert if needed
                            current_area = self.world_map.get_current_area()
                            if current_area and current_area.check_building_collision(self.player.x, self.player.y):
                                self.player.x = original_x
                                self.player.y = original_y
                            else:
                                self.player_moved = True
                                self.movement_cooldown = self.movement_delay
                        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                            if self.SFX_ARROW: self.SFX_ARROW.play()
                            self.player.move(1, 0)
                            # Check collision and revert if needed
                            current_area = self.world_map.get_current_area()
                            if current_area and current_area.check_building_collision(self.player.x, self.player.y):
                                self.player.x = original_x
                                self.player.y = original_y
                            else:
                                self.player_moved = True
                                self.movement_cooldown = self.movement_delay
                    
                    # Handle town cutscene dialogue advancement
                    if self.state == "overworld" and event.key == pygame.K_SPACE:
                        current_area = self.world_map.get_current_area()
                        if current_area and current_area.cutscene_active and current_area.guard:
                            # Advance dialogue
                            current_area.guard["current_dialogue"] += 1
                            current_area.cutscene_timer = 0
                            
                            # Check if we've reached the end of dialogue
                            if current_area.guard["current_dialogue"] >= len(current_area.guard["dialogue"]):
                                current_area.cutscene_phase = 2  # End cutscene
                    
                    # Pass input to battle screen
                    if self.state == "battle" and self.battle_screen:
                        self.battle_screen.handle_input(event, self)
            
            # Handle button clicks
            if self.state == "start_menu":
                self.start_button.update(mouse_pos)
                self.quit_button.update(mouse_pos)
                
                if self.start_button.is_clicked(mouse_pos, mouse_click):
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    self.state = "opening_cutscene"
                    self.opening_cutscene = OpeningCutscene()  # Reset cutscene
                    
                if self.quit_button.is_clicked(mouse_pos, mouse_click):
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    running = False
                    
            elif self.state == "character_select":
                self.warrior_button.update(mouse_pos)
                self.mage_button.update(mouse_pos)
                self.rogue_button.update(mouse_pos)
                self.back_button.update(mouse_pos)
                
                if self.warrior_button.is_clicked(mouse_pos, mouse_click):
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    self.player = Character("Warrior")
                    self.state = "overworld"
                    self.start_game()
                    
                if self.mage_button.is_clicked(mouse_pos, mouse_click):
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    self.player = Character("Mage")
                    self.state = "overworld"
                    self.start_game()
                    
                if self.rogue_button.is_clicked(mouse_pos, mouse_click):
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    self.player = Character("Rogue")
                    self.state = "overworld"
                    self.start_game()
                    
                if self.back_button.is_clicked(mouse_pos, mouse_click):
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    self.state = "start_menu"
                    
            elif self.state == "overworld":
                pass
                    
            elif self.state == "battle":
                battle_ended = self.battle_screen.update()
                
                if battle_ended:
                    # Boss battle win
                    if hasattr(self.battle_screen.enemy, 'enemy_type') and "boss_dragon" in self.battle_screen.enemy.enemy_type:
                        if self.battle_screen.result == "win":
                            self.player.just_leveled_up = False
                            self.player.kills += 1
                            self.player.gain_exp(45)  # Boss gives more exp than regular enemies (25)
                            self.score += 25  # Boss gives more score too
                            self.player.boss_cooldown = True  # Set cooldown after boss battle
                            self.player.last_boss_level = self.player.level  # Set after the fight
                            if self.battle_screen.enemy.enemy_type == "boss_dragon":
                                self.boss_defeated = True
                                self.state = "victory"
                                self.battle_screen = None
                                self.music.update(self.state, False)  # Explicitly reset music state
                            else:
                                print(f"Boss battle ended - transitioning to overworld")
                                self.state = "overworld"
                                self.battle_screen = None
                                self.music.update(self.state, False)  # Explicitly reset music state
                            continue
                        elif self.battle_screen.result == "lose":
                            self.state = "game_over"
                            self.battle_screen = None
                            self.music.update(self.state, False)  # Explicitly reset music state
                            continue
                        elif self.battle_screen.result == "escape":
                            self.player.exp = 0
                            self.player.just_leveled_up = False
                            self.player.boss_cooldown = True  # Set cooldown after boss battle
                            self.player.last_boss_level = self.player.level  # Set after the fight
                            print(f"Boss battle escaped - transitioning to overworld")
                            self.state = "overworld"
                            self.battle_screen = None
                            self.music.update(self.state, False)  # Explicitly reset music state
                            continue
                    else:
                        if self.battle_screen.result == "win":
                            self.player.kills += 1
                            self.player.gain_exp(25)
                            self.score += 10
                            self.start_transition()
                            print(f"Battle ended - transitioning to overworld")
                            self.state = "overworld"
                            self.battle_screen = None
                            self.music.update(self.state, False)  # Explicitly reset music state
                        elif self.battle_screen.result == "lose":
                            self.state = "game_over"
                            self.battle_screen = None
                            self.music.update(self.state, False)  # Explicitly reset music state
                        elif self.battle_screen.result == "escape":
                            self.player.exp = 0
                            self.player.just_leveled_up = False
                            print(f"Battle escaped - transitioning to overworld")
                            self.state = "overworld"
                            self.battle_screen = None
                            self.music.update(self.state, False)  # Explicitly reset music state
                            continue
            
            elif self.state == "game_over":
                self.start_button.update(mouse_pos)
                self.back_button.update(mouse_pos)
                
                if self.start_button.is_clicked(mouse_pos, mouse_click):
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    self.state = "character_select"
                    
                if self.back_button.is_clicked(mouse_pos, mouse_click):
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    self.state = "start_menu"
                    
            elif self.state == "victory":
                self.start_button.update(mouse_pos)
                self.back_button.update(mouse_pos)
                
                if self.start_button.is_clicked(mouse_pos, mouse_click):
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    self.state = "character_select"
                    
                if self.back_button.is_clicked(mouse_pos, mouse_click):
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    self.state = "start_menu"
            
            self.update()
            self.draw(screen)
            
            # Handle victory music completion
            if self.state == "victory" and not pygame.mixer.music.get_busy():
                # After victory music plays once, return to menu
                self.state = "start_menu"
                self.music.update(self.state)
            
            clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
    
    def start_game(self):
        # Reset game state for a new game
        self.enemies = []
        self.items = []
        self.score = 0
        self.game_time = 0
        self.spawn_timer = 0
        self.item_timer = 0
        self.player_moved = False
        self.movement_cooldown = 0
        self.boss_battle_triggered = False
        self.boss_defeated = False
        
        # Reset world map
        self.world_map = WorldMap()
        
        # Position player in center area (1,1) at center position
        if self.player:
            self.player.x = AREA_WIDTH + (AREA_WIDTH // 2)
            self.player.y = AREA_HEIGHT + (AREA_HEIGHT // 2)
        
        # Spawn initial enemies and items in starting area
        for _ in range(3):
            self.spawn_enemy()
        for _ in range(2):
            self.spawn_item()

# ============================================================================
# MUSIC SYSTEM - Procedural Chiptune Music Generation
# ============================================================================
class MusicSystem:
    """
    Generates dynamic chiptune music that changes based on game state.
    Creates different musical themes for different areas and situations.
    
    Music Types:
    - Start Menu: Epic title theme
    - Overworld: Calm adventure theme
    - Town: Peaceful town theme
    - Battle: Intense combat theme
    - Boss Battle: Epic boss theme
    - Victory: Triumphant victory theme
    - Game Over: Somber ending theme
    """
    def __init__(self):
        self.current_track = None
        self.last_state = None
        self.boss_battle_active = False
        
        try:
            # Store raw bytes instead of BytesIO objects
            self.start_menu_music_bytes = self.sound_to_wav_bytes(self.generate_start_menu_music())
            self.overworld_music_bytes = self.sound_to_wav_bytes(self.generate_overworld_music())
            self.town_music_bytes = self.sound_to_wav_bytes(self.generate_town_music())
            self.battle_music_bytes = self.sound_to_wav_bytes(self.generate_battle_music())
            self.boss_music_bytes = self.sound_to_wav_bytes(self.generate_boss_music())
            self.victory_music_bytes = self.sound_to_wav_bytes(self.generate_victory_music())
            self.game_over_music_bytes = self.sound_to_wav_bytes(self.generate_game_over_music())
            print('Music bytes created successfully')
        except Exception as e:
            print(f"Failed to create music bytes: {e}")
            self.start_menu_music_bytes = self.overworld_music_bytes = self.battle_music_bytes = None
            self.boss_music_bytes = self.victory_music_bytes = self.game_over_music_bytes = None
    
    def generate_start_menu_music(self):
        # Epic title screen theme
        melody = [
            (523.25, 0.5), (659.25, 0.5), (783.99, 0.5), (987.77, 0.5),  # C5, E5, G5, B5
            (880.00, 0.5), (783.99, 0.5), (659.25, 0.5), (523.25, 0.5),  # A5, G5, E5, C5
            (440.00, 0.5), (523.25, 0.5), (659.25, 0.5), (783.99, 0.5),  # A4, C5, E5, G5
            (659.25, 0.5), (523.25, 0.5), (440.00, 0.5), (392.00, 0.5)   # E5, C5, A4, G4
        ] * 2
        
        bass = [
            (130.81, 1), (146.83, 1), (164.81, 1), (174.61, 1),  # C3, D3, E3, F3
            (196.00, 1), (220.00, 1), (246.94, 1), (261.63, 1)   # G3, A3, B3, C4
        ] * 2
        
        percussion = [
            (200, 0.5), (0, 0.5), (150, 0.5), (0, 0.5),  # Slow dramatic drums
            (200, 0.5), (0, 0.5), (150, 0.5), (0, 0.5)
        ] * 4
        
        return self.generate_chiptune_song(melody, bass, percussion=percussion, bpm=80, volume=0.25)
    
    def sound_to_wav_bytes(self, sound):
        try:
            arr = pygame.sndarray.array(sound)
            memfile = io.BytesIO()
            with wave.open(memfile, 'wb') as wf:
                wf.setnchannels(2)
                wf.setsampwidth(2)  # 16 bits
                wf.setframerate(44100)
                wf.writeframes(arr.astype(np.int16).tobytes())
            return memfile.getvalue()  # Return the bytes content
        except Exception as e:
            print(f"Error converting sound to WAV: {e}")
            return None
    def update(self, game_state, is_boss_battle=False, current_area=None):
        # Only update when state or boss battle status changes
        if game_state == self.last_state and is_boss_battle == self.boss_battle_active:
            return
        
        print(f'MusicSystem: State change detected! "{self.last_state}" -> "{game_state}", boss: {self.boss_battle_active} -> {is_boss_battle}')
        self.last_state = game_state
        self.boss_battle_active = is_boss_battle
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(0.5)
        
        try:
            if game_state == "start_menu" and self.start_menu_music_bytes:
                print('MusicSystem: Playing start menu music')
                pygame.mixer.music.load(io.BytesIO(self.start_menu_music_bytes))
                pygame.mixer.music.play(-1)
            elif game_state == "opening_cutscene" and self.start_menu_music_bytes:
                print('MusicSystem: Playing cutscene music')
                pygame.mixer.music.load(io.BytesIO(self.start_menu_music_bytes))
                pygame.mixer.music.play(-1)
            elif game_state == "character_select" and self.start_menu_music_bytes:
                print('MusicSystem: Playing character select music')
                pygame.mixer.music.load(io.BytesIO(self.start_menu_music_bytes))
                pygame.mixer.music.play(-1)
            elif game_state == "overworld":
                # Check if we're in a town area
                if current_area and current_area.area_type == "town" and self.town_music_bytes:
                    print('MusicSystem: Playing town music')
                    pygame.mixer.music.load(io.BytesIO(self.town_music_bytes))
                    pygame.mixer.music.play(-1)
                elif self.overworld_music_bytes:
                    print('MusicSystem: Playing overworld music')
                    pygame.mixer.music.load(io.BytesIO(self.overworld_music_bytes))
                    pygame.mixer.music.play(-1)
            elif game_state == "battle":
                if is_boss_battle and self.boss_music_bytes:
                    print('MusicSystem: Playing boss music')
                    pygame.mixer.music.load(io.BytesIO(self.boss_music_bytes))
                    pygame.mixer.music.play(-1)
                elif self.battle_music_bytes:
                    print('MusicSystem: Playing battle music')
                    pygame.mixer.music.load(io.BytesIO(self.battle_music_bytes))
                    pygame.mixer.music.play(-1)
                else:
                    print('MusicSystem: WARNING - No battle music available!')
            elif game_state == "victory" and self.victory_music_bytes:
                print('MusicSystem: Playing victory music')
                pygame.mixer.music.load(io.BytesIO(self.victory_music_bytes))
                pygame.mixer.music.play(0)
            elif game_state == "game_over" and self.game_over_music_bytes:
                print('MusicSystem: Playing game over music')
                pygame.mixer.music.load(io.BytesIO(self.game_over_music_bytes))
                pygame.mixer.music.play(0)
            else:
                print(f'MusicSystem: No music for state: {game_state}')
        except Exception as e:
            print(f"Music playback error: {e}")
    def generate_overworld_music(self):
        # Calm adventure theme
        melody = [
            (440, 0.5), (523.25, 0.5), (659.25, 0.5), (783.99, 0.5),  # A4, C5, E5, G5
            (659.25, 0.5), (523.25, 0.5), (440, 1),                   # E5, C5, A4
            (392, 0.5), (493.88, 0.5), (587.33, 0.5), (698.46, 0.5),  # G4, B4, D5, F5
            (659.25, 0.5), (587.33, 0.5), (523.25, 1)                 # E5, D5, C5
        ]
        bass = [
            (130.81, 1), (146.83, 1), (164.81, 1), (174.61, 1),  # C3, D3, E3, F3
            (196.00, 1), (220.00, 1), (246.94, 1), (261.63, 1)   # G3, A3, B3, C4
        ]
        return self.generate_chiptune_song(melody, bass, bpm=90, volume=0.2)
    
    def generate_town_music(self):
        # Peaceful town theme with bells and gentle melody
        melody = [
            (523.25, 0.5), (587.33, 0.5), (659.25, 0.5), (698.46, 0.5),  # C5, D5, E5, F5
            (783.99, 0.5), (698.46, 0.5), (659.25, 0.5), (587.33, 0.5),  # G5, F5, E5, D5
            (523.25, 0.5), (493.88, 0.5), (440.00, 0.5), (392.00, 0.5),  # C5, B4, A4, G4
            (440.00, 0.5), (493.88, 0.5), (523.25, 1.0)                  # A4, B4, C5
        ]
        bass = [
            (261.63, 1.0), (293.66, 1.0), (329.63, 1.0), (349.23, 1.0),  # C4, D4, E4, F4
            (392.00, 1.0), (440.00, 1.0), (493.88, 1.0), (523.25, 1.0)   # G4, A4, B4, C5
        ]
        percussion = [
            (50, 0.5), (0, 0.5), (30, 0.5), (0, 0.5),  # Gentle bell-like rhythm
            (50, 0.5), (0, 0.5), (30, 0.5), (0, 0.5)
        ]
        lead = [
            (784.00, 0.25), (0, 0.25), (880.00, 0.25), (0, 0.25),  # G5, rest, A5, rest
            (987.77, 0.25), (0, 0.25), (1046.50, 0.25), (0, 0.25),  # B5, rest, C6, rest
            (880.00, 0.25), (0, 0.25), (784.00, 0.25), (0, 0.25),  # A5, rest, G5, rest
            (659.25, 0.25), (0, 0.25), (587.33, 0.25), (0, 0.25)   # E5, rest, D5, rest
        ]
        return self.generate_chiptune_song(melody, bass, percussion, lead, bpm=120, volume=0.15)
    def generate_battle_music(self):
        # Intense battle theme
        melody = [
            (587.33, 0.25), (659.25, 0.25), (783.99, 0.25), (659.25, 0.25),  # D5, E5, G5, E5
            (587.33, 0.25), (523.25, 0.25), (493.88, 0.25), (440, 0.25),     # D5, C5, B4, A4
            (392, 0.25), (440, 0.25), (493.88, 0.25), (587.33, 0.25),        # G4, A4, B4, D5
            (659.25, 0.25), (587.33, 0.25), (523.25, 0.25), (493.88, 0.25)   # E5, D5, C5, B4
        ] * 2
        bass = [
            (98.00, 0.5), (110.00, 0.5), (123.47, 0.5), (130.81, 0.5),  # G2, A2, B2, C3
            (146.83, 0.5), (164.81, 0.5), (185.00, 0.5), (196.00, 0.5)   # D3, E3, F#3, G3
        ] * 2
        percussion = [
            (150, 0.25), (0, 0.25), (100, 0.25), (0, 0.25),  # Kick, rest, snare, rest
            (150, 0.25), (0, 0.25), (100, 0.25), (0, 0.25)
        ] * 4
        return self.generate_chiptune_song(melody, bass, percussion=percussion, bpm=140, volume=0.25)
    def generate_boss_music(self):
        # Epic boss battle theme
        melody = [
            (220, 0.25), (261.63, 0.25), (329.63, 0.25), (392.00, 0.25),  # A3, C4, E4, G4
            (493.88, 0.25), (392.00, 0.25), (329.63, 0.25), (261.63, 0.25),  # B4, G4, E4, C4
            (293.66, 0.25), (349.23, 0.25), (440.00, 0.25), (523.25, 0.25),  # D4, F4, A4, C5
            (659.25, 0.25), (523.25, 0.25), (440.00, 0.25), (349.23, 0.25)   # E5, C5, A4, F4
        ] * 2
        bass = [
            (82.41, 0.5), (87.31, 0.5), (92.50, 0.5), (98.00, 0.5),  # E2, F2, F#2, G2
            (110.00, 0.5), (123.47, 0.5), (138.59, 0.5), (146.83, 0.5)  # A2, B2, C#3, D3
        ] * 2
        percussion = [
            (200, 0.125), (0, 0.125), (150, 0.125), (0, 0.125),  # Fast drums
            (100, 0.125), (0, 0.125), (150, 0.125), (0, 0.125),
            (200, 0.125), (0, 0.125), (150, 0.125), (0, 0.125),
            (100, 0.125), (0, 0.125), (150, 0.125), (200, 0.125)
        ] * 2
        lead = [
            (523.25, 0.25), (0, 0.25), (659.25, 0.25), (0, 0.25),  # C5, rest, E5, rest
            (783.99, 0.25), (0, 0.25), (987.77, 0.25), (0, 0.25),  # G5, rest, B5, rest
            (880.00, 0.25), (0, 0.25), (698.46, 0.25), (0, 0.25),  # A5, rest, F5, rest
            (587.33, 0.25), (0, 0.25), (493.88, 0.25), (0, 0.25)   # D5, rest, B4, rest
        ]
        return self.generate_chiptune_song(melody, bass, percussion, lead, bpm=160, volume=0.3)
    def generate_victory_music(self):
        # Triumphant victory theme
        melody = [
            (659.25, 0.3), (783.99, 0.3), (987.77, 0.3), (880.00, 0.5),  # E5, G5, B5, A5
            (0, 0.2), (783.99, 0.3), (880.00, 0.3), (1046.50, 0.5),      # rest, G5, A5, C6
            (0, 0.2), (987.77, 0.3), (1174.66, 0.3), (1318.51, 1.0)      # rest, B5, D6, E6
        ]
        bass = [
            (261.63, 0.5), (329.63, 0.5), (392.00, 0.5), (523.25, 0.5),  # C4, E4, G4, C5
            (392.00, 0.5), (523.25, 0.5), (659.25, 0.5), (783.99, 1.0)   # G4, C5, E5, G5
        ]
        percussion = [
            (300, 0.1), (0, 0.1), (400, 0.1), (0, 0.1),  # Fast drum roll
            (500, 0.1), (0, 0.1), (600, 0.1), (0, 0.1),
            (700, 0.5)  # Cymbal crash
        ]
        return self.generate_chiptune_song(melody, bass, percussion, bpm=120, volume=0.3)
    def generate_game_over_music(self):
        # Somber game over theme
        melody = [
            (261.63, 1.0), (246.94, 1.0), (220.00, 1.0), (196.00, 2.0),  # C4, B3, A3, G3
            (174.61, 1.0), (164.81, 1.0), (146.83, 1.0), (130.81, 2.0)   # F3, E3, D3, C3
        ]
        bass = [
            (65.41, 2.0), (61.74, 2.0), (55.00, 2.0), (49.00, 4.0),  # C2, B1, A1, G1
            (43.65, 2.0), (41.20, 2.0), (36.71, 2.0), (32.70, 4.0)   # F1, E1, D1, C1
        ]
        return self.generate_chiptune_song(melody, bass, bpm=60, volume=0.25)
    def generate_chiptune_song(self, melody, bass, percussion=None, lead=None, bpm=220, volume=0.16):
        """
        Core chiptune generation algorithm that combines multiple musical tracks.
        
        Args:
            melody: List of (frequency, duration) tuples for main melody
            bass: List of (frequency, duration) tuples for bass line
            percussion: Optional list of (frequency, duration) tuples for drums
            lead: Optional list of (frequency, duration) tuples for lead synth
            bpm: Beats per minute for tempo
            volume: Overall volume level (0.0 to 1.0)
        """
        melody = [list(note) for note in melody]
        bass = [list(note) for note in bass]
        if percussion is not None:
            percussion = [list(note) for note in percussion]
        if lead is not None:
            lead = [list(note) for note in lead]
        song = np.zeros((0, 2), dtype=np.int16)
        melody_idx = bass_idx = perc_idx = lead_idx = 0
        melody_len = len(melody)
        bass_len = len(bass)
        perc_len = len(percussion) if percussion is not None else 0
        lead_len = len(lead) if lead is not None else 0
        while (melody_idx < melody_len or bass_idx < bass_len or
               (percussion is not None and perc_idx < perc_len) or
               (lead is not None and lead_idx < lead_len)):
            if melody_idx < melody_len:
                m_freq, m_beats = melody[melody_idx]
            else:
                m_freq, m_beats = 0, 0.25
            if bass_idx < bass_len:
                b_freq, b_beats = bass[bass_idx]
            else:
                b_freq, b_beats = 0, 0.25
            if percussion is not None and perc_idx < perc_len:
                p_freq, p_beats = percussion[perc_idx]
            else:
                p_freq, p_beats = 0, 0.25
            if lead is not None and lead_idx < lead_len:
                l_freq, l_beats = lead[lead_idx]
            else:
                l_freq, l_beats = 0, 0.25
            step_beats = min(m_beats, b_beats, p_beats, l_beats)
            step_duration = 60 / bpm * step_beats
            t = np.linspace(0, step_duration, int(44100 * step_duration), False)
            # Generate waves
            m_wave = np.sin(m_freq * 2 * np.pi * t) if m_freq > 0 else np.zeros_like(t)
            b_wave = 0.25 * np.sign(np.sin(b_freq * 2 * np.pi * t)) if b_freq > 0 else np.zeros_like(t)
            p_wave = 0.18 * np.sign(np.sin(p_freq * 2 * np.pi * t)) if percussion is not None and p_freq > 0 else np.zeros_like(t)
            l_wave = 0.18 * np.sin(l_freq * 2 * np.pi * t) if lead is not None and l_freq > 0 else np.zeros_like(t)
            # Combine waves
            wave = m_wave + b_wave + p_wave + l_wave
            wave = np.clip(wave, -1, 1)
            # Convert to audio
            audio = (wave * volume * 32767).astype(np.int16)
            audio_stereo = np.column_stack((audio, audio))
            song = np.concatenate((song, audio_stereo))
            # Update note durations
            if melody_idx < melody_len:
                melody[melody_idx][1] -= step_beats
                if melody[melody_idx][1] <= 0:
                    melody_idx += 1
            if bass_idx < bass_len:
                bass[bass_idx][1] -= step_beats
                if bass[bass_idx][1] <= 0:
                    bass_idx += 1
            if percussion is not None and perc_idx < perc_len:
                percussion[perc_idx][1] -= step_beats
                if percussion[perc_idx][1] <= 0:
                    perc_idx += 1
            if lead is not None and lead_idx < lead_len:
                lead[lead_idx][1] -= step_beats
                if lead[lead_idx][1] <= 0:
                    lead_idx += 1
        return pygame.sndarray.make_sound(song)

# --- DragonBoss: Progressive boss for each level ---
DRAGON_BOSS_COLORS = [
    ((255, 69, 0), (255, 140, 0)),      # Red-Orange
    ((0, 191, 255), (0, 255, 255)),    # Blue-Cyan
    ((50, 205, 50), (124, 252, 0)),    # Green-Lime
    ((148, 0, 211), (255, 0, 255)),    # Purple-Magenta
    ((255, 215, 0), (255, 255, 0)),    # Gold-Yellow
    ((255, 20, 147), (255, 105, 180)), # Pink
    ((255, 255, 255), (200, 200, 200)),# White-Grey
    ((255, 99, 71), (255, 160, 122)),  # Tomato-Salmon
    ((70, 130, 180), (176, 224, 230)), # SteelBlue-PowderBlue
    ((139, 69, 19), (222, 184, 135)),  # Brown-Tan
]

# ============================================================================
# BOSS ENEMY CLASSES - Special enemies with unique abilities
# ============================================================================
class DragonBoss(Enemy):
    """
    Special boss enemy with enhanced abilities and unique visual effects.
    More powerful than regular enemies with special attack patterns.
    """
    def __init__(self, boss_level):
        super().__init__(player_level=5 + boss_level * 2)
        self.size = 120
        self.x = 700
        self.y = 180
        self.enemy_type = f"boss_dragon_{boss_level}"
        self.name = f"Dragon Boss Lv.{boss_level}"
        # Stat scaling
        self.health = self.max_health = 200 + boss_level * 60
        self.strength = 18 + boss_level * 4
        self.speed = 6 + boss_level // 2
        # Color cycling
        color_idx = (boss_level - 1) % len(DRAGON_BOSS_COLORS)
        self.dragon_color, self.fire_color = DRAGON_BOSS_COLORS[color_idx]
        self.color = self.dragon_color
        self.movement_cooldown = 0
        self.movement_delay = 40
        self.animation_offset = 0
        self.attack_animation = 0
        self.hit_animation = 0
        self.fire_breathing = False
        self.fire_breath_timer = 0
    def start_attack_animation(self):
        self.attack_animation = 20
        self.fire_breathing = True
        self.fire_breath_timer = 20
    def update_animation(self):
        self.animation_offset = math.sin(pygame.time.get_ticks() * 0.005) * 2
        if self.attack_animation > 0:
            self.attack_animation -= 1
        if self.hit_animation > 0:
            self.hit_animation -= 1
        if self.fire_breathing:
            self.fire_breath_timer -= 1
            if self.fire_breath_timer <= 0:
                self.fire_breathing = False
    def draw(self, surface):
        offset_x = 0
        offset_y = self.animation_offset
        if self.attack_animation > 0:
            offset_x = 10 * math.sin(self.attack_animation * 0.2)
        if self.hit_animation > 0:
            offset_x = random.randint(-4, 4)
            offset_y = random.randint(-4, 4)
        x = self.x + offset_x
        y = self.y + offset_y
        # --- Draw a more dragon-like boss, facing left ---
        # Body
        pygame.draw.ellipse(surface, self.dragon_color, (x, y + 60, 180, 60))
        # Tail
        pygame.draw.polygon(surface, (200, 50, 50), [
            (x + 180, y + 90), (x + 240, y + 80), (x + 180, y + 110)
        ])
        # Legs
        pygame.draw.rect(surface, (120, 40, 20), (x + 120, y + 110, 18, 30), border_radius=8)
        pygame.draw.rect(surface, (120, 40, 20), (x + 40, y + 110, 18, 30), border_radius=8)
        # Claws
        pygame.draw.polygon(surface, (255, 255, 255), [
            (x + 120, y + 140), (x + 118, y + 150), (x + 124, y + 150)
        ])
        pygame.draw.polygon(surface, (255, 255, 255), [
            (x + 40, y + 140), (x + 38, y + 150), (x + 44, y + 150)
        ])
        # Wings (bat-like, flipped)
        wing_y = y + 60
        pygame.draw.polygon(surface, (180, 50, 50), [
            (x + 120, wing_y), (x + 170, wing_y - 60), (x + 60, wing_y - 80), (x + 10, wing_y - 40), (x + 60, wing_y)
        ])
        pygame.draw.polygon(surface, (180, 50, 50), [
            (x + 60, wing_y), (x + 10, wing_y - 60), (x, wing_y - 20), (x + 20, wing_y + 10)
        ])
        # Head (distinct, with open mouth, facing left)
        head_x = x - 40
        head_y = y + 70
        pygame.draw.ellipse(surface, self.dragon_color, (head_x, head_y, 60, 40))
        # Jaw (open)
        pygame.draw.polygon(surface, (200, 50, 50), [
            (head_x + 20, head_y + 30), (head_x, head_y + 50), (head_x + 5, head_y + 35), (head_x + 10, head_y + 30)
        ])
        # Teeth
        for i in range(3):
            pygame.draw.polygon(surface, (255, 255, 255), [
                (head_x + 12 + i*6, head_y + 38), (head_x + 10 + i*6, head_y + 45), (head_x + 14 + i*6, head_y + 38)
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
        # Eye
        pygame.draw.circle(surface, (255, 255, 255), (head_x + 15, head_y + 15), 7)
        pygame.draw.circle(surface, (0, 0, 0), (head_x + 13, head_y + 15), 3)
        # Fire breath animation (large cone from mouth to player, facing left)
        if self.fire_breathing:
            mouth_x = head_x - 10
            mouth_y = head_y + 40
            player_x = 200 + 25
            player_y = 300 + 25
            for i in range(30):
                t = i / 30
                fx = int(mouth_x * (1-t) + player_x * t + random.randint(-10, 10))
                fy = int(mouth_y * (1-t) + player_y * t + random.randint(-10, 10))
                size = int(10 * (1-t) + 40 * t)
                # Use the boss's fire color, fade alpha
                base = self.fire_color
                color = (base[0], base[1], base[2], max(0, 200 - i * 6))
                fire_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(fire_surf, color, (size, size), size)
                surface.blit(fire_surf, (fx - size, fy - size))
        # Health bar (with HP numbers)
        bar_width = 120
        bar_x = x + 60
        bar_y = y + 20
        pygame.draw.rect(surface, (20, 20, 30), (bar_x, bar_y, bar_width, 16), border_radius=2)
        health_width = (bar_width - 2) * (self.health / self.max_health)
        pygame.draw.rect(surface, HEALTH_COLOR, (bar_x + 1, bar_y + 1, health_width, 14), border_radius=2)
        # HP numbers
        hp_text = font_small.render(f"{self.health}/{self.max_health}", True, (255,255,255))
        hp_rect = hp_text.get_rect(center=(bar_x + bar_width//2, bar_y + 8))
        surface.blit(hp_text, hp_rect)
        # Name
        name_text = font_medium.render(self.name, True, (255, 215, 0))
        name_rect = name_text.get_rect(midtop=(x + 120, y - 10))
        surface.blit(name_text, name_rect)

# Place BossDragon right after DragonBoss for proper definition order
# --- DragonBoss: Progressive boss for each level ---
# ... existing code for DragonBoss ...

class BossDragon(Enemy):
    """
    Final boss enemy with the most powerful abilities and unique visual design.
    Represents the ultimate challenge in the game.
    """
    def __init__(self):
        super().__init__(player_level=10)
        self.size = 120
        self.x = 700
        self.y = 180
        self.enemy_type = "boss_dragon"
        self.name = "Malakor, the Dragon"
        self.health = 400
        self.max_health = 400
        self.strength = 35
        self.speed = 10
        self.color = (255, 69, 0)
        self.movement_cooldown = 0
        self.movement_delay = 40
        self.animation_offset = 0
        self.attack_animation = 0
        self.hit_animation = 0
        self.fire_breathing = False
        self.fire_breath_timer = 0
    def start_attack_animation(self):
        self.attack_animation = 20
        self.fire_breathing = True
        self.fire_breath_timer = 20
    def update_animation(self):
        self.animation_offset = math.sin(pygame.time.get_ticks() * 0.005) * 2
        if self.attack_animation > 0:
            self.attack_animation -= 1
        if self.hit_animation > 0:
            self.hit_animation -= 1
        if self.fire_breathing:
            self.fire_breath_timer -= 1
            if self.fire_breath_timer <= 0:
                self.fire_breathing = False
    def draw(self, surface):
        offset_x = 0
        offset_y = self.animation_offset
        if self.attack_animation > 0:
            offset_x = 10 * math.sin(self.attack_animation * 0.2)
        if self.hit_animation > 0:
            offset_x = random.randint(-4, 4)
            offset_y = random.randint(-4, 4)
        x = self.x + offset_x
        y = self.y + offset_y
        # --- Draw a more dragon-like boss, facing left ---
        # Body
        pygame.draw.ellipse(surface, DRAGON_COLOR, (x, y + 60, 180, 60))
        # Tail
        pygame.draw.polygon(surface, (200, 50, 50), [
            (x + 180, y + 90), (x + 240, y + 80), (x + 180, y + 110)
        ])
        # Legs
        pygame.draw.rect(surface, (120, 40, 20), (x + 120, y + 110, 18, 30), border_radius=8)
        pygame.draw.rect(surface, (120, 40, 20), (x + 40, y + 110, 18, 30), border_radius=8)
        # Claws
        pygame.draw.polygon(surface, (255, 255, 255), [d
            (x + 120, y + 140), (x + 118, y + 150), (x + 124, y + 150)
        ])
        pygame.draw.polygon(surface, (255, 255, 255), [
            (x + 40, y + 140), (x + 38, y + 150), (x + 44, y + 150)
        ])
        # Wings (bat-like, flipped)
        wing_y = y + 60
        pygame.draw.polygon(surface, (180, 50, 50), [
            (x + 120, wing_y), (x + 170, wing_y - 60), (x + 60, wing_y - 80), (x + 10, wing_y - 40), (x + 60, wing_y)
        ])
        pygame.draw.polygon(surface, (180, 50, 50), [
            (x + 60, wing_y), (x + 10, wing_y - 60), (x, wing_y - 20), (x + 20, wing_y + 10)
        ])
        # Head (distinct, with open mouth, facing left)
        head_x = x - 40
        head_y = y + 70
        pygame.draw.ellipse(surface, DRAGON_COLOR, (head_x, head_y, 60, 40))
        # Jaw (open)
        pygame.draw.polygon(surface, (200, 50, 50), [
            (head_x + 20, head_y + 30), (head_x, head_y + 50), (head_x + 5, head_y + 35), (head_x + 10, head_y + 30)
        ])
        # Teeth
        for i in range(3):
            pygame.draw.polygon(surface, (255, 255, 255), [
                (head_x + 12 + i*6, head_y + 38), (head_x + 10 + i*6, head_y + 45), (head_x + 14 + i*6, head_y + 38)
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
        # Eye
        pygame.draw.circle(surface, (255, 255, 255), (head_x + 15, head_y + 15), 7)
        pygame.draw.circle(surface, (0, 0, 0), (head_x + 13, head_y + 15), 3)
        # Fire breath animation (large cone from mouth to player, facing left)
        if self.fire_breathing:
            mouth_x = head_x - 10
            mouth_y = head_y + 40
            player_x = 200 + 25
            player_y = 300 + 25
            for i in range(30):
                t = i / 30
                fx = int(mouth_x * (1-t) + player_x * t + random.randint(-10, 10))
                fy = int(mouth_y * (1-t) + player_y * t + random.randint(-10, 10))
                size = int(10 * (1-t) + 40 * t)
                color = (255, 140 + random.randint(0, 100), 0, max(0, 200 - i * 6))
                fire_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(fire_surf, color, (size, size), size)
                surface.blit(fire_surf, (fx - size, fy - size))
        # Health bar (with HP numbers)
        bar_width = 120
        bar_x = x + 60
        bar_y = y + 20
        pygame.draw.rect(surface, (20, 20, 30), (bar_x, bar_y, bar_width, 16), border_radius=2)
        health_width = (bar_width - 2) * (self.health / self.max_health)
        pygame.draw.rect(surface, HEALTH_COLOR, (bar_x + 1, bar_y + 1, health_width, 14), border_radius=2)
        # HP numbers
        hp_text = font_small.render(f"{self.health}/{self.max_health}", True, (255,255,255))
        hp_rect = hp_text.get_rect(center=(bar_x + bar_width//2, bar_y + 8))
        surface.blit(hp_text, hp_rect)
        # Name
        name_text = font_medium.render(self.name, True, (255, 215, 0))
        name_rect = name_text.get_rect(midtop=(x + 120, y - 10))
        surface.blit(name_text, name_rect)

if __name__ == "__main__":
    game = Game()
    game.run()