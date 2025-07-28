"""
DRAGON'S LAIR RPG - Music System Module
=======================================

This module contains the MusicSystem class for procedural music generation.
"""

import pygame
import numpy as np
import io
import wave
from config.constants import *

class MusicSystem:
    """
    Generates dynamic chiptune music that changes based on game state.
    Creates different musical themes for different areas and situations.
    
    Music Types:
    - Start Menu: Epic title theme
    - Overworld: Calm adventure theme
    - Town: Peaceful town theme
    - Battle: Intense combat theme
    - Boss Battle: Epic boss theme
    - Victory: Triumphant victory theme
    - Game Over: Somber ending theme
    """
    def __init__(self):
        self.current_track = None
        self.last_state = None
        self.boss_battle_active = False
        
        try:
            # Store raw bytes instead of BytesIO objects
            self.start_menu_music_bytes = self.sound_to_wav_bytes(self.generate_start_menu_music())
            self.overworld_music_bytes = self.sound_to_wav_bytes(self.generate_overworld_music())
            self.town_music_bytes = self.sound_to_wav_bytes(self.generate_town_music())
            self.battle_music_bytes = self.sound_to_wav_bytes(self.generate_battle_music())
            self.boss_music_bytes = self.sound_to_wav_bytes(self.generate_boss_music())
            self.victory_music_bytes = self.sound_to_wav_bytes(self.generate_victory_music())
            self.game_over_music_bytes = self.sound_to_wav_bytes(self.generate_game_over_music())
            print('Music bytes created successfully')
        except Exception as e:
            print(f"Failed to create music bytes: {e}")
            self.start_menu_music_bytes = self.overworld_music_bytes = self.battle_music_bytes = None
            self.boss_music_bytes = self.victory_music_bytes = self.game_over_music_bytes = None
    
    def generate_start_menu_music(self):
        # Epic title screen theme
        melody = [
            (523.25, 0.5), (659.25, 0.5), (783.99, 0.5), (987.77, 0.5),  # C5, E5, G5, B5
            (880.00, 0.5), (783.99, 0.5), (659.25, 0.5), (523.25, 0.5),  # A5, G5, E5, C5
            (440.00, 0.5), (523.25, 0.5), (659.25, 0.5), (783.99, 0.5),  # A4, C5, E5, G5
            (659.25, 0.5), (523.25, 0.5), (440.00, 0.5), (392.00, 0.5)   # E5, C5, A4, G4
        ] * 2
        
        bass = [
            (130.81, 1), (146.83, 1), (164.81, 1), (174.61, 1),  # C3, D3, E3, F3
            (196.00, 1), (220.00, 1), (246.94, 1), (261.63, 1)   # G3, A3, B3, C4
        ] * 2
        
        percussion = [
            (200, 0.5), (0, 0.5), (150, 0.5), (0, 0.5),  # Slow dramatic drums
            (200, 0.5), (0, 0.5), (150, 0.5), (0, 0.5)
        ] * 4
        
        return self.generate_chiptune_song(melody, bass, percussion=percussion, bpm=80, volume=0.25)
    
    def sound_to_wav_bytes(self, sound):
        try:
            arr = pygame.sndarray.array(sound)
            memfile = io.BytesIO()
            with wave.open(memfile, 'wb') as wf:
                wf.setnchannels(2)
                wf.setsampwidth(2)  # 16 bits
                wf.setframerate(44100)
                wf.writeframes(arr.astype(np.int16).tobytes())
            return memfile.getvalue()  # Return the bytes content
        except Exception as e:
            print(f"Error converting sound to WAV: {e}")
            return None
    
    def update(self, game_state, is_boss_battle=False, current_area=None):
        # Only update when state or boss battle status changes
        if game_state == self.last_state and is_boss_battle == self.boss_battle_active:
            return
        
        self.last_state = game_state
        self.boss_battle_active = is_boss_battle
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(0.5)
        
        try:
            if game_state == "start_menu" and self.start_menu_music_bytes:
                pygame.mixer.music.load(io.BytesIO(self.start_menu_music_bytes))
                pygame.mixer.music.play(-1)
            elif game_state == "opening_cutscene" and self.start_menu_music_bytes:
                pygame.mixer.music.load(io.BytesIO(self.start_menu_music_bytes))
                pygame.mixer.music.play(-1)
            elif game_state == "character_select" and self.start_menu_music_bytes:
                pygame.mixer.music.load(io.BytesIO(self.start_menu_music_bytes))
                pygame.mixer.music.play(-1)
            elif game_state == "overworld":
                # Check if we're in a town area
                if current_area and current_area.area_type == "town" and self.town_music_bytes:
                    pygame.mixer.music.load(io.BytesIO(self.town_music_bytes))
                    pygame.mixer.music.play(-1)
                elif self.overworld_music_bytes:
                    pygame.mixer.music.load(io.BytesIO(self.overworld_music_bytes))
                    pygame.mixer.music.play(-1)
            elif game_state == "battle":
                if is_boss_battle and self.boss_music_bytes:
                    pygame.mixer.music.load(io.BytesIO(self.boss_music_bytes))
                    pygame.mixer.music.play(-1)
                elif self.battle_music_bytes:
                    pygame.mixer.music.load(io.BytesIO(self.battle_music_bytes))
                    pygame.mixer.music.play(-1)
                else:
                    print('MusicSystem: WARNING - No battle music available!')
            elif game_state == "victory" and self.victory_music_bytes:
                pygame.mixer.music.load(io.BytesIO(self.victory_music_bytes))
                pygame.mixer.music.play(0)
            elif game_state == "game_over" and self.game_over_music_bytes:
                pygame.mixer.music.load(io.BytesIO(self.game_over_music_bytes))
                pygame.mixer.music.play(0)
            else:
                print(f'MusicSystem: No music for state: {game_state}')
        except Exception as e:
            print(f"Music playback error: {e}")
    
    def generate_overworld_music(self):
        # Calm adventure theme
        melody = [
            (440, 0.5), (523.25, 0.5), (659.25, 0.5), (783.99, 0.5),  # A4, C5, E5, G5
            (659.25, 0.5), (523.25, 0.5), (440, 1),                   # E5, C5, A4
            (392, 0.5), (493.88, 0.5), (587.33, 0.5), (698.46, 0.5),  # G4, B4, D5, F5
            (659.25, 0.5), (587.33, 0.5), (523.25, 1)                 # E5, D5, C5
        ]
        bass = [
            (130.81, 1), (146.83, 1), (164.81, 1), (174.61, 1),  # C3, D3, E3, F3
            (196.00, 1), (220.00, 1), (246.94, 1), (261.63, 1)   # G3, A3, B3, C4
        ]
        return self.generate_chiptune_song(melody, bass, bpm=90, volume=0.2)
    
    def generate_town_music(self):
        # Peaceful town theme with bells and gentle melody
        melody = [
            (523.25, 0.5), (587.33, 0.5), (659.25, 0.5), (698.46, 0.5),  # C5, D5, E5, F5
            (783.99, 0.5), (698.46, 0.5), (659.25, 0.5), (587.33, 0.5),  # G5, F5, E5, D5
            (523.25, 0.5), (493.88, 0.5), (440.00, 0.5), (392.00, 0.5),  # C5, B4, A4, G4
            (440.00, 0.5), (493.88, 0.5), (523.25, 1.0)                  # A4, B4, C5
        ]
        bass = [
            (261.63, 1.0), (293.66, 1.0), (329.63, 1.0), (349.23, 1.0),  # C4, D4, E4, F4
            (392.00, 1.0), (440.00, 1.0), (493.88, 1.0), (523.25, 1.0)   # G4, A4, B4, C5
        ]
        percussion = [
            (50, 0.5), (0, 0.5), (30, 0.5), (0, 0.5),  # Gentle bell-like rhythm
            (50, 0.5), (0, 0.5), (30, 0.5), (0, 0.5)
        ]
        lead = [
            (784.00, 0.25), (0, 0.25), (880.00, 0.25), (0, 0.25),  # G5, rest, A5, rest
            (987.77, 0.25), (0, 0.25), (1046.50, 0.25), (0, 0.25),  # B5, rest, C6, rest
            (880.00, 0.25), (0, 0.25), (784.00, 0.25), (0, 0.25),  # A5, rest, G5, rest
            (659.25, 0.25), (0, 0.25), (587.33, 0.25), (0, 0.25)   # E5, rest, D5, rest
        ]
        return self.generate_chiptune_song(melody, bass, percussion, lead, bpm=120, volume=0.15)
    
    def generate_battle_music(self):
        # Intense battle theme
        melody = [
            (587.33, 0.25), (659.25, 0.25), (783.99, 0.25), (659.25, 0.25),  # D5, E5, G5, E5
            (587.33, 0.25), (523.25, 0.25), (493.88, 0.25), (440, 0.25),     # D5, C5, B4, A4
            (392, 0.25), (440, 0.25), (493.88, 0.25), (587.33, 0.25),        # G4, A4, B4, D5
            (659.25, 0.25), (587.33, 0.25), (523.25, 0.25), (493.88, 0.25)   # E5, D5, C5, B4
        ] * 2
        bass = [
            (98.00, 0.5), (110.00, 0.5), (123.47, 0.5), (130.81, 0.5),  # G2, A2, B2, C3
            (146.83, 0.5), (164.81, 0.5), (185.00, 0.5), (196.00, 0.5)   # D3, E3, F#3, G3
        ] * 2
        percussion = [
            (150, 0.25), (0, 0.25), (100, 0.25), (0, 0.25),  # Kick, rest, snare, rest
            (150, 0.25), (0, 0.25), (100, 0.25), (0, 0.25)
        ] * 4
        return self.generate_chiptune_song(melody, bass, percussion=percussion, bpm=140, volume=0.25)
    
    def generate_boss_music(self):
        # Epic boss battle theme
        melody = [
            (220, 0.25), (261.63, 0.25), (329.63, 0.25), (392.00, 0.25),  # A3, C4, E4, G4
            (493.88, 0.25), (392.00, 0.25), (329.63, 0.25), (261.63, 0.25),  # B4, G4, E4, C4
            (293.66, 0.25), (349.23, 0.25), (440.00, 0.25), (523.25, 0.25),  # D4, F4, A4, C5
            (659.25, 0.25), (523.25, 0.25), (440.00, 0.25), (349.23, 0.25)   # E5, C5, A4, F4
        ] * 2
        bass = [
            (82.41, 0.5), (87.31, 0.5), (92.50, 0.5), (98.00, 0.5),  # E2, F2, F#2, G2
            (110.00, 0.5), (123.47, 0.5), (138.59, 0.5), (146.83, 0.5)  # A2, B2, C#3, D3
        ] * 2
        percussion = [
            (200, 0.125), (0, 0.125), (150, 0.125), (0, 0.125),  # Fast drums
            (100, 0.125), (0, 0.125), (150, 0.125), (0, 0.125),
            (200, 0.125), (0, 0.125), (150, 0.125), (0, 0.125),
            (100, 0.125), (0, 0.125), (150, 0.125), (200, 0.125)
        ] * 2
        lead = [
            (523.25, 0.25), (0, 0.25), (659.25, 0.25), (0, 0.25),  # C5, rest, E5, rest
            (783.99, 0.25), (0, 0.25), (987.77, 0.25), (0, 0.25),  # G5, rest, B5, rest
            (880.00, 0.25), (0, 0.25), (698.46, 0.25), (0, 0.25),  # A5, rest, F5, rest
            (587.33, 0.25), (0, 0.25), (493.88, 0.25), (0, 0.25)   # D5, rest, B4, rest
        ]
        return self.generate_chiptune_song(melody, bass, percussion, lead, bpm=160, volume=0.3)
    
    def generate_victory_music(self):
        # Triumphant victory theme
        melody = [
            (659.25, 0.3), (783.99, 0.3), (987.77, 0.3), (880.00, 0.5),  # E5, G5, B5, A5
            (0, 0.2), (783.99, 0.3), (880.00, 0.3), (1046.50, 0.5),      # rest, G5, A5, C6
            (0, 0.2), (987.77, 0.3), (1174.66, 0.3), (1318.51, 1.0)      # rest, B5, D6, E6
        ]
        bass = [
            (261.63, 0.5), (329.63, 0.5), (392.00, 0.5), (523.25, 0.5),  # C4, E4, G4, C5
            (392.00, 0.5), (523.25, 0.5), (659.25, 0.5), (783.99, 1.0)   # G4, C5, E5, G5
        ]
        percussion = [
            (300, 0.1), (0, 0.1), (400, 0.1), (0, 0.1),  # Fast drum roll
            (500, 0.1), (0, 0.1), (600, 0.1), (0, 0.1),
            (700, 0.5)  # Cymbal crash
        ]
        return self.generate_chiptune_song(melody, bass, percussion, bpm=120, volume=0.3)
    
    def generate_game_over_music(self):
        # Somber game over theme
        melody = [
            (261.63, 1.0), (246.94, 1.0), (220.00, 1.0), (196.00, 2.0),  # C4, B3, A3, G3
            (174.61, 1.0), (164.81, 1.0), (146.83, 1.0), (130.81, 2.0)   # F3, E3, D3, C3
        ]
        bass = [
            (65.41, 2.0), (61.74, 2.0), (55.00, 2.0), (49.00, 4.0),  # C2, B1, A1, G1
            (43.65, 2.0), (41.20, 2.0), (36.71, 2.0), (32.70, 4.0)   # F1, E1, D1, C1
        ]
        return self.generate_chiptune_song(melody, bass, bpm=60, volume=0.25)
    
    def generate_chiptune_song(self, melody, bass, percussion=None, lead=None, bpm=220, volume=0.16):
        """
        Core chiptune generation algorithm that combines multiple musical tracks.
        
        Args:
            melody: List of (frequency, duration) tuples for main melody
            bass: List of (frequency, duration) tuples for bass line
            percussion: Optional list of (frequency, duration) tuples for drums
            lead: Optional list of (frequency, duration) tuples for lead synth
            bpm: Beats per minute for tempo
            volume: Overall volume level (0.0 to 1.0)
        """
        melody = [list(note) for note in melody]
        bass = [list(note) for note in bass]
        if percussion is not None:
            percussion = [list(note) for note in percussion]
        if lead is not None:
            lead = [list(note) for note in lead]
        song = np.zeros((0, 2), dtype=np.int16)
        melody_idx = bass_idx = perc_idx = lead_idx = 0
        melody_len = len(melody)
        bass_len = len(bass)
        perc_len = len(percussion) if percussion is not None else 0
        lead_len = len(lead) if lead is not None else 0
        while (melody_idx < melody_len or bass_idx < bass_len or
               (percussion is not None and perc_idx < perc_len) or
               (lead is not None and lead_idx < lead_len)):
            if melody_idx < melody_len:
                m_freq, m_beats = melody[melody_idx]
            else:
                m_freq, m_beats = 0, 0.25
            if bass_idx < bass_len:
                b_freq, b_beats = bass[bass_idx]
            else:
                b_freq, b_beats = 0, 0.25
            if percussion is not None and perc_idx < perc_len:
                p_freq, p_beats = percussion[perc_idx]
            else:
                p_freq, p_beats = 0, 0.25
            if lead is not None and lead_idx < lead_len:
                l_freq, l_beats = lead[lead_idx]
            else:
                l_freq, l_beats = 0, 0.25
            step_beats = min(m_beats, b_beats, p_beats, l_beats)
            step_duration = 60 / bpm * step_beats
            t = np.linspace(0, step_duration, int(44100 * step_duration), False)
            # Generate waves
            m_wave = np.sin(m_freq * 2 * np.pi * t) if m_freq > 0 else np.zeros_like(t)
            b_wave = 0.25 * np.sign(np.sin(b_freq * 2 * np.pi * t)) if b_freq > 0 else np.zeros_like(t)
            p_wave = 0.18 * np.sign(np.sin(p_freq * 2 * np.pi * t)) if percussion is not None and p_freq > 0 else np.zeros_like(t)
            l_wave = 0.18 * np.sin(l_freq * 2 * np.pi * t) if lead is not None and l_freq > 0 else np.zeros_like(t)
            # Combine waves
            wave = m_wave + b_wave + p_wave + l_wave
            wave = np.clip(wave, -1, 1)
            # Convert to audio
            audio = (wave * volume * 32767).astype(np.int16)
            audio_stereo = np.column_stack((audio, audio))
            song = np.concatenate((song, audio_stereo))
            # Update note durations
            if melody_idx < melody_len:
                melody[melody_idx][1] -= step_beats
                if melody[melody_idx][1] <= 0:
                    melody_idx += 1
            if bass_idx < bass_len:
                bass[bass_idx][1] -= step_beats
                if bass[bass_idx][1] <= 0:
                    bass_idx += 1
            if percussion is not None and perc_idx < perc_len:
                percussion[perc_idx][1] -= step_beats
                if percussion[perc_idx][1] <= 0:
                    perc_idx += 1
            if lead is not None and lead_idx < lead_len:
                lead[lead_idx][1] -= step_beats
                if lead[lead_idx][1] <= 0:
                    lead_idx += 1
        return pygame.sndarray.make_sound(song) 