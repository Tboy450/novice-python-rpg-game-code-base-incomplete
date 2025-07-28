"""
Boss System Test Script
=======================

This script demonstrates the BossSystem functionality.
It shows how boss battles are triggered and managed.

RESOURCE: This demonstrates the systems.boss_system.BossSystem class.
"""

import pygame
import sys
from systems.boss_system import BossSystem
from entities.player_characters.character import Character
from entities.boss_dragons import DragonBoss, BossDragon

def test_boss_system():
    """Test the BossSystem functionality"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Boss System Test")
    clock = pygame.time.Clock()
    
    # Create boss system
    boss_system = BossSystem()
    
    # Create test player
    player = Character("Warrior")
    player.level = 5
    player.just_leveled_up = True
    player.boss_cooldown = False
    player.last_boss_level = 0
    
    # Test variables
    test_level = 5
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Test boss battle trigger
                    should_trigger, boss_enemy = boss_system.check_boss_battle_trigger(player)
                    if should_trigger:
                        print(f"Boss battle triggered! Level {player.level}")
                        print(f"Boss enemy: {boss_enemy.name}")
                        boss_system.start_boss_battle(player, boss_enemy)
                    else:
                        print("No boss battle triggered")
                elif event.key == pygame.K_1:
                    # Test level 10 (final boss)
                    player.level = 10
                    player.just_leveled_up = True
                    player.boss_cooldown = False
                    print("Set to level 10 - should trigger final boss")
                elif event.key == pygame.K_2:
                    # Test progressive boss
                    player.level = 7
                    player.just_leveled_up = True
                    player.boss_cooldown = False
                    print("Set to level 7 - should trigger progressive boss")
                elif event.key == pygame.K_3:
                    # Reset test
                    player.level = 5
                    player.just_leveled_up = True
                    player.boss_cooldown = False
                    player.last_boss_level = 0
                    boss_system.reset_boss_state()
                    print("Reset test state")
        
        # Draw
        screen.fill((20, 20, 40))
        
        # Draw test information
        info_lines = [
            f"Player Level: {player.level}",
            f"Just Leveled Up: {player.just_leveled_up}",
            f"Boss Cooldown: {player.boss_cooldown}",
            f"Last Boss Level: {player.last_boss_level}",
            f"Boss Battle Triggered: {boss_system.boss_battle_triggered}",
            f"Boss Defeated: {boss_system.boss_defeated}",
            "",
            "Controls:",
            "SPACE - Test boss battle trigger",
            "1 - Set to level 10 (final boss)",
            "2 - Set to level 7 (progressive boss)",
            "3 - Reset test state"
        ]
        
        for i, line in enumerate(info_lines):
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (50, 50 + i * 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    test_boss_system() 