import pygame


class Pieces:
    def __init__(self, x, y, image, square, name, piecePool, player = None, enemy = False):
        self.x = x
        self.y = y
        self.image = image
        self.square = square
        self.name = name
        self.enemy = enemy
        self.piecePool = piecePool
        self.revealed = False
        self.player = player

    def move(self, square):
        if square.piece:
            square.piece.square = None
        self.square.piece = None
        self.square = square
        self.square.piece = self

    def validateMove(self, square, enemyMove = False):
        if self.enemy and not enemyMove:
            return False
        if square.piece and enemyMove == square.piece.enemy:
            return False
        if square.lake:
            return False
        xdiff = abs(self.square.gridX - square.gridX)
        ydiff = abs(self.square.gridY - square.gridY)
        if not (xdiff == 1 or ydiff == 1) and not self.name == "scout":
            return False
        if not (self.square.sx == square.sx or self.square.sy == square.sy):
            return False
        if self.name == "flag" or self.name == "bomb":
            return False
        if self.name == "scout":
            if self.square.gridX > square.gridX and ydiff == 0:
                for i in range(self.square.gridX - 1, square.gridX, -1):
                    if square.board.grid[i][square.gridY].piece or not self.validateMove(square.board.grid[i][square.gridY], enemyMove):
                        return False
            elif self.square.gridX < square.gridX and ydiff == 0:
                for i in range(self.square.gridX + 1, square.gridX, 1):
                    if square.board.grid[i][square.gridY].piece or not self.validateMove(square.board.grid[i][square.gridY], enemyMove):
                        return False
            elif self.square.gridY > square.gridY and xdiff == 0:
                for i in range(self.square.gridY - 1, square.gridY, -1):
                    if square.board.grid[square.gridX][i].piece or not self.validateMove(square.board.grid[square.gridX][i], enemyMove):
                        return False
            elif self.square.gridY < square.gridY and xdiff == 0:
                for i in range(self.square.gridY + 1, square.gridY, 1):
                    if square.board.grid[square.gridX][i].piece or not self.validateMove(square.board.grid[square.gridX][i], enemyMove):
                        return False
            else:
                return False
        return True

    def getValidSquares(self, enemyMove):
        validMove = []
        for column in self.square.board.grid:
            for square in column:
                if self.validateMove(square, enemyMove):
                    validMove.append(square)
        return validMove

    def strength(self):
        if self.name == "flag":
            return 0
        elif self.name == "spy":
            return 1
        elif self.name == "scout":
            return 2
        elif self.name == "miner":
            return 3
        elif self.name == "sergeant":
            return 4
        elif self.name == "lieutenant":
            return 5
        elif self.name == "captain":
            return 6
        elif self.name == "major":
            return 7
        elif self.name == "colonel":
            return 8
        elif self.name == "general":
            return 9
        elif self.name == "marshal":
            return 10
        elif self.name == "bomb":
            return 11
        else:
            return -1

    def attack(self, enemyPiece):
        self.revealed = True
        enemyPiece.revealed = True
        if self.strength() >= enemyPiece.strength() or (self.name == "miner" and enemyPiece.name == "bomb") or (self.name == "spy" and enemyPiece.name == "marshal"):
            enemyPiece.piecePool.addPiece()
            self.move(enemyPiece.square)
            if enemyPiece.enemy:
                enemyPiece.player.pieces.remove(enemyPiece)
            if enemyPiece.name == "flag":
                self.square.board.die(enemyPiece)
        else:
            self.square.piece = None
            self.square = None
            if self.enemy:
                self.player.pieces.remove(self)



