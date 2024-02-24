"""
This is our main driver file. It will be responsible for handling user input and
displaying the current GameState object.
"""

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512 # 400 is another option
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animation later on
IMAGES = {}

'''
Initialize a global dicitionary of images. This will be called exactly once in the main
'''
def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("imgs/"+ piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: we can access an image by saying 'IMAGES['wp']'
    
'''
The main driver for our code. This will handle user input and updating the graphics
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made
    
    load_images() # only do this once, before the while loop
    running = True
    sqSelected = () # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] # keeps track of player clicks (two tuples: [(6: 4), (4, 4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                # Check if the right mouse button was clicked
                if e.button == 3: # 3 corresponds to the right mouse button
                    gs.undoMove()
                    moveMade = True
                else: # If the mouse button is clicked, handle selection and move logic
                    # If there is more added to the screen the calcualtion should be changed to incoraparate the extra space used
                    location = p.mouse.get_pos() # (x, y) location of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col): # the use clicked the same square twice
                        sqSelected = () #deselect
                        playerClicks = [] # clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) # append for both 1st and 2nd clicks
                    if len(playerClicks) == 2: # after 2nd click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        if move in validMoves: # this will check if the move is valid before moving the piece
                            gs.makeMove(move)
                            moveMade = True
                        # reset users clicks
                        sqSelected = ()
                        playerClicks = []
                    # TODO: There seems to be a probelm with how the reselect works
                    #     playerClicks = [sqSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
        if moveMade: # This checks for new valid moves only after a move has been made
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        
'''
Responsible for all the graphincs within a current game state.
'''
def drawGameState(screen, gs):
    drawBoard(screen) # This will draw the squares on the board
    # TODO: add in pieces highlighting or move suggestions
    drawPieces(screen, gs.board) #draw pieces on top of those squares

'''
Draw the squares on the board. The top left of the square is always light
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color(0, 128, 0, 255)]
    for index in range(DIMENSION * DIMENSION):
        row = index // DIMENSION
        col = index % DIMENSION
        x = col * SQ_SIZE
        y = row * SQ_SIZE
        x_offset = (row + col) % 2
        color = colors[x_offset]
        p.draw.rect(screen, color, p.Rect(x, y, SQ_SIZE, SQ_SIZE))
    
'''
Draw the piece on the board using the current GameState.board
'''
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":  # not an empty square
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    
if __name__ == "__main__":
    main()