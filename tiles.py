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

def draw_tile(win, centerColor='r', r1='b', r2='b', r3='g', r4='b'):
    """
    Draw a tile using graphics.py drawing commands.
    
    Parameters:
    win: graphics window
    centerColor: center color ('r' for red, 'y' for yellow)
    r1: left side color ('b' for blue, 'g' for green)
    r2: bottom side color ('b' for blue, 'g' for green)
    r3: right side color ('b' for blue, 'g' for green)
    r4: top side color ('b' for blue, 'g' for green)
    
    Returns: None on success, error message string if validation fails
    
    Places the tile in the bottom right corner of the client window.
    """
    print(f"draw_tile called with: centerColor={centerColor}, r1={r1}, r2={r2}, r3={r3}, r4={r4}")
    outlineColor='black'
    # Validate centerColor separately (r or y)
    center_valid_colors = ['r', 'y']
    if centerColor not in center_valid_colors:
        return f"Error: centerColor must be 'r' or 'y', got '{centerColor}'"
    
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
    if centerColor == 'y':
        center_fill_color = "yellow"
    
    # Draw tile background (same color as center)
    p1 = Point(tile_x, tile_y)
    p2 = Point(tile_x + tile_size, tile_y + tile_size)
    tile_rect = Rectangle(p1, p2)
    tile_rect.setFill(center_fill_color)
    tile_rect.setOutline(outlineColor)
    tile_rect.setWidth(2)
    tile_rect.draw(win)

    # Draw side indicators based on r1, r2, r3, r4 parameters
    # r4: top side, r3: right side, r2: bottom side, r1: left side
    # Top side (r4)
    top_width = tile_size
    top_height = tile_size 
    top_x_calc = tile_x + (tile_size - top_width) 
    top_y_calc = tile_y
    top_color = "blue" if r4 == 'b' else "green"
    p1 = Point(top_x_calc, top_y_calc)
    p2 = Point(top_x_calc + top_width, top_y_calc + top_height)
    top_rect = Rectangle(p1, p2)
    top_rect.setFill(top_color)
    top_rect.setOutline(outlineColor)
    top_rect.draw(win)
    
    # Right side (r3) - triangle
    right_color = "blue" if r3 == 'b' else "green"
    # Create triangle with 3 points:
    # - Center of tile
    # - Top right corner of tile
    # - Bottom right corner of tile
    p1 = Point(tile_x + x_mid, tile_y + y_mid)  # Center
    p2 = Point(tile_x + tile_size, tile_y)  # Top right corner
    p3 = Point(tile_x + tile_size, top_y_calc + top_height)  # Bottom right corner
    print(f"Polygon coordinates: ({p1.x}, {p1.y}), ({p2.x}, {p2.y}), ({p3.x}, {p3.y})")
    # Also display polygon coordinates in the window
    right_triangle = Polygon(p1, p2, p3)
    right_triangle.setFill(right_color)
    right_triangle.setOutline(outlineColor)
    right_triangle.draw(win)
    
    # Bottom side (r2)
    bottom_width = tile_size // 2
    bottom_height = tile_size // 6
    bottom_x_calc = tile_x + (tile_size - bottom_width) // 2
    bottom_y_calc = tile_y + tile_size - bottom_height
    bottom_color = "blue" if r2 == 'b' else "green"
    p1 = Point(bottom_x_calc, bottom_y_calc)
    p2 = Point(bottom_x_calc + bottom_width, bottom_y_calc + bottom_height)
    bottom_rect = Rectangle(p1, p2)
    bottom_rect.setFill(bottom_color)
    bottom_rect.setOutline(outlineColor)
    bottom_rect.draw(win)
    
    # Left side (r1)
    left_width = tile_size // 6
    left_height = tile_size // 2
    left_x_calc = tile_x
    left_y_calc = tile_y + (tile_size - left_height) // 2
    left_color = "blue" if r1 == 'b' else "green"
    p1 = Point(left_x_calc, left_y_calc)
    p2 = Point(left_x_calc + left_width, left_y_calc + left_height)
    left_rect = Rectangle(p1, p2) 
    left_rect.setFill(left_color)
    left_rect.setOutline(outlineColor)
    left_rect.draw(win)
    
    # Draw center (same color as background, no border) - drawn after sides
    center_size = tile_size // 3
    center_x = tile_x + (tile_size - center_size) // 2
    center_y = tile_y + (tile_size - center_size) // 2
    p1 = Point(center_x, center_y)
    p2 = Point(center_x + center_size, center_y + center_size)
    center_rect = Rectangle(p1, p2) 
    center_rect.setFill(center_fill_color)
    center_rect.setOutline(center_fill_color)  # Same color as fill, no visible border
    center_rect.setWidth(1)
    center_rect.draw(win)
    
    return None  # Success

def create_tile_gif(centerColor, r1='b', r2='b', r3='b', r4='b'):
    """
    Create a GIF file from tile parameters using PIL/Pillow.
    
    Parameters:
    centerColor: center color ('r' for red, 'y' for yellow)
    r1: left side color ('b' for blue, 'g' for green)
    r2: bottom side color ('b' for blue, 'g' for green)
    r3: right side color ('b' for blue, 'g' for green)
    r4: top side color ('b' for blue, 'g' for green)
    
    Returns: None on success, error message string if validation fails
    """
    # Validate centerColor separately (r or y)
    center_valid_colors = ['r', 'y']
    if centerColor not in center_valid_colors:
        return f"Error: centerColor must be 'r' or 'y', got '{centerColor}'"
    
    # Validate side parameters (b or g)
    side_valid_colors = ['b', 'g']
    for param_name, param_value in [('r1', r1), ('r2', r2), ('r3', r3), ('r4', r4)]:
        if param_value not in side_valid_colors:
            return f"Error: {param_name} must be 'b' or 'g', got '{param_value}'"
    
    # Generate filename: r1+r2+r3+r4 + '_' + centerColor + '.gif'
    # Convert centerColor to uppercase for filename (R for red, Y for yellow)
    centerColor_upper = centerColor.upper()
    filename = f"{r1}{r2}{r3}{r4}-{centerColor_upper}.gif"
    filepath = os.path.join("assets", filename)
    
    # Check if file already exists, return if it does
    if os.path.exists(filepath):
        print(f"File {filepath} already exists, skipping creation")
        return None
    
    # Create PIL image to draw the tile
    tile_size = TILEHEIGHT
    center_fill_color = "red" if centerColor == 'r' else "yellow"
    img = Image.new('RGB', (tile_size, tile_size), center_fill_color)
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([0, 0, tile_size, tile_size], outline="black", width=2)
    
    # Draw side indicators based on r1, r2, r3, r4
    # r4: top side, r3: right side, r2: bottom side, r1: left side
    top_width = tile_size // 2
    top_height = tile_size // 6
    top_x = (tile_size - top_width) // 2
    top_y = 0
    top_color = "blue" if r4 == 'b' else "green"
    draw.rectangle([top_x, top_y, top_x + top_width, top_y + top_height], 
                   fill=top_color, outline="black")
    
    right_width = tile_size // 6
    right_height = tile_size // 2
    right_x = tile_size - right_width
    right_y = (tile_size - right_height) // 2
    right_color = "blue" if r3 == 'b' else "green"
    # Draw triangle instead of rectangle
    draw.polygon([
        (right_x, right_y),
        (right_x, right_y + right_height),
        (right_x + right_width, right_y + right_height // 2)
    ], fill=right_color, outline="black")
    
    bottom_width = tile_size // 2
    bottom_height = tile_size // 6
    bottom_x = (tile_size - bottom_width) // 2
    bottom_y = tile_size - bottom_height
    bottom_color = "blue" if r2 == 'b' else "green"
    draw.rectangle([bottom_x, bottom_y, bottom_x + bottom_width, bottom_y + bottom_height], 
                   fill=bottom_color, outline="black")
    
    left_width = tile_size // 6
    left_height = tile_size // 2
    left_x = 0
    left_y = (tile_size - left_height) // 2
    left_color = "blue" if r1 == 'b' else "green"
    draw.rectangle([left_x, left_y, left_x + left_width, left_y + left_height], 
                   fill=left_color, outline="black")
    
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

def draw_rrry_r_tile(win):
    """
    Draw a RRRY-R tile using graphics.py drawing commands.
    RRRY pattern: Red-Red-Red-Yellow (top, right, bottom, left)
    Center: Red
    
    Places the tile in the bottom right corner of the client window.
    """
    # Calculate tile position in bottom right corner
    win_width = win.getWidth()
    win_height = win.getHeight()
    
    tile_size = TILEHEIGHT
    tile_x = win_width - tile_size - 10  # 10 pixels padding from right
    tile_y = win_height - tile_size - 10  # 10 pixels padding from bottom
    
    # Draw tile background (light gray)
    tile_rect = Rectangle(Point(tile_x, tile_y), 
                        Point(tile_x + tile_size, tile_y + tile_size))
    tile_rect.setFill("lightgray")
    tile_rect.setOutline("black")
    tile_rect.setWidth(2)
    tile_rect.draw(win)
    
    # Draw center (red)
    center_size = tile_size // 3
    center_x = tile_x + (tile_size - center_size) // 2
    center_y = tile_y + (tile_size - center_size) // 2
    center_rect = Rectangle(Point(center_x, center_y), 
                          Point(center_x + center_size, center_y + center_size))
    center_rect.setFill("red")
    center_rect.setOutline("black")
    center_rect.setWidth(1)
    center_rect.draw(win)
    
    # Draw side indicators (RRRY pattern: Red-Red-Red-Yellow)
    # Top side (red)
    top_width = tile_size // 2
    top_height = tile_size // 6
    top_x = tile_x + (tile_size - top_width) // 2
    top_y = tile_y
    top_rect = Rectangle(Point(top_x, top_y), 
                      Point(top_x + top_width, top_y + top_height))
    top_rect.setFill("red")
    top_rect.setOutline("black")
    top_rect.draw(win)
    
    # Right side (red)
    right_width = tile_size // 6
    right_height = tile_size // 2
    right_x = tile_x + tile_size - right_width
    right_y = tile_y + (tile_size - right_height) // 2
    right_rect = Rectangle(Point(right_x, right_y), 
                         Point(right_x + right_width, right_y + right_height))
    right_rect.setFill("red")
    right_rect.setOutline("black")
    right_rect.draw(win)
    
    # Bottom side (red)
    bottom_width = tile_size // 2
    bottom_height = tile_size // 6
    bottom_x = tile_x + (tile_size - bottom_width) // 2
    bottom_y = tile_y + tile_size - bottom_height
    bottom_rect = Rectangle(Point(bottom_x, bottom_y), 
                           Point(bottom_x + bottom_width, bottom_y + bottom_height))
    bottom_rect.setFill("red")
    bottom_rect.setOutline("black")
    bottom_rect.draw(win)
    
    # Left side (yellow)
    left_width = tile_size // 6
    left_height = tile_size // 2
    left_x = tile_x
    left_y = tile_y + (tile_size - left_height) // 2
    left_rect = Rectangle(Point(left_x, left_y), 
                        Point(left_x + left_width, left_y + left_height))
    left_rect.setFill("yellow")
    left_rect.setOutline("black")
    left_rect.draw(win)