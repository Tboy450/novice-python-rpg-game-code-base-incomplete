"""
Setup script for Dragon's Lair RPG - A Retro-Style Adventure Game
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    with open("../README.md", "r", encoding="utf-8") as fh:
        return fh.read()

setup(
    name="dragons-lair-rpg",
    version="1.0.0",
    author="Dragon's Lair RPG Team",
    author_email="dragonslair@example.com",
    description="A retro-style RPG adventure game with dragon battles and chiptune music",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dragons-lair-rpg",
    packages=find_packages(exclude=["build", "docs", "tests", "assets", "legacy"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pygame>=2.0.0",
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "dragons-lair=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.py"],
    },
    keywords="game, rpg, pygame, dragon, adventure, retro, chiptune",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/dragons-lair-rpg/issues",
        "Source": "https://github.com/yourusername/dragons-lair-rpg",
        "Documentation": "https://github.com/yourusername/dragons-lair-rpg#readme",
    },
) 