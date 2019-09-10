import abc
from space import Space
from colorama import Fore, Back, Style

class MetaPiece(abc.ABCMeta):
    @property
    def code(cls):
        return cls._code

    @property
    def name(cls):
        return cls.__name__

class Piece(object, metaclass=MetaPiece):
    space = None
    board = None
    player = None
    #hasMoved = False    
    
    def __init__(self, board, player, space = None):
        self.space = space
        self.board = board
        self.player = player
        if space and space.piece != self:
            space.piece = self
            
        # Holds a list of pieces moved (starting with self)
        #  from  move action (WHY >1? think castling)
        # Holds a list of pieces killed along with the space they were killed at.
        #   (think 'En Passant' kills), shouldn' be greater than 1 but why not make it generic
        # ( [piece, prevSpace, newSpace], [killedPiece, space] )
        self.moveHistory = []

    @property
    def code(self):
        return type(self).code

    @property
    def name(self):
        return type(self).name

    @property
    def hasMoved(self):
        #print(f"self.moveHistory = {self.moveHistory}, {bool(len(self.moveHistory))}")
        #print(f"self.moveHistory = {self.moveHistory}, {bool(self.moveHistory)}")
        return bool(self.moveHistory)
    
    def __str__(self):
        #return "%s-%s" % (self.player.code, self.name)
        foreColor, backColor = self.space.getColors()
        foreColor = self.player.color
        #return f"{foreColor}{backColor}(%s-%s){Style.RESET_ALL}" % (self.player, self.code)
        return f"{foreColor}{backColor}-[%s]-{Style.RESET_ALL}" % (self.code)


    @abc.abstractmethod
    def getMoves(self, space = None):
        """
        Uses pieces current space, unless another space is provided to check is if the piece was there.
        Returns:
        * A list of valid spaces this piece can move too.
        * A list of oppenent's pieces in danger.
        """
        raise NotImplementedError

    def filterMove(self, space):
        rtnVal = True
        #Emulate move
        #print(repr(space))
        self.move(space, checking = True)
        #See if result is Check or not
        #print("self = %s, (%s,%s)" % (self, self.space.x, self.space.y))
        #print("self.player.opponent = %s, self.player = %s" % (self.player.opponent, self.player))
        if not self.player.opponent.isChecking(): #Not check, valid move.
            rtnVal = False
        #Undo emulated move
        self.undoMove()
        return rtnVal

    
    def filterMoveList(self, moveList):
        newMoveList = [] #moveList
        for newSpace in moveList:
            if not self.filterMove(newSpace):
                newMoveList.append(newSpace)
            ##Emulate move
            #self.move(newSpace)
            ##See if result is Check or not
            #if not self.player.opponent.isChecking(): #Not check, valid move.
            #    newMoveList.append(newSpace)
            ##Undo emulated move
            #self.undoMove()
            
        return newMoveList

    # [( [(piece, prevSpace, newSpace)], [(killedPiece, space)], [(newPiece, space)] ), ...]
    def move(self, newSpace, checking = False):
        prevSpace = self.space
        piece = newSpace.piece
        killedPieces = []
        actionList = []
        newPieces = []
        #print(f"piece = {piece}")
        if piece:
            killedPieces.append(tuple([piece, newSpace]))
            piece.player.kill(piece)
        actionList.append(tuple([self, prevSpace, newSpace]))
        #!TODO: maybe return the moveHistory action to caller for a global history?
        #Maybe not as undoing global would be hard to undo associated piece history and vice versa
        self.moveHistory.append(tuple([actionList, killedPieces, newPieces]))
        prevSpace.piece = None
        newSpace.piece = self
        self.space = newSpace
        return piece

    def undoMove(self):
        actionList, killedPieces, createdPieces = self.moveHistory.pop()
        #Now Undo create pieces in order
        #Do this before unkilling pieces to avoid unsetting a killed kiece space
        for piece, newSpace in reversed(createdPieces):
            newSpace.piece = None
            self.player.pieces.remove(piece)

        #Now unkill pieces in order
        for piece, newSpace in reversed(killedPieces):
            newSpace.piece = piece
            piece.space = newSpace
            piece.player.unkill(piece)

        #Undo Actions in order
        ##print(f"actionList = {actionList}, killedPieces = {killedPieces}, createdPieces = {createdPieces}")
        for piece, prevSpace, newSpace in reversed(actionList):
            prevSpace.piece = piece
            if newSpace.piece == piece:
                newSpace.piece = None
            piece.space = prevSpace

        
    """
    Checks to see if a space is valid:
      * Space is on board
      * Space has no piece
      * Space has enemy piece
    Takes:
      * X,Y Coords
      * Space
      * tuple(X,Y)
      * None
    """
    def isValidSpace(self, x, y = None):
        if x == None:
            return False
        if isinstance(x, Space):
            space = x
        elif isinstance(x, tuple): #board.getSpaceAtPos takes tuple or x,y as args
            space = self.board.getSpaceAtPos(x)
        else:
            space = self.board.getSpaceAtPos(x, y)
        if not space or (space.piece and space.piece.player == self.player):
            return False
        else:
            return True
            #if space.piece and space.piece.player != self.player:
    
    """
    Check direction from space for first occurance of:
       * end of board(space before)
       * friendly piece(space before)
       * enemy piece
    maxSpace is number of spaces to try (useful for king)
    Returns a list of all valid spaces in that direction
    Returns the oppenent's piece in danger
    """
    def checkRelativeDirection(self, deltX, deltY, space, maxSpace = None, doFilter = True):
        moveList = []
        myX, myY = space.getPos()
        #Get first space
        nextSpace = self.board.getSpaceAtPos(myX + deltX, myY + deltY)
        ##if not nextSpace:
        ##    print("%s, (%s, %s)" % (None, None, None))
        ##else:
        ##    print("%s, (%s, %s)" % (nextSpace, nextSpace.x, nextSpace.y))
        dangerPiece = None
        while(self.isValidSpace(nextSpace)):
            ##print("myX = %s, myY = %s" % (myX, myY))
            ##print("maxSpace = %s" % maxSpace)
            if maxSpace != None:
                if maxSpace < 1:
                    break
                else:
                    maxSpace -= 1
            #Check if resulting move will result in checking self.
            if doFilter:
                isFiltered = self.filterMove(nextSpace)
            else:
                isFiltered = False
            if not isFiltered:
                moveList.append(nextSpace)
            if nextSpace.piece: #If there's a piece at this space. it's the last space.
                if not isFiltered: dangerPiece = nextSpace.piece
                break
            myX, myY = nextSpace.getPos()
            nextSpace = self.board.getSpaceAtPos(myX + deltX, myY + deltY)
            ##if not nextSpace:
            ##    print("%s, (%s, %s)" % (None, None, None))
            ##else:
            ##    print("%s, (%s, %s)" % (nextSpace, nextSpace.x, nextSpace.y))
        return moveList, dangerPiece
    
    #@abc.abstractmethod
    #def getDisplay(self):
    #    """Method that should do something."""
    #    raise NotImplementedError

"""
Pieces that move lineraly out in specific directions.
Such as Queen, Bishop, King, etc.
Must include list of directions can move: _dirs
Optional Number of spaces piece can move, defaults to unlimited
"""
class DirectionalPiece(Piece):
    _max_moves = None
    
    def getMoves(self, space = None, doFilter = True):
        moveList = []
        dangerZone = []
        if not space: space = self.space
        for d in self._dirs:
            moves, dangerPiece = self.checkRelativeDirection(*d, space, self._max_moves, doFilter)
            #print("moves = %s, dangerPiece = %s" % (moves, dangerPiece))
            moveList += moves
            if dangerPiece:
                dangerZone.append(dangerPiece)
        #!TODO: Filter out moves that would result in moving/staying in check
        
        return moveList, dangerZone

