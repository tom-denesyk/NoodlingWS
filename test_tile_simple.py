from graphics import *
from tiles import draw_tile

# Create a graphics window
win = GraphWin("Tile Test", 600, 500)
win.setBackground("white")

# Draw a tile with parameters (r, b, b, g, b)
# playerColor='r', r1='b', r2='b', r3='g', r4='b'
# Triangle green, side triangles blue, center red
print("Drawing tile with parameters: playerColor='r', r1='b', r2='b', r3='g', r4='b'")
result = draw_tile(win, 'r', 'b', 'b', 'g', 'b')
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