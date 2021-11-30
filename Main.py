import pygame
pygame.init()

from textButton import textButton
from draggable import draggable
from Square import Square
from PiecePool import PiecePool
from Board import Board
from Enemy import Enemy
from Pieces import Pieces
screen = pygame.display.set_mode((900, 1000))
pygame.display.set_caption("Stratego")
Menufont = pygame.font.Font("Fonts/BungeeInline-Regular.ttf",100)
TextFont = pygame.font.Font("Fonts/Cinzel-VariableFont_wght.ttf",20)
state = "menu"
board = Board(screen, 47, 50, 10, 10, 80, 80, 1)
enemy = Enemy(board)
scout = pygame.transform.scale(pygame.image.load("Images/stratego-scout.png"), (80, 80))
#2,4 - 3,5  6,4 -7,5
captain = pygame.transform.scale(pygame.image.load("Images/stratego-captain.png"), (80,80))

bomb = pygame.transform.scale(pygame.image.load("Images/stratego-bomb.png"), (80,80))

colonel = pygame.transform.scale(pygame.image.load("Images/stratego-colonel.png"), (80,80))

flag = pygame.transform.scale(pygame.image.load("Images/stratego-flag.png"), (80,80))

general = pygame.transform.scale(pygame.image.load("Images/stratego-general.png"), (80,80))

lieutenant = pygame.transform.scale(pygame.image.load("Images/stratego-lieutenant.png"), (80,80))

major = pygame.transform.scale(pygame.image.load("Images/stratego-major.png"), (80,80))

marshal = pygame.transform.scale(pygame.image.load("Images/stratego-marshal.png"), (80,80))

miner = pygame.transform.scale(pygame.image.load("Images/stratego-miner.png"), (80,80))

spy = pygame.transform.scale(pygame.image.load("Images/stratego-spy.png"), (80,80))

sergeant = pygame.transform.scale(pygame.image.load("Images/stratego-sergeant.png"), (80,80))

eventListeners = []

updates = []

piecePools = []

draggables = []

setupInit = False

boardbg = pygame.image.load("Images/Stratego board.jpg")
boardbg = pygame.transform.scale(boardbg, (900, 900))

playButton = textButton(lambda: switchScreen("setup"), screen, "play", 390, 540, 100, 60, TextFont)
updates.append(playButton)
eventListeners.append(playButton)

def switchScreen(newState):
    global state
    state = newState

def showMenu():
    global eventListeners
    # menu
    screen.fill((18, 165, 175))
    titleText = Menufont.render("Stratego", True, (0, 0, 0))
    titleTextRect = titleText.get_rect()
    titleTextRect.center = (450, 200)
    screen.blit(titleText, titleTextRect)

def initSetup():
    global setupInit, flag, bomb, spy, scout, miner, sergeant, lieutenant, major, captain, colonel, general, marshal, updates, eventListeners
    setupInit = True
    updates = []
    eventListeners = []
    flagPool = makePiecePool(1, flag, 40, 910, "flag")
    spyPool = makePiecePool(1, spy, 200, 910, "spy")
    scoutPool = makePiecePool(8, scout, 280, 910, "scout")
    minerPool = makePiecePool(5, miner, 345, 910, "miner")
    sergeantPool = makePiecePool(4, sergeant, 415, 910, "sergeant")
    lieutenantPool = makePiecePool(4, lieutenant, 490, 910, "lieutenant")
    captainPool = makePiecePool(4, captain, 560, 910, "captain")
    majorPool = makePiecePool(3, major, 620, 910, "major")
    colonelPool = makePiecePool(2, colonel, 685, 910, "colonel")
    generalPool = makePiecePool(1, general, 740, 910, "general")
    marshalPool = makePiecePool(1, marshal, 820, 910, "marshal")
    bombPool = makePiecePool(6, bomb, 120, 900, "bomb")
    updates.append(board)
    eventListeners.append(board)
    autofillB = textButton(lambda: board.autoFill(piecePools), screen, "autofill", 400, 850, 80, 40, TextFont)
    updates.append(autofillB)
    eventListeners.append(autofillB)

def showSetup():
    global state
    global boardbg
    if not setupInit:
        initSetup()
    screen.fill((0, 0, 255))

    screen.blit(boardbg, (0, 0))

    timeToPlay = True

    for piecePool in piecePools:
        if piecePool.lastPiece:
            updates.append(piecePool.lastPiece)
            eventListeners.append(piecePool.lastPiece)
            draggables.append(piecePool.lastPiece)
            piecePool.lastPiece = None

        if piecePool.numberpieces > 0:
            timeToPlay = False

    for draggable in draggables:
        if draggable.piece:
            square = board.coordinatesToSquare(draggable.piece.x, draggable.piece.y)
            if square and square.validatePlacement():
                square.piece = draggable.piece
                draggable.piece.square = square
            else:
                draggable.piecePool.addPiece()
            updates.remove(draggable)
            eventListeners.remove(draggable)
            draggables.remove(draggable)
            draggable.piece = None

    if timeToPlay and len(draggables) == 0:
        state = "play"
        for piece in piecePools:
            piece.draggable = False
            piece.refill()
            if piece in eventListeners:
                eventListeners.remove(piece)
        enemy.placePieces(piecePools)
        board.play = True

def showPlay():
    global updates
    global eventListeners
    global state
    screen.fill((255, 0, 0))
    screen.blit(boardbg, (0, 0))
    board.dead()
    if board.enemyTurn == True:
        enemy.move()
        board.enemyTurn = False
    if board.endgame:
        updates = []
        eventListeners = []
        state = "Game Over"

def showGameOver():
    screen.fill((0, 0, 0))
    titleText = Menufont.render("Game Over", True, (255, 255, 255))
    titleTextRect = titleText.get_rect()
    titleTextRect.center = (450, 200)
    winner = "blue" if board.player1 else "red"
    textText = TextFont.render(winner + " team wins!", True, (255, 255, 255))
    textTextRect = textText.get_rect()
    textTextRect.center = (450, 300)
    screen.blit(titleText, titleTextRect)
    screen.blit(textText, textTextRect)

def makeDraggable(image, x, y):
    drag = draggable(screen, image, x, y)
    eventListeners.append(drag)
    updates.append(drag)
    return drag

def makePiecePool(numberpieces, images, x, y, name):
    pool = PiecePool(numberpieces, images, x, y, screen, TextFont, name)
    eventListeners.append(pool)
    updates.append(pool)
    piecePools.append(pool)
    return pool

playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        for b in eventListeners:
            b.handleEvent(event)
    if state == "menu":
        showMenu()
    elif state == "setup":
        showSetup()
    elif state == "play":
        showPlay()
    elif state == "Game Over":
        showGameOver()
    for listeners in updates:
        listeners.update()
    pygame.display.flip()
pygame.quit()


