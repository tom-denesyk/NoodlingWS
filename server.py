from noodling import *                            
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" 
import asyncio                                    
import pygame

sel = selectors.DefaultSelector()
#
def accept_wrapper(sel, numClients, sock):
    con, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    con.setblocking(True)
    #data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    ADDR.append(addr)
    CON.append(con) 
    events = selectors.EVENT_READ # Don't worry about selectors.EVENT_WRITE
    sel.register(con, events, data=None)
    if len(CON) == numClients:
        boardInit(sel)
#
def castlingServerMain(arg):
    bufferSize = 8192
    # next create a socket object
    host = ''
    if arg == '2':
        numClients = 2
    else:
        numClients = 1
    #host_ip = socket.gethostbyname('scholomanse.com')
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host, SERVER_PORT))
    lsock.listen()
    print(f"Listening on {(host, SERVER_PORT)}")
    lsock.setblocking(True) # eekeekeek
    sel.register(lsock, selectors.EVENT_READ, data=None)
    while len(CON) != numClients:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                if key.data is None and len(CON) < numClients:
                    accept_wrapper(sel, numClients, key.fileobj)

    opcode = PLAY_CODE
    clock = pygame.time.Clock()

    while opcode != QUIT_CODE:
        clock.tick(1)
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            opcode = QUIT_CODE    # still more hdr bytes to rx
            continue

        dict = dictRx(sel)
        if dict != None:
            opcode = dict[OPCODE_] 
            if opcode == MOUSE_XY_CODE:
                if len(CON) == numClients:
                    opcode = play(sel, int(dict[CONIDX_]), int(dict[X_]), int(dict[Y_]))
            else:
                opcode == QUITE_CODE
    for i in range(0, len(CON)) :
        #print("close con[", i, "]")
        CON[i].close()

    sel.close()

    #print("Server done")
#
def main():
    args = sys.argv [1:] 
    if len(sys.argv) == 1:
        numClients = 1
    else:
        numClients = args[0]

    castlingServerMain(numClients)

main()
