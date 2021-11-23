import pygame
from Pieces import Pieces
import random


class Enemy:
    def __init__(self, board):
        self.pieces = []
        self.board = board
    def placePieces(self, piecepools):
        for column in self.board.grid:
            for square in column:
                if square.validatePlacement(True):
                    random.shuffle(piecepools)
                    for pool in piecepools:
                        if pool.numberpieces > 0:
                            piece = Pieces(square.sx, square.sy, pool.images, square, pool.name, pool, self, True)
                            square.piece = piece
                            pool.removePiece()
                            self.pieces.append(piece)
                            break
    def move(self):
        randoo = []
        while len(randoo) == 0:
            rando = random.randint(0, len(self.pieces) - 1)
            piece = self.pieces[rando]
            randoo = piece.getValidSquares(enemyMove = True)
        rand = random.randint(0, len(randoo) - 1)
        piecee = randoo[rand]
        if piecee.piece:
            piece.attack(piecee.piece)
        else:
            piece.move(piecee)




