"""
DRAGON'S LAIR RPG - Particle System Module
==========================================

This module contains the ParticleSystem class for visual effects.
"""

import pygame
import random
import math
from config.constants import *

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
        """Update particle position and age"""
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.age += 1
        return self.age >= self.lifetime
        
    def draw(self, surface):
        """Draw particle with alpha blending and size fading"""
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
        """Add a single particle to the system"""
        self.particles.append(Particle(x, y, color, velocity, size, lifetime))
        
    def add_explosion(self, x, y, color, count=20, size_range=(2, 5), speed_range=(1, 3), lifetime_range=(20, 40)):
        """Create an explosion effect with multiple particles"""
        for _ in range(count):
            angle = random.uniform(0, math.pi*2)
            speed = random.uniform(*speed_range)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            size = random.uniform(*size_range)
            lifetime = random.randint(*lifetime_range)
            self.add_particle(x, y, color, velocity, size, lifetime)
            
    def add_beam(self, x1, y1, x2, y2, color, width=3, particle_count=10, speed=2):
        """Create a beam effect between two points"""
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
        """Update all particles and remove expired ones"""
        self.particles = [p for p in self.particles if not p.update()]
        
    def draw(self, surface, world_map=None):
        """Draw all particles with optional world coordinate conversion"""
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