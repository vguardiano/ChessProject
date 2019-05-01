import pygame
import math
import os

from board import Board

width = 512
height = 512
isFlipped = 0

selectedPiece = (-1, -1)
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
    board.drawMoves(selectedPiece[0], selectedPiece[1], windown)
    board.drawPieces(windown)
    pygame.display.update()

def mouse2grid(position):
    return (int(position[0]/64), int(position[1]/64))

def main():
    global selectedPiece, validMoves, lastPieceMove

    run = True
    flipEveryMove = True

    clock = pygame.time.Clock()
    board.flipBoard()
    turn = "white"
    print("{}'s turn to move.".format(turn.capitalize()))

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
                if event.key == pygame.K_k:
                    flipEveryMove = (1 + flipEveryMove) % 2
                if event.key == pygame.K_f:
                    selectedPiece = (-1, -1)
                    validMoves = []
                    board.flipBoard()

            if event.type == pygame.MOUSEMOTION:
                pass

            if event.type ==  pygame.MOUSEBUTTONDOWN:
                (x, y) = mouse2grid(pygame.mouse.get_pos())
                if (y, x) in validMoves:
                    print("Start: {}, End: {}".format(selectedPiece, (y, x)))
                    board.movePiece(selectedPiece, (y, x), windown)
                    pygame.draw.rect(windown, (255, 127, 80), (selectedPiece[0] * 64, selectedPiece[1] * 64, 64, 64), 3)
                    pygame.draw.rect(windown, (255, 127, 80), (y * 64, x * 64, 64, 64), 3)
                    validMoves = []
                    selectedPiece = (-1, -1)
                    if turn == "white":
                        turn = "black"
                    else:
                        turn = "white"
                    print("{}'s turn to move.".format(turn.capitalize()))
                    if flipEveryMove:
                        board.flipBoard()
                else:
                    if board.board[y][x] != "*":
                        if board.board[y][x].color == turn:
                            board.selectPiece(y, x)
                            selectedPiece = (y, x)
                            validMoves = board.board[y][x].validMoves(board)
                            # print("Selected a {} {} at ({}, {}) or {}".format(board.board[y][x].color, board.board[y][x].rank, y, x, board.boardCoordinates((y, x))))
                        else:
                            validMoves = []
                            selectedPiece = (-1, -1)

                    else:
                        validMoves = []
                        selectedPiece = (-1, -1)
                        # print("Blank square at ({}, {}) or {}".format(y, x, board.boardCoordinates((y, x))))
                # board.drawBoard()

main()
