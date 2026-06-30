from graphics import *
from random import randrange
from noodling_values import *

win = GraphWin("noodling", XMAXGAME+1, YMAXGAME+1)
win.setBackground(BKGDCOLOR)

def getWin():
    return win

####################################################
# Constants
####################################################
randoButtX1 = GRIDMAXX+HALFWIDTH
randoButtX2 = GRIDMAXX+DOUBLEWIDTH
randoButtY1 =  HALFHEIGHT+TILEHEIGHT*2
randoButtY2 =  randoButtY1 + TILEHEIGHT
randomPt1 = Point(randoButtX1, randoButtY1)
randomPt2 = Point(randoButtX2, randoButtY2)
rightMostPt = Point(randoButtX2+FULLWIDTH*3, randoButtY2) 
randomTextPoint = Point(randoButtX1+HALFWIDTH, randoButtY1+HALFHEIGHT)

quitButtX1 = randoButtX1
quitButtX2 = randoButtX2
quitButtY1 = randoButtY1+TILEHEIGHT
quitButtY2 = randoButtY2+TILEHEIGHT
quitPt1 = Point(quitButtX1, quitButtY1)
quitPt2 = Point(quitButtX2, quitButtY2)
quitTextPoint = Point(quitButtX1+HALFWIDTH, quitButtY1+HALFHEIGHT)

StatusTxtPt = [Point(randoButtX1+FULLWIDTH*2, HALFHEIGHT+TILEHEIGHT*0.25), 
               Point(randoButtX1+FULLWIDTH*2, HALFHEIGHT+TILEHEIGHT),
               Point(randoButtX1+FULLWIDTH*2, HALFHEIGHT+TILEHEIGHT*1.25)]

StatusBoxPt1 = Point(randoButtX1, HALFHEIGHT)
StatusBoxPt2 = Point(XMAXGAME, HALFHEIGHT+TILEHEIGHT*2)

lockCnt = [0, 0]
likeForLike = [0, 0]
oneForAnother = [0, 0]
playerColor = [PLAYERRED, PLAYERYELLOW]

#
rand_init = 0
man_init = 1
rot_free = 2
swap     = 3

# ################################################
# Tiles
# ################################################
freeTiles = []
placedTiles = []
gridBoxes = []

def isQuit(p):
    return p.getX() >= quitPt1.getX() and p.getX() <= quitPt2.getX() and p.getY() >= quitPt1.getY() and p.getY() <= quitPt2.getY()
#
def isInGrid(p):
    return p.getX() >= GRIDMINX and p.getX() <= GRIDMAXX and p.getY() >= GRIDMINY and p.getY() <= GRIDMAXY
#
def isInRandomBox(p):
    return p.getX() >= randomPt1.getX() and p.getX() <= randomPt2.getX() and p.getY() >= randomPt1.getY() and p.getY() <= randomPt2.getY()
#
def idxInGridBoxes(point):
    for i in range(0, len(gridBoxes)):
        if gridBoxes[i].isInTile(point) == 1:
            return i
    return BADIDX
#
def idxInGrid(point):
    for i in range(0, len(placedTiles)):
        if placedTiles[i].isInTile(point) == 1:
            return i
    return BADIDX
#

# ################################################
# Logging
# ################################################
log_actions = []
log_pt = []
def log(action, p):
    if action >= rand_init and action <= swap:
        log_actions.append(action)
        log_pt.append(p)
    else:
        print("illegal action")

# ################################################
# Classes
# ################################################
class GridTile():
    #
    def __init__(self, point):
        self.p1 = point
        self.p2 = Point(point.getX()+FULLWIDTH, point.getY()+TILEHEIGHT)
    #
    def dump(self):
        print("X", self.p.getX(), "Y", self.p.getY())
    #
    def draw(self):
        rec = Rectangle(self.p1, self.p2)
        rec.setOutline(GREY)
        rec.draw(getWin())
    #
    def isInTile(self, point):
        if point.getX() > self.p1.getX():
            if point.getX() < self.p2.getX():
                if point.getY() > self.p1.getY():
                    if point.getY() < self.p2.getY():
                        return 1
        return 0
#
class TileObject():
    def __init__(self, point, sides):
        #import ipdb; ipdb.set_trace()        
        self.player      = PLAYERBLACK

        self.sides       = sides
        self.locked      = 0
            
        self.p1          = point
        self.p2          = Point(point.getX()+FULLWIDTH, point.getY()+TILEHEIGHT)

        x = self.p1.getX()
        y = self.p1.getY()
        self.txtPos = []
        self.txtPos.append(Point(x + HALFWIDTH,      y + 12)) 
        self.txtPos.append(Point(x + FULLWIDTH - 12, y + HALFHEIGHT )) 
        self.txtPos.append(Point(x + HALFWIDTH,      y + TILEHEIGHT-12)) 
        self.txtPos.append(Point(x + 12,             y + HALFHEIGHT )) 

#
    def dump(self):
        print("Tile")
        print("player     ", self.player     )
        print("sides      ", hex(self.sides) , colors.get(self.sides))
        print("x1",      self.p1.getX()    )
        print("y1",      self.p1.getY()    )
        print("x2",      self.p2.getX()    )
        print("y2",      self.p2.getY()    )
        print("-----------")
#
    def rotate(self):
        self.sides = self.sides << 3
        if self.sides & 0x10:
            self.sides = self.sides | 0x1
        if self.sides & 0x20:
            self.sides = self.sides | 0x2
        if self.sides & 0x40:
            self.sides = self.sides | 0x4
        if self.sides & 0x80:
            self.sides = self.sides | 0x8
        self.sides = self.sides & 0xF
#
    def erase(self):
        rec = Rectangle(self.p1, self.p2)
        rec.setFill(BKGDCOLOR)
        rec.setOutline(BKGDCOLOR)
        rec.setWidth(BORDERWIDTH)
        rec.draw(getWin())

#
    def rotateN(self, n):
        for i in range (0, n):
            self.rotate()

#
    def getColor_n(self, n):
        #import ipdb; ipdb.set_trace()
        val = self.sides & (1<<n)
        if val != 0: return BLUE
        else:        return GREEN
 #
    def topColor(self):
        if self.sides & 1: return BLUE
        else:return GREEN
#
    def rightColor(self):
        if self.sides & 2: return BLUE
        else:return GREEN
#
    def bottomColor(self):
        if self.sides & 4: return BLUE
        else:return GREEN
#
    def LeftColor(self):
        if self.sides & 8: return BLUE
        else:return GREEN
#
    def setPosition(self, p):
        self.p1 = p
        self.p2 = Point(p.getX()+FULLWIDTH, p.getY()+TILEHEIGHT)
        x = self.p1.getX()
        y = self.p1.getY()
        self.txtPos[0] = Point(x + HALFWIDTH,      y + 12           )                
        self.txtPos[1] = Point(x + FULLWIDTH - 12, y + HALFHEIGHT ) 
        self.txtPos[2] = Point(x + HALFWIDTH,      y + TILEHEIGHT-12)  
        self.txtPos[3] = Point(x + 12,             y + HALFHEIGHT ) 
#
    def trianglesDraw(self, i):
        t= []
        p1x = self.p1.getX()
        p1y = self.p1.getY()
        p2x = self.p2.getX()
        p2y = self.p2.getY()
        t.append(Polygon(self.p1, 
                              Point(p1x+HALFWIDTH, p1y+HALFHEIGHT), 
                              Point(self.p2.getX(), p1y)
                              )
                     )
#
        t.append(Polygon(Point(self.p2.getX(), p1y), 
                              Point(p1x+HALFWIDTH, p1y+HALFHEIGHT), 
                              self.p2
                              )
                      )
#             
        t.append(Polygon(self.p2, 
                              Point(p1x+HALFWIDTH, p1y+HALFHEIGHT), 
                              Point(p1x, self.p2.getY())
                              )
                      )
#             
        t.append(Polygon(Point(p1x, self.p2.getY()), 
                              Point(p1x+HALFWIDTH, p1y+HALFHEIGHT), 
                              self.p1)
                      )
        if i < len(t):
            color = self.getColor_n(i)
            t[i].setFill(color)
            t[i].setOutline(color)
            t[i].draw(getWin())
        else:
            log("Eek!")
#
    def isInTile(self, point):
        if point.getX() > self.p1.getX(): 
            if point.x < self.p2.getX(): 
                if point.y > self.p1.getY(): 
                    if point.y < self.p2.getY():
                        return 1
        return 0
#
    def draw(self, color):
        #import ipdb; ipdb.set_trace()
        for i in range(0, 4):
            self.trianglesDraw(i)

        pt = Point(self.p1.getX()+ HALFWIDTH, self.p1.getY()+ HALFHEIGHT)
        if self.player != PLAYERBLACK:
            c = Circle(pt, PLAYERRADIUS)
            c.setFill(self.player)
            c.draw(getWin())

        if self.p1.getY() < GRIDMAXY:
            message = Text(pt, "LOCKED")
            message.setFace('courier')
            message.setStyle('bold')
            message.setSize(7)

            if self.locked:
                message.setOutline('black')
            else:
                message.setOutline(self.player)

            message.draw(getWin())
# ###################################################
#
def r_inc(r):
    if r   == ROT000: return ROT090
    elif r == ROT090: return ROT180
    elif r == ROT180: return ROT270
    elif r == ROT270: return ROT000
    else:
        log("r_inc error")

def otherPlayer(p):
    if p == PLAYERBLACK:  return PLAYERRED
    elif p == PLAYERRED: return PLAYERYELLOW
    else:              return PLAYERRED
#

def prepListOfreeTiles():
    j = 0
    x = FREETILEX
    y = FREETILEY
    #import ipdb; ipdb.set_trace()
    for i in range(0,MAXNUM_gggb):
        obj = TileObject(Point(x, y), GGGB)
        obj.rotateN(i)
        obj.draw(BKGDCOLOR)
        #obj.dump()

        freeTiles.append(obj)
        x = x + FULLWIDTH
        j = j + 1
    #
    x = FREETILEX
    y = FREETILEY+TILEHEIGHT
    i = 0
    for i in range(0,MAXNUM_bbbg):
        obj = TileObject(Point(x, y), BBBG)
        obj.rotateN(i)
        obj.draw(BKGDCOLOR)
        freeTiles.append(obj)
        x = x + FULLWIDTH
        j = j + 1
    #
    x = FREETILEX
    y = FREETILEY+DOUBLEHEIGHT
    i = 0
    for i in range(0,MAXNUM_bbgg):
        obj = TileObject(Point(x, y), BBGG)
        obj.rotateN(i)
        obj.draw(BKGDCOLOR)

        freeTiles.append(obj)
        x = x + FULLWIDTH
        j = j + 1

    #
    return freeTiles


#
def gridRandomInit():
    x = GRIDMINX
    y = GRIDMINY
    player = playerColor[randrange(len(playerColor))]
    gIdx = 0
    while len(freeTiles) > 1:        
        idx = randrange(len(freeTiles))
        obj = freeTiles.pop(idx)
        placedTiles.append(obj)
        placedTiles[gIdx].player = player
        player = otherPlayer(player)
        placedTiles[gIdx].erase()
        placedTiles[gIdx].setPosition(Point(x, y))
        placedTiles[gIdx].draw(player)
        gIdx = gIdx+1
        x = x + FULLWIDTH
        if x >= GRIDMAXX:
            x = GRIDMINX
            y = y+TILEHEIGHT
    #getWin().getMouse()
    freeTiles[0].erase()
    freeTiles[0].setPosition(Point(FREETILEX, FREETILEY))
    freeTiles[0].player = player
    freeTiles[0].draw(player)

#
def initTilePlacement():
    prepListOfreeTiles()

    randomBox = Rectangle(randomPt1, randomPt2)
    randomBox.setFill("gray4")
    randomBox.setOutline(BKGDCOLOR)
    randomBox.setWidth(BORDERWIDTH)
    randomBox.draw(getWin())

    quitBox = Rectangle(quitPt1, quitPt2)
    quitBox.setFill("gray4")
    randomBox.setOutline(BKGDCOLOR)
    randomBox.setWidth(BORDERWIDTH)
    quitBox.draw(getWin())

    message = Text(quitTextPoint, "Quit")
    message.setOutline('white')
    message.setFace('courier')
    message.setStyle('bold')
    message.setSize(16)
    message.draw(getWin())
    rc = PLAY

    gridRandomInit()      
    randomBox.undraw()                          
    randomBox.setFill(BKGDCOLOR)                
    randomBox.draw(getWin())                         

    return rc

#
def isInSpareTile(point):
    return point.getX() >= freeTiles[0].p1.getX() and point.getX() <= freeTiles[0].p2.getX() and point.getY() >= freeTiles[0].p1.getY() and point.getY() <= freeTiles[0].p2.getY()
#
# top = 0, rt = 1, bottom = 2, left = 3
# Score per tile: check each side for abutment with a tile whose side is same type and player is same
# Max score per tile is 4. side, top, and bottom tiles get +1 for any side that is on an edge of the grid 

def lockEval():
    otherSideMask = [4, 8, 1, 2]
    lockCnt = 0
    i = 0
    #import ipdb; ipdb.set_trace()
    for gdIdx in range (0, len(placedTiles)):
        placedTiles[gdIdx].locked = 0
        score = [0, 0, 0, 0]
        for q in range (0, 4):
            otherIdx = adjacent[q][gdIdx]
            otherTile = placedTiles[otherIdx]
            if otherIdx == BADIDX:
                score[q] = 1
            else:
                if otherTile.player == placedTiles[gdIdx].player:
                    tileSide = placedTiles[gdIdx].sides & 1 << q
                    adjSide = otherTile.sides & otherSideMask[q]
                    val1 = tileSide == 0
                    val2 = adjSide == 0
                    if val1 == val2:
                        # adjacent sides match
                        score[q] = 1
                    else:
                        otherTile.locked = 0
                        score[q] = 0

        if score[0] and score[1] and score[2] and score[3]:
            placedTiles[gdIdx].locked = 1

        placedTiles[gdIdx].draw(placedTiles[gdIdx].player)
            # print("gdIdx ", gdIdx, "locked ")
    # print("-------")
#
def isLockedOut(point, player):
    idx = idxInGrid(point)
    rc = 1
    if idx != BADIDX:
        for q in range (0, 4):
            otherIdx = adjacent[q][idx]
            if otherIdx != BADIDX:
                 if placedTiles[otherIdx].locked and placedTiles[otherIdx].player != player:
                     rc = 0
                     break
    else:
        rc = 0

    return rc

#
# swap means r to red or yellow to yellow
# replacement means red to yellow or yellow to red

# numMoves = swaps + replacements

def evalReplaceables():
    oneForAnother[0] = 0
    oneForAnother[1] = 0
    replaceables = []
    found = 0

    for player in range(0, 2):
        replaceables.clear()
        for gdIdx in range(0, len(placedTiles)):
            if placedTiles[gdIdx].player != playerColor[player]:
                if placedTiles[gdIdx].locked == 0:
                    foundALock = 0
                    for q in range (0, 4):
                        otherIdx = adjacent[q][gdIdx] 
                        if otherIdx != BADIDX:
                            if placedTiles[otherIdx].player != playerColor[player]:
                                if placedTiles[otherIdx].locked:
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
        oneForAnother[player] = len(replaceables)

# Can always replace r with r or y with y
def evalLikeForLike():
    likeForLike[0] = 0
    likeForLike[1] = 0
    
    for player in range(0, 2):
        for gdIdx in range(0, len(placedTiles)):
                if placedTiles[gdIdx].player == playerColor[player]:
                    likeForLike[player] += 1
#
def evalLockCnt():
    lockCnt[0] = 0
    lockCnt[1] = 0

    for i in range(0, len(placedTiles)):
        if placedTiles[i].locked:
            if placedTiles[i].player == PLAYERRED:
                lockCnt[0] += 1
            else:
                lockCnt[1] += 1
#
def printStatus():
    lockEval()

    scoreBox = Rectangle(StatusBoxPt1, StatusBoxPt2)
    scoreBox.setFill(BKGDCOLOR)
    scoreBox.setOutline(BKGDCOLOR)
    scoreBox.draw(getWin())
    evalLockCnt()
    evalLikeForLike()
    evalReplaceables()

    txt = ["Red: {val1:2d} LOCKED, {val2:2d} R to R, {val3:2d} Y to R", 
           "Yel: {val1:2d} LOCKED, {val2:2d} Y to Y, {val3:2d} R to Y"]
    for player in range (0, 2) :
        message = Text(StatusTxtPt[player], txt[player].format(val1=lockCnt[player], val2=likeForLike[player], val3=oneForAnother[player]))
        message.setOutline('black')
        message.setFace('courier')
        message.setStyle('bold')
        message.setSize(14)
        message.draw(getWin())

#
def drawTile(point):
    gdIdx = idxInGrid(point)

    if gdIdx != BADIDX:
        obj1 = placedTiles.pop(gdIdx)
        x = obj1.p1.getX()
        y = obj1.p1.getY()
        obj2 = freeTiles.pop(0)
        obj2.setPosition(Point(x, y))
        obj1.setPosition(Point(FREETILEX, FREETILEY))
        freeTiles.insert(0, obj1)
        placedTiles.insert(gdIdx, obj2)

        placedTiles[gdIdx].draw(BKGDCOLOR)
        freeTiles[0].locked = 0
        freeTiles[0].draw(BKGDCOLOR)

        #lockEval()
        printStatus()

#
def gameOver():
    txt = []
    pt = Point(GRIDMAXX + FULLWIDTH, (GRIDMINY + HALFHEIGHT) +  (TILEHEIGHT*2))

    if oneForAnother[0] == 0 or oneForAnother[1] == 0:
       tie = 0
       if lockCnt[1] != 0 or lockCnt[0] != 0:
           if lockCnt[1] > lockCnt[0]:
               # 0 wins
               txt.append("Yellow WINS!")
           elif lockCnt[0] > lockCnt[1]:
               # 0 wins
               txt.append("Red WINS!")
           elif lockCnt[0] == lockCnt[1]:
               tie = 1
               txt.append("DRAW")
       if tie == 0:
           message = Text(pt, txt)
           message.setOutline('black')
           message.setFace('courier')
           message.setStyle('bold')
           message.setSize(18)
           message.draw(getWin())
           return 1
    
    return 0

         
#
def play(point):
    if isQuit(point) == True:
        return QUIT
    elif gameOver():
        return CARRYON
    elif isInSpareTile(point) == True:
        freeTiles[0].rotate()
        freeTiles[0].draw(BKGDCOLOR)
    else:
        if isLockedOut(point, freeTiles[0].player):
            drawTile(point)

        gameOver()
        return CARRYON
#
def nextGridPoint(p):
    x = p.getX()
    y = p.getY()
    if x == -1 and y == -1:
        x = GRIDMINX
        y = GRIDMINY
    else:
        x = x + FULLWIDTH
        if x >= GRIDMAXX:
            x = GRIDMINX
            y = y + TILEHEIGHT
    return Point(x, y)
#
def gridInit():
    evalCount = 0

    x = GRIDMINX
    y = GRIDMINY
    p = Point(x, y)
    
    for i in range(0, 25):
        gridBoxes.append(GridTile(p))
        p = nextGridPoint(p)
        # eek gridBoxes[i].draw()

    row = ["A","B","C","D","E"]
    col = ["1","2","3","4","5"]
    for i in range(0, 5):
        ptRow = Point(HALFWIDTH/2, (GRIDMINY + HALFHEIGHT) +  (TILEHEIGHT*i))
        messageRow = Text(ptRow, row[i])
        messageRow.setOutline('BLACK')
        messageRow.setFace('courier')
        messageRow.setStyle('bold')
        messageRow.setSize(10)
        messageRow.draw(getWin())

        ptCol = Point((GRIDMINX + HALFWIDTH) +  (FULLWIDTH*i), HALFHEIGHT/2)
        messageCol = Text(ptCol, col[i])
        messageCol.setOutline('BLACK')
        messageCol.setFace('courier')
        messageCol.setStyle('bold')
        messageCol.setSize(10)
        messageCol.draw(getWin())

    for i in range(0, len(gridBoxes)):
        gridBoxes[i].draw()

#
def main():
    import ipdb; 
    #ipdb.set_trace()

    gridInit()

    if initTilePlacement() == PLAY:
        printStatus()
        while True:
            point = getWin().getMouse()
            if play(point) == QUIT:
                break
            else:
                continue
    getWin().close()

main()
