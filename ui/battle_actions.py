# Action methods extracted from BattleScreen class
import random

# These functions are meant to be used as methods of BattleScreen, so they expect 'self' as the first argument.
def execute_attack(self):
    damage = self.player.strength
    self.enemy.health -= damage
    if self.player.type == "Mage":
        self.add_log(f"Fireball dealt {damage} damage to {self.enemy.name}!")
    elif self.player.type == "Rogue":
        self.add_log(f"Knife throw dealt {damage} damage to {self.enemy.name}!")
    else:
        self.add_log(f"You dealt {damage} damage to {self.enemy.name}!")
        if self.enemy.enemy_type == "fiery":
            self.particle_system.add_explosion(700 + 30, 250 + 30, FIRE_COLORS[0], count=30, size_range=(2, 6), speed_range=(1, 4), lifetime_range=(15, 30))
        elif self.enemy.enemy_type == "shadow":
            self.particle_system.add_explosion(700 + 30, 250 + 30, SHADOW_COLORS[1], count=20, size_range=(3, 8), speed_range=(0.5, 2), lifetime_range=(20, 40))
        else:
            self.particle_system.add_explosion(700 + 30, 250 + 30, ICE_COLORS[2], count=25, size_range=(2, 5), speed_range=(1, 3), lifetime_range=(15, 25))
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
    self.particle_system.add_beam(200 + 25, 350 + 15, 700 + 30, 250 + 30, self.magic_effect['color'], width=5, particle_count=15, speed=3)
    self.particle_system.add_explosion(700 + 30, 250 + 30, self.magic_effect['color'], count=40, size_range=(3, 7), speed_range=(1, 5), lifetime_range=(15, 30))
    self.state = "enemy_turn"
    self.action_cooldown = self.action_delay

def execute_item(self):
    heal_amount = 30
    self.player.health = min(self.player.max_health, self.player.health + heal_amount)
    self.add_log(f"Restored {heal_amount} HP!")
    for _ in range(20):
        x = random.randint(200, 200 + PLAYER_SIZE)
        y = random.randint(300, 300 + PLAYER_SIZE)
        self.particle_system.add_particle(x, y, HEALTH_COLOR, (random.uniform(-0.5, 0.5), random.uniform(-1, -0.5)), 3, 30)
    self.state = "enemy_turn"
    self.action_cooldown = self.action_delay

def execute_run(self):
    if random.random() < 0.7:
        self.add_log("You successfully escaped!")
        self.battle_ended = True
        self.result = "escape"
        self.show_summary = True
    else:
        self.add_log("Escape failed! The enemy attacks!")
        self.state = "enemy_turn"
        self.action_cooldown = self.action_delay 