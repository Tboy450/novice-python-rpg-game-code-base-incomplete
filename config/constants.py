"""
DRAGON'S LAIR RPG - Game Constants and Configuration (v1.2.0)
============================================================

This module contains all the constants, colors, and configuration settings
used throughout the game.

WHAT THIS FILE DOES:
===================
This file is like a "settings menu" for the entire game. It defines:
- Screen size and performance settings
- All the colors used in the game
- Font sizes and types
- World map settings
- Game state names

FOR NOVICE CODERS:
==================
Constants are like "rules" that don't change during the game.
Instead of writing the same numbers over and over, we define them once here.
This makes it easy to change things like screen size or colors.

COLOR SYSTEM EXPLANATION:
========================
Colors in Pygame are defined as (Red, Green, Blue) tuples:
- Each number goes from 0 (dark) to 255 (bright)
- (0, 0, 0) = Black, (255, 255, 255) = White
- (255, 0, 0) = Red, (0, 255, 0) = Green, (0, 0, 255) = Blue

RETRO 80s COLOR PALETTE:
========================
This game uses a retro 80s color scheme:
- Hot pink borders and health bars
- Cyan text and mana bars
- Dark blue backgrounds
- Bright, vibrant colors for effects
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
# ===============================
# These control how the game looks and runs
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700  # Game window size
PLAYER_SIZE = 50                          # How big the player character is
ENEMY_SIZE = 40                           # How big enemies are
ITEM_SIZE = 30                            # How big collectible items are
FPS = 60                                 # Frames per second (game speed)

# Visual Design - Retro 80s Color Palette
# =======================================
# Core UI Colors (User Interface colors)
BACKGROUND = (10, 10, 30)        # Dark blue background (like night sky)
UI_BG = (20, 15, 40)             # UI panel background (darker blue)
UI_BORDER = (255, 105, 180)      # Hot pink borders (retro style)
TEXT_COLOR = (0, 255, 255)       # Cyan text (bright and readable)
GRID_COLOR = (50, 50, 80)        # Grid lines (subtle blue-gray)

# Character and Entity Colors
# ==========================
# These define what color each type of character/object is
PLAYER_COLOR = (0, 255, 0)       # Green player (easy to spot)
ENEMY_COLOR = (255, 0, 0)        # Red enemies (danger!)
DRAGON_COLOR = (255, 69, 0)      # Red-orange dragons (fire breathing)
ITEM_COLOR = (255, 215, 0)       # Gold items (valuable and shiny)

# Status Bar Colors
# =================
# Colors for health, mana, and experience bars
HEALTH_COLOR = (255, 105, 180)   # Hot pink health (matches UI theme)
MANA_COLOR = (0, 255, 255)       # Cyan mana (magical blue)
EXP_COLOR = (255, 255, 0)        # Yellow experience (golden)

# Special Effect Color Palettes
# =============================
# These are lists of colors that create gradient effects
# Fire effect gradient (orange to yellow - like real fire)
FIRE_COLORS = [(255, 100, 0), (255, 150, 0), (255, 200, 50)]
# Ice effect gradient (light blue to white - like ice crystals)
ICE_COLORS = [(100, 200, 255), (150, 220, 255), (200, 240, 255)]
# Shadow effect gradient (dark blue to purple - mysterious)
SHADOW_COLORS = [(40, 40, 80), (70, 70, 120), (100, 100, 150)]
# Magic effect gradient (purple to pink - magical)
MAGIC_COLORS = [(150, 0, 255), (200, 50, 255), (255, 100, 255)]

# Enemy Colors by Type
# ====================
# Different enemy types have different colors
ENEMY_COLORS = {
    "fiery": (255, 100, 0),      # Orange-red for fire enemies
    "shadow": (100, 100, 150),   # Blue-gray for shadow enemies
    "ice": (100, 200, 255),      # Light blue for ice enemies
    "enemy": (255, 0, 0)         # Red for regular enemies
}

# Boss Dragon Colors
# ==================
# Each boss dragon has a unique color scheme
# Format: (primary_color, secondary_color)
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
# PYGAME INITIALIZATION AND SETUP
# ============================================================================

# Create the main game window
# ===========================
# This creates the actual window that the game runs in
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dragon's Lair RPG")  # Window title
clock = pygame.time.Clock()  # Controls game speed (FPS)

# Font System Setup
# =================
# Try to load custom fonts, fall back to system fonts if not available
# Fonts are like "fonts" in a word processor - they control how text looks
try:
    font_large = pygame.font.Font("freesansbold.ttf", 48)      # Main titles (big text)
    font_medium = pygame.font.Font("freesansbold.ttf", 32)     # UI headers (medium text)
    font_small = pygame.font.Font("freesansbold.ttf", 24)      # Regular text (normal size)
    font_tiny = pygame.font.Font("freesansbold.ttf", 18)       # Small labels (tiny text)
    font_cinematic = pygame.font.Font("freesansbold.ttf", 28)  # Cutscene text (special)
except:
    # Fallback to system fonts if custom fonts not found
    # This ensures the game works even if the font files are missing
    font_large = pygame.font.SysFont("Courier", 48, bold=True)
    font_medium = pygame.font.SysFont("Courier", 32, bold=True)
    font_small = pygame.font.SysFont("Courier", 24, bold=True)
    font_tiny = pygame.font.SysFont("Courier", 18, bold=True)
    font_cinematic = pygame.font.SysFont("Courier", 28, bold=True)

# ============================================================================
# WORLD AND GRID SYSTEM CONFIGURATION
# ============================================================================

# Grid System (for movement and collision detection)
# ================================================
# The game world is divided into a grid (like a chess board)
# This makes movement and collision detection easier
GRID_SIZE = 50                    # Size of each grid square (in pixels)
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE   # Number of grid columns
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE # Number of grid rows

# World Map System (3x3 grid of areas)
# ====================================
# The game world is a 3x3 grid, like this:
# [Area 0,0] [Area 0,1] [Area 0,2]
# [Area 1,0] [Area 1,1] [Area 1,2]
# [Area 2,0] [Area 2,1] [Area 2,2]
WORLD_SIZE = 3                    # 3x3 world grid
AREA_WIDTH = SCREEN_WIDTH         # Each area is full screen width
AREA_HEIGHT = SCREEN_HEIGHT       # Each area is full screen height
WORLD_WIDTH = WORLD_SIZE * AREA_WIDTH    # Total world width
WORLD_HEIGHT = WORLD_SIZE * AREA_HEIGHT  # Total world height

# ============================================================================
# GAME STATE CONSTANTS
# ============================================================================

# Game States
# ===========
# The game can be in different "modes" - these are the names for each mode
GAME_STATE_START_MENU = "start_menu"           # Title screen
GAME_STATE_OPENING_CUTSCENE = "opening_cutscene" # Story introduction
GAME_STATE_CHARACTER_SELECT = "character_select" # Choose your character
GAME_STATE_OVERWORLD = "overworld"             # Main gameplay area
GAME_STATE_BATTLE = "battle"                   # Combat screen
GAME_STATE_GAME_OVER = "game_over"             # You died screen
GAME_STATE_VICTORY = "victory"                 # You won screen 