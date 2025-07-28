#!/usr/bin/env python3
"""
Test script for boss system functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from entities.player_characters.character import Character
from systems.boss_system import BossSystem

def test_boss_system():
    """Test the boss system functionality"""
    print("🧪 Testing Boss System...")
    
    # Create a player
    player = Character("Warrior")
    print(f"Player created: Level {player.level}")
    
    # Create boss system
    boss_system = BossSystem()
    print("Boss system created")
    
    # Test initial state
    should_trigger, boss_enemy = boss_system.check_boss_battle_trigger(player)
    print(f"Initial check: should_trigger={should_trigger}, boss_enemy={boss_enemy}")
    
    # Level up player
    player.gain_exp(100)  # This should trigger level up
    print(f"After gaining exp: Level {player.level}, just_leveled_up={player.just_leveled_up}")
    
    # Test boss trigger after level up
    should_trigger, boss_enemy = boss_system.check_boss_battle_trigger(player)
    print(f"After level up: should_trigger={should_trigger}, boss_enemy={boss_enemy}")
    
    if should_trigger and boss_enemy:
        print(f"✅ Boss battle would be triggered! Boss type: {type(boss_enemy).__name__}")
        # Test starting boss battle
        success = boss_system.start_boss_battle(player, boss_enemy)
        print(f"Boss battle started: {success}")
        print(f"Player boss_cooldown: {player.boss_cooldown}")
        print(f"Player just_leveled_up: {player.just_leveled_up}")
    else:
        print("❌ Boss battle not triggered")
        print(f"   just_leveled_up: {player.just_leveled_up}")
        print(f"   level > 1: {player.level > 1}")
        print(f"   not boss_cooldown: {not player.boss_cooldown}")
        print(f"   level > last_boss_level: {player.level > player.last_boss_level}")

if __name__ == "__main__":
    test_boss_system() 