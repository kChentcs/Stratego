import pygame
from Square import Square
from Pieces import Pieces
import random


class Board:
    def __init__(self, screen, x, y, row, column, sw, sh, bw):
        self.screen = screen
        self.x = x
        self.y = y
        self.row = row
        self.column = column
        self.squareWidth = sw
        self.squareHeight = sh
        self.borderWidth = bw
        self.grid = []
        self.play = False
        self.selected = None
        self.enemyTurn = False
        self.endgame = False
        self.player1 = False

        for i in range(column):
            newList = []
            for j in range(row):
                lake = (j == 4 or j == 5) and (i == 2 or i == 3 or i == 6 or i == 7)
                s = Square(i * (self.squareWidth) + self.x, j * (self.squareHeight) + self.y, self.squareWidth, self.squareHeight, self.borderWidth, self.screen, self, i, j, lake)
                newList.append(s)
            self.grid.append(newList)

    def update(self):
        for column in self.grid:
            for square in column:
                square.update()

    def handleEvent(self, event):
        for column in self.grid:
            for square in column:
                square.handleEvent(event)

    def coordinatesToSquare(self, x, y):
        i = int((x - self.x)/self.squareWidth)
        j = int((y - self.y)/self.squareHeight)
        if i >= 0 and i < self.column and j >= 0 and j < self.row:
            print("i = " + str(i) + " j =" + str(j))
            return self.grid[i][j]
        else:
            return None

    def autoFill(self, piecePools):
        for column in self.grid:
            for square in column:
                if square.validatePlacement():
                    random.shuffle(piecePools)
                    for pool in piecePools:
                        if pool.numberpieces > 0:
                            piece = Pieces(square.sx, square.sy, pool.images, square, pool.name, pool)
                            square.piece = piece
                            pool.removePiece()
                            break

    def select(self, square):
        if self.selected:
            self.selected.selected = False
        if self.selected and self.selected.piece and self.selected.piece.validateMove(square):
            if square.piece and square.piece.enemy == True:
                self.selected.piece.attack(square.piece)
            else:
                self.selected.piece.move(square)
            self.selected = None
            self.enemyTurn = True
        else:
            self.selected = square
            square.selected = True

    def die(self, piece):
        self.endgame = True
        self.player1 = piece.enemy
