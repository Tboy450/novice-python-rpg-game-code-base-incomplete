# 🐉 Dragon's Lair RPG - Modular Edition

A comprehensive, modular RPG game built with Python and Pygame, featuring turn-based combat, character progression, and an expansive world to explore.

## 🎮 What This Game Is

**Dragon's Lair RPG** is a complete role-playing game that combines classic RPG elements with modern modular architecture. Players choose from three character classes (Warrior, Mage, Rogue), battle enemies across a procedurally generated world, and face increasingly powerful boss dragons as they progress.

### 🎯 Key Features

- **Three Character Classes**: Warrior (tank), Mage (magic), Rogue (stealth)
- **Turn-Based Combat**: Strategic battles with attack, magic, item, and run options
- **Progressive Boss System**: Boss dragons that evolve and become stronger as you level up
- **Dragon Evolution Mechanics**: Boss dragons change appearance, stats, and abilities based on player level
- **Character-Specific Attack Effects**: Unique visual effects for each character class
- **Dynamic Music System**: Music changes based on game state and area
- **Particle Effects**: Rich visual feedback for all combat actions
- **World Exploration**: 3x3 grid world with different area types
- **Town System**: Interactive towns with cutscenes and NPCs

## 🚀 How to Play

### Getting Started
1. **Install Python 3.8+** and Pygame
2. **Run the game**: `python main.py`
3. **Choose your character**: Warrior, Mage, or Rogue
4. **Explore the world**: Use arrow keys or WASD to move
5. **Battle enemies**: Touch enemies to initiate combat
6. **Level up**: Gain experience to unlock boss battles
7. **Face the dragons**: Defeat progressively stronger boss dragons

### Controls
- **Movement**: Arrow keys or WASD
- **Menu Navigation**: Arrow keys + Enter
- **Battle Actions**: Mouse clicks on action buttons
- **Map View**: M key
- **Pause/Menu**: ESC key
- **Skip Cutscenes**: Any key during cutscenes

### Combat System
- **Attack**: Basic physical attack with character-specific effects
- **Magic**: Powerful spell with particle explosions and beam effects
- **Item**: Use healing potions with particle effects
- **Run**: 70% chance to escape with visual feedback

## 🏗️ Project Structure

```
pygame_organized/
├── main.py                 # Game entry point
├── core/                   # Core game systems
│   ├── game.py            # Main game loop and state management
│   ├── game_events.py     # Event handling and input processing
│   ├── game_ui.py         # UI drawing and overlay systems
│   └── game_utils.py      # Utility functions
├── entities/              # Game entities and characters
│   ├── enemy.py           # Base enemy class
│   ├── boss_dragons.py    # Boss dragon classes with evolution
│   ├── item.py            # Collectible items
│   └── player_characters/ # Character classes and animations
├── systems/               # Game systems
│   ├── boss_system.py     # Boss battle management
│   ├── dragon_evolution.py # Dragon evolution mechanics
│   └── particle_system.py # Visual effects system
├── ui/                    # User interface components
│   ├── battle_screen.py   # Combat interface
│   ├── start_screen.py    # Main menu
│   └── button.py          # Interactive buttons
├── world/                 # World generation and areas
│   ├── world_map.py       # World map management
│   └── world_area.py      # Individual area generation
├── config/                # Configuration and constants
└── tests/                 # Test files for all systems
```

## ⚔️ Combat System

### Character Classes

#### 🛡️ Warrior
- **Role**: Tank/Paladin (now looks like a Paladin)
- **Attack Effect**: Holy slash with golden particles and a glowing sword animation
- **Special**: High health and defense
- **Animation**: Armored, noble Paladin with a shining sword

#### 🔮 Mage
- **Role**: Magic damage dealer
- **Attack Effect**: Fireball projectile with animated trail and explosion
- **Special**: High magic damage and mana
- **Animation**: Mystical, robed Mage with magical effects

#### 🗡️ Rogue
- **Role**: Stealth/Assassin (now looks like an Assassin)
- **Attack Effect**: Throwing knives with spinning animation and particle effects
- **Special**: High speed and critical hits
- **Animation**: Agile, assassin-like Rogue with throwing knives

### Battle Mechanics
- **Turn-Based**: Player and enemy take turns
- **Damage Delay**: 0.5-second delay for impactful combat

## 🖥️ User Interface

### HUD (Heads-Up Display)
The game features a comprehensive HUD that displays:
- **Player Stats**: Health, Mana, Experience bars with real-time updates
- **Combat Info**: Score, time played, kills count, items collected
- **Area Information**: Current area type with descriptions
- **Mini-Map**: Visual representation of visited areas (labeled as "Mini-Map")
- **Position Tracking**: Grid coordinates for precise navigation
- **Controls**: On-screen control hints for easy reference

### UI Features
- **Real-time Updates**: All stats update immediately when changed
- **Visual Feedback**: Color-coded health/mana bars
- **Area Descriptions**: Contextual information about current location
- **Progress Tracking**: Experience and level progression display
- **Screen Shake**: Visual feedback for powerful attacks
- **Particle Effects**: Rich visual effects for all actions
- **Character-Specific Effects**: Unique animations for each class

## 🐉 Boss System & Dragon Evolution

### Progressive Boss Battles
- **Trigger**: Boss battles occur after leveling up (level 2+)
- **Evolution**: Boss dragons become stronger and more visually impressive
- **Final Boss**: Malakor, the Dragon Lord at level 10

### Dragon Evolution Mechanics

#### Evolution Tiers
1. **Young Dragon** (Level 2-3): Basic boss with simple effects
2. **Adolescent Dragon** (Level 3-4): Enhanced aura and fire breath
3. **Adult Dragon** (Level 4-5): Improved stats and animations
4. **Veteran Dragon** (Level 5-6): Advanced visual effects
5. **Elite Dragon** (Level 6-7): Powerful aura and enhanced attacks
6. **Champion Dragon** (Level 7-8): Legendary status with glow effects
7. **Legendary Dragon** (Level 8-9): Ancient power with red eye glow
8. **Ancient Dragon** (Level 9): Elder status with enhanced abilities
9. **Elder Dragon** (Level 9): Pre-final boss with maximum evolution
10. **Malakor, the Dragon Lord** (Level 10): Ultimate final boss

#### Evolution Effects
- **Aura Intensity**: Increases with evolution tier (0.3 to 1.0)
- **Fire Breath Size**: Scales from 1.0x to 2.5x
- **Particle Count**: Ranges from 20 to 60 particles
- **Glow Effects**: Activated at tier 5+ with color changes
- **Wing Animation Speed**: Increases with evolution (1.0x to 2.8x)
- **Eye Glow Colors**: White → Red → Gold progression

#### Stat Scaling
- **Health Multiplier**: 1.0x to 3.0x based on tier
- **Strength Multiplier**: 1.0x to 2.0x based on tier
- **Speed Multiplier**: 1.0x to 1.5x based on tier

### Boss Battle Features
- **Evolution Tracking**: Records all dragon evolutions
- **Progress System**: Shows evolution progress and next tier
- **Visual Effects**: Aura, flash effects, and enhanced animations
- **Music Integration**: Special boss music for evolved dragons
- **Victory Tracking**: Records defeated bosses and evolution history

## 🎨 Visual Enhancements

### Character Animations
- **Movement Animations**: Smooth character movement with leg/arm animations
- **Battle Animations**: Character-specific attack and magic animations
- **Hit Animations**: Visual feedback when taking damage
- **Drawing System**: Detailed character sprites with armor, weapons, and features

### Particle Effects
- **Attack Effects**: Character-specific projectiles and particles
- **Magic Effects**: Explosions, beams, and magical particles
- **Healing Effects**: Upward-moving health particles
- **Escape Effects**: Gold particles for successful escapes
- **Failure Effects**: Red particles for failed actions

### Screen Effects
- **Screen Shake**: Impact feedback for powerful attacks
- **Transition Effects**: Smooth state transitions
- **Flash Effects**: Evolution and special event flashes
- **Aura Effects**: Boss dragon auras with varying intensity

## 🎵 Music System

### Dynamic Music
- **Start Menu**: Epic title theme
- **Character Select**: Heroic selection music
- **Overworld**: Calm adventure theme
- **Battle**: Intense combat music
- **Boss Battle**: Epic boss themes
- **Victory**: Triumphant victory music
- **Game Over**: Somber defeat music

### Music Features
- **State-Based**: Music changes with game state
- **Boss Detection**: Special music for boss battles
- **Area-Based**: Different music for different world areas
- **Procedural Generation**: Computer-generated chiptune music

## 🧪 Testing

### Test Files
- `tests/test_boss_system.py`: Boss system functionality
- `tests/test_dragon_evolution.py`: Dragon evolution mechanics
- `tests/test_dark_knight.py`: Enemy system tests
- `tests/test_guard_entities.py`: Guard entity tests

### Running Tests
```bash
python tests/test_dragon_evolution.py
python tests/test_boss_system.py
```

## 📊 Current Status

### ✅ Completed Features
- **Modular Architecture**: Clean separation of concerns
- **Character System**: Three classes with unique abilities
- **Combat System**: Turn-based with character-specific effects
- **Boss System**: Progressive boss battles with evolution
- **Dragon Evolution**: 10-tier evolution system with visual effects
- **Particle System**: Rich visual effects for all actions
- **Music System**: Dynamic music based on game state
- **World System**: 3x3 grid with different area types
- **UI System**: Complete interface with buttons and overlays
- **Animation System**: Smooth character and enemy animations
- **Documentation**: Comprehensive novice-friendly documentation

### 🎯 Recent Improvements
- **Dragon Evolution System**: Complete 10-tier evolution with visual effects
- **Boss Fight Activation**: Automatic boss battles after leveling up
- **Evolution Tracking**: Records and tracks all dragon evolutions
- **Enhanced Visual Effects**: Aura, flash, and particle effects for evolved dragons
- **Stat Scaling**: Progressive stat increases based on evolution tier
- **Character-Specific Attack Effects**: Unique visual effects for each class
- **Damage Delay System**: 0.5-second delay for impactful combat
- **ESC/Pause Functionality**: Modular pause system
- **Comprehensive Documentation**: Novice-friendly explanations throughout
- **Overworld Stats Display Fixes**: Player stats (health, mana, XP, kills, items) now update instantly and are always visible in the overworld HUD. Stats are clearly labeled and color-coded for easy reading.
- **Boss Dragon Fight Activation**: Boss battles now trigger reliably after leveling up, with clear on-screen prompts and smooth transitions. No more missed boss fights!
- **Boss Progression & Evolution**: Boss dragons evolve visually and statistically as you level up. Each evolution tier is labeled (e.g., "Young Dragon", "Champion Dragon", "Malakor, the Dragon Lord") and comes with new effects, colors, and abilities. The README now lists all tiers and their effects.
- **Magic Animation & Crash Fixes**: Magic attacks (like Mage's fireball) now have robust animations and particle effects. Game no longer crashes when using magic, even if animations overlap or are triggered rapidly. All magic effects are explained for beginners.
- **Character Class Visuals & Attacks**: Warrior is now a Paladin with a glowing holy slash, Mage has a fireball attack with animated effects, and Rogue is now an assassin with throwing knives. Each class has a unique look and attack animation, all explained for beginners.

## 🚀 Quick Start

1. **Clone the repository**
2. **Install dependencies**: `pip install pygame`
3. **Run the game**: `python main.py`
4. **Choose your character** and begin your adventure!

## 📝 For Developers

### Architecture Overview
The game uses a modular architecture with clear separation of concerns:
- **Core Systems**: Game loop, events, and state management
- **Entity Systems**: Characters, enemies, and items
- **System Modules**: Boss, evolution, and particle systems
- **UI Components**: Screens, buttons, and overlays
- **World Generation**: Areas, maps, and exploration

### Adding New Features
1. **Identify the appropriate module** for your feature
2. **Follow the existing patterns** for consistency
3. **Add comprehensive documentation** with novice-friendly explanations
4. **Create tests** for new functionality
5. **Update the README** with new features

### Code Quality
- **Novice-Friendly**: Clear comments and documentation
- **Modular Design**: Clean separation of concerns
- **Comprehensive Testing**: Test files for all major systems
- **Consistent Styling**: Follow existing code patterns
- **Documentation**: Detailed explanations for all features

---

**Dragon's Lair RPG** - A complete, modular RPG experience with progressive boss battles and dragon evolution mechanics! 🐉✨ 