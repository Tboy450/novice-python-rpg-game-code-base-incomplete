# Battle UI helpers extracted from BattleScreen class
from ui.button import Button
from config.constants import UI_BORDER

# Example: Battle option buttons setup (positions and labels)
def create_battle_buttons():
    """
    Creates the four main battle option buttons (Attack, Magic, Item, Run).
    Returns:
        list: List of Button objects for the battle screen.
    """
    return [
        Button(50, 525, 180, 50, "ATTACK"),
        Button(250, 525, 180, 50, "MAGIC"),
        Button(450, 525, 180, 50, "ITEM"),
        Button(650, 525, 180, 50, "RUN")
    ]

# (Add health bar drawing, overlays, or other UI helpers here as needed) 