import abc
from board import Board
from piece import Piece
from chessPieces import *
from colorama import Fore, Style
from controller import HumanController, HumanChessController, DumbChessController

''' 
Used to create class properties for the different player classes.
These class properties should not be changeable.
'''
class MetaPlayer(abc.ABCMeta):

    @property
    def code(cls):
        return cls._code

    @property
    def name(cls):
        return cls.__name__

    @property
    def color(cls):
        return cls._color

    
class Player(object, metaclass=MetaPlayer):
    #Must give the class a _code values.
    pieces = []
    killedPieces = []
    active = False
    opponent = None
    controller = None
    
    #!TODO: at constructor add self to instances. Use this to automatically set opponents.
    #_instances = []
    
    @property
    def code(self):
        return type(self).code

    @property
    def name(self):
        return type(self).name

    @property
    def color(self):
        return type(self).color

    def __str__(self):
        return self.code
    
    @abc.abstractmethod
    def __init__(self, board, ControllerCls = None):
        self.pieces = []
        self.killedPieces = []
        self.active = False
        self.board = board
        if not ControllerCls:
            self.controller = HumanController(self)
        else:
            self.controller = ControllerCls(self)

    def setOpponent(self, oppPlayer):
        self.opponent = oppPlayer
    
    def isActive(self):
        return self.active

    def setActive(self):
        self.active = True

    def setNotActive(self):
        self.active = False

    def getPieces(self):
        return self.pieces

    def kill(self, piece):
        self.killedPieces.append(piece)
        self.pieces.remove(piece)

    def unkill(self, piece):
        self.pieces.append(piece)
        self.killedPieces.remove(piece)

    def addPiece(self, PieceCls, space):
        piece = PieceCls(self.board, self, space)
        self.pieces.append(piece)
        return piece
        
    def getPiecesByType(self, piece_cls):
        piece_list = []
        for p in self.pieces:
            if isinstance(p, piece_cls):
                piece_list.append(p)

        return piece_list
            
    def selectPiece(self):
        return self.controller.selectPiece()

    def selectMove(self):
        return self.controller.selectMove()

    def selectNewPiece(self):
        return self.controller.selectNewPiece()


class ChessPlayer(Player):
    #Expects _pawn_row
    #Expects _back_row
    
    def __init__(self, board, ControllerCls = None):
        super().__init__(board, ControllerCls)
        self.setUpPieces(self.board)
        self.inCheck = False
        if not ControllerCls:
            self.controller = HumanChessController(self)

    #@classmethod
    def setUpPieces(self, board):
        y = self._pawn_row
        for x in range(0,8):
            space = board.getSpaceAtPos(x,y)
            piece = Pawn(board, self, space)
            self.pieces.append(piece)

        y = self._back_row
        backPieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        #backPieces = [Rook, None, None, Queen, King, None, None, Rook]
        x = 0
        for pieceCls in backPieces:
            if pieceCls:
                piece = pieceCls(board, self, board.getSpaceAtPos(x, y))
                self.pieces.append(piece)
            x += 1

    '''
    Have user select a new piece. Pawn and King selections are not valid choices.
    '''
    def selectNewPiece(self):
        piece_class = super().selectNewPiece()
        #print(f"piece_class = {piece_class}, is Pawn: {isinstance(piece_class, Pawn)}")
        while not piece_class or piece_class == Pawn or piece_class == King:
            print(f"'{piece_class}' is not a valid selection.")
            piece_class = super().selectNewPiece()
        return piece_class
    
    def getKing(self):
        for p in self.pieces:
            if isinstance(p, King):
                return p
            
    def isChecking(self, piece = None, newSpace = None):
        #Check if any on my pieces have the king in danger.
        for p in self.pieces:
            moveList, dangerZone = p.getMoves(newSpace, doFilter = False)
            #if newSpace:
            
            #else:
            #    moveList, dangerZone = p.getMoves()
            for dp in dangerZone:
                if isinstance(dp, King):
                    #if newSpace:
                    #    print("Checking Piece: %s, (%s, %s)" % (p, newSpace.x, newSpace.y))
                    #else:
                    #    print("Checking Piece: %s, (%s, %s)" % (p, p.space.x, p.space.y))
                    return dp.player
        return None

    """
    Check if there are any moves possible. If not, you're Checkmate bud.
    """
    def isCheckMate(self):
        for p in self.pieces:
            moveList, dangerZone = p.getMoves()
            if moveList:
                return False
        return True

    
class WhitePlayer(ChessPlayer):
    _code = 'W'
    _color = Fore.CYAN
    _pawn_row = 6
    _back_row = 7
    
    def __init__(self, board, ControllerCls = None):
        super().__init__(board, ControllerCls)
        self.active = True #White goes first.

        
class BlackPlayer(ChessPlayer):
    _code = 'B'
    _color = Fore.RED
    _pawn_row = 1
    _back_row = 0

