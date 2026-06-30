from graphics import *
from random import randrange
from noodling_values import *
from noodling import *
import socket
import pickle
import threading
from time import sleep
import sys                      
import time

ClientWin = GraphWin("client", GAMEMAXX+1, GAMEMAXY+1)
ClientWin.setBackground(BKGDCOLOR)
#
class QuitBox():
    def __init__(self):
        self.box = Rectangle(quitClientPt1, quitClientPt2)
        self.box.setFill(BKGDCOLOR)
        self.box.setOutline('white')
        self.message = Text(quitClientTextPoint, "Quit")
        self.message.setOutline('white')
        self.message.setFace('courier')
        self.message.setStyle('bold')
        self.message.setSize(16)
    def draw(self, win):
        self.box.draw(win)
        self.message.draw(win)
#
class ReplayBox():
    def __init__(self):
        self.box = Rectangle(replayPt1, replayPt2)
        self.box.setFill(BKGDCOLOR)
        self.box.setOutline('white')
        self.message = Text(replayTextPoint, "Replay")
        self.message.setOutline('white')
        self.message.setFace('courier')
        self.message.setStyle('bold')
        self.message.setSize(16)
    def draw(self, win):
        self.box.draw(win)
        self.message.draw(win)
#
class ShutDown():
    def __init__(self):
        self.box = Rectangle(shutdownPt1, shutdownPt2)
        self.box.setFill(BKGDCOLOR)
        self.box.setOutline('white')
        self.message = Text(shutdownTextPoint, "Shutdown")
        self.message.setOutline('white')
        self.message.setFace('courier')
        self.message.setStyle('bold')
        self.message.setSize(16)
    def draw(self, win):
        self.box.draw(win)
        self.message.draw(win)
#
quitBox = QuitBox()
replayBox = ReplayBox()
quitServerBox = ShutDown()

def drawQuitBox(win):
    quitBox.draw(win)
#
def drawReplayBox(win):
    replayBox.draw(win)
#
def drawQuitServer():
    quitServerBox.draw(None)

#
def isClient():
    return True
#
SERVERIP = '192.168.50.190'
#
def castlingClient():
    bufferSize = 8192

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if trace == True:
            print ("castlingClient: Socket successfully created")
    except socket.error as err:
        print ("castlingClient: socket creation failed with error %s" %(err))

    #h_name = socket.gethostname()
    #host_ip = socket.gethostbyname(h_name)
    host_ip = SERVERIP
    # connecting to the server
    serverPort = port

    try:
        sock.connect((host_ip, serverPort))
    except Exception as e:
        print("something's wrong with %s:%d. Exception is %s" % (host_ip, serverPort, e)) 
    i = 0
    start_millisec = time.time_ns() / 1000000
    once = False
    drawQuitBox(ClientWin)
    drawReplayBox(ClientWin)

    while True:
        data = sock.recv(bufferSize)
        dataLen = len(data)
        if dataLen != 0:
            #print("client rx ", i)
            i +=1
            obj = pickle.loads(data)
            if obj.rc == MOUSE_POLL:
                if once == False:
                    once = True
                    end_millisec = time.time_ns() / 1000000
                    duration = end_millisec - start_millisec
                    print("duration =", duration, "msec")

                if trace == True:
                    print("Client ", obj.playerIdx, "recd MOUSE_POLL")
                m = Mouse(ClientWin, MOUSE_PT)
                while True:
                    point = ClientWin.checkMouse()
                    if point != None:
                        m.point = point
                        break;

                m_string = pickle.dumps(m)
                sock.sendall(m_string)
            elif obj.rc == DRAW_RC:
                if trace == True:
                    print("Client recd DRAW_RC")
                obj.draw(ClientWin)
                if doAcks == True:
                    ack = Delimiter(obj.rc)
                    ack_string = pickle.dumps(ack)
                    sock.sendall(ack_string)
                    if trace == True:
                        print("Sent DRAW ACK")
            elif obj.rc == QUIT_RC:
                if doAcks == True:
                    ack = Delimiter(obj.rc)
                    ack_string = pickle.dumps(ack)
                    sock.sendall(ack_string)
                if trace == True:
                    print("Client recd QUIT_RC")
                break

        else:
            if trace == True:
                print(i, ": clientRcv ", dataLen)
            break

    if trace == True:
        print("Client done")

    ClientWin.close()


def main():
    castlingClient()

    ClientWin.close()

main()
