from noodling import *                            
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" 
import asyncio                                    
import pygame

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
                txtToSurface(surface, dict[STR_], \
                             int(dict[X_]), int(dict[Y_]), \
                             int(dict[FGD_]), int(dict[FGD_]), \
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
#async def main():
#    castlingClient()

asyncio.run(main())
#main()











