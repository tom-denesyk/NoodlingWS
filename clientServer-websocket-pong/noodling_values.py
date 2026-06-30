SERVER_PORT = 2222  # initiate portNum above 1024
SERVER_NAME = "scholomanse.com"


#
#SERVER_NAME = "localhost"  #eekeek
# global variables and funtions

#
HEADERLEN_FMT = '{0:06d}'
OPCODE_  = 'OP'
DATA_LEN_ = 'LEN'
CONIDX_ = 'CONIDX'
X_      = 'X'
Y_      = 'Y'
FGD_    = 'FGD'
BGD_    = 'BGD'
PLAYER_ = 'PLAYER'
FONT_   = 'FONT'
POINTS_ = 'PTS'
STR_    = 'STR'
LOCKED_ = 'LOCKED'
ROT_    = 'ROT'
SIDES_  = 'SIDES'

NONE_CODE          = 'NONE_CODE'     
QUIT_CODE          = 'QUIT_CODE'     
MOUSE_XY_CODE      = 'MOUSE_XY_CODE' 
REPLAY_CODE        = 'REPLAY_CODE'   
PLAY_CODE          = 'PLAY_CODE'     
CLIENT_ID_CODE     = 'CLIENT_ID_CODE'
HEADER_CODE        = 'HEADER_CODE'   
TXT_CODE           = 'TXT_CODE'      
TILE_CODE          = 'TILE_CODE'     
#
TILEHEIGHT = 80
DOUBLEHEIGHT = TILEHEIGHT*2
HALFHEIGHT = TILEHEIGHT/2

TILEWIDTH = 80
DOUBLEWIDTH = TILEWIDTH*2
HALFWIDTH  = TILEWIDTH/2
# ---
GRIDMINX = HALFWIDTH/2
GRIDMINY = HALFHEIGHT
GRIDMAXX = 5*TILEWIDTH+GRIDMINX
GRIDMAXY = 5*TILEHEIGHT+GRIDMINY

XMINGAME = 0
YMINGAME = 0
GAMEMAXX = GRIDMAXX+GRIDMINX
GAMEMAXY = GRIDMAXY+TILEHEIGHT*3/2

FREETILEIDX = 26
FREETILEX1 = GRIDMINX
FREETILEX2 = FREETILEX1 + TILEWIDTH
FREETILEY1 = GRIDMAXY+20
FREETILEY2 = FREETILEY1 + TILEHEIGHT

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0) 
GREEN  = (0, 255, 0) 
BLUE   = (0, 0, 255) 
YELLOW = (255, 255, 0) 

WHITE_I = 0  
BLACK_I = 1  
RED_I   = 2    
GREEN_I = 3  
BLUE_I  = 4   
YELLOW_I= 5 
#
def tripToColEnum(trip):
    if trip == WHITE:
        return WHITE_I
    elif trip == BLACK:
        return BLACK_I  
    elif trip == RED:
        return RED_I    
    elif trip == GREEN:
        return GREEN_I  
    elif trip == BLUE:
        return BLUE_I   
    elif trip == YELLOW:
        return YELLOW_I
    else:
        print("EekEek tripToColEnum")
        return BLACK_I 
#
def colEnumToTrip(colStr):
    col = int(colStr)
    if col == WHITE_I:
        return WHITE
    elif col == BLACK_I:
        return BLACK  
    elif col == RED_I:
        return RED    
    elif col == GREEN_I:
        return GREEN  
    elif col == BLUE_I:
        return BLUE   
    elif col == YELLOW_I:
        return YELLOW
    else:
        print("EekEek colEnumToTrip")
        return BLACK 
#
BKGDCOLOR = BLACK
PLAYERNUL = BLACK
PLAYER0 = RED
PLAYER1 = YELLOW

def colorToPlayerString(color):
    if color == PLAYER0:
        return 'PLAYER0 (RED)'
    elif color == PLAYER1:
        return 'PLAYER1 (YELLOW)'
    else:
        return 'None'

TOP     = 0
RIGHT   = 1
BOTTOM  = 2
LEFT    = 3

GREY = "grey"
MAXNUM_BBBG  = 8
MAXNUM_GGGB  = 8
MAXNUM_BBGG = 10
BADIDX = -1

GGGG = 0x0  #0000
GGGB = 0x1  #1110
GGBG = 0x2  #0010
GGBB = 0x3  #0011
GBGG = 0x4  #0100
GBGB = 0x5  #0101  NA
GBBG = 0x6  #0110
GBBB = 0x7  #0111
BGGG = 0x8  #1000
BGGB = 0x9  #1001
BGBG = 0xA  #1010
BGBB = 0xB  #1011
BBGG = 0xC  #1100
BBGB = 0xD  #1101
BBBG = 0xE  #1110
BBBB = 0xF  #1111

colors = {
    GGGG:"gggg",
    BBBG:"BBBG",
    GGBG:"ggbg",
    GGBB:"ggbb",
    GBGG:"gbgg",
    GBGB:"gbgb",
    GBBG:"gbbg",
    GBBB:"gbbb",
    BGGG:"bggg",
    BGGB:"bggb",
    BGBG:"bgbg",
    BGBB:"bgbb",
    BBGG:"BBGG",
    BBGB:"bbgb",
    GGGB:"GGGB",
    BBBB:"bbbb",
    }

#
TOP = [-1, -1, -1, -1, -1,
        0,  1,  2,  3,  4,
        5,  6,  7,  8,  9,
       10, 11, 12, 13, 14,
       15, 16, 17, 18, 19]

RT  = [ 1,  2,  3,  4, -1,
        6,  7,  8,  9, -1,
       11, 12, 13, 14, -1,            # [ 0, 1, 2, 3, 4,
       16, 17, 18, 19, -1,            #   5, 6, 7, 8, 9,
       21, 22, 23, 24, -1]            #  10,11,12,13,14,

BOT = [ 5,  6,  7,  8,  9,            #  15,16,17,18,19,
       10, 11, 12, 13, 14,            #  20,21,22,23,24]
       15, 16, 17, 18, 19,
       20, 21, 22, 23, 24,
       -1, -1, -1, -1, -1 ]

LFT = [-1,  0,  1,  2,  3,
       -1,  5,  6,  7,  8,
       -1, 10, 11, 12, 13,
       -1, 15, 16, 17, 18,
       -1, 20, 21, 22, 23]

ADJACENT = []
ADJACENT.append(TOP)
ADJACENT.append(RT)
ADJACENT.append(BOT)
ADJACENT.append(LFT)

