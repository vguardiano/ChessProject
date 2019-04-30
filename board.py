import pygame

from pieces import Bishop
from pieces import Knight
from pieces import Queen
from pieces import King
from pieces import Rook
from pieces import Pawn

def legalCoord(x, bdSize):
    if x >= 0 and x < bdSize:
        return True
    else:
        return False

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.flipped = 0
        self.board = [['*'] * self.cols for _ in range(self.rows)]

        families = ["white", "black"]

        for i, color in enumerate(families):
            self.board[7*i][3] = King(7*i, 3, color)
            self.board[7*i][4] = Queen(7*i, 4, color)

            for k in range(2):
                self.board[7*i][7*k] = Rook(7*i, 7*k, color)
                self.board[7*i][1+5*k] = Knight(7*i, 1+5*k, color)
                self.board[7*i][2+3*k] = Bishop(7*i, 2+3*k, color)

            for k in range(8):
                self.board[1+5*i][k] = Pawn(1+5*i, k, color)

        # self.board[4][3] = King(4, 3,"black")
        # # for i in range(3):
        # #     self.board[3][2+i] = Pawn(3,2+i,"white")
        # #     self.board[5][2+i] = Pawn(5,2+i,"white")
        # self.board[3][3] = Queen(3,3,"white")
        # self.board[4][2] = Pawn(4,2,"black")
        # self.board[4][4] = Pawn(4,4,"black")
        # self.board[2][4] = Rook(2,4,"black")
        # self.board[3][1] = Knight(3,1,"white")
        # self.board[4][5] = Bishop(4,5,"black")

    def drawPieces(self, windown):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != "*":
                    self.board[row][col].drawPiece(windown)

    def selectPiece(self, row, col):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != "*":
                    self.board[row][col].selected = False

        if self.board[row][col] != "*":
            self.board[row][col].selected = True

    def drawMoves(self, row, col, windown):
        if self.board[row][col] != "*":
            moves = self.board[row][col].validMoves(self)
            for move in moves:
                colorDiff = -100 * ((move[0] + move[1]) % 2)
                if self.board[move[0]][move[1]] != "*":
                    if(self.board[move[0]][move[1]].color != self.board[row][col].color):
                        squareColor = (255 + colorDiff, 0, 0);
                else:
                    squareColor = (0, 255 + colorDiff, 0)
                pygame.draw.rect(windown, squareColor, (move[1] * 64, move[0] * 64, 64, 64))
                pygame.draw.rect(windown, (25, 86, 12), (col * 64, row * 64, 64, 64), 3)

    def movePiece(self, start, end):
        self.board[end[1]][end[0]] = self.board[start[1]][start[0]]
        self.board[start[1]][start[0]] = "*"
        removed = self.board[end[1]][end[0]]
            ### PAINT LAST SQUARE - To Do
        return removed

    def boardCoordinates(self, position):
        boardYCoordinates = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        if not self.flipped: return boardYCoordinates[7 - position[1]]+str(position[0] + 1)
        else: return boardYCoordinates[position[1]]+str(8 - position[0])

    def flipBoard(self):
        self.flipped = (1 + self.flipped) % 2
        if self.flipped:
            print("Board is Flipped !!")
        else:
            print("Board is not Flipped !!")
        tempBoard = [['*'] * 8 for _ in range(8)]
        for row in range(8):
            for col in range(8):
                tempBoard[7 - row][7 - col] = self.board[row][col]
                if self.board[row][col] != "*":
                    tempBoard[7 - row][7 - col].row = 7 - self.board[row][col].row
                    tempBoard[7 - row][7 - col].col = 7 - self.board[row][col].col
        self.board = tempBoard
