from piece import Piece, DirectionalPiece

class Pawn(Piece):
    _code = 'P'


    def __init__(self, board, player, space = None):
        super().__init__(board, player, space)
        self.double_moved = False
        #White pawns can only move up board, black down board.
        if self.player.code == 'W':
            self.dir_coef = -1
        else:
            self.dir_coef = 1
    '''
    Returns:
      * A list of valid spaces this piece can move too.
      * A list of oppenent's pieces in danger.
    '''
    def getMoves(self, space = None, doFilter = True):
        moveList = []
        dangerZone = []
        if not space: space = self.space
        #Check diagonal attack spaces:
        myX, myY = self.space.getPos()
        
        #Check single forward move:
        space = self.board.getSpaceAtPos(myX, myY + self.dir_coef)
        if not space.piece:
            moveList.append(space)
        
        #Check double forward move:
        if not self.hasMoved:#len(self.moveHistory):#self.hasMoved:
            if not space.piece: #Check if 1 space is clear
                space = self.board.getSpaceAtPos(myX, myY + self.dir_coef * 2) #Check if 2 space is clear too
                if not space.piece:
                    moveList.append(space)

        #Filter out checking non kill set of moves
        if doFilter:
            moveList = self.filterMoveList(moveList)
        
        diagSpaces =  [(myX + 1, myY + self.dir_coef), (myX - 1, myY + self.dir_coef)]
        for dS in diagSpaces:
            space = self.board.getSpaceAtPos(dS)
            if space and space.piece and space.piece.player != self.player:
                #Check if move would result in check, avoid adding to dangerZone if true.
                if not doFilter or not self.filterMove(space):
                    moveList.append(space)
                    dangerZone.append(space.piece)

        #Check En Passant (attack diagonal empty space if adj pawn double moved):
        #!TODO: Do this later:
        return moveList, dangerZone

    #!TODO: Change inherited Move to try and remove En Passant piece if valid.
    # [( [(piece, prevSpace, newSpace)], [(killedPiece, space)], [(newPiece, space)] ), ...]
    # Added Logic to change piece if moved to opposite side of the board.
    # Added doFilter to signal wether to prompt for new piece. Used to check if a move is valid before the actual move.
    def move(self, newSpace, checking = False):
        old_space = self.space
        piece = super().move(newSpace)
        #Check piece is at end of board.
        ##print(f"endY = {newSpace.y + self.dir_coef}")
        if not checking:
            if newSpace.y + self.dir_coef >= self.board.maxY or newSpace.y + self.dir_coef < 0:
                actionList, killedPieces, createdPieces = self.moveHistory.pop()
                #promt user for new piece
                new_piece_cls = self.player.selectNewPiece()
                #Kill Current Piece
                self.player.kill(self)
                killedPieces.append(tuple([self, newSpace]))
                #Add New Piece to newSpace
                new_piece = self.player.addPiece(new_piece_cls, newSpace)
                createdPieces.append(tuple([new_piece, newSpace]))
                self.moveHistory.append(tuple([actionList, killedPieces, createdPieces]))
        return piece

        
class Rook(DirectionalPiece):
    _code = 'R'
    _dirs = [
                 (0,-1),
	(-1, 0),         (1, 0),
	         (0, 1),        
    ]

    # Calculate if this piece can viably castle. Called by the King piece.
    # Simplifies the logic vs King calculating from each rooks perspective. 
    def canCastle(self, king = None, king_move_list = None, space = None, doFilter = True):
        if self.hasMoved:
            return None
        
        #If Passing king assume non-rook checks have been done. It's an efficiency thing
        if not king: 
            king = self.player.getKing()
            if king.hasMoved:
                return None

            if self.player.inCheck:
                return None
            
        moveList, dangerZone = self.getMoves(space, doFilter)
        y = self.space.y
        x = self.space.x
        xDir = 1 if x < king.space.x else -1
        x += xDir #Don't check rooks current spot
        ##print(f"self = {self}, ({self.space.x},{self.space.y})")
        ##print(f"king = {king}, ({king.space.x},{king.space.y})")
        ##print(f"xDir = {xDir}")
        #isClear = True
        #Check if path is clear between rook and king
        while(x != king.space.x):
            if self.board.getSpaceAtPos(x,y) not in moveList:
                ##print(f"pos = ({x}, {y}), moveList = {moveList}")
                return None
                #return moveList, dangerZone
            x += xDir
        #Check if king moves through check:
        #king_move_list, king_danger_zone = king.getMoves(space, doFilter)
        if not king_move_list:
            king_move_list, king_danger_zone = king.getMoves(space, False)
        xDir *= -1
        ##print(f"pos = ({x}, {y}), xDir = {xDir}")
        ##print(f"king_move_list = {king_move_list}")
        if self.board.getSpaceAtPos(x + xDir,y) not in king_move_list:
            ##print(f" = ({x + xDir}, {y}), king_move_list = {king_move_list}")
            return None
        #Check if king ends in check:
        kingSpace = self.board.getSpaceAtPos(x + (xDir*2),y)
        if king.filterMove(kingSpace):
            ##print(f"King filtered: {kingSpace}, ({x + xDir*2}, {y})")
            return None
        ##print(f"kingSpace = {kingSpace}")
        return kingSpace
        #self.board.getSpaceAtPos(dS)

class Knight(DirectionalPiece):
    _code = 'H'
    _dirs = [
                 (-1,-2), ( 1,-2),
        (-2,-1),                   ( 2,-1),
        (-2, 1),                   ( 2, 1),
                 (-1, 2), ( 1, 2)
    ]
    _max_moves = 1

class Bishop(DirectionalPiece):
    _code = 'B'
    _dirs = [
	(-1,-1),          (1,-1),
        
	(-1, 1),          (1, 1)
    ]

class Queen(DirectionalPiece):
    _code = 'Q'
    _dirs = [
	(-1,-1), ( 0,-1), ( 1,-1),
	(-1, 0),          ( 1, 0),
	(-1, 1), ( 0, 1), ( 1, 1)
    ]

class King(DirectionalPiece):
    _code = 'K'
    _max_moves = 1
    _dirs = [
        (-1,-1), ( 0,-1), ( 1,-1),
        (-1, 0),          ( 1, 0),
        (-1, 1), ( 0, 1), ( 1, 1)
    ]

    # Added ability to castle.
    def move(self, newSpace, checking = False):
        #Check if move is castle.
        old_pos = self.space.getPos()
        x_delta = newSpace.x - self.space.x
        ##print(f"x_delta = {x_delta}, abs(x_delta) = {abs(x_delta)}")
        isCastle = False
        if abs(x_delta) >= 2: #Is castle!
            isCastle = True
            if x_delta < 0:
                x_delta = -1
            else:
                x_delta = 1
            
        piece = super().move(newSpace)
        if isCastle:
            actionList, killedPieces, createdPieces = self.moveHistory.pop()
            #Get right rook
            rooks = self.player.getPiecesByType(Rook)
            rook = None
            for rook in rooks:
                ##print(f"self.space.x = {self.space.x}, rook.space.x = {rook.space.x}")
                ##print(f"x_delta = {x_delta}")
                if self.space.x > rook.space.x and x_delta < 0:
                    break
                elif self.space.x < rook.space.x and x_delta > 0:
                    break
                else:
                    rook = None 
            ##print(f"right rook = {rook}")
            ##print(f"(x, y) = ({rook.space.x}, {rook.space.y})")
            #move rook to right spot
            prevRookSpace = rook.space
            newRookSpace = self.board.getSpaceAtPos(old_pos[0] + x_delta, old_pos[1])
            ##print(f"newRookSpace = {newRookSpace}")
            prevRookSpace.piece = None
            newRookSpace.piece = rook
            rook.space = newRookSpace
            actionList.append(tuple([rook, prevRookSpace, newRookSpace]))
            #edit move history
            self.moveHistory.append(tuple([actionList, killedPieces, createdPieces]))
            
        return piece
    
    # Adds ability to castle is addition to directional move
    def getMoves(self, space = None, doFilter = True):
        moveList, dangerZone = super().getMoves(space, doFilter)

        if not doFilter:
            return moveList, dangerZone
        
        #Check if King moved
        if self.hasMoved:
            return moveList, dangerZone
        
        #Check if king is in check
        if self.player.inCheck:
            return moveList, dangerZone
        #For each Rook for my player check if valid candiate to castle.
        rooks = self.player.getPiecesByType(Rook)
        for rook in rooks:
            castleSpace = rook.canCastle(self, moveList, space, doFilter)
            ##print(f"castleSpace = {castleSpace}")
            if castleSpace:
                #Rook Can castle so lets add that move to move set
                #No pieces can be captured in a castle move so we dont worry about danger_zone.
                moveList.append(castleSpace)
                #castle_space = self.board.getSpaceAtPos(self.space.x + (xDir*2), self.space.y)
        return moveList, dangerZone
