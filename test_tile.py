from graphics import *
from tiles import draw_tile
from noodling_values import GAMEMAXX, GAMEMAXY

def main():
    # Create a graphics window the same size as the client window
    win = GraphWin("Tile Test", GAMEMAXX + 1, GAMEMAXY + 1)
    win.setBackground("black")
    
    # Test with specific values: centerColor='r', r1='r', r2='r', r3='r', r4='y'
    print("Drawing tile with centerColor='r', r1='r', r2='r', r3='r', r4='y'...")
    result = draw_tile(win, 'r', 'r', 'r', 'r', 'y')
    if result is None:
        print("Success: Tile drawn successfully")
        print("Tile configuration:")
        print("  Center: Red")
        print("  Left side: Red")
        print("  Bottom side: Red")
        print("  Right side: Red")
        print("  Top side: Yellow")
    else:
        print(f"Error: {result}")
    
    # Add explanatory text
    text = Text(Point(GAMEMAXX/2, GAMEMAXY/2), "Tile Test: R-RRR-Y")
    text.setTextColor("white")
    text.setSize(20)
    text.draw(win)
    
    instructions = Text(Point(GAMEMAXX/2, GAMEMAXY/2 + 30), "Click anywhere to close")
    instructions.setTextColor("white")
    instructions.setSize(14)
    instructions.draw(win)
    
    # Wait for mouse click to close
    win.getMouse()
    win.close()

if __name__ == "__main__":
    main()