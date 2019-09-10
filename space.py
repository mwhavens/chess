from colorama import Fore, Back, Style

class Space:
    piece = None
    active = False
    clickable = False
    #COLORS are (Foreground, Background)
    __WHITE_COLOR = (Fore.LIGHTWHITE_EX, Back.LIGHTBLACK_EX)
    __BLACK_COLOR = (Fore.LIGHTBLACK_EX, Back.BLACK)
    
    def __init__(self, x, y, piece = None):
        self.x = x
        self.y = y
        self.piece = piece

    @staticmethod
    def pos2coord(pos):
        return "%s%s" % (
            chr(ord('A') + pos[0]),
            8 - pos[1]
        )

    @staticmethod
    def coord2pos(coord):
        coord = coord.upper()
        x = ord(coord[0]) - ord('A')
        y = 8 - int(coord[1])
        return (x,y)

    #Return color of Text, background    
    def getColors(self):
        #If x+y is even, White square, else black square.
        if (self.x + self.y) % 2 == 0:
            return self.__WHITE_COLOR #Space.__WHITE_COLOR[0], Space.__BLACK_COLOR[1] #White
        return self.__BLACK_COLOR #Space.__BLACK_COLOR[0], Space.__WHITE_COLOR[1]#'Black'

    def getPos(self):
        return (self.x, self.y)

    def __repr__(self):
        #foreColor, backColor = self.getColors()
        return self.pos2coord((self.x, self.y))
        #return "(%s,%s)" % (self.x, self.y)
    
    def __str__(self):
        if self.piece: return str(self.piece)
        foreColor, backColor = self.getColors()
        return f"{foreColor}{backColor}(%s,%s){Style.RESET_ALL}" % (self.x, self.y)

        if self.color() == 'white':
            return 'O'
        else: #Black
            return 'X'
