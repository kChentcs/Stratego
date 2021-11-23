import pygame
from Pieces import Pieces
from PiecePool import PiecePool


class Square:
    def __init__(self, x, y, sqw, sqh, b, screen, board, gridX, gridY, lake = False):
        self.sx = x
        self.sy = y
        self.sqw = sqw
        self.sqh = sqh
        self.border = b
        self.screen = screen
        self.lake = lake
        self.piece = None
        self.board = board
        self.rect = pygame.Rect(self.sx, self.sy, self.sqw, self.sqh)
        self.selected = False
        self.gridX = gridX
        self.gridY = gridY

    def update(self):
        if not self.lake:
            if not self.piece:
                if self.sx > 20 and self.sy > 500 and self.piece == None and self.board.play == False:
                    s = pygame.Surface((self.sqw, self.sqh))
                    s.set_alpha(100)
                    s.fill((0, 255, 0))
                    self.screen.blit(s, (self.sx, self.sy))
            else:
                if self.piece.enemy:
                    pygame.draw.rect(self.screen, (200, 50, 50), self.rect, 0)
                    if self.piece.revealed:
                        self.screen.blit(self.piece.image, (self.sx, self.sy))
                else:
                    pygame.draw.rect(self.screen, (50, 50, 200), self.rect, 0)
                    self.screen.blit(self.piece.image, (self.sx, self.sy))
            borderColor = (255, 255, 255) if self.selected else (0, 0, 0)
            pygame.draw.rect(self.screen, borderColor, self.rect, self.border)

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if event.button == 3 and self.piece and self.board.play == False:
                self.piece.piecePool.addPiece()
                self.piece.square = None
                self.piece = None
            elif event.button == 1 and self.board.play:
                self.board.select(self)

    def validatePlacement(self, enemy = False):
        if self.piece:
            return False
        elif (self.sx <= 20 or self.sy <= 500) and not enemy:
            return False
        elif enemy and (self.sx <= 20 or self.sy >= 300):
            return False
        else:
            return True
