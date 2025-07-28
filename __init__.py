"""
Dragon's Lair RPG - Main Package
================================

This is the main package for Dragon's Lair RPG, a retro-style adventure game
built with Pygame. This package contains all the game modules and systems.

RESOURCE: This makes the entire directory a proper Python package.
"""

__version__ = "1.0.0"
__author__ = "Dragon's Lair RPG Team"
__email__ = "dragonslair@example.com"
__description__ = "A Retro-Style Adventure Game built with Pygame"
__url__ = "https://github.com/yourusername/dragons-lair-rpg"

# Package metadata
__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "__description__",
    "__url__",
]

# Import main game function for easy access
from .main import main

# Package description for novice coders
"""
WHAT THIS PACKAGE DOES:
=======================
This is the main package for Dragon's Lair RPG. It contains:

1. GAME MODULES:
   - audio: Music and sound system
   - config: Game constants and settings
   - core: Main game logic and state management
   - entities: Characters, enemies, and items
   - systems: Particle effects and boss system
   - ui: User interface components
   - utils: Utility functions
   - world: World map and area management

2. MAIN ENTRY POINT:
   - main.py: The main game file that starts everything

3. PACKAGE FEATURES:
   - Complete RPG game with 3x3 world map
   - Turn-based combat system
   - Procedurally generated music
   - Multiple character classes
   - Boss battles and progression
   - Cross-platform compatibility

FOR NOVICE CODERS:
==================
This package is like a complete game in a box:
- Everything needed to run the game is included
- You can install it with pip: pip install dragons-lair-rpg
- You can run it with: dragons-lair-rpg
- All the code is organized into logical modules

USAGE:
======
# Install the package
pip install dragons-lair-rpg

# Run the game
dragons-lair-rpg

# Or run directly from source
python main.py
""" 