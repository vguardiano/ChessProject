import pygame
import os

def legalCoord(x, bdSize):
    if x >= 0 and x < bdSize:
        return True
    else:
        return False

def lineMoviments(self, board):
    increment = 1
    moves = []
    for orientation in [-1, 1]:
        while increment <= 8:
            if legalCoord(self.row + orientation * increment, 8):
                if board[self.row + orientation * increment][self.col] == "*":
                    moves.append((self.row + orientation * increment, self.col))
                else:
                    if board[self.row + orientation * increment][self.col].color != self.color:
                        moves.append((self.row + orientation * increment, self.col))
                        break
                    else:
                        break
            increment += 1
        increment = 1

        while increment <= 8:
            if legalCoord(self.col + orientation * increment, 8):
                if board[self.row][self.col + orientation * increment] == "*":
                    moves.append((self.row, self.col + orientation * increment))
                else:
                    if board[self.row][self.col + orientation * increment].color != self.color:
                        moves.append((self.row, self.col + orientation * increment))
                        break
                    else:
                        break
            increment += 1
        increment = 1

    return moves

def diagonalMoviments(self, board):
    increment = 1
    moves = []
    for orientation in [-1, 1]:
        while increment <= 8:
            if legalCoord(self.row + orientation * increment, 8) and legalCoord(self.col + orientation * increment, 8):
                if board[self.row + orientation * increment][self.col + orientation * increment] == "*":
                    moves.append((self.row + orientation * increment, self.col + orientation * increment))
                else:
                    if board[self.row + orientation * increment][self.col + orientation * increment].color != self.color:
                        moves.append((self.row + orientation * increment, self.col + orientation * increment))
                        break
                    else:
                        break
            increment += 1
        increment = 1

        while increment <= 8:
            if legalCoord(self.row + orientation * increment, 8) and legalCoord(self.col - orientation * increment, 8):
                if board[self.row + orientation * increment][self.col - orientation * increment] == "*":
                    moves.append((self.row + orientation * increment, self.col - orientation * increment))
                else:
                    if board[self.row + orientation * increment][self.col - orientation * increment].color != self.color:
                        moves.append((self.row + orientation * increment, self.col - orientation * increment))
                        break
                    else:
                        break
            increment += 1
        increment = 1

    return moves

ranks = ["King", "Queen", "Bishop", "Knight", "Rook", "Pawn"]

b = []
w = []

B = []
W = []

for rank in ranks:
    b.append(pygame.image.load(os.path.join("img","black_{}.png".format(rank))))
    w.append(pygame.image.load(os.path.join("img","white_{}.png".format(rank))))

for i in range(6):
    B.append(pygame.transform.scale(b[i], (65, 65)))
    W.append(pygame.transform.scale(w[i], (65, 65)))

class Pieces:
    image_index = -1

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False

    def move(self):
        pass

    def isSelected(self):
        return self.selected

    def drawPiece(self, windown):
        if self.color == "white":
            drawThis = W[self.image_index]
        else:
            drawThis = B[self.image_index]

        windown.blit(drawThis, (self.col * 64, self.row * 64))

class Pawn(Pieces):
    rank = "Pawn"
    image_index = 5

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.first = True
        self.queen = False

    def validMoves(self, Board):
        row, col = self.row, self.col
        board = Board.board
        moves = []

        if not Board.flipped:
            if self.color == "white":
                orientation = 1
            else:
                orientation = -1
        else:
            if self.color == "white":
                orientation = -1
            else:
                orientation = 1

        if row == 1 + 5 * ((2 + orientation) % 3) and board[row + orientation * 1][col] == '*':
            if board[row + orientation * 2][col] == "*":
                moves.append((row + orientation * 2, col))

        if board[row + orientation * 1][col] == "*":
            moves.append((row + orientation * 1, col))

        for k in [-1, 1]:
            if legalCoord(row + orientation * 1, 8) and legalCoord(col + k, 8):
                if board[row + orientation * 1][col + k] != "*":
                    if board[row + orientation * 1][col + k].color != self.color:
                        moves.append((row + orientation * 1, col + k))

        return moves

class Rook(Pieces):
    rank = "Rook"
    image_index = 4

    def validMoves(self, Board):
        return lineMoviments(self, Board.board)

class Knight(Pieces):
    rank = "Knight"
    image_index = 3

    def validMoves(self, Board):
        moveOffsets = [(-1,-2),(-1,2),(-2,-1),(-2,1),(1,-2),(1,2),(2,-1),(2,1)]
        row, col = self.row, self.col
        board = Board.board
        moves = []

        for offset in moveOffsets:
            newRow = row + offset[0]
            newCol = col + offset[1]
            if legalCoord(newRow, 8) and legalCoord(newCol, 8) and (board[newRow][newCol] == "*" or board[newRow][newCol].color != self.color):
                moves.append((newRow, newCol))

        return moves

class Bishop(Pieces):
    rank = "Bishop"
    image_index = 2

    def validMoves(self, Board):
        return diagonalMoviments(self, Board.board)

class Queen(Pieces):
    rank = "Queen"
    image_index = 1

    def validMoves(self, Board):
        return lineMoviments(self, Board.board) + diagonalMoviments(self, Board.board)

class King(Pieces):
    rank = "King"
    image_index = 0

    def validMoves(self, Board):
        moveOffsets = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        row, col = self.row, self.col
        board = Board.board
        moves = []

        for offset in moveOffsets:
            newRow, newCol = row + offset[0], col + offset[1]
            if legalCoord(newRow, 8) and legalCoord(newCol, 8):
                if board[newRow][newCol] == "*":
                    moves.append((newRow, newCol))
                elif board[newRow][newCol].color != self.color:
                    moves.append((newRow, newCol))

        return moves
