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
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ]
        self.whiteToMove = True
        self.moveLog = []