# Town layout and procedural generation extracted from WorldArea class

def generate_town_layout(self):
    """
    Generates the detailed layout for the town area, including buildings, boundaries, and decorations.
    Only runs if the area_type is 'town'.
    """
    if self.area_type != "town":
        return
    # Create town boundaries (walls/gates at the top)
    self.town_boundaries = [
        {"type": "gate", "x": 450, "y": 200, "width": 100, "height": 60},
        {"type": "wall", "x": 0, "y": 200, "width": 450, "height": 20},
        {"type": "wall", "x": 550, "y": 200, "width": 450, "height": 20},
        {"type": "tower", "x": 400, "y": 180, "width": 40, "height": 80},
        {"type": "tower", "x": 560, "y": 180, "width": 40, "height": 80},
    ]
    # Create main buildings
    self.buildings = [
        {"type": "town_hall", "x": 400, "y": 380, "width": 200, "height": 140, "color": (200, 180, 160), "style": "grand", "collision": True},
        {"type": "shop", "x": 60, "y": 430, "width": 140, "height": 90, "color": (180, 160, 200), "style": "magical", "collision": True},
        {"type": "inn", "x": 800, "y": 430, "width": 140, "height": 90, "color": (200, 160, 140), "style": "cozy", "collision": True},
        {"type": "blacksmith", "x": 100, "y": 570, "width": 120, "height": 80, "color": (140, 120, 100), "style": "industrial", "collision": True},
        {"type": "library", "x": 780, "y": 570, "width": 120, "height": 80, "color": (160, 180, 200), "style": "mystical", "collision": True},
        {"type": "house", "x": 750, "y": 340, "width": 70, "height": 60, "color": (150, 130, 110), "style": "cottage", "collision": True},
        {"type": "stall", "x": 450, "y": 530, "width": 100, "height": 50, "color": (170, 150, 130), "style": "market", "collision": True},
    ]
    # Create decorative elements (no collision)
    self.decorations = [
        {"type": "lamp", "x": 150, "y": 300, "width": 20, "height": 60},
        {"type": "lamp", "x": 850, "y": 300, "width": 20, "height": 60},
        {"type": "lamp", "x": 150, "y": 650, "width": 20, "height": 60},
        {"type": "lamp", "x": 850, "y": 650, "width": 20, "height": 60},
        {"type": "tree", "x": 50, "y": 250, "width": 30, "height": 50},
        {"type": "tree", "x": 920, "y": 250, "width": 30, "height": 50},
        {"type": "tree", "x": 50, "y": 700, "width": 30, "height": 50},
        {"type": "tree", "x": 920, "y": 700, "width": 30, "height": 50},
        {"type": "flowers", "x": 200, "y": 270, "width": 40, "height": 20},
        {"type": "flowers", "x": 760, "y": 270, "width": 40, "height": 20},
        {"type": "flowers", "x": 200, "y": 730, "width": 40, "height": 20},
        {"type": "flowers", "x": 760, "y": 730, "width": 40, "height": 20},
    ]
    # Create smoke sources for buildings
    self.smoke_sources = [
        {"x": 150, "y": 430},  # Shop chimney
        {"x": 850, "y": 430},  # Inn chimney
        {"x": 180, "y": 570},  # Blacksmith chimney
        {"x": 820, "y": 570},  # Library chimney
    ] 