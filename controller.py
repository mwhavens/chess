import abc
from piece import Piece
from chessPieces import *
from board import Board
from time import sleep
import random

class Controller(object, metaclass=abc.ABCMeta):
    player = None
    board = None
    _name = "GenericController"


    def __init__(self, player):
        self.player = player
        self.board = player.board

    @property
    def name(self):
        return HumanController._name

    @abc.abstractmethod
    def selectPiece(self):
        """Method that should do something."""
        raise NotImplementedError

    @abc.abstractmethod
    def selectMove(self):
        """Method that should do something."""
        raise NotImplementedError

    @abc.abstractmethod
    def selectNewPiece(self):
        """Method that should do something."""
        raise NotImplementedError

    

class HumanController(Controller):
    _name = "Human"

    def getUserSpaceSelection(self, msg):
        coord = input(msg)
        pos = Board.coord2pos(coord)
        space = self.board.getSpaceAtPos(pos)
        return space

    def selectPiece(self):
        piece = None
        while not piece:
            space = self.getUserSpaceSelection("Select Piece to move:")
            if space.piece and space.piece.player == self.player:
                piece = space.piece
        #print(f"piece = {piece.__dict__}")
        return piece
        #return Board.coord2pos(pieceCoord)

    def selectMove(self):
        move = None
        while not move:
            move = self.getUserSpaceSelection("Select Space to move Piece to:")

        return move
        #moveCoord = raw_input("Select Space to move Piece to:")
        #return Board.coord2pos(moveCoord)

    def selectNewPiece(self):
        myClass = None
        while not myClass:
            pieceClass = input("Select new piece:")
            try:
                myClass = eval(pieceClass)
            except:
                myClass = None
        return myClass


class HumanChessController(HumanController):

    def selectNewPiece(self):
        piece_class = super().selectNewPiece()
        #print(f"piece_class = {piece_class}, is Pawn: {isinstance(piece_class, Pawn)}")
        while not piece_class or piece_class == Pawn or piece_class == King:
            print(f"'{piece_class}' is not a valid selection.")
            piece_class = super().selectNewPiece()
        return piece_class

    
class DumbCompController(Controller):
    _name = "Dumb Computer"
    _valid_moves = []
    
    def selectPiece(self):
        invalid_pieces = set()
        #Get a random piece with valid moves
        piece = None
        while not piece:
            piece = random.choice(self.player.pieces)
            print(f"Trying piece: {piece} -- invalid_pieces = {invalid_pieces}")
            if piece in invalid_pieces:
                piece = None
                continue
            self._valid_moves = piece.getMoves()[0]
            print(f"self._valid_moves = {self._valid_moves}")
            if not self._valid_moves:
                invalid_pieces.add(piece)
                piece = None
        sleep(1)
        return piece
    
    def selectMove(self):
        move_space = random.choice(self._valid_moves)
        self._valid_moves = []
        sleep(1)
        return move_space

    @abc.abstractmethod
    def selectNewPiece(self):
        """Method that should do something."""
        raise NotImplementedError 
    

class DumbChessController(DumbCompController):
    
    def selectNewPiece(self):
        return Queen
