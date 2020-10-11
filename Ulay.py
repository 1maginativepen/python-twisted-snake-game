import pygame, random, sys
from pygame.locals import *
from os import system, name
import winsound,time

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
bg = pygame.image.load("Images/back.png")
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)


# For Color Configurations of the Panel
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
YELLOW    = (255,   242,  18)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
NAVYBLUE  = (  0,   0, 128)
LASTLEVEL = (255, 150, 10)
BGCOLOR = BLACK

#Snake eat apple
frequency = 2500
duration = 30


UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

FPS = 10
GAMEOVERIMAGE = "Images/GAMEOVER.png"
GAMEWINIMAGE = "Images/grats.png"
GAMEOVERIMAGEWRONGFOOD = "Images/GAMEOVER2.png"
GAMEOVERIMAGEEATFAKES = "Images/GAMEOVER3.png"
HEAD = 0 # syntactic sugar: index of the worm's head
SCORELEADER = []
FOODLEADER = [0,0,0]
FOODLIST = []
REMOTE = [0]
DEATH = [0]
for x in range (0, 3): 
    SCORELEADER.append(random.randint(1, 9))


def main():
    
    global FPSCLOCK, DISPLAYSURF, BASICFONT, FPS, __SnakeColor

    pygame.init()
    __SnakeColor = 0
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Ulay - ImaginativePen')
    
    showStartScreen()
    while True:
        runGame()
        if(DEATH[0] == 0):
            showGameOverScreen()
            rerollFoods()
            FOODLEADER[0] = 0
            FOODLEADER[1] = 0
            FOODLEADER[2] = 0
            REMOTE[0] = 0
        elif(DEATH[0] == 1):
            showGameOverScreen()
            rerollFoods()
            FOODLEADER[0] = 0
            FOODLEADER[1] = 0
            FOODLEADER[2] = 0
            REMOTE[0] = 0
        else:
            showGameOverScreen1()
            rerollFoods()
            FOODLEADER[0] = 0
            FOODLEADER[1] = 0
            FOODLEADER[2] = 0
            REMOTE[0] = 0
def FoodTeleport():
    print()
    
def FPSADD():
    FPS = FPS + 5

def mainmenusound():
    gameOverSound = pygame.mixer.Sound('Sounds/openingsound.wav') 
    gameOverSound.play()

def soundTeleport(): 
    gameOverSound = pygame.mixer.Sound('Sounds/teleport.wav') 
    gameOverSound.play()
    
def soundDead():
    gameOverSound = pygame.mixer.Sound('Sounds/gameover.wav')
#    pygame.mixer.music.stop()
    gameOverSound.play()

def countdownTimer():
    #clock = pygame.time.Clock() #FPSCLOCK
    #counter, text = 10, '10'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000) 

    while True:
        for e in pygame.event.get():
            if e.type == pygame.USEREVENT: 
                counter -= 1
                text = str(counter).rjust(3) if counter > 0 else 'boom!' 
            if e.type == pygame.QUIT: break
        else: 
            clock.tick(60)
            continue
        break
    
def runGame():
    clear()  
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT 
    # Start the apple in a random place.
    apple = getRandomLocation()
    banana = getRandomLocation1()
    mango = getRandomLocation2()
    enemy1_ = randomenemy1()
    enemy2_ = randomenemy2()
    enemy3_ = randomenemy3()
    
    counter, text = 10, '10'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 500)
    
    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            #event for countdown timer before food gets new location
            if event.type == pygame.USEREVENT: 
                counter -= 1
                text = str(counter).rjust(3)
                if counter > 0:
                    print('')
                else: 
                    counter = 5
                    apple = getRandomLocation()
                    banana = getRandomLocation1()
                    mango = getRandomLocation2() 
                    enemy1_ = randomenemy1()
                    enemy2_ = randomenemy2()
                    enemy3_ = randomenemy3()
                    drawApple(apple)
                    drawBanana(apple)
                    drawMango(mango)  
                    enemy1(enemy1_)
                    enemy2(enemy2_)
                    enemy3(enemy3_)
                    soundTeleport()
                
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT: 
            DEATH[0] = 0
            soundDead()
            del FOODLIST[0:len(FOODLIST)] 
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:  
                del FOODLIST[0:len(FOODLIST)] 
                return # game over

                                                                                                                                    # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment 
            if(REMOTE[0]==0):
                FOODLEADER[0] = 1 
                REMOTE[0] = 1
                FOODLIST.append(SCORELEADER[0])
                if(FOODLEADER[0] == 0):
                    apple = getRandomLocation() # set a new apple somewhere              
                else:
                    gameOverSound = pygame.mixer.Sound('Sounds/eat.wav') 
                    gameOverSound.play() 
            elif(REMOTE[0] > 0):
                print("EASTER EGG")
            else:
                return
        elif wormCoords[HEAD]['x'] == banana['x'] and wormCoords[HEAD]['y'] == banana['y']:
            # don't remove worm's tail segment 
            if(REMOTE[0]==1):
                FOODLEADER[1] = 1
                REMOTE[0] = 2
                FOODLIST.append(SCORELEADER[1])
                if(FOODLEADER[1] == 0):
                    banana = getRandomLocation1() # set a new banana somewhere  
                else:
                    gameOverSound = pygame.mixer.Sound('Sounds/eat.wav') 
                    gameOverSound.play()
            elif(REMOTE[0]==0):
                DEATH[0]=1
                return
            elif(REMOTE[1] == 1 or REMOTE[1] ==2):
                print("EASTER EGG")
            else:
                return
        elif wormCoords[HEAD]['x'] == mango['x'] and wormCoords[HEAD]['y'] == mango['y']:
            # don't remove worm's tail segment 
            if(REMOTE[0]==2):
                FOODLEADER[2] = 1
                REMOTE[0]=0
                FOODLIST.append(SCORELEADER[2])
                if(FOODLEADER[2] == 0):
                    mango = getRandomLocation2() # set a new mango somewhere 
                else:
                    gameOverSound = pygame.mixer.Sound('Sounds/eat.wav') 
                    gameOverSound.play()
                    rerollFoods()
                    FOODLEADER[0] = 0
                    FOODLEADER[1] = 0
                    FOODLEADER[2] = 0
            elif(REMOTE[0]==0 or REMOTE[0]==1):
                DEATH[0]=1
                return
            else:
                return
        elif wormCoords[HEAD]['x'] == enemy1_['x'] and wormCoords[HEAD]['y'] == enemy1_['y']:                                                            #enemy coords
            # don't remove worm's tail segment 
            DEATH[0]=2
            return
        elif wormCoords[HEAD]['x'] == enemy2_['x'] and wormCoords[HEAD]['y'] == enemy2_['y']:                                                            #enemy coords
            # don't remove worm's tail segment 
            DEATH[0]=2
            return
        elif wormCoords[HEAD]['x'] == enemy3_['x'] and wormCoords[HEAD]['y'] == enemy3_['y']:                                                            #enemy coords
            # don't remove worm's tail segment 
            DEATH[0]=2
            return
        else:
            del wormCoords[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead) 
        DISPLAYSURF.fill(BGCOLOR) 
        background_image = pygame.image.load("Images/back.png").convert()
        DISPLAYSURF.blit(background_image, [0, 0])

        #Changing Snake Color Depends on Speed.
        if len(wormCoords) - 3  >= 0 and len(wormCoords) - 3 < 5:  
            drawWorm(wormCoords,1)
        if len(wormCoords) - 3  >= 5 and len(wormCoords) - 3 < 10:  
            drawWorm(wormCoords,2)
        if len(wormCoords) - 3  >= 10 and len(wormCoords) - 3 < 15:  
            drawWorm(wormCoords,3)
        if len(wormCoords) - 3  >= 15 and len(wormCoords) - 3 < 20:  
            drawWorm(wormCoords,4)
        if len(wormCoords) - 3  >= 20 and len(wormCoords) - 3 < 25: 
            drawWorm(wormCoords,5)
        if len(wormCoords) - 3  >= 25:  
            drawWorm(wormCoords,6)
             
        drawApple(apple)
        drawBanana(banana)
        drawMango(mango)
        enemy1(enemy1_)
        enemy2(enemy2_)
        enemy3(enemy3_)
        drawScore(len(wormCoords) - 3)
        drawPattern()
        pygame.display.update()
        
        #Snake Speed increase when score hits 10,20,30,40,50
        if len(wormCoords) - 3  >= 0 and len(wormCoords) - 3 < 5: 
            FPSCLOCK.tick(FPS) 
        if len(wormCoords) - 3  >= 5 and len(wormCoords) - 3 < 10: 
            FPSCLOCK.tick(FPS+5) 
        if len(wormCoords) - 3  >= 10 and len(wormCoords) - 3 < 15: 
            FPSCLOCK.tick(FPS+10) 
        if len(wormCoords) - 3  >= 15 and len(wormCoords) - 3 < 20: 
            FPSCLOCK.tick(FPS+15) 
        if len(wormCoords) - 3  >= 20 and len(wormCoords) - 3 < 25:
            FPSCLOCK.tick(FPS+20) 
        if len(wormCoords) - 3  >= 25: 
            FPSCLOCK.tick(FPS+25) 
            
def snakeColor(index,colorValue):
    if index == 1000:
       _snakecolor = colorValue
    else:
        _snakecolor = index   
    return _snakecolor
    
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen(): 
    background_image = pygame.image.load("Images/Ulay.png").convert()
    DISPLAYSURF.blit(background_image, [0, 0])
    mainmenusound()
    while True:  
        if checkForKeyPress(): 
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS) 


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)} 

def getRandomLocation1():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def getRandomLocation2():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def randomenemy1():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def randomenemy2():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def randomenemy3():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def showGameOverScreen(): 
    background_image = pygame.image.load(GAMEOVERIMAGE).convert()
    DISPLAYSURF.blit(background_image, [0, 0])   
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue
    time.sleep(3)
    while True:
        if checkForKeyPress(): 
#            pygame.mixer.music.play()
            pygame.event.get() # clear event queue
            return

def showWinnerScreen(): 
    background_image = pygame.image.load(GAMEWINIMAGE).convert()
    DISPLAYSURF.blit(background_image, [0, 0])   
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue
    time.sleep(3)
    while True:
        if checkForKeyPress(): 
#            pygame.mixer.music.play()
            pygame.event.get() # clear event queue
            return

def showGameOverScreen1(): 
    background_image = pygame.image.load(GAMEOVERIMAGEWRONGFOOD).convert()
    DISPLAYSURF.blit(background_image, [0, 0])   
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue
    time.sleep(3)
    while True:
        if checkForKeyPress(): 
#            pygame.mixer.music.play()
            pygame.event.get() # clear event queue
            return

def showGameOverScreen1(): 
    background_image = pygame.image.load(GAMEOVERIMAGEEATFAKES).convert()
    DISPLAYSURF.blit(background_image, [0, 0])   
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue
    time.sleep(3)
    while True:
        if checkForKeyPress(): 
#            pygame.mixer.music.play()
            pygame.event.get() # clear event queue
            return
    
myscore = 0

def SumScore():
    scorescore = BASICFONT.render('Total Score : %s' % (sum(FOODLIST)), True, WHITE)
    scorescoreRect = scorescore.get_rect()
    scorescoreRect.topleft = (10, 30)
    DISPLAYSURF.blit(scorescore, scorescoreRect)

def drawList():
    listlist = BASICFONT.render('Food Bag : %s' % (FOODLIST), True, WHITE)
    listRect = listlist.get_rect()
    listRect.topleft = (10, 10)
    DISPLAYSURF.blit(listlist, listRect)
    SumScore()

def drawScore(score): 
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (10, WINDOWHEIGHT - 20)
    drawList()
    DISPLAYSURF.blit(scoreSurf, scoreRect) 

    if sum(FOODLIST) >= 20:
        del FOODLIST[0:len(FOODLIST)] 
        __SnakeColor = 0
        showWinnerScreen()


def rerollFoods(): 
    SCORELEADER[0]=random.randint(1, 9)
    SCORELEADER[1]=random.randint(1, 9)
    while(SCORELEADER[1]==SCORELEADER[0]):
        SCORELEADER[1]=random.randint(1, 9)
    while(SCORELEADER[2]==SCORELEADER[0] or SCORELEADER[2]==SCORELEADER[1]):
        SCORELEADER[2]=random.randint(1, 9) 
    drawPattern()
    print(SCORELEADER)

def drawPattern(): 
    patternSurf = BASICFONT.render('Get In: %s' % (SCORELEADER), True, WHITE)
    patternRect = patternSurf.get_rect()
    patternRect.topleft = (10, WINDOWHEIGHT -40)
    DISPLAYSURF.blit(patternSurf, patternRect) 


def drawWorm(wormCoords,color):                                                                                                         #Snake Body Color
    if color == 1:        
        for coord in wormCoords:
            x = coord['x'] * CELLSIZE
            y = coord['y'] * CELLSIZE
            wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormInnerSegmentRect)
    if color == 2:        
        for coord in wormCoords:
            x = coord['x'] * CELLSIZE
            y = coord['y'] * CELLSIZE
            wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, WHITE, wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, WHITE, wormInnerSegmentRect)
    if color == 3:        
        for coord in wormCoords:
            x = coord['x'] * CELLSIZE
            y = coord['y'] * CELLSIZE
            wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, RED, wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, RED, wormInnerSegmentRect)
    if color == 4:        
        for coord in wormCoords:
            x = coord['x'] * CELLSIZE
            y = coord['y'] * CELLSIZE
            wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, DARKGRAY, wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, DARKGRAY, wormInnerSegmentRect)
    if color == 5:        
        for coord in wormCoords:
            x = coord['x'] * CELLSIZE
            y = coord['y'] * CELLSIZE
            wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, NAVYBLUE, wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, NAVYBLUE, wormInnerSegmentRect)
    if color == 6:        
        for coord in wormCoords:
            x = coord['x'] * CELLSIZE
            y = coord['y'] * CELLSIZE
            wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, LASTLEVEL, wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, LASTLEVEL, wormInnerSegmentRect)


def drawApple(coord): 
    if(FOODLEADER[0]==0):
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE) 
        pygame.draw.rect(DISPLAYSURF, RED, appleRect)
        appleInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, WHITE, appleInnerSegmentRect)

        appleIDSurf = BASICFONT.render('%s' % (SCORELEADER[0]), True, BLACK)
        appleIDRect = appleIDSurf.get_rect()
        appleIDRect.topleft = (x+5,y)
        DISPLAYSURF.blit(appleIDSurf, appleIDRect) 

def drawBanana(coord): 
    if(FOODLEADER[1]==0):
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        bananaRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE) 
        pygame.draw.rect(DISPLAYSURF, YELLOW, bananaRect)
        bananaInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, WHITE, bananaInnerSegmentRect)

        bananaIDSurf = BASICFONT.render('%s' % (SCORELEADER[1]), True, BLACK)
        bananaIDRect = bananaIDSurf.get_rect()
        bananaIDRect.topleft = (x+5,y)
        DISPLAYSURF.blit(bananaIDSurf, bananaIDRect) 

def drawMango(coord): 
    if(FOODLEADER[2]==0):
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        mangoRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE) 
        pygame.draw.rect(DISPLAYSURF, GREEN, mangoRect)
        mangoInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, WHITE, mangoInnerSegmentRect)

        mangoIDSurf = BASICFONT.render('%s' % (SCORELEADER[2]), True, BLACK)
        mangoIDRect = mangoIDSurf.get_rect()
        mangoIDRect.topleft = (x+5,y)
        DISPLAYSURF.blit(mangoIDSurf, mangoIDRect) 
  
def enemy1(coord): 
    if(FOODLEADER[2]==0):
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        mangoRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE) 
        pygame.draw.rect(DISPLAYSURF, RED, mangoRect)
        mangoInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, WHITE, mangoInnerSegmentRect)

def enemy2(coord): 
    if(FOODLEADER[2]==0):
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        mangoRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE) 
        pygame.draw.rect(DISPLAYSURF, YELLOW, mangoRect)
        mangoInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, WHITE, mangoInnerSegmentRect)

def enemy3(coord): 
    if(FOODLEADER[2]==0):
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        mangoRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE) 
        pygame.draw.rect(DISPLAYSURF, GREEN, mangoRect)
        mangoInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, WHITE, mangoInnerSegmentRect)

def clear():  
    if name == 'nt': 
        _ = system('cls') 
   
    else: 
        _ = system('clear')

clear() 
main()
