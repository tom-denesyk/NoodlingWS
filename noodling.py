import os
import sys, pygame
import json                                       
from pygame.locals import *
from random import randrange
from noodling_values import *
import time
import socket
import pickle
import traceback
import selectors
import copy
#
CON = []
ADDR = []
BUFFER_SIZE = 8192
LOCK_CNT = [0, 0]
GAME_OVER = False
LIKE_FOR_LIKE = [0, 0]
ONE_FOR_ANOTHER = [0, 0]
PLAYER_COLOR = [PLAYER0, PLAYER1]
TRACE  = True
BLACK = (0, 0, 0)
QUITX1 = FREETILEX1+TILEWIDTH
QUITX2 = GRIDMAXX

QUITY1 =  FREETILEY1+HALFHEIGHT #GRIDMAXY-TILEHEIGHT
QUITY2 =  FREETILEY1+TILEHEIGHT*0.75

REPLAYX1 = FREETILEX1+TILEWIDTH
REPLAYX2 = GRIDMAXX
REPLAYY1 = FREETILEY1+TILEHEIGHT*0.76
REPLAYY2 = FREETILEY1+TILEHEIGHT

#
def traceOnSurface(surface, txt):
    if surface != None:
        txt1 = ":" + str(traceOnSurface.cnt) + ":" + str(txt)
        txtToSurface(surface, txt1, \
                     TILEWIDTH*4, traceOnSurface.y, \
                     WHITE, BKGDCOLOR)
        traceOnSurface.y += 50
        traceOnSurface.cnt += 1
        if traceOnSurface.y >= GAMEMAXY:
            traceOnSurface.y = 10
        #pygame.display.update()
traceOnSurface.y = 10
traceOnSurface.cnt = 0
#
def print_(surface, txt):
    if False and print_.trace == True:
        print(str)
        loc = os.getcwd()
        #traceFilePath = "c:\temp"
        #os.chdir(traceFilePath)
        f = open("trace.txt", "a")
        f.write(str(txt))
        f.write("\n")
        f.flush()
        f.close()

        traceOnSurface(surface, txt)

print_.trace = True
#
def formHeaderDict(dictStr):
    h = {OPCODE_:HEADER_CODE,  \
         DATA_LEN_:HEADERLEN_FMT.format(len(dictStr))}
    return h
#
def formQuitDict():
    dict = {OPCODE_:QUIT_CODE}
    return dict
#
#def formReplayDict():
#    dict = {OPCODE_:REPLAY_CODE}
#    return dict
#
def formClientIdDict(player, conIdx):
    dict = {OPCODE_:CLIENT_ID_CODE,       \
            PLAYER_:HEADERLEN_FMT.format(tripToColEnum(player)), \
            CONIDX_:HEADERLEN_FMT.format(conIdx)}
    return dict
#
def formTextDict(conIdx, fgd, bgd, x, y, str, font='freesansboldTom.ttf', points = 12):
    dict = {OPCODE_:TXT_CODE,        \
            CONIDX_:HEADERLEN_FMT.format(conIdx),          \
            FGD_:HEADERLEN_FMT.format(tripToColEnum(fgd)), \
            BGD_:HEADERLEN_FMT.format(tripToColEnum(bgd)), \
            X_:HEADERLEN_FMT.format(int(x)),               \
            Y_:HEADERLEN_FMT.format(int(y)),               \
            FONT_:font,                                    \
            POINTS_:HEADERLEN_FMT.format(points),          \
            STR_:str}
    return dict
#
def formTileDict(conIdx, x, y, player, sides, rot, locked = 0):
    rot = rot % 4
    if rot > 3:
        str = "rot == " + str(rot)
        print(str)
        rot = 0

    dict = {OPCODE_:TILE_CODE,             \
            CONIDX_:HEADERLEN_FMT.format(conIdx),                \
            X_:HEADERLEN_FMT.format(int(x)),                     \
            Y_:HEADERLEN_FMT.format(int(y)),                     \
            PLAYER_:HEADERLEN_FMT.format(tripToColEnum(player)), \
            SIDES_:HEADERLEN_FMT.format(sides),                  \
            ROT_:HEADERLEN_FMT.format(rot),                      \
            LOCKED_:HEADERLEN_FMT.format(locked)}
    return dict
#
tmpDict = formTileDict(0, 0, 0, RED, BBBG, 0)
tmpDictStr = json.dumps(tmpDict)
hTmp = formHeaderDict(tmpDictStr)
hTmpStr = json.dumps(hTmp)
HDR_LEN = len(hTmpStr)
#
HDR_RX_UNDERWAY     = 1
PAYLOAD_RX_UNDERWAY = 2
PAYLOAD_RDY         = 3
RD_ERROR            = 4
#
def txDictToSock(sock, dict): 
    txDictToSock.count += 1
    #print_(dict)
    dictStr = json.dumps(dict)
    h = {OPCODE_:HEADER_CODE,  \
         DATA_LEN_:HEADERLEN_FMT.format(len(dictStr))}
    hstr = json.dumps(h)
    try:
        #print("Send Header", len(hstr), "DictStr ", h[DATA_LEN_]);
        sock.sendall(hstr.encode('utf-8'))
        sock.sendall(dictStr.encode('utf-8'))
    except:
        print(traceback.format_exc())

#
txDictToSock.count = 0
#
def sendTheDictToAllCONs(dict):
    for conIdx in range(0, len(CON)):
        try:
            sock = CON[conIdx]
            txDictToSock(sock, dict)
        except:
            #print_(traceback.format_exc())
            #print("lost connection")
            break;
#
def dictRx(sel, surface=None):
    events = sel.select(timeout=1)
    if events:
        for key, mask in events:
            sock = key.fileobj
            data = key.data
            if mask & selectors.EVENT_READ:
                try:
                    #traceOnSurface(surface, "dictRx")
                    print_(surface, "mask & selectors.EVENT_READ")
                    hstr = sock.recv(HDR_LEN)
                    hdict = json.loads(hstr)
                    if hdict[OPCODE_] == HEADER_CODE:
                        print_(surface, "hdict[OPCODE_] == HEADER_CODE")
                        #print("Rd dist", int(hdict[DATA_LEN_]))
                        print_(surface, hstr)
                        data = sock.recv(int(hdict[DATA_LEN_]))
                        print_(surface, data)
                        data_dict = json.loads(data)
                        #events.clear()
                        return data_dict
                    else:
                        print_(surface, "hdict[OPCODE_] != HEADER_CODE")
                        print(traceback.format_exc())
                        #events.clear()
                        return None
                except:
                    print(traceback.format_exc())
                    #events.clear()
                    return None
            #
    else:
        return None
#
def boardInit(sel):
    GAME_OVER = False
    freeTile.clear()
    placedTile.clear()
    gridRandomInit()
    lockEval()
    evalLikeForLikeForScore()
    evalReplaceablesForScore()

    #printStatus(sel)
    drawGridAndFreeTile(sel)

    if len(CON) != 0:
        fgd = []
        fgd.append(RED)
        fgd.append(YELLOW)
        txt = ['RED PLAYER', 'YELLOW PLAYER', 'BOTH PLAYERS']
        for conIdx in range(0, len(CON)):
            if len(CON) == 1:
                str = "RED and YELLOW"
                fgd[conIdx] = WHITE
            else:
                # Check whose turn it is based on free tile player color
                freeTilePlayerEnum = int(freeTile[0][PLAYER_])
                currentColorEnum = tripToColEnum(fgd[conIdx])
                if freeTilePlayerEnum == currentColorEnum:
                    str = txt[conIdx] + "'s turn"
                else:
                    str = txt[conIdx]
            dict = formTextDict(conIdx, fgd[conIdx], BLUE, DOUBLEWIDTH, TILEHEIGHT/4, str)
            txDictToSock(CON[conIdx], dict)

            dict = formClientIdDict(fgd[conIdx], conIdx)
            txDictToSock(CON[conIdx], dict)

# ################################################
# Tiles
# ################################################
freeTile = []
placedTile = []
grid = []
#
def isInQuitBox(x, y):
    if (x >= QUITX1):
        if (x <= QUITX2):
            if (y >= QUITY1):
                if (y <= QUITY2):
                    return True
    return False
#
def isInReplayBox(x, y):
    if (x >= REPLAYX1):
        if (x <= REPLAYX2):
            if (y >= REPLAYY1):
                if (y <= REPLAYY2):
                    return True
    return False
#
def getTileIdx(x, y):
    tilex = GRIDMINX
    tiley = GRIDMINY
    if (x >= FREETILEX1) and (x <= FREETILEX2) and (y >= FREETILEY1) and (y <= FREETILEY2):
        return FREETILEIDX
    else:
        gdIdx = 0
        while tilex != GRIDMAXX and tiley != GRIDMAXY:
            if x >= tilex and x < tilex + TILEWIDTH:
                if y >= tiley and y < tiley + TILEHEIGHT:
                    return gdIdx
            gdIdx += 1
            tilex = tilex + TILEWIDTH
            if tilex == GRIDMAXX:
                tilex = GRIDMINX
                tiley += TILEHEIGHT
        return BADIDX
#
def txtToSurface(surface, str, x, y, fgd, bgd, font='freesansboldTom.ttf', points = 12):
    font = pygame.font.Font(font, points)
    text = font.render(str, True, WHITE, BKGDCOLOR,)
    rect = text.get_rect()
    rect.center = (x, y)
    surface.blit(text, rect)
#
def getTileFileName(dict):
    sides = int(dict[SIDES_])
    player = colEnumToTrip(int(dict[PLAYER_]))
    if dict[OPCODE_] == TILE_CODE:
        fileName = None
        if sides == BBBG:
            fileName = "bbbg"
        elif sides == GGGB:
            fileName = "gggb"
        elif sides == BBGG:
            fileName = "bbgg"
        else:
            print("Eek! getTileFileName")

        if fileName == None:
            print("Eek! fileName == None")
        elif player == PLAYER0:
            fileName = fileName + '-R.gif'
        else:
            fileName = fileName + '-Y.gif'

        return fileName

#
def tileToSurface(surface, dict):
    rot = int(dict[ROT_])

    if rot >= 0 and rot < 4:
        x = int(dict[X_])
        y = int(dict[Y_])
        player = colEnumToTrip(dict[PLAYER_])
        gdIdx = getTileIdx(x, y)
        loc = os.getcwd()
        os.chdir(r'assets')
        fileName = getTileFileName(dict)
        tile = pygame.image.load(fileName)
        os.chdir(loc)
        angle = rot * 90
        tile = pygame.transform.rotate(tile, angle)
        boundry = tile.get_rect()
        boundry = boundry.move(x, y)
        surface.blit(tile, boundry)
        if gdIdx != BADIDX:
            if gdIdx != FREETILEIDX:
                placedTile[gdIdx] = dict
            else:
                freeTile[0] = dict

        if y < GRIDMAXY:
            if int(dict[LOCKED_]):
                txtToSurface(surface, "LOCKED", x+HALFWIDTH, y+HALFHEIGHT, player, BLACK)
    else:
        #print("Eek! rot > 3", rot)
        return None

#
def setPosition(dict, x, y):
    try:
        dict[X_] = HEADERLEN_FMT.format(int(x))
        dict[Y_] = HEADERLEN_FMT.format(int(y))
    except:
        print(traceback.format_exc())
def otherPlayer(player):
    if player == PLAYER0:   return PLAYER1
    elif player == PLAYER1: return PLAYER0
    else:
        return PLAYER0
#
# 26 free tiles of various types.
def prepListOfreeTiles():
    j = 0
    x = FREETILEX1
    y = FREETILEY1
    player = PLAYER0
    for rot in range(0,MAXNUM_BBBG):
        d= formTileDict(0, x, y, player, BBBG, rot)
        freeTile.append(d)
        player = otherPlayer(player)
        x = x + TILEWIDTH
        j = j + 1
    #
    x = FREETILEX1
    y = FREETILEY2
    rot = 0
    player = PLAYER0
    for rot in range(0,MAXNUM_GGGB):
        d= formTileDict(0, x, y, player, GGGB, rot)
        freeTile.append(d)
        player = otherPlayer(player)
        x = x + TILEWIDTH
        j = j + 1
    #
    x = FREETILEX1
    y = FREETILEY1+DOUBLEHEIGHT
    rot = 0
    player = PLAYER0
    for rot in range(0,MAXNUM_BBGG):
        d= formTileDict(0, x, y, player, BBGG, rot)
        freeTile.append(d)
        player = otherPlayer(player)
        x = x + TILEWIDTH
        j = j + 1
#
def gridRandomInit():
    freeTile.clear()
    placedTile.clear()
    prepListOfreeTiles()
    x = GRIDMINX
    y = GRIDMINY
    player = PLAYER_COLOR[randrange(len(PLAYER_COLOR))]
    gdIdx = 0
    while len(freeTile) > 1:
        idx = randrange(len(freeTile))
        if colEnumToTrip(freeTile[idx][PLAYER_]) == player:
            obj = freeTile.pop(idx)
            placedTile.append(obj)

            setPosition(placedTile[gdIdx], x, y)
            player = otherPlayer(player)
            gdIdx = gdIdx+1
            x = x + TILEWIDTH
            if x >= GRIDMAXX:
                x = GRIDMINX
                y = y+TILEHEIGHT

    setPosition(freeTile[0], FREETILEX1, FREETILEY1)

#
def drawGridAndFreeTile(sel, surface=None):
    for gdIdx in range(0, len(placedTile)):
        if surface==None:
            sendTheDictToAllCONs(placedTile[gdIdx])
        else:
            tileToSurface(surface, placedTile[gdIdx])

    if surface==None:
        sendTheDictToAllCONs(freeTile[0])
    else:
        tileToSurface(surface, freeTile[0])
#
def isInFreeTile(x, y):
    return x >= FREETILEX1 and x <= FREETILEX2 and y >= FREETILEY1 and y <= FREETILEY2
#
# Score per tile: check each side for abutment with a tile whose side is same type and player is same
# Max score per tile is 4. side, top, and bottom tiles get +1 for any side that is on an edge of the grid
def rotateN(sides, rot):
    for i in range(0, rot):
        sides = sides | sides << 4
        sides = (sides >> 1) & 0xF
    return sides
#
def lockEval():
    otherSideMask = [4, 8, 1, 2]
    i = 0
    for gdIdx in range (0, len(placedTile)):
        placedTile[gdIdx][LOCKED_] = 0
        score = [0, 0, 0, 0]
        for i in range (0, 4):
            otherIdx = ADJACENT[i][gdIdx]
            if otherIdx == BADIDX:
                score[i] = 1
            else:
                otherTile = placedTile[otherIdx]
                if otherTile[PLAYER_] == placedTile[gdIdx][PLAYER_]:
                    adjSides = rotateN(int(otherTile[SIDES_]), int(otherTile[ROT_]))
                    gdIdxRotatedSides = rotateN(int(placedTile[gdIdx][SIDES_]), int(placedTile[gdIdx][ROT_]))
                    if ((gdIdxRotatedSides & (1 << i) != 0) == (adjSides & otherSideMask[i] != 0)):
                        score[i] = 1
                    else:
                        score[i] = 0
                        break

        locked = ((score[0] and score[1] and score[2] and score[3]) == True)
        placedTile[gdIdx][LOCKED_] = HEADERLEN_FMT.format(locked)
        LOCK_CNT[0] = 0
        LOCK_CNT[1] = 0

        for i in range(0, len(placedTile)):
            if int(placedTile[i][LOCKED_]) != 0:
                if colEnumToTrip(placedTile[i][PLAYER_]) == PLAYER0:
                    LOCK_CNT[0] += 1
                else:
                    LOCK_CNT[1] += 1

#
def isLockedOut(gdIdx, player):
    lockedOut = 0
    if gdIdx != BADIDX:
        if int(placedTile[gdIdx][LOCKED_]) and \
            colEnumToTrip(placedTile[gdIdx][PLAYER_]) != player:
            lockedOut = 1
        else:
            for i in range (0, 4):
                otherIdx = ADJACENT[i][gdIdx]
                if otherIdx != BADIDX:
                     if int(placedTile[otherIdx][LOCKED_]) and \
                         colEnumToTrip(placedTile[otherIdx][PLAYER_]) != player:
                         lockedOut = 1
                         break
    else:
        lockedOut = 1

    return lockedOut

#
# swap means r to red or yellow to yellow
# replacement means red to yellow or yellow to red

# numMoves = swaps + replacements

def evalReplaceablesForScore():
    ONE_FOR_ANOTHER[0] = 0
    ONE_FOR_ANOTHER[1] = 0
    replaceables = []
    found = 0

    for player in range(0, 2):
        replaceables.clear()
        for gdIdx in range(0, len(placedTile)):
            if colEnumToTrip(placedTile[gdIdx][PLAYER_]) != PLAYER_COLOR[player]:
                if int(placedTile[gdIdx][LOCKED_]) == 0:
                    foundALock = 0
                    for i in range (0, 4):
                        otherIdx = ADJACENT[i][gdIdx]
                        if otherIdx != BADIDX:
                            if colEnumToTrip(placedTile[otherIdx][PLAYER_]) != PLAYER_COLOR[player]:
                                if int(placedTile[otherIdx][LOCKED_]):
                                    foundALock = 1
                                    break
                    if foundALock == 0:
                        found = 0
                        for i in range(0, len(replaceables)):
                            if replaceables[i] == gdIdx:
                                found = 1
                                break

                        if found == 0:
                            replaceables.append(gdIdx)
        ONE_FOR_ANOTHER[player] = len(replaceables)

# Can always replace r with r or y with y
def evalLikeForLikeForScore():
    LIKE_FOR_LIKE[0] = 0
    LIKE_FOR_LIKE[1] = 0

    for player in range(0, 2):
        for gdIdx in range(0, len(placedTile)):
                if colEnumToTrip(placedTile[gdIdx][PLAYER_]) == PLAYER_COLOR[player]:
                    LIKE_FOR_LIKE[player] += 1
# for a 1 client game always use connection 0
# for a two client system, red (PLAYER0) player is always connection 0
def activePlayerCon():
    if len(CON) == 1:
        return (CON[0], 0)
    elif colEnumToTrip(freeTile[0][PLAYER_]) == PLAYER0:
        return (CON[0], 0)
    else:
        return (CON[1], 1)

#
def printStatusOnClient(surface):
    txt = ["{val1:2d} LOCKED,{val2:2d} RtoR,{val3:2d} YtoR",
           "{val1:2d} LOCKED,{val2:2d} YtoY,{val3:2d} RtoY"]
    fgd = []
    fgd.append(RED)
    fgd.append(YELLOW)
    for i in range (0, 2) :
        txtToSurface(surface, \
                     txt[i].format(val1=LOCK_CNT[i], val2=LIKE_FOR_LIKE[i], val3=ONE_FOR_ANOTHER[i]), \
                     FREETILEX1+TILEWIDTH*2.8, FREETILEY1+TILEHEIGHT*(0.2+i*0.25), \
                     fgd[i], BLACK)
#
def gridTileAction(sel, x, y):
    print("x, y = ", x, y)
    gdIdx = getTileIdx(x, y)
    if evalForGameOver(sel, conIdx) == False and gdIdx != BADIDX:
        if isLockedOut(gdIdx, colEnumToTrip(freeTile[0][PLAYER_])) == 0:
            obj1 = placedTile.pop(gdIdx)
            x = int(obj1[X_])
            y = int(obj1[Y_])
            obj2 = freeTile.pop(0)
            setPosition(obj2, x, y)
            setPosition(obj1, FREETILEX1, FREETILEY1)
            freeTile.insert(0, obj1)
            placedTile.insert(gdIdx, obj2)
            freeTile[0][LOCKED_] = HEADERLEN_FMT.format(0)
        lockEval()
        evalLikeForLikeForScore()
        evalReplaceablesForScore()

        sendTheDictToAllCONs(placedTile[gdIdx])

        for i in range (0, 4):
            otherIdx = ADJACENT[i][gdIdx]
            if otherIdx != BADIDX:
                sendTheDictToAllCONs(placedTile[otherIdx])

        sendTheDictToAllCONs(freeTile[0])

        # Update turn labels after each move
        fgd = []
        fgd.append(RED)
        fgd.append(YELLOW)
        txt = ['RED PLAYER', 'YELLOW PLAYER', 'BOTH PLAYERS']
        for conIdx in range(0, len(CON)):
            if len(CON) == 1:
                str = "RED and YELLOW"
                fgd[conIdx] = WHITE
            else:
                # Check whose turn it is based on free tile player color enum
                freeTilePlayerEnum = int(freeTile[0][PLAYER_])
                currentColorEnum = tripToColEnum(fgd[conIdx])
                if freeTilePlayerEnum == currentColorEnum:
                    str = txt[conIdx] + "'s turn"
                else:
                    str = txt[conIdx]
            dict = formTextDict(conIdx, fgd[conIdx], BLUE, DOUBLEWIDTH, TILEHEIGHT/4, str)
            txDictToSock(CON[conIdx], dict)

        return PLAY_CODE
#
def evalForGameOverOnClient(surface):
    txt = []
    activePlayer = 1
    inactivePlayer = 0
    if freeTile[0][PLAYER_] == PLAYER0:
        activePlayer = 0
        inactivePlayer = 1

    if (ONE_FOR_ANOTHER[activePlayer] == 0) and (ONE_FOR_ANOTHER[inactivePlayer] == 0):
        gameOver = True
    elif (ONE_FOR_ANOTHER[activePlayer] == 0):
        gameOver = True
    else:
        gameOver = False

    if gameOver == True:
        winner = LOCK_CNT[0] != LOCK_CNT[1]

        # get the announcement color
        if LOCK_CNT[activePlayer] > LOCK_CNT[inactivePlayer]:
            announcementColor = BLUE #PLAYER_COLOR[activePlayer]
        elif LOCK_CNT[inactivePlayer] > LOCK_CNT[activePlayer]:
            announcementColor = WHITE #PLAYER_COLOR[inactivePlayer]
        else:
            announcementColor = WHITE #GREEN

        if announcementColor == RED:
            txt = 'RED WINS - GAME OVER'
        elif announcementColor == YELLOW:
            txt = 'YELLOW WINS - GAME OVER'
        else:
            txt = 'DRAW!'

        txtToSurface(surface, txt, \
                     GRIDMAXX/2, (GRIDMINY + HALFHEIGHT) +  (TILEHEIGHT*2), \
                     announcementColor, BLACK)
    else:
        gameOver = False
    return gameOver

#
def evalForGameOver(sel, conIdx=0):
    txt = []
    activePlayer = 1
    inactivePlayer = 0
    if freeTile[0][PLAYER_] == PLAYER0:
        activePlayer = 0
        inactivePlayer = 1

    if (ONE_FOR_ANOTHER[activePlayer] == 0) and (ONE_FOR_ANOTHER[inactivePlayer] == 0):
        gameOver = True
    elif (ONE_FOR_ANOTHER[activePlayer] == 0):
        gameOver = True
    else:
        gameOver = False

    if gameOver == True:
        winner = LOCK_CNT[0] != LOCK_CNT[1]

        # get the announcement color
        if LOCK_CNT[activePlayer] > LOCK_CNT[inactivePlayer]:
            announcementColor = PLAYER_COLOR[activePlayer]
        elif LOCK_CNT[inactivePlayer] > LOCK_CNT[activePlayer]:
            announcementColor = PLAYER_COLOR[inactivePlayer]
        else:
            announcementColor = GREEN

        if announcementColor == RED:
            txt = 'RED WINS - GAME OVER'
        elif announcementColor == YELLOW:
            txt = 'YELLOW WINS - GAME OVER'
        else:
            txt = 'DRAW!'

        dict = formTextDict(conIdx, announcementColor, \
                            BLACK, GRIDMAXX/2, \
                            (GRIDMINY + HALFHEIGHT) +  (TILEHEIGHT*2), txt)
        sendTheDictToAllCONs(dict)
    else:
        gameOver = False
    return gameOver
#

def play(sel, conIdx, x, y):
    #print(type(x), type(y))
    opcode = NONE_CODE
    if isInQuitBox(x, y) == True:     #Sept 4: quits server and all clients
        print("QUIT BOX!")
        opcode = QUIT_CODE
        sendTheDictToAllCONs(formQuitDict())
    elif isInReplayBox(x, y) == True:
        boardInit(sel)
        print("REPLAY BOX!")
        #sendTheDictToAllCONs(formReplayDict())
        opcode = PLAY_CODE
    elif evalForGameOver(sel, conIdx) == False and isInFreeTile(x, y) == True:
        print("Rotate free tile")
        rot = int(freeTile[0][ROT_])
        rot += 1
        if rot == 4:
            rot = 0
        freeTile[0][ROT_] = HEADERLEN_FMT.format(rot)
        sendTheDictToAllCONs(freeTile[0])
        opcode = NONE_CODE
    else:
        opcode = gridTileAction(sel, x, y)

    #print_opcode(opcode)
    return opcode
#


