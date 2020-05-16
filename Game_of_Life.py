
# Conway's Game of Life by Sara Inigo

import numpy as np
import pygame
import time

pygame.init()
# Width and height of the screen
width, height = 500, 500
# Screen creation
screen = pygame.display.set_mode((height, width))
# Color of screen
bg = 25,25,25
screen.fill(bg)

# Number of cells of the board
nxC, nyC = 25, 25
dimCW = width/nxC
dimCH = height/nyC

# State of the cells (live = 1, dead = 0)
# Initialize to zero
gameState = np.zeros((nxC, nyC))

# stick
#gameState[5, 3] = 1
#gameState[5, 4] = 1
#gameState[5, 5] = 1

# mobile
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Control game execution
pauseExect = False

# Loop to see board
while True:
    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)

    # register keyboard events
    ev = pygame.event.get()

    # We will pause the execution of the game if a key is pressed
    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        # We will revive and kill mouse clicked cells on the screen (revive = left click, kill = right click)
        mouseClick = pygame.mouse.get_pressed()
        # print(mouseClick)
        if sum(mouseClick) > 0:
            # Position in pixels of the mouse click
            posX, posY = pygame.mouse.get_pos()
            # Cell of the mouse click
            celX, celY = int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH))
            newGameState[celX, celY] = not mouseClick[2]

    for y in range(0,nxC):
        for x in range(0, nyC):

            if not pauseExect:

                # Compute number of nearest neighbors alive
                #  (% nxC gives toroidal effect to the board)
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                          gameState[(x) % nxC, (y-1) % nyC] + \
                          gameState[(x+1) % nxC, (y-1) % nyC] + \
                          gameState[(x-1) % nxC, (y) % nyC] + \
                          gameState[(x+1) % nxC, (y) % nyC] + \
                          gameState[(x-1) % nxC, (y+1) % nyC] + \
                          gameState[(x) % nxC, (y+1) % nyC] + \
                          gameState[(x+1) % nxC, (y+1) % nyC]

                # Rule 1: Any dead cell with exactly three live neighbours will come to life
                if gameState[x,y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Rule 2: Any live cell with fewer than two live neighbours dies (underpopulation)
                # Rule 3: Any live cell with more than three live neighbours dies (overpopulation)
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

                # Rule 4: Any live cell with two or three live neighbours lives, unchanged, to the next generation

            # Create polygon for each cell
            poly = [((x)*dimCW, y*dimCH),
                    ((x+1)*dimCW, y*dimCH),
                    ((x+1)*dimCW, (y+1)*dimCH),
                    ((x)*dimCW, (y+1)*dimCH)]

            # Draw the cell for each x,y pair (live: white square, dead = empty square)
            if newGameState[x,y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (225, 225, 225), poly, 0)

    # Update game state
    gameState = np.copy(newGameState)

    # Update screen
    pygame.display.flip()