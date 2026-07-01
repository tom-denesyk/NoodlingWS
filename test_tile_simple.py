from tiles import create_tile_gif

# Test create_tile_gif with parameters (r, b, b, g, b)
# playerColor='r', r1='b', r2='b', r3='g', r4='b'
print("Testing create_tile_gif with parameters: playerColor='r', r1='b', r2='b', r3='g', r4='b'")
result = create_tile_gif('r', 'b', 'b', 'g', 'b')
if result is not None:
    print(f"Error: {result}")
else:
    print("GIF created successfully!")
    print("Filename should be: bbgg-R.gif (r1+r2+r3+r4-playerColor)")
    print("Should be in ./assets directory")