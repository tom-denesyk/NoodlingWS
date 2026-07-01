from graphics import *
from tiles import draw_tile

# Create a graphics window
win = GraphWin("Tile Test", 600, 500)
win.setBackground("white")

# Draw a tile with parameters (r, g, g, b, b)
# centerColor='r', r1='g', r2='g', r3='b', r4='b'
print("Drawing tile with parameters: centerColor='r', r1='g', r2='g', r3='b', r4='b'")
result = draw_tile(win, 'r', 'g', 'g', 'b', 'b')
if result is not None:
    print(f"Error: {result}")
else:
    print("Tile drawn successfully!")
    
    # Display message in window
    message = Text(Point(300, 480), "Tile drawn successfully! Click to close.")
    message.setTextColor("black")
    message.draw(win)

# Wait for user to click to close
win.getMouse()
win.close()