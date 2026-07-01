from graphics import *
from noodling_values import *
import os

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Installing PIL/Pillow...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw

def get_tile_drawing_commands(playerColor, r1, r2, r3, r4, tile_size=TILEHEIGHT):
    """
    Get the drawing commands for a tile that can be used by both graphics.py and PIL.
    
    Parameters:
    playerColor: center color ('r' for red, 'y' for yellow)
    r1: left side color ('b' for blue, 'g' for green)
    r2: bottom side color ('b' for blue, 'g' for green)
    r3: right side color ('b' for blue, 'g' for green)
    r4: top side color ('b' for blue, 'g' for green)
    tile_size: size of the tile
    
    Returns: dict with drawing commands for background, triangles, and center
    """
    # Calculate center color
    center_fill_color = "red" if playerColor == 'r' else "yellow"
    
    # Calculate colors for sides
    top_color = "blue" if r4 == 'b' else "green"
    right_color = "blue" if r3 == 'b' else "green"
    bottom_color = "blue" if r2 == 'b' else "green"
    left_color = "blue" if r1 == 'b' else "green"
    
    # Calculate center size
    center_size = tile_size // 3
    center_x = (tile_size - center_size) // 2
    center_y = (tile_size - center_size) // 2
    
    return {
        'background': {
            'color': center_fill_color,
            'x': 0,
            'y': 0,
            'width': tile_size,
            'height': tile_size
        },
        'top_triangle': {
            'color': top_color,
            'points': [
                (tile_size // 2, tile_size // 2),  # Center
                (0, 0),  # Top left corner
                (tile_size, 0)  # Top right corner
            ]
        },
        'right_triangle': {
            'color': right_color,
            'points': [
                (tile_size // 2, tile_size // 2),  # Center
                (tile_size, 0),  # Top right corner
                (tile_size, tile_size)  # Bottom right corner
            ]
        },
        'bottom_triangle': {
            'color': bottom_color,
            'points': [
                (tile_size // 2, tile_size // 2),  # Center
                (0, tile_size),  # Bottom left corner
                (tile_size, tile_size)  # Bottom right corner
            ]
        },
        'left_triangle': {
            'color': left_color,
            'points': [
                (tile_size // 2, tile_size // 2),  # Center
                (0, 0),  # Top left corner
                (0, tile_size)  # Bottom left corner
            ]
        },
        'center': {
            'color': center_fill_color,
            'x': center_x,
            'y': center_y,
            'width': center_size,
            'height': center_size
        }
    }

def draw_tile(win, playerColor='r', r1='b', r2='b', r3='g', r4='b'):
    """
    Draw a tile using graphics.py drawing commands.
    
    Parameters:
    win: graphics window
    playerColor: center color ('r' for red, 'y' for yellow)
    r1: left side color ('b' for blue, 'g' for green)
    r2: bottom side color ('b' for blue, 'g' for green)
    r3: right side color ('b' for blue, 'g' for green)
    r4: top side color ('b' for blue, 'g' for green)
    
    Returns: None on success, error message string if validation fails
    
    Places the tile in the bottom right corner of the client window.
    """
    print(f"draw_tile called with: playerColor={playerColor}, r1={r1}, r2={r2}, r3={r3}, r4={r4}")
    outlineColor='black'
    # Validate playerColor separately (r or y)
    center_valid_colors = ['r', 'y']
    if playerColor not in center_valid_colors:
        return f"Error: playerColor must be 'r' or 'y', got '{playerColor}'"
    
    # Validate side parameters (b or g)
    side_valid_colors = ['b', 'g']
    for param_name, param_value in [('r1', r1), ('r2', r2), ('r3', r3), ('r4', r4)]:
        if param_value not in side_valid_colors:
            return f"Error: {param_name} must be 'b' or 'g', got '{param_value}'"
    
    # Only proceed with drawing if we have a valid window
    if win is None:
        return None  # Validation passed, but no window to draw on
    
    # Calculate tile position in bottom right corner
    win_width = win.getWidth()
    win_height = win.getHeight()
    
    tile_size = TILEHEIGHT
    tile_x = win_width - tile_size - 10  # 10 pixels padding from right
    tile_y = win_height - tile_size - 10  # 10 pixels padding from bottom
    
    # Get drawing commands
    commands = get_tile_drawing_commands(playerColor, r1, r2, r3, r4, tile_size)
    
    # Draw background
    bg = commands['background']
    p1 = Point(tile_x + bg['x'], tile_y + bg['y'])
    p2 = Point(tile_x + bg['x'] + bg['width'], tile_y + bg['y'] + bg['height'])
    print(f"Background rectangle: fill={bg['color']}, outline={outlineColor}, coords=({p1.x}, {p1.y}), ({p2.x}, {p2.y})")
    tile_rect = Rectangle(p1, p2)
    tile_rect.setFill(bg['color'])
    tile_rect.setOutline(outlineColor)
    tile_rect.setWidth(2)
    tile_rect.draw(win)
    
    # Draw triangles
    triangles = ['top_triangle', 'right_triangle', 'bottom_triangle', 'left_triangle']
    for triangle_name in triangles:
        tri = commands[triangle_name]
        points = [Point(tile_x + p[0], tile_y + p[1]) for p in tri['points']]
        print(f"{triangle_name}: fill={tri['color']}, outline={outlineColor}, coords=({points[0].x}, {points[0].y}), ({points[1].x}, {points[1].y}), ({points[2].x}, {points[2].y})")
        polygon = Polygon(points[0], points[1], points[2])
        polygon.setFill(tri['color'])
        polygon.setOutline(outlineColor)
        polygon.draw(win)
    
    # Draw center
    center = commands['center']
    p1 = Point(tile_x + center['x'], tile_y + center['y'])
    p2 = Point(tile_x + center['x'] + center['width'], tile_y + center['y'] + center['height'])
    print(f"Center rectangle: fill={center['color']}, outline={center['color']}, coords=({p1.x}, {p1.y}), ({p2.x}, {p2.y})")
    center_rect = Rectangle(p1, p2)
    center_rect.setFill(center['color'])
    center_rect.setOutline(center['color'])
    center_rect.setWidth(1)
    center_rect.draw(win)
    
    return None  # Success

def create_tile_gif(playerColor = 'r', r1='b', r2='b', r3='g', r4='b'):
    """
    Create a GIF file from tile parameters using PIL/Pillow.
    
    Parameters:
    playerColor: center color ('r' for red, 'y' for yellow)
    r1: left side color ('b' for blue, 'g' for green)
    r2: bottom side color ('b' for blue, 'g' for green)
    r3: right side color ('b' for blue, 'g' for green)
    r4: top side color ('b' for blue, 'g' for green)
    
    Returns: None on success, error message string if validation fails
    """
    # Validate playerColor separately (r or y)
    center_valid_colors = ['r', 'y']
    if playerColor not in center_valid_colors:
        return f"Error: playerColor must be 'r' or 'y', got '{playerColor}'"
    
    # Validate side parameters (b or g)
    side_valid_colors = ['b', 'g']
    for param_name, param_value in [('r1', r1), ('r2', r2), ('r3', r3), ('r4', r4)]:
        if param_value not in side_valid_colors:
            return f"Error: {param_name} must be 'b' or 'g', got '{param_value}'"
    
    # Generate filename: r1+r2+r3+r4 + '_' + playerColor + '.gif'
    # Convert playerColor to uppercase for filename (R for red, Y for yellow)
    playerColor_upper = playerColor.upper()
    filename = f"{r1}{r2}{r3}{r4}-{playerColor_upper}.gif"
    filepath = os.path.join("assets", filename)
    
    # Check if file already exists, return if it does
    if os.path.exists(filepath):
        print(f"File {filepath} already exists, skipping creation")
        return None
    
    # Create PIL image to draw the tile
    tile_size = TILEHEIGHT
    commands = get_tile_drawing_commands(playerColor, r1, r2, r3, r4, tile_size)
    
    # Create image with background color
    bg = commands['background']
    img = Image.new('RGB', (tile_size, tile_size), bg['color'])
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([0, 0, tile_size, tile_size], outline="black", width=2)
    
    # Draw triangles using the same coordinates as draw_tile
    triangles = ['top_triangle', 'right_triangle', 'bottom_triangle', 'left_triangle']
    for triangle_name in triangles:
        tri = commands[triangle_name]
        draw.polygon(tri['points'], fill=tri['color'], outline="black")
    
    # Draw center
    center = commands['center']
    draw.rectangle([center['x'], center['y'], center['x'] + center['width'], center['y'] + center['height']], 
                   fill=center['color'], outline=center['color'])
    
    # Create assets directory if it doesn't exist
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    # Save as GIF
    img.save(filepath, 'GIF')
    print(f"Successfully saved {filepath}")
    
    return None  # Success

