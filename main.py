from noodling import *                            
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" 
import asyncio                                    
import pygame
import sys
from tiles import create_tile_gif

#
sel = selectors.DefaultSelector()
#
def formMouseDict(conIdx, x, y):
    j = {OPCODE_:MOUSE_XY_CODE, \
         CONIDX_:HEADERLEN_FMT.format(conIdx),        \
         X_:HEADERLEN_FMT.format(x), \
         Y_:HEADERLEN_FMT.format(y)}
    return j
#
def checkForMouseXY(clientId, freeTile, sock):
    doit = 0
    x = 0
    y = 0
    for event in pygame.event.get():
        print(pygame.event.event_name(event.type))
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if pygame.mouse.get_pressed()[0]:
                if int(clientId[PLAYER_]) == WHITE_I or freeTile == None \
                    or freeTile[PLAYER_] == clientId[PLAYER_]:
                    x = pygame.mouse.get_pos()[0] 
                    y = pygame.mouse.get_pos()[1]
                    doit = 1
                    break
        elif event.type == pygame.QUIT:
            print("Invoke QUIT BOX Actions")
            x = QUITX1 + 1
            y = QUITY1 + 1
            doit = 1
            break

    if doit != 0:
        dict = formMouseDict(int(clientId[CONIDX_]), int(x), int(y))
        txDictToSock(sock, dict)
        pygame.event.clear()

#
async def main():
    pygame.init()
    
    # Generate required GIFs if they don't exist
    print("Generating required GIF files...")
    # Side encoding: r4 (top, bit 0), r3 (right, bit 1), r2 (bottom, bit 2), r1 (left, bit 3)
    # 'b' (blue) = bit=1, 'g' (green) = bit=0
    # BBBG (0xE = 1110): r4='g', r3='b', r2='b', r1='b' -> bbbg
    # GGGB (0x1 = 0001): r4='b', r3='g', r2='g', r1='g' -> gggb
    # BBGG (0xC = 1100): r4='g', r3='g', r2='b', r1='b' -> bbgg
    gif_configs = [
        ('r', 'b', 'b', 'g', 'g'),  # BBGG-R: r1='b', r2='b', r3='g', r4='g'
        ('y', 'b', 'b', 'g', 'g'),  # BBGG-Y
        ('r', 'g', 'g', 'g', 'b'),  # GGGB-R: r1='g', r2='g', r3='g', r4='b'
        ('y', 'g', 'g', 'g', 'b'),  # GGGB-Y
        ('r', 'b', 'b', 'b', 'g'),  # BBBG-R: r1='b', r2='b', r3='b', r4='g'
        ('y', 'b', 'b', 'b', 'g'),  # BBBG-Y
    ]
    
    for config in gif_configs:
        playerColor, r1, r2, r3, r4 = config
        result = create_tile_gif(playerColor, r1, r2, r3, r4)
        if result is not None:
            print(f"Error creating GIF: {result}")
    
    print("GIF generation complete.")
    
    # Parse command line arguments for window positioning
    window_x = 0
    window_y = 0
    if len(sys.argv) > 1:
        try:
            window_x = int(sys.argv[1])
            if len(sys.argv) > 2:
                window_y = int(sys.argv[2])
        except ValueError:
            window_x = 0
            window_y = 0
    
    # Set window position using environment variable
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_x},{window_y}"
    
    surface = pygame.display.set_mode((GAMEMAXX, GAMEMAXY))
    pygame.display.set_caption("Client")
    pygame.display.update()
    # #################
    gridRandomInit()
    drawGridAndFreeTile(sel, surface)      
    lockEval()
    evalLikeForLikeForScore()
    evalReplaceablesForScore()
    printStatusOnClient(surface)
    # ##################
    txtToSurface(surface, "Click to RESTART", \
                 FREETILEX1+TILEWIDTH*2.8, FREETILEY1+TILEHEIGHT*0.95, \
                 WHITE, BKGDCOLOR)
    pygame.display.update()
    txtToSurface(surface, "Click to QUIT", \
                 FREETILEX1+TILEWIDTH*2.8, FREETILEY1+TILEHEIGHT*0.7, \
                 WHITE, BKGDCOLOR)
    pygame.display.update()

    clientId = None
    print("listening for", SERVER_NAME, ":", SERVER_PORT) 
    server_addr = ("127.0.0.1", SERVER_PORT)
    print("listening for", server_addr) 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(True)    
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(sock, events, data=None)
    loop = True

    clock = pygame.time.Clock()

    while loop == True:
        clock.tick(30)
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            loop = False
            continue

        if clientId != None:
            checkForMouseXY(clientId, freeTile, sock)

        dict = dictRx(sel)
        if dict != None:
            opcode = dict[OPCODE_]
            print(opcode)
            if opcode == TXT_CODE:
                # Clear the area where text will be drawn to avoid artifacts
                x = int(dict[X_])
                y = int(dict[Y_])
                points = int(dict[POINTS_])
                # Create a much larger rectangle to clear (very generous to handle "'s turn" suffix)
                # Use fixed size based on maximum expected text length
                max_text_length = 20  # Maximum expected characters (e.g., "YELLOW PLAYER's turn")
                text_width = max_text_length * points * 0.7  # Fixed generous width
                text_height = points * 2.0  # Increased height multiplier
                clear_rect = pygame.Rect(x - text_width/2, y - text_height/2, text_width, text_height)
                pygame.draw.rect(surface, BLACK, clear_rect)
                
                txtToSurface(surface, dict[STR_], \
                             int(dict[X_]), int(dict[Y_]), \
                             int(dict[FGD_]), int(dict[BGD_]), \
                             dict[FONT_], int(dict[POINTS_]))
                pygame.display.update()
            elif opcode == TILE_CODE:
                gdIdx = getTileIdx(int(dict[X_]), int(dict[Y_]))
                if gdIdx == FREETILEIDX:
                    freeTile = dict
                else:
                    placedTile[gdIdx] = dict

                tileToSurface(surface, dict)
                pygame.display.update()

                if gdIdx < FREETILEIDX and gdIdx >= 0:
                    lockEval()
                    evalLikeForLikeForScore()
                    evalReplaceablesForScore()
                    evalLikeForLikeForScore()
                    evalReplaceablesForScore()
                    evalForGameOverOnClient(surface)
                    printStatusOnClient(surface)

                pygame.display.update()
            elif opcode == CLIENT_ID_CODE:
                clientId = dict
            elif opcode == QUIT_CODE:
                loop = False
            #elif opcode == REPLAY_CODE:
            #    loop = False
            else:
                str = "eekeek" + opcode
                print(str)
                loop = False
        else:
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                loop = False

        await asyncio.sleep(0)  # Very important, and keep it 0

    sel.close()
    sys.exit()
#
asyncio.run(main())











