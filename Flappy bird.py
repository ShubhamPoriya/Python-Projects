from pygame.locals import *
import random
import sys
import pygame

FPS = 32  # Frames per second i.e. how fast the screen will refresh when rendering images
SCREENWIDTH = 300
SCREENHEIGHT = 500
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = int(SCREENHEIGHT*0.8)
GAME_SPRITES = {}
GAME_SOUNDS = {}

PLAYER = r'C:\Users\shubh\Downloads\flappy\gallery\sprites\bird.png'
BACKGROUND = r'C:\Users\shubh\Downloads\flappy\gallery\sprites\background.png'
PIPE = r'C:\Users\shubh\Downloads\flappy\gallery\sprites\pipe.png'

def welcome():
    '''Shows welcome message on screen '''
    playerx = int((SCREENWIDTH/2) - 10)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            # if user clicks cross button 
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # if user presses space or up key, start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

# ------ Main game function ------

def maingame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    # Create 2 pipes

    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()

    # Create list of upper pipe
    upperpipes = [
        {'x' : SCREENWIDTH + 200, 'y' : newpipe1[0]['y']},
        {'x' : SCREENWIDTH + 200 + int(SCREENWIDTH/2), 'y' : newpipe2[0]['y']}
    ]
    # List of lower pipes
    lowerpipes = [
        {'x' : SCREENWIDTH + 200, 'y' : newpipe1[1]['y']},
        {'x' : SCREENWIDTH + 200 + int(SCREENWIDTH/2), 'y' : newpipe2[1]['y']}
    ]

    pipeVelX = -4 # pipe velocity backwards in -X direction <----

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8   # Velocity while flapping
    playerFlapped = False  # True only when bird is flapping 

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

            crashTest = isCollide(playerx, playery, upperpipes, lowerpipes) # This function is returned if the player is crashed
            if crashTest:
                return

        # Check for Score
        playerMidpos = playerx + int(GAME_SPRITES['player'].get_width()/2)
        for pipe in upperpipes:
            pipeMidpos = pipe['x'] + int(GAME_SPRITES['pipe'][0].get_width()/2)
            if pipeMidpos <= playerMidpos < pipeMidpos + 4:
                score += 1
                print(f"Your score is {score}.")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, (GROUNDY - playerHeight - playery))


        # Move pipes to the left  <----
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            upperpipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX  

        # Add a new pipe when pipe is about the leave the screen

        if 0 < upperpipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperpipes.append(newPipe[0])
            lowerpipes.append(newPipe[1])

        # If pipe gets out of screen, remove the pipe
        if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        # Blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        mydigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, 0.12*SCREENHEIGHT))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperpipes, lowerpipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerpipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():

    """generate two pipes (one straight and one rotated) and blit on screen"""
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = int(SCREENHEIGHT/3)
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    
    pipe = [
        {'x': pipex, 'y': -y1}, # upper pipe -- [0]
        {'x': pipex, 'y': y2}  # lower pipe  -- [1]
    ] 
    return pipe



# ------------ Main Program Starts --------------

if __name__ == "__main__":  
    # The main point from where out program will start
    pygame.init()  # Initialise the pygame module
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by Shubham Poriya")
    GAME_SPRITES['numbers'] = (
        pygame.image.load(r'C:\Users\shubh\Downloads\flappy\gallery\sprites\1.png').convert_alpha(),
        pygame.image.load(r'C:\Users\shubh\Downloads\flappy\gallery\sprites\2.png').convert_alpha(),
        pygame.image.load(r'C:\Users\shubh\Downloads\flappy\gallery\sprites\3.png').convert_alpha(),
        pygame.image.load(r'C:\Users\shubh\Downloads\flappy\gallery\sprites\4.png').convert_alpha(),
        pygame.image.load(r'C:\Users\shubh\Downloads\flappy\gallery\sprites\5.png').convert_alpha(),
        pygame.image.load(r'C:\Users\shubh\Downloads\flappy\gallery\sprites\6.png').convert_alpha(),
        pygame.image.load(r'C:\Users\shubh\Downloads\flappy\gallery\sprites\7.png').convert_alpha(),
        pygame.image.load(r'C:\Users\shubh\Downloads\flappy\gallery\sprites\8.png').convert_alpha(),
        pygame.image.load(r'C:\Users\shubh\Downloads\flappy\gallery\sprites\9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load(r'C:\Users\shubh\Downloads\flappy\gallery\sprites\message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load(r'C:\Users\shubh\Downloads\flappy\gallery\sprites\base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

# -))) Game Sound (((-

    GAME_SOUNDS['die'] = pygame.mixer.Sound(r'C:\Users\shubh\Downloads\flappy\gallery\audio\die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound(r'C:\Users\shubh\Downloads\flappy\gallery\audio\hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound(r'C:\Users\shubh\Downloads\flappy\gallery\audio\point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound(r'C:\Users\shubh\Downloads\flappy\gallery\audio\swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound(r'C:\Users\shubh\Downloads\flappy\gallery\audio\wing.wav')

    GAME_SPRITES['background'] = pygame.transform.scale(pygame.image.load(r'C:\Users\shubh\Downloads\flappy\gallery\sprites\background.png').convert(), (SCREENWIDTH, SCREENHEIGHT))
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcome()  # Diplay message unitl player clicks to play
        maingame() # this is the main game function