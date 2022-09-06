import os
import random
import pygame
pygame.init()

# Colors
white = (255,255,255)
red = (255,0,0)
green = (30,140,20)
black = (0,0,0)

screenHeight = 600
screenWidth = 1000
# Creating Window
GameWindow = pygame.display.set_mode((screenWidth,screenHeight))

# Title of the Game
pygame.display.set_caption("Snake Game")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None,55)
'''
backImage = pygame.image.load("backgroundImg.jpeg")
backImage = pygame.transform.scale(backImage, (screenWidth,screenHeight)).convert_alpha()
'''
def text_screen(text,color,x,y):
    screen_text = font.render(text,True, color)
    GameWindow.blit(screen_text, [x,y])

def plot_Snake(GameWindow,color,snakeList,snakeSize):
    for x,y in snakeList:
        pygame.draw.rect(GameWindow, color, [x, y, snakeSize, snakeSize])

def Main():

    snakeList = []
    snakeLength = 1

    # Food
    food_x = random.randint(0,screenWidth)
    food_y = random.randint(0,screenHeight)

    # Game Specific Variable
    exitGame = False
    gameOver = False
    snake_x = 45
    snake_y = 55
    snakeSize = 10 
    fps = 30
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5

    # Score of the game
    score = 0

    # Check if HighScore.txt File is Exists
    if(not os.path.exists("HighScore.txt")):
        with open("HighScore.txt","w") as f:
            f.write("0")

    # High-Score File 
    with open("HighScore.txt","r+") as f:
        highScore = f.read()

    while not exitGame:
        if gameOver:
            with open("HighScore.txt","w+") as f:
                f.write(str(highScore))
            GameWindow.fill(white)
            text_screen("Game Over!",red,400,180)
            text_screen("Press Enter To Start Again...",green,260,230)

            # Quiting Using GUI Cross Button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:    # K_RETURN is Enter Key
                        Main()

        else:
            # Quiting Using GUI Cross Button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame = True
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<10 and abs(snake_y - food_y)<10:
                score += 10
                food_x = random.randint(20, screenWidth/2)
                food_y = random.randint(20,screenHeight/2)
                snakeLength += 5
                if score > int(highScore):
                    highScore = score
                    
            GameWindow.fill(white)
            # ##GameWindow.fill(backImage,(0,0))
            text_screen("Score : "+str(score) + " HighScore : " +str(highScore),red,5,5)       #Score On the Sreen

            pygame.draw.rect(GameWindow,red,[food_x,food_y, snakeSize,snakeSize])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snakeList.append(head)

            # Game Over (Snake Clash with Wall)
            if len(snakeList)>snakeLength:
                del snakeList[0]

            # Game Over (Snake Eat his Body)
            if head in snakeList[:-1]:
                gameOver = True

            # Handling Game Over
            if snake_x<0 or snake_x>screenWidth or snake_y<0 or snake_y>screenHeight:
                gameOver = True

            plot_Snake(GameWindow, black, snakeList, snakeSize)
            # pygame.draw.rect(GameWindow, black, [snake_x, snake_y, snakeSize, snakeSize])
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

Main()