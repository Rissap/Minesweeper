import sys
import pygame
from random import randint

pygame.init()

RUN = True
SUCCESS = True
DELAY = 100
CELL_SIZE = 20
FIELD_SIZE = (10, 10)
SURACE_POSITION = (20, 50)
SURFACE_SIZE = (FIELD_SIZE[0]*CELL_SIZE, FIELD_SIZE[1]*CELL_SIZE)
SCREEN_SIZE = (FIELD_SIZE[0]*CELL_SIZE+40, FIELD_SIZE[1]*CELL_SIZE+70)

SCREEN = pygame.display.set_mode(SCREEN_SIZE)
SCREEN.fill(pygame.Color(80, 80, 190))

MINE_AMOUNT = 10
MINE_POSITION = []
FLAG_POSITION = []
QUESTION_POSITION = []
CELL_POSITION = [[x for x in range(0, 10)] for _ in range(0, 10)]

SPRITES = {
    "cell": pygame.image.load('res/cell.png').convert_alpha(),
    "flag": pygame.image.load('res/flag.png').convert_alpha(),
    "question": pygame.image.load('res/question.png').convert_alpha(),
    "mine": pygame.image.load('res/mine.png').convert_alpha()
}

FONT = pygame.font.SysFont('font/chewy.ttf', 24)


def set_numbers(surface):
    for row in range(FIELD_SIZE[0]):
        for col in range(FIELD_SIZE[0]):
            if CELL_POSITION[row][col] == -10 and [row, col] not in MINE_POSITION:
                amount = 0
                for i in range(row-1, row+2):
                    for j in range(col-1, col+2):
                        try:
                            if [i, j] in MINE_POSITION:
                                amount +=1
                        except IndexError:
                            pass
                if amount > 0:
                    text_surf = FONT.render(str(amount), True, pygame.Color(20, 255, 50))
                    surface.blit(text_surf, (col*CELL_SIZE, row*CELL_SIZE))


def render_surface():
    surface = pygame.Surface(SURFACE_SIZE)
    surface.fill(pygame.Color(200, 200, 255))

    for row in range(len(CELL_POSITION)):
        for col in CELL_POSITION[row]:
            surface.blit(SPRITES["cell"], (col*CELL_SIZE, row*CELL_SIZE))

    if not SUCCESS:
        for cell in MINE_POSITION:
            surface.blit(SPRITES["mine"], (cell[1]*CELL_SIZE, cell[0]*CELL_SIZE))    

    for cell in FLAG_POSITION:
        surface.blit(SPRITES["flag"], (cell[1]*CELL_SIZE, cell[0]*CELL_SIZE))

    for cell in QUESTION_POSITION:
        surface.blit(SPRITES["question"], (cell[1]*CELL_SIZE, cell[0]*CELL_SIZE))

    set_numbers(surface)
    return surface


def set_mark(position):
    y, x = (position[0]-20)//CELL_SIZE, (position[1]-50)//CELL_SIZE

    if y not in CELL_POSITION[x]:
        return True

    if [x, y] not in FLAG_POSITION and [x, y] not in QUESTION_POSITION:
        FLAG_POSITION.append([x, y])
        return True
    else:
        try:
            del FLAG_POSITION[FLAG_POSITION.index([x, y])]
        except:
            pass
    
    if [x, y] in QUESTION_POSITION:
        try:
            del QUESTION_POSITION[QUESTION_POSITION.index([x, y])]
        except:
            pass
    else:
        QUESTION_POSITION.append([x, y])
        return True


def open_cell(position):
    y, x = (position[0]-20)//CELL_SIZE, (position[1]-50)//CELL_SIZE

    if [x, y] in MINE_POSITION:
        return False

    if [x, y] in FLAG_POSITION or [x, y] in QUESTION_POSITION:
        return True

    try:
        CELL_POSITION[x][y] = -10
        return True
    except ValueError:
        return True


def set_mine():
    new_mine = [randint(0, FIELD_SIZE[0]), randint(0, FIELD_SIZE[0])]
    if new_mine not in MINE_POSITION:
        MINE_POSITION.append(new_mine)

    if len(MINE_POSITION) <= MINE_AMOUNT:
        set_mine()



set_mine()
while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONUP and SUCCESS:
            position = pygame.mouse.get_pos()
            if event.button == 1: #leftclick
                SUCCESS = open_cell(position)
            if event.button == 3: #rightclick
                set_mark(position)
        elif not SUCCESS:
            pass
        else:
            pass

    surface = render_surface()
    SCREEN.blit(surface, SURACE_POSITION)
    pygame.display.flip()
    pygame.time.delay(DELAY)

