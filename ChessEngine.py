"""
This class is responsible for storing all the information about the current state fo a chess game. It will
also be responsible fro determining the valid moves at the current state. It will also keep a move log.
"""

class GameState():
    def __init__(self):
        # TODO: Check for better ways to store board information. Improvement needed for AI engine.
        # board is an 8x8 2d list, each element of the list has 2 characters.
        # The first character represents the color of the piece, 'b' or 'w'
        # The second character character repersents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'P'
        # "--" repersents empty spaces on the board.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
    
    '''
    Takes a Move as parameter and executes it (this will not work for "castling,
    pawn promotion, and en-passant)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so wer can undo it later
        self.whiteToMove = not self.whiteToMove # swap players after a turn

    '''
    Undo the last move made
    '''
    def undoMove(self): 
        if len(self.moveLog) != 0: # Check if there are moves to undo
            last_move = self.moveLog.pop() # Remove the last move from the move log
            self.board[last_move.startRow][last_move.startCol] = last_move.pieceMoved
            self.board[last_move.endRow][last_move.endCol] = last_move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #Switch turns back
            
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() #for now we will not worry about checks
        
    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = [] # Test to see if the validation works
        for row in range(len(self.board)): # number of rows
            for col in range(len(self.board[row])): # number of cols in given row
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves) # this call the appropriate move function based on piece type
        return moves
    
    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''
    # Todo: Add the logic for en passant
    def getPawnMoves(self, row, col, moves):
        if self.whiteToMove: # check the white pawn moves
            if self.board[row - 1][col] == "--": # 1 square pawn advance
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == "--": # 2 square pawn move
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0: # captures to the left
                if self.board[row - 1][col - 1][0] == 'b': # check if enemy piece to capture
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
            if col + 1 <= 7: # captures to the right
                if self.board[row - 1][col + 1][0] == 'b': # check if enemy piece to capture
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
        else: # check the black pawn
            if self.board[row + 1][col] == "--": # 1 square pawn advance
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--": # 2 square pawn move
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0: # captures to the right
                if self.board[row + 1][col - 1][0] == 'w': # check if enemy piece to capture
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if col + 1 <= 7: # captures to the left
                if self.board[row + 1][col + 1][0] == 'w': # check if enemy piece to capture
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
    
    '''
    Get all the rook moves for the rook located at row, col and add these moves to the list
    '''
    # Todo: Add logic for rook moves
    def getRookMoves(self, row, col, moves):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1)) # Up, down, left, right
        for d in directions: # Iterate over each direction
            for i in range(1, 8): # Iterate over each possible distance a rook can move in the current direction
                # Calculate the row and column of the square the rook would land on
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                # Check if the calculated end square is within the bounds of the chessboard
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    # Get the piece at the end square
                    endPiece = self.board[endRow][endCol]
                    # If the end square is empty, append the move to the moves list
                    if endPiece == "--":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    # If the end square contains an opponent's piece
                    elif endPiece[0] != self.board[row][col][0]:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    # If the end square contains the rook's own piece
                    else:
                        break
                # If the end square is outside the bounds of the board
                else:
                    break
    
    '''
    Get all the knight moves for the knight located at row, col and add these moves to the list
    '''
    # Todo: Add logic for rook moves
    def getKnightMoves(self, row, col, moves):
        # The possible knight move directions in terms of changes in row and column
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                      (1, -2), (1, 2), (2, -1), (2, 1))
        # Iterate over each directions
        for d in directions:
            # Calculate the row and column the knight will land on
            endRow = row + d[0]
            endCol = col + d[1]
            # Check if the calculated end square is with bounds of the board
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                # If the end square is empty or contains an opponent's piece
                if endPiece == "--" or endPiece[0] != self.board[row][col][0]:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

    '''
    Get all the bishop moves for the bishop located at row, col and add these moves to the list
    '''
    def getBishopMoves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # Up-left, up-right, down-left, down-right
        for d in directions: # Iterate over each directions
            # Calculate the row and column the bishop will land on
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] != self.board[row][col][0]:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    
    '''
    Get all the queen moves for the queen located at row, col and add these moves to the list
    '''
    # Todo: Add logic for rook moves
    def getQueenMoves(self, row, col, moves):
        self.getRookMoves(row, col, moves)
        self.getBishopMoves(row, col, moves)
    
    '''
    Get all the king moves for the king located at row, col and add these moves to the list
    '''
    # Todo: Add logic for rook moves
    def getKingMoves(self, row, col, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1))
        for d in directions:
            endRow = row + d[0]
            endCol = col + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] != self.board[row][col][0]:
                    moves.append(Move((row, col), (endRow, endCol), self.board))
    
class Move():
    
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol # This will create a unique ID for each move
        print(self.moveID)
        
    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move): # This makes sure that 'other' is of 'Move' class
            return self.moveID == other.moveID
        return False
        
    def getChessNotation(self):
        # TODO: Change this to use real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]