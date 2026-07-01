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
    x_mid = tile_x - TILEWIDTH/2
    y_mid = tile_y - TILEHEIGHT/2
    # Calculate center color (also used for background)
    center_fill_color = "red" 
    if playerColor == 'y':
        center_fill_color = "yellow"
    print(f"center_fill_color: {center_fill_color}")
    
    # Draw tile background (same color as center)
    p1 = Point(tile_x, tile_y)
    p2 = Point(tile_x + tile_size, tile_y + tile_size)
    print(f"Background rectangle: fill={center_fill_color}, outline={outlineColor}, coords=({p1.x}, {p1.y}), ({p2.x}, {p2.y})")
    tile_rect = Rectangle(p1, p2)
    tile_rect.setFill(center_fill_color)
    tile_rect.setOutline(outlineColor)
    tile_rect.setWidth(2)
    tile_rect.draw(win)

    # Draw side indicators based on r1, r2, r3, r4 parameters
    # r4: top side, r3: right side, r2: bottom side, r1: left side
    # Top side (r4) - triangle
    top_color = "blue" if r4 == 'b' else "green"
    # Create triangle with 3 points:
    # - Center of tile
    # - Min x, min y (top left corner)
    # - Max x, min y (top right corner)
    p1 = Point(tile_x + tile_size/2, tile_y + tile_size/2)  # Center
    p2 = Point(tile_x, tile_y)  # Top left corner
    p3 = Point(tile_x + tile_size, tile_y)  # Top right corner
    print(f"Top triangle: fill={top_color}, outline={outlineColor}, coords=({p1.x}, {p1.y}), ({p2.x}, {p2.y}), ({p3.x}, {p3.y})")
    top_triangle = Polygon(p1, p2, p3)
    top_triangle.setFill(top_color)
    top_triangle.setOutline(outlineColor)
    top_triangle.draw(win)
    
    # Right side (r3) - triangle
    right_color = "blue" if r3 == 'b' else "green"
    # Create triangle with 3 points:
    # - Center of tile
    # - Top right corner of tile
    # - Bottom right corner of tile
    p1 = Point(tile_x + tile_size/2, tile_y + tile_size/2)  # Center
    p2 = Point(tile_x + tile_size, tile_y)  # Top right corner
    p3 = Point(tile_x + tile_size, tile_y + tile_size)  # Bottom right corner
    print(f"Right triangle: fill={right_color}, outline={outlineColor}, coords=({p1.x}, {p1.y}), ({p2.x}, {p2.y}), ({p3.x}, {p3.y})")
    right_triangle = Polygon(p1, p2, p3)
    right_triangle.setFill(right_color)
    right_triangle.setOutline(outlineColor)
    right_triangle.draw(win)
    
    # Bottom side (r2) - triangle
    bottom_color = "blue" if r2 == 'b' else "green"
    # Create triangle with 3 points:
    # - Center of tile
    # - Min x, max y (bottom left corner)
    # - Max x, max y (bottom right corner)
    p1 = Point(tile_x + tile_size/2, tile_y + tile_size/2)  # Center
    p2 = Point(tile_x, tile_y + tile_size)  # Bottom left corner
    p3 = Point(tile_x + tile_size, tile_y + tile_size)  # Bottom right corner
    print(f"Bottom triangle: fill={bottom_color}, outline={outlineColor}, coords=({p1.x}, {p1.y}), ({p2.x}, {p2.y}), ({p3.x}, {p3.y})")
    bottom_triangle = Polygon(p1, p2, p3)
    bottom_triangle.setFill(bottom_color)
    bottom_triangle.setOutline(outlineColor)
    bottom_triangle.draw(win)
    
    # Left side (r1) - triangle
    left_color = "blue" if r1 == 'b' else "green"
    # Create triangle with 3 points:
    # - Center of tile
    # - Min x, min y (top left corner)
    # - Min x, max y (bottom left corner)
    p1 = Point(tile_x + tile_size/2, tile_y + tile_size/2)  # Center
    p2 = Point(tile_x, tile_y)  # Top left corner
    p3 = Point(tile_x, tile_y + tile_size)  # Bottom left corner
    print(f"Left triangle: fill={left_color}, outline={outlineColor}, coords=({p1.x}, {p1.y}), ({p2.x}, {p2.y}), ({p3.x}, {p3.y})")
    left_triangle = Polygon(p1, p2, p3)
    left_triangle.setFill(left_color)
    left_triangle.setOutline(outlineColor)
    left_triangle.draw(win)
    
    # Draw center (same color as background, no border) - drawn after sides
    center_size = tile_size // 3
    center_x = tile_x + (tile_size - center_size) // 2
    center_y = tile_y + (tile_size - center_size) // 2
    p1 = Point(center_x, center_y)
    p2 = Point(center_x + center_size, center_y + center_size)
    print(f"Center rectangle: fill={center_fill_color}, outline={center_fill_color}, coords=({p1.x}, {p1.y}), ({p2.x}, {p2.y})")
    center_rect = Rectangle(p1, p2) 
    center_rect.setFill(center_fill_color)
    center_rect.setOutline(center_fill_color)  # Same color as fill, no visible border
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
    #if os.path.exists(filepath):
    #    print(f"File {filepath} already exists, skipping creation")
    #    return None
    
    # Create PIL image to draw the tile
    tile_size = TILEHEIGHT
    center_fill_color = "red" if playerColor == 'r' else "yellow"
    img = Image.new('RGB', (tile_size, tile_size), center_fill_color)
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([0, 0, tile_size, tile_size], outline="black", width=2)
    
    # Draw side indicators based on r1, r2, r3, r4
    # r4: top side, r3: right side, r2: bottom side, r1: left side
    # Use triangles matching draw_tile logic
    
    # Top side (r4) - triangle
    top_color = "blue" if r4 == 'b' else "green"
    # Triangle with center + top-left + top-right corners
    draw.polygon([
        (tile_size // 2, tile_size // 2),  # Center
        (0, 0),  # Top left corner
        (tile_size, 0)  # Top right corner
    ], fill=top_color, outline="black")
    
    # Right side (r3) - triangle
    right_color = "blue" if r3 == 'b' else "green"
    # Triangle with center + top-right + bottom-right corners
    draw.polygon([
        (tile_size // 2, tile_size // 2),  # Center
        (tile_size, 0),  # Top right corner
        (tile_size, tile_size)  # Bottom right corner
    ], fill=right_color, outline="black")
    
    # Bottom side (r2) - triangle
    bottom_color = "blue" if r2 == 'b' else "green"
    # Triangle with center + bottom-left + bottom-right corners
    draw.polygon([
        (tile_size // 2, tile_size // 2),  # Center
        (0, tile_size),  # Bottom left corner
        (tile_size, tile_size)  # Bottom right corner
    ], fill=bottom_color, outline="black")
    
    # Left side (r1) - triangle
    left_color = "blue" if r1 == 'b' else "green"
    # Triangle with center + top-left + bottom-left corners
    draw.polygon([
        (tile_size // 2, tile_size // 2),  # Center
        (0, 0),  # Top left corner
        (0, tile_size)  # Bottom left corner
    ], fill=left_color, outline="black")
    
    # Draw center (same color as background, no border) - drawn after sides
    center_size = tile_size // 3
    center_x = (tile_size - center_size) // 2
    center_y = (tile_size - center_size) // 2
    # center_fill_color already set above
    draw.rectangle([center_x, center_y, center_x + center_size, center_y + center_size], 
                   fill=center_fill_color, outline=center_fill_color)
    
    # Create assets directory if it doesn't exist
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    # Save as GIF
    img.save(filepath, 'GIF')
    print(f"Successfully saved {filepath}")
    
    return None  # Success

