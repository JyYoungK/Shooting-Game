import pygame
import sys
from time import sleep
from PIL import Image
import random
import glob

padWidth = 480
padHeight = 640
rockImage = ["img/rock01.png", "img/rock02.png", "img/rock03.png", "img/rock04.png", "img/rock05.png", "img/rock06.png", "img/rock07.png", "img/rock08.png", "img/rock09.png", "img/rock10.png", "img/rock11.png", "img/rock12.png", "img/rock13.png", "img/rock14.png", "img/rock15.png"]
##for rock in glob.glob("img/*.png"):
##    im=Image.open(rock)
##    rockImage.append(im)


def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def writeScore(count):
    global gamePad
    font = pygame.font.SysFont("comicsansms", 20)
    text = font.render("Destroyed: " + str(count), True, (255,255,255))
    gamePad.blit(text, (10,0))
    
def writePassed(count):
    global gamePad
    font = pygame.font.SysFont("comicsansms", 20)
    text = font.render("Missed: " + str(count), True, (255,0,0))
    gamePad.blit(text, (350,0))

def writeMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.SysFont("comicsansms", 60)
    text = textfont.render(text, True, (250, 0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()

def crash():
    global gamePad
    writeMessage("Game Over")

def gameOver():
    global gamePad
    writeMessage("Game Over")
    
def initGame():
    global gamePad, clock, background, plane, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption("Shooting Game")         #Name of the game
    background = pygame.image.load("img/background.png")  #Background Picture
    plane = pygame.image.load("img/fighter.png")          #Airplane Picture
    missile = pygame.image.load("img/missile.png")
    explosion = pygame.image.load("img/explosion.png")
    clock = pygame.time.Clock()
    pygame.mixer.music.load("sound/music.wav")
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound("sound/missile.wav")    #Missile Sound
    gameOverSound = pygame.mixer.Sound("sound/gameover.wav")  #Game Over Sound
    clock = pygame.time.Clock()
 
def runGame():
    global gamePad, clock, background, plane, missile, explosion, missileSound, gameOverSound
    #Airplane Size
    planeSize = plane.get_rect().size
    planeWidth = planeSize[0]
    planeHeight = planeSize[1]

    #Default airplane position
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    missileXY = []

    rock = pygame.image.load(random.choice(rockImage)) #Choose 1 random rock
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]

    rockX = random.randrange(0, padWidth - rockWidth) #Rock spawns at a random position
    rockY = 0
    rockSpeed = 2

    #When the missile hits the rock
    isShot = False
    shotCount = 0
    rockPassed = 0
    onGame = False
    
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:           #Terminate Game
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:      #Move left
                    fighterX -= 5 

                elif event.key == pygame.K_RIGHT:   #Move right
                    fighterX += 5

                elif event.key == pygame.K_SPACE:   #Space to shoot missile
                    missileSound.play()
                    missileX = x+planeWidth/2
                    missileY = y-planeHeight
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                 

        drawObject(background, 0, 0)              #Create Background
        # Reset Airplane Position
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - planeWidth:
            x = padWidth - planeWidth

        if y < rockY + rockHeight:
            if (rockX > x and rockX < x + planeWidth) or (rockX + rockWidth > x and rockX + rockWidth < x + planeWidth):
                crash()
                
        drawObject(plane, x, y)                   #Create Airplane

        #Draw missile on screen
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10                        
                missileXY[i][1] = bxy[1]            
                
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1
                        
                if bxy[1] <= 0:                     # Missile going out of the screen
                    try:
                        missileXY.remove(bxy)       # Remove Missile if it goes out of the screen
                    except:
                        pass
                    
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        writeScore(shotCount)
        rockY += rockSpeed    #Makes the rock fall
        
        if rockY > padHeight:#When rock passes the bottom line
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        if rockPassed == 3: #Game ends when you miss 3 rocks
            gameOver() 
        writePassed(rockPassed)

        if isShot:
            drawObject(explosion, rockX, rockY)
            ##destroySound.play()
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
##          destroySound = pygame.mixer.Sound(random.choice(explosionSound)) #Choose a random noise
            isShot = False

            rockSpeed += 0.2 #Increase the difficulty until Speed is 12
            if rockSpeed >= 9:
                rockSpeed = 9

        drawObject(rock, rockX, rockY)


        pygame.display.update()
        clock.tick(60)

    pygame.quit()

initGame()
runGame()
