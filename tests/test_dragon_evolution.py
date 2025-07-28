"""
DRAGON'S LAIR RPG - Dragon Evolution System Tests
================================================

This module tests the DragonEvolutionSystem class to ensure
dragon evolution mechanics work correctly.

RESOURCE: This demonstrates the systems.dragon_evolution.DragonEvolutionSystem class.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from config.constants import *
from systems.dragon_evolution import DragonEvolutionSystem


def test_dragon_evolution_system():
    """Test the dragon evolution system functionality"""
    print("🧪 Testing Dragon Evolution System...")
    
    # Initialize the evolution system
    evolution_system = DragonEvolutionSystem()
    
    # Test evolution tier calculation
    print("\n📊 Testing Evolution Tiers:")
    for level in range(1, 12):
        tier = evolution_system.get_evolution_tier(level)
        evolution_name = evolution_system.get_evolution_name(tier)
        print(f"  Level {level} -> Tier {tier}: {evolution_name}")
    
    # Test stat scaling
    print("\n⚔️ Testing Stat Scaling:")
    base_stats = {"health": 200, "strength": 20, "speed": 10}
    for level in [2, 5, 8, 10]:
        evolved_stats = evolution_system.get_evolved_dragon_stats(base_stats, level)
        tier = evolution_system.get_evolution_tier(level)
        print(f"  Level {level} (Tier {tier}):")
        print(f"    Health: {base_stats['health']} -> {evolved_stats['health']}")
        print(f"    Strength: {base_stats['strength']} -> {evolved_stats['strength']}")
        print(f"    Speed: {base_stats['speed']} -> {evolved_stats['speed']}")
    
    # Test evolution effects
    print("\n✨ Testing Evolution Effects:")
    for tier in [0, 3, 6, 9]:
        effects = evolution_system.get_evolution_effects(tier)
        print(f"  Tier {tier} Effects:")
        print(f"    Aura Intensity: {effects['aura_intensity']:.2f}")
        print(f"    Fire Breath Size: {effects['fire_breath_size']:.2f}")
        print(f"    Particle Count: {effects['particle_count']}")
        print(f"    Glow Effect: {effects['glow_effect']}")
        print(f"    Wing Speed: {effects['wing_animation_speed']:.2f}")
    
    # Test evolution recording
    print("\n📝 Testing Evolution Recording:")
    evolution_system.record_evolution(3, "dragon_boss", 1)
    evolution_system.record_evolution(6, "dragon_boss", 4)
    evolution_system.record_evolution(10, "boss_dragon", 9)
    
    summary = evolution_system.get_evolution_summary()
    print(f"  Total Evolutions: {summary['total_evolutions']}")
    print(f"  Highest Tier: {summary['highest_tier']}")
    print(f"  Evolution Count: {summary['evolution_count']}")
    
    # Test evolution progress
    print("\n📈 Testing Evolution Progress:")
    for level in [2, 5, 8, 10]:
        progress = evolution_system.get_evolution_progress(level)
        print(f"  Level {level}:")
        print(f"    Current Tier: {progress['current_tier']}")
        print(f"    Progress: {progress['progress_percentage']:.1f}%")
        print(f"    Next Evolution: Level {progress['next_evolution_level']}")
        print(f"    Evolution Name: {progress['evolution_name']}")
    
    # Test evolution triggering
    print("\n🎯 Testing Evolution Triggering:")
    for level in [2, 5, 8, 10]:
        current_tier = evolution_system.get_evolution_tier(level - 1)
        new_tier = evolution_system.get_evolution_tier(level)
        should_trigger = evolution_system.should_trigger_evolution(level, current_tier)
        print(f"  Level {level}: Tier {current_tier} -> {new_tier}, Should Trigger: {should_trigger}")
    
    print("\n✅ Dragon Evolution System Tests Complete!")
    return True


if __name__ == "__main__":
    # Initialize pygame for testing
    pygame.init()
    
    # Run tests
    test_dragon_evolution_system()
    
    # Cleanup
    pygame.quit() 