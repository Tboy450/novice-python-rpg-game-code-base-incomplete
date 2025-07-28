"""
Android Utilities Module
========================

This module contains utility functions for Android-specific functionality.
"""

def is_android():
    """
    Detects if the game is running on Android platform.
    Used for enabling touch controls and platform-specific features.
    
    Returns:
        bool: True if running on Android, False otherwise
    """
    import os
    import sys
    return (
        sys.platform.startswith("android") or
        "ANDROID_ARGUMENT" in os.environ
    ) 