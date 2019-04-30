import pygame
import math
import os

from board import Board

width = 512
height = 512
isFlipped = 0

selectedPiece = (0, 0)
lastPieceMove = (0, 0)
validMoves = []

windown = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")

board_background = pygame.image.load(os.path.join("img", "blue.png"))
board_background = pygame.transform.scale(board_background, (512, 512))

board = Board(8, 8)


def redraw_gamewindow():
    global windown, board, selectedPiece, lastPieceMove

    windown.blit(board_background, (0, 0))
    x, y = mouse2grid(pygame.mouse.get_pos())
    board.drawMoves(selectedPiece[0], selectedPiece[1], windown)
    board.drawPieces(windown)

    pygame.display.update()

def mouse2grid(position):
    return (int(position[0]/64), int(position[1]/64))

def main():
    global selectedPiece, isFlipped
    clock = pygame.time.Clock()
    run = True

    while run:
        redraw_gamewindow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_f:
                    board.flipBoard()

            if event.type == pygame.MOUSEMOTION:
                pass

            if event.type ==  pygame.MOUSEBUTTONDOWN:
                (x, y) = mouse2grid(pygame.mouse.get_pos())
                if board.board[y][x] != "*":
                    board.selectPiece(y, x)
                    selectedPiece = (y, x)
                    print("Selected a {} {} at ({}, {}) or {}".format(board.board[y][x].color, board.board[y][x].rank, y, x, board.boardCoordinates((y, x))))
                else:
                    print("Blank square at ({}, {}) or {}".format(y, x, board.boardCoordinates((y, x))))
main()
