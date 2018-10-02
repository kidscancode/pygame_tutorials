import pygame
import time
import random

pygame.init()
pygame.mixer.init()


display_width = 800
display_height = 600
car_width = 56

black = (0,0,0)
white = (255,255,255)
green = (0,255,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("A bit racey")

clock = pygame.time.Clock()

carImg = pygame.image.load('racingCar.png')

# rectangle obstracles display:-

def blockDisplay(color,blockX,blockY,blockWidth,blockHeight):
	pygame.draw.rect(gameDisplay,color,[blockX,blockY,blockWidth,blockHeight])

# car displays:-

def car(x,y):
	gameDisplay.blit(carImg,(x,y))


#message display if car crashes:-

def text_object(text,font):
	textSurface = font.render(text,True,black)
	return textSurface , textSurface.get_rect()


def message(text):
	largeText = pygame.font.Font('freesansbold.ttf',70)
	TextSurf , TextRect = text_object(text,largeText)
	TextRect.center = ( (display_width/2),(display_height/2) )
	
	gameDisplay.fill(white)
	gameDisplay.blit(TextSurf,TextRect)
	pygame.display.update()
	time.sleep(2)
	game_loop()


def crash(score):
	message("Your Score " + str(score) )


# score display:-

def score_text_object(text,font):
	textSurface = font.render(text,True,green)
	return textSurface , textSurface.get_rect()


def scoreMessage(text):
	largeText = pygame.font.Font('freesansbold.ttf',15)
	TextSurf , TextRect = score_text_object(text,largeText)
	TextRect.center = (13,10)
	gameDisplay.blit(TextSurf,TextRect)
	pygame.display.update()


def scoreDisplay(score):
	scoreMessage("Your Score " + str(score) )


def game_loop():
	score=0
	carX = (display_width * 0.45)
	carY = (display_height * 0.8)

	car_x_change = 0
	gameExit = False

	# block config:-

	blockX = random.randrange(0,display_width)
	blockY = -600
	blockWidth = 100
	blockHeight = 100
	blockColor = black
	blockSpeed = 9

	while not gameExit:

		# Event capturing:-
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					car_x_change = -5
				elif event.key == pygame.K_RIGHT:
					car_x_change = 5

			if	event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					car_x_change=0
			
		# update background based on event captured:-	
		carX = carX + car_x_change					

		if carX<=0 or carX>=display_width - car_width:
			crash(score)	

		if blockY>display_height:
			score = score + 1
			blockSpeed += 1
			blockY = -display_height
			blockX = random.randrange(0,display_width)

		if (carX>blockX and carX<blockX+blockWidth and carY<blockY+blockHeight) or (carX+car_width>blockX and carX+car_width<blockX+blockWidth and carY<blockY+blockHeight):
			crash(score)

		
		#update frontend based on background event:-
		gameDisplay.fill(white)
		
		blockDisplay(blockColor,blockX,blockY,blockWidth,blockHeight)
		blockY = blockY + blockSpeed
		car(carX,carY)
		scoreDisplay(score)
		pygame.display.update()
		clock.tick(60)

game_loop()
pygame.quit()





