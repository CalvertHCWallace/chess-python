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
    load_images() # only do this once, before the while loop
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
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
    for index, piece in enumerate(board):
        row = index // DIMENSION
        col = index % DIMENSION
    
if __name__ == "__main__":
    main()