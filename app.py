#!/usr/bin/env python
from time import sleep
import traceback
#from . import Board # import Board
from game import ChessGame

class App:

    windowWidth = 800
    windowHeight = 600
    player = 0
    #!TODO: Create a SURFACE OBJ TO HOLD ALL SURFACES.
    
    def __init__(self):
        self._running = True
        #self._display_surf = None
        #self._image_surf = None
        #self._block_surf = None
        #self.board = Board()
        #self.player = Player(self.maze)
        #self.comp = Computer(self.maze, self.player)
        self.game = ChessGame()


    def get_user_command(self):
        print('\n') # Make sure we're on a new line!
        command = input(f"Whatcha talkin bout Willis({list(self.game.commands.keys())}): ")
        self.game = self.game.run_command(command)
        self.game.board.printBoard()
        
    def on_execute(self):
        while True:
            try:
                self.game.doTurn()
                if self.game.gg: #Check if GameOver
                    break
            except KeyboardInterrupt:
                break
            except EOFError:
                #Get user command
                self.get_user_command()
            except:
                traceback.print_exc()
                pass       
        #self.board.printBoard()
        #sleep(5)

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()

