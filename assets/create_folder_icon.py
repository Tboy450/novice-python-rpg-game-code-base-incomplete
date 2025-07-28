"""
Create Dragon Icon for pygame_organized folder
This script generates a dragon icon that can be used as a folder icon
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
except ImportError:
    print("Pillow not installed. Install with: pip install Pillow")
    exit(1)

def create_dragon_icon(size=(256, 256), output_file="folder_icon.ico"):
    """Create a dragon icon for the folder"""
    
    # Create a new image with a dark background
    img = Image.new('RGBA', size, (20, 20, 40, 255))
    draw = ImageDraw.Draw(img)
    
    # Dragon colors
    dragon_colors = {
        'body': (139, 69, 19),      # Brown
        'wings': (178, 34, 34),      # Red
        'claws': (255, 215, 0),      # Gold
        'eyes': (255, 0, 0),         # Red
        'fire': (255, 69, 0),        # Orange
    }
    
    # Calculate positions
    center_x, center_y = size[0] // 2, size[1] // 2
    dragon_size = min(size) // 3
    
    # Draw dragon body (simplified)
    body_points = [
        (center_x - dragon_size//2, center_y + dragon_size//4),
        (center_x + dragon_size//2, center_y + dragon_size//4),
        (center_x + dragon_size//3, center_y + dragon_size//2),
        (center_x - dragon_size//3, center_y + dragon_size//2),
    ]
    draw.polygon(body_points, fill=dragon_colors['body'])
    
    # Draw dragon head
    head_radius = dragon_size // 4
    draw.ellipse([
        center_x - head_radius, center_y - head_radius,
        center_x + head_radius, center_y + head_radius
    ], fill=dragon_colors['body'])
    
    # Draw eyes
    eye_radius = head_radius // 4
    draw.ellipse([
        center_x - head_radius//2 - eye_radius, center_y - eye_radius,
        center_x - head_radius//2 + eye_radius, center_y + eye_radius
    ], fill=dragon_colors['eyes'])
    draw.ellipse([
        center_x + head_radius//2 - eye_radius, center_y - eye_radius,
        center_x + head_radius//2 + eye_radius, center_y + eye_radius
    ], fill=dragon_colors['eyes'])
    
    # Draw wings
    wing_points = [
        (center_x - dragon_size//2, center_y - dragon_size//4),
        (center_x - dragon_size, center_y - dragon_size//2),
        (center_x - dragon_size//2, center_y - dragon_size//2),
    ]
    draw.polygon(wing_points, fill=dragon_colors['wings'])
    
    wing_points2 = [
        (center_x + dragon_size//2, center_y - dragon_size//4),
        (center_x + dragon_size, center_y - dragon_size//2),
        (center_x + dragon_size//2, center_y - dragon_size//2),
    ]
    draw.polygon(wing_points2, fill=dragon_colors['wings'])
    
    # Draw fire breath
    fire_points = [
        (center_x, center_y - head_radius),
        (center_x - head_radius//2, center_y - dragon_size//2),
        (center_x + head_radius//2, center_y - dragon_size//2),
    ]
    draw.polygon(fire_points, fill=dragon_colors['fire'])
    
    # Add text
    try:
        # Try to use a system font
        font_size = size[0] // 12
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    text = "Dragon's Lair"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (size[0] - text_width) // 2
    text_y = size[1] - font_size - 10
    
    # Draw text with outline
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
    
    # Save as ICO file
    img.save(output_file, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print(f"Dragon icon created: {output_file}")
    
    # Also save as PNG for preview
    png_file = output_file.replace('.ico', '.png')
    img.save(png_file, format='PNG')
    print(f"PNG preview created: {png_file}")
    
    return output_file

def create_desktop_ini_for_folder():
    """Create a desktop.ini file to set the folder icon (Windows)"""
    
    desktop_ini_content = """[.ShellClassInfo]
IconResource=C:\\path\\to\\your\\folder_icon.ico,0
[ViewState]
Mode=
Vid=
FolderType=Generic
"""
    
    with open("desktop.ini", "w") as f:
        f.write(desktop_ini_content)
    
    print("desktop.ini created - you'll need to update the path to your icon file")
    print("Then set the folder as a system folder: attrib +s pygame_organized")

if __name__ == "__main__":
    print("Creating Dragon Icon for pygame_organized folder...")
    
    # Create the icon
    icon_file = create_dragon_icon()
    
    # Create desktop.ini for Windows folder icon
    create_desktop_ini_for_folder()
    
    print("\nTo use this as a folder icon on Windows:")
    print("1. Copy the .ico file to a permanent location")
    print("2. Update the path in desktop.ini")
    print("3. Make the folder a system folder: attrib +s pygame_organized")
    print("4. Set the folder to read-only: attrib +r pygame_organized")
    
    print("\nFor macOS/Linux, you can use the .png file as a folder icon")
    print("through your file manager's folder properties.") 