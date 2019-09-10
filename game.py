import abc
import pickle
from os import path
from board import Board
from player import WhitePlayer, BlackPlayer
from controller import HumanController, HumanChessController, DumbChessController

BASE_DIR = path.dirname(__file__)
SAVE_DIR = path.join(BASE_DIR, 'saves')

class Game:
    
    def __init__(self):
        self.activePiece = None
        self.moveableSpaces = []
        self.TurnStep = 0
        self.moveList = []
        self.gg = False
        
        #Set up Board
        self.board = Board()

        #Set up Players
        self.players = []
        self.curPlayerIndex = 0 #1st Player Goes First
        self.commands = {
            'SAVE': self.save,
            'LOAD': self.load,
            'UNDO': self.undo,
            'QUIT': self.quitter,
            'JK': self.resume_game,
        }

    #!TODO: Add decorator for command!
    def save(self):
        #Prompt user for name:
        file_name = input(f"File name to save as: ")
        print("Saving Game")
        fileObject = open(path.join(SAVE_DIR, file_name + '.chz' ),'wb')
        pickle.dump(self,fileObject)
        fileObject.close()
        return self

    #!TODO: Add decorator for command!
    def load(self):
        file_name = input(f"File name to load: ")
        print("Loading Game")
        fileObject = open(path.join(SAVE_DIR, file_name + '.chz'),'rb')
        self = pickle.load(fileObject)
        fileObject.close()
        return self
    
    #!TODO: Add decorator for command!
    def undo(self):
        print("Undoing Move")
        return self

    #!TODO: Add decorator for command!
    def resume_game(self):
        print("Resuming game")
        return self

    #!TODO: Add decorator for command!
    def quitter(self):
        print("Quitter!")
        return self

    def run_command(self, command_str):
        command_str = command_str.upper()
        if command_str not in self.commands:
            print(f"Unknown command: '{command_str}'. Please use one of the following\n{list(self.commands.keys())}")
        else:
            return self.commands[command_str]()
    
    @classmethod
    def alertUser(cls, msg):
        print(msg)

    def getActivePlayer(self):
        return self.players[self.curPlayerIndex]

    def selectPiece(self):
        return self.getActivePlayer().selectPiece()

    def isPieceValid(self, piece):
        if not piece.space:
            return False
        if piece.player != self.getActivePlayer():
            return False
        return True
    
    def selectMove(self):
        return self.getActivePlayer().selectMove()

    def isMoveValid(self, piece, space):
        if piece != self.activePiece:
            return False
        return space in self.moveableSpaces

    def startTurn(self):
        print(f"Starting {self.getActivePlayer().name}'s Turn:")
        #Do stuff
        self.TurnStep += 1
        
    @abc.abstractmethod
    def doTurn(self):
        """Method that should do something."""
        raise NotImplementedError

    def endTurn(self):
        print("Ending turn")
        #Print Board
        self.board.printBoard()
        #Swith active player
        if self.curPlayerIndex < len(self.players) - 1:
            self.curPlayerIndex += 1
        else:
            self.curPlayerIndex = 0
        #Reset Turn Step
        self.TurnStep = 0
        self.activePiece = None
        self.moveableSpaces = []

    def undoTurn(self):
        pass
        
class ChessGame(Game):

    def __init__(self):
        super().__init__()
        self.players.append(WhitePlayer(self.board))#, DumbChessController)) #White player goes first so add him first.
        self.players.append(BlackPlayer(self.board, DumbChessController))
        self.players[0].setOpponent(self.players[1])
        self.players[1].setOpponent(self.players[0])
        self.board.printBoard()
        self.isCheck = False
        
    def startTurn(self):
        activePlayer = self.getActivePlayer()
        #Check for stalemate and checkmate
        if activePlayer.isCheckMate():
            if activePlayer.inCheck:
                self.gg = activePlayer
                self.alertUser(f"Check Mate!")
                return
            else:
                self.gg = True #self.getActivePlayer()
                self.alertUser(f"Stalemate!")
                return
        elif activePlayer.inCheck:
            self.alertUser(f"Check!")
        return super().startTurn()
        
    def endTurn(self):
        #Check if checking
        isChecked = self.getActivePlayer().isChecking()
        if isChecked:
            isChecked.inCheck = True
            #self.isCheck = True
            #self.alertUser(f"Check!")
        return super().endTurn()

    def doTurn(self):
        if self.TurnStep == 0:
            self.startTurn()
        elif self.TurnStep == 1:
            piece = self.selectPiece()
            #print(f"piece = {piece.__dict__}")
            if self.isPieceValid(piece):
                possibleMoves, dangerZone = piece.getMoves()
                if possibleMoves:
                    self.activePiece = piece
                    self.moveableSpaces = possibleMoves
                    self.TurnStep += 1
                else:
                    self.alertUser(f"{piece} has no moves!")
            else:
                self.alertUser(f"{piece} is not valid selection!")
        elif self.TurnStep == 2:
            self.alertUser(f"{self.activePiece} can move to: {self.moveableSpaces}")
            space2Move = self.selectMove()
            if self.isMoveValid(self.activePiece, space2Move):
                self.activePiece.move(space2Move)
                self.moveList.append(self.activePiece)
                self.TurnStep += 1
            else:
                #No Valid Move selection, let user reselect piece to move.
                self.alertUser(f"{self.activePiece} cannot move to {space2Move}!")
                self.activePiece = None
                self.moveableSpaces = []
                self.TurnStep -= 1
        else:
            self.endTurn()


            
