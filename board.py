from space import Space
#from player import WhitePlayer, BlackPlayer
import re

strip_ANSI_pat = re.compile(r"""
    \x1b     # literal ESC
    \[       # literal [
    [;\d]*   # zero or more digits or semicolons
    [A-Za-z] # a letter
    """, re.VERBOSE).sub

def strip_ANSI(s):
    return strip_ANSI_pat("", s)

class Board:
    maxX = 8
    maxY = 8
    #players = []
    #curPlayer = None
    activeSpace = None
    moveableSpaces = []
    
    def __init__(self):
        #Set up the Board with SPACES!
        self.__myboard = []
        for curY in range(self.maxY):
            curList = []
            self.__myboard.append([Space(curX, curY) for curX in range(self.maxX)])

        #Set up Players now!
        #self.curPlayer = WhitePlayer(self)
        #blackPlayer = BlackPlayer(self)
        #self.players.append(self.curPlayer)
        #self.players.append(blackPlayer)
        #self.curPlayer.setOpponent(blackPlayer)
        #blackPlayer.setOpponent(self.curPlayer)
        #Setup random piece for funzies
        #self.testPieces.append(Piece(self, 'W', self.__myboard[1][1]))

    '''
    Converters for Chess coordinate(G5, A7, etc.) to/from 2x array position ((6,3), (0,1), etc.)
    '''
    @staticmethod
    def pos2coord(pos):
        return "%s%s" % (
            chr(ord('A') + pos[0]),
            Board.maxY - pos[1]
        )

    @staticmethod
    def coord2pos(coord):
        coord = coord.upper()
        x = ord(coord[0]) - ord('A')
        y = 8 - int(coord[1])
        return (x,y)
        
        
    def getSpaceAtPos(self, pos, y = None):
        if y == None:
            x = pos[0]
            y = pos[1]
        else:
            x = pos
        if x < 0 or y < 0:
            return None
        try:
            return self.__myboard[y][x]
        except:
            return None
        
    def printBoard(self):
        lineLen = None
        #firstIter = True
        for y in range(len(self.__myboard)):
            lineStr = "{:<4}|".format(self.maxY - y)
            for x in range(len(self.__myboard[y])):
                lineStr += "%s|" % self.__myboard[y][x]
            if lineLen == None:
                lineLen = len(strip_ANSI(lineStr)) - 4
                padLenth = int((lineLen) / len(self.__myboard))
                myHeader = "{:<4}|".format("")
                elemStr = '{:^%s}' % padLenth
                for i in range(len(self.__myboard[y])):
                    myHeader += elemStr.format(chr(ord('A') + i))
                print(myHeader)
                print('----' + '-' * lineLen)
            print(lineStr)
            print('    ' + '-' * lineLen)
        #print('    ' + '-' * lineLen)

    
