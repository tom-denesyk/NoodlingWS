from graphics import *
from tiles import draw_tile
from noodling_values import GAMEMAXX, GAMEMAXY, TILEHEIGHT
import os
import sys

# Try to import PIL/Pillow, install if not available
try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Installing PIL/Pillow...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw

def export_tile_as_gif(centerColor, r1, r2, r3, r4, filename):
    """
    Draw a tile and export it as a GIF file using PIL/Pillow.
    """
    # Create PIL image to draw the tile
    tile_size = TILEHEIGHT
    img = Image.new('RGB', (tile_size, tile_size), 'lightgray')
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([0, 0, tile_size, tile_size], outline="black", width=2)
    
    # Draw center
    center_size = tile_size // 3
    center_x = (tile_size - center_size) // 2
    center_y = (tile_size - center_size) // 2
    center_fill_color = "red" if centerColor == 'r' else "yellow"
    draw.rectangle([center_x, center_y, center_x + center_size, center_y + center_size], 
                   fill=center_fill_color, outline="black")
    
    # Draw side indicators based on r1, r2, r3, r4
    # r4: top side, r3: right side, r2: bottom side, r1: left side
    top_width = tile_size // 2
    top_height = tile_size // 6
    top_x = (tile_size - top_width) // 2
    top_y = 0
    top_color = "red" if r4 == 'r' else "yellow"
    draw.rectangle([top_x, top_y, top_x + top_width, top_y + top_height], 
                   fill=top_color, outline="black")
    
    right_width = tile_size // 6
    right_height = tile_size // 2
    right_x = tile_size - right_width
    right_y = (tile_size - right_height) // 2
    right_color = "red" if r3 == 'r' else "yellow"
    draw.rectangle([right_x, right_y, right_x + right_width, right_y + right_height], 
                   fill=right_color, outline="black")
    
    bottom_width = tile_size // 2
    bottom_height = tile_size // 6
    bottom_x = (tile_size - bottom_width) // 2
    bottom_y = tile_size - bottom_height
    bottom_color = "red" if r2 == 'r' else "yellow"
    draw.rectangle([bottom_x, bottom_y, bottom_x + bottom_width, bottom_y + bottom_height], 
                   fill=bottom_color, outline="black")
    
    left_width = tile_size // 6
    left_height = tile_size // 2
    left_x = 0
    left_y = (tile_size - left_height) // 2
    left_color = "red" if r1 == 'r' else "yellow"
    draw.rectangle([left_x, left_y, left_x + left_width, left_y + left_height], 
                   fill=left_color, outline="black")
    
    # Save as GIF
    img.save(filename, 'GIF')
    print(f"Successfully saved {filename}")

def main():
    # Create assets1 directory if it doesn't exist
    if not os.path.exists("assets1"):
        os.makedirs("assets1")
    
    # Export a tile with red center and all red sides
    print("Exporting tile with red center and all red sides...")
    export_tile_as_gif('r', 'r', 'r', 'r', 'r', "assets1/all-red.gif")
    
    # Export a tile with yellow center and mixed sides
    print("Exporting tile with yellow center and mixed sides...")
    export_tile_as_gif('y', 'r', 'y', 'r', 'y', "assets1/mixed.gif")
    
    print("Export complete!")

if __name__ == "__main__":
    main()