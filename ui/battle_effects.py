# Effect and animation methods extracted from BattleScreen class
# These functions are designed to be used as methods of BattleScreen (pass self as first argument)
import random


def add_screen_shake(self, intensity=5, duration=10):
    """
    Triggers a screen shake effect during battle for visual feedback.
    Args:
        intensity (int): How strong the shake is (pixels).
        duration (int): How many frames the shake lasts.
    """
    self.screen_shake = duration
    self.shake_intensity = intensity


def start_attack_animation(self):
    """
    Starts the attack animation for the player, including projectiles and particles
    based on the character class (Warrior, Mage, Rogue).
    """
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
    """
    Starts the magic animation for the player (e.g., fireball, magic circle).
    """
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