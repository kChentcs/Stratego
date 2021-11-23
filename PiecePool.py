import pygame
from draggable import draggable
from Pieces import Pieces


class PiecePool:
    def __init__(self, numberpieces, images, x, y, screen, font, name, drag = True):
        self.numberpieces = numberpieces
        self.images = images
        self.x = x
        self.y = y
        self.screen = screen
        self.font = font
        self.text = font.render(str(self.numberpieces)+"x", True, 0)
        self.lastPiece = None
        self.name = name
        self.drag = drag
        self.maxpieces = numberpieces


    def update(self):
        self.screen.blit(self.images, (self.x, self.y))
        self.screen.blit(self.text, (self.x + 35, self.y + 60))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            rect = pygame.Rect(self.x, self.y, 80, 80)
            if self.numberpieces > 0 and rect.collidepoint(event.pos) and self.drag == True:
                self.lastPiece = draggable(self.screen, self.images, event.pos[0], event.pos[1], self.name, self)
                self.lastPiece.click = True
                self.numberpieces -= 1
                self.text = self.font.render(str(self.numberpieces) + "x", True, 0)

    def addPiece(self):
        self.numberpieces += 1
        self.text = self.font.render(str(self.numberpieces) + "x", True, 0)

    def removePiece(self):
        self.numberpieces -= 1
        self.text = self.font.render(str(self.numberpieces) + "x", True, 0)

    def setPiece(self, n):
        self.numberpieces = n
        self.text = self.font.render(str(self.numberpieces) + "x", True, 0)

    def refill(self):
        self.setPiece(self.maxpieces)