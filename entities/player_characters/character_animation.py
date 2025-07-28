# Character animation and drawing methods for player characters
import pygame
import math
import random
from config.constants import *

# These methods implement the CharacterBase interface and are called by battle/UI modules.

def update_animation(self):
    """Update the character's animation state (called every frame by game/UI)."""
    self.animation_offset = math.sin(pygame.time.get_ticks() * 0.005) * 2
    if self.attack_animation > 0:
        self.attack_animation -= 1
    if self.hit_animation > 0:
        self.hit_animation -= 1

def start_attack_animation(self):
    """Start the attack animation - different for each character type"""
    self.attack_animation = 10  # Reverted to original value

def start_hit_animation(self):
    """Start the hit animation when taking damage"""
    self.hit_animation = 5

def start_magic_animation(self):
    """Start the magic animation - same for all character types"""
    self.magic_animation = 15

def draw(self, surface):
    """Draw the character sprite (called by UI/battle modules)."""
    # --- Full detailed drawing logic for Warrior, Mage, Rogue ---
    # This code is adapted from the original pycore whole file for modular use.
    # Each class has unique visual features and attack/hit animation effects.
    
    offset_x = self.animation_offset
    offset_y = self.animation_offset
    
    if self.attack_animation > 0:
        if self.type == "Warrior":
            offset_x = 10 * math.sin(self.attack_animation * 0.2)  # Increased from 5 to 10
        elif self.type == "Mage":
            offset_y -= 10 * (1 - self.attack_animation / 10)  # Increased from 5 to 10
        else:  # Rogue
            offset_x = -10 * math.sin(self.attack_animation * 0.2)  # Increased from 5 to 10
            
    if self.hit_animation > 0:
        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)
    
    x = self.x + offset_x
    y = self.y + offset_y
    
    # --- Drawing logic for each class ---
    if self.type == "Warrior":
        draw_warrior(self, surface, x, y)
    elif self.type == "Mage":
        draw_mage(self, surface, x, y)
    else:  # Rogue
        draw_rogue(self, surface, x, y)

def draw_warrior(self, surface, x, y):
    """Draw Warrior character with noble paladin appearance"""
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

def draw_mage(self, surface, x, y):
    """Draw Mage character with mystical appearance"""
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

def draw_rogue(self, surface, x, y):
    """Draw Rogue character with stealthy appearance"""
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

def draw_stats(self, surface, x, y):
    """Draw the character's stats (HP, MP, EXP, etc.) on the given surface (called by UI/battle modules)."""
    # --- Full detailed stat bar and text drawing logic ---
    # This code is adapted from the original pycore whole file for modular use.
    
    # Health bar - simplified for debugging
    pygame.draw.rect(surface, (255, 0, 0), (x, y, 200, 25))  # Red background
    health_width = 196 * (self.health / self.max_health)
    pygame.draw.rect(surface, (0, 255, 0), (x + 2, y + 2, health_width, 21))  # Green health bar
    health_text = font_small.render(f"HP: {self.health}/{self.max_health}", True, (255, 255, 255))
    surface.blit(health_text, (x + 210, y + 4))
    
    # Mana bar - simplified for debugging
    pygame.draw.rect(surface, (0, 0, 255), (x, y + 30, 200, 20))  # Blue background
    mana_width = 196 * (self.mana / self.max_mana)
    pygame.draw.rect(surface, (0, 255, 255), (x + 2, y + 32, mana_width, 16))  # Cyan mana bar
    mana_text = font_small.render(f"MP: {self.mana}/{self.max_mana}", True, (255, 255, 255))
    surface.blit(mana_text, (x + 210, y + 32))
    
    # Experience bar - simplified for debugging
    pygame.draw.rect(surface, (128, 128, 128), (x, y + 55, 200, 15))  # Gray background
    exp_width = 196 * (self.exp / self.exp_to_level)
    pygame.draw.rect(surface, (255, 255, 0), (x + 2, y + 57, exp_width, 11))  # Yellow exp bar
    exp_text = font_small.render(f"Level: {self.level}  Exp: {self.exp}/{self.exp_to_level}", True, (255, 255, 255))
    surface.blit(exp_text, (x, y + 75))
    
    # Stats text
    stats_text = font_small.render(f"Str: {self.strength}  Def: {self.defense}  Spd: {self.speed}", True, (255, 255, 255))
    surface.blit(stats_text, (x, y + 100)) 