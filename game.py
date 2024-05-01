import random
import sys
import pygame
from pygame.locals import *  # Basic pygame imports

# Global Variables for the game
FPS = 40
screenwidth = 289
screenheight = 511
# it sets the width and height of our screen
screen = pygame.display.set_mode((screenwidth, screenheight))

basey=screenheight * 0.75

game_images = {}




def welcomeScreen():
    """
 It shows welcome images on the screen
    """

    playerx = int(screenwidth / 5)
    playery = int((screenheight - game_images['player'].get_height()) / 2)
    messagex = int((screenwidth - game_images['message'].get_width()) / 2)
    messagey = int(screenheight * 0.25)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if the user clicks escape button or quit button , our screen will close
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user clicks any space button or uparrow button then our function returns
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            # if the user doesn't click any button
            else:
                screen.blit(game_images['background'], (0, 0))


                screen.blit(game_images['player'], (playerx, playery))
                screen.blit(game_images['message'], (messagex, messagey))
                screen.blit(game_images['base'], (basex, basey))
           



                pygame.display.update()
                FPSCLOCK.tick(FPS)



def mainGame():
    score = 0
    playerx = int(screenwidth / 5)
    playery = int(screenwidth / 2)
    basex = 0

    # Create a pipe for blitting on the screen
    pipe1 = getRandomPipe()


    # my List of upper pipes
    upperPipes = [
        {'x': screenwidth+10, 'y': pipe1[0]['y']}


    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': screenwidth+10, 'y': pipe1[1]['y']}


    ]

    pipevelocity = -5

    birdvelocity = -9


    gravity = 0.75


    playerFlapped = False  # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    birdvelocity = -9
                    playerFlapped = True


        crashTest = isCollide(playerx, playery, upperPipes,
                              lowerPipes)  # This function will return true if the player is crashed
        if crashTest:
            return

            # check for score
        playerMidPos = playerx + game_images['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_images['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 5:
                score += 1
                print(f"Your score is {score}")





        if  not playerFlapped:
            birdvelocity += gravity

        if playerFlapped:
            playerFlapped = False
        playerHeight = game_images['player'].get_height()
        playery = playery + min(birdvelocity, basey - playery - playerHeight)
        #
        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipevelocity
            lowerPipe['x'] += pipevelocity

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -game_images['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our images now
        screen.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(game_images['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_images['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(game_images['base'], (basex, basey))
        screen.blit(game_images['player'], (playerx, playery))
        digits = [int(x) for x in list(str(score))]
        width = 0
        for digit in digits:
            width += game_images['numbers'][digit].get_width()
        Xoffset = (screenwidth - width) / 2

        for digit in digits:
            screen.blit(game_images['numbers'][digit], (Xoffset,screenheight * 0.12))
            Xoffset += game_images['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)





def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery+game_images["player"].get_height() == basey  or playery < 0:

        return True

    for pipe in upperPipes:
        pipeHeight = game_images['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']-(game_images["player"].get_width()/2)) < game_images['pipe'][0].get_width()):

            return True

    for pipe in lowerPipes:
        if (playery + game_images['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']-(game_images["player"].get_width()/2)) < \
                game_images['pipe'][0].get_width():

            return True

    return False


def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = game_images['pipe'][0].get_height()
    offset = screenheight / 3
    y2 = offset + random.randrange(0, int(screenheight - game_images['base'].get_height() - 1.1* offset))
    pipeX = screenwidth + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe
        {'x': pipeX, 'y': y2}  # lower Pipe
    ]
    return pipe


if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init()  # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird game')
    game_images['numbers'] = (
        pygame.image.load('flappy bird/images/0.png').convert_alpha(),
        pygame.image.load('flappy bird/images/1.png').convert_alpha(),
        pygame.image.load('flappy bird/images/2.png').convert_alpha(),
        pygame.image.load('flappy bird/images/3.png').convert_alpha(),
        pygame.image.load('flappy bird/images/4.png').convert_alpha(),
        pygame.image.load('flappy bird/images/5.png').convert_alpha(),
        pygame.image.load('flappy bird/images/6.png').convert_alpha(),
        pygame.image.load('flappy bird/images/7.png').convert_alpha(),
        pygame.image.load('flappy bird/images/8.png').convert_alpha(),
        pygame.image.load('flappy bird/images/9.png').convert_alpha(),
    )

    game_images['message'] = pygame.image.load('flappy bird/images/message.png').convert_alpha()
    game_images['base'] = pygame.image.load('flappy bird/images/base.png').convert_alpha()
    game_images['pipe'] = (pygame.transform.rotate(pygame.image.load("flappy bird/images/pipe.png").convert_alpha(), 180),
                            pygame.image.load("flappy bird/images/pipe.png").convert_alpha()
                            )




    game_images['background'] = pygame.image.load("flappy bird/images/background.png").convert()
    game_images['player'] = pygame.image.load("flappy bird/images/bird.png").convert_alpha()

    while True:
        welcomeScreen()  # Shows welcome screen to the user until he presses a button
        mainGame()





