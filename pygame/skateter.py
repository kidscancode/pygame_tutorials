import pygame
import time

pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

display_width = 500
display_height = 400

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Skater Boy")

SkaterImg = pygame.image.load('skater.png')

def Skater(x,y):
	gameDisplay.blit(SkaterImg,(x,y))


def blockDisplay(color,blockX,blockY,blockWidth,blockHeight):
	pygame.draw.rect(gameDisplay,color,[blockX,blockY,blockWidth,blockHeight])


def ballDisplay(color,ballX,ballY,ball_rad):
	pygame.draw.circle(gameDisplay, color, [ballX, ballY], ball_rad)



clock = pygame.time.Clock()
	 		

def text_object(text,font):
	textSurface = font.render(text,True,red)
	return textSurface , textSurface.get_rect()


def message(text):
	largeText = pygame.font.Font('freesansbold.ttf',70)
	TextSurf , TextRect = text_object(text,largeText)
	TextRect.center = ( (display_width/2),(display_height/2) )
	
	gameDisplay.fill(black)
	gameDisplay.blit(TextSurf,TextRect)
	pygame.display.update()

	time.sleep(2)
	game_loop()


def loose():
	message("You Miss")



def game_loop():

	miss = False

	# skater config:-

	skateX = 215
	skateY = display_height - 12
	skate_width = 79 
	skate_height = 12
	skateSpeed = 0

	# ball config:-

	color = red
	ballX = 255
	ballY = display_height - 19
	ball_x_speed = 3
	ball_y_speed = -2
	ball_rad = 7
		 		


	while not miss:

		# event handlers:-

		for event in pygame.event.get(): 
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					skateSpeed = -5
				elif event.key == pygame.K_RIGHT:
					skateSpeed = 5

			if	event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					skateSpeed=0		


		# background update:-

		# skate Board updatons:-

		skateX = skateX + skateSpeed

		if skateX <= 0:
			skateX=0
		if skateX >= display_width-skate_width:
			skateX=display_width-skate_width	


		# Ball Updations:-	

		ballX += ball_x_speed
		ballY += ball_y_speed

		if ballX + ball_rad >= display_width:
			ball_x_speed = -ball_x_speed

		if ballX - ball_rad <= 0:
			ball_x_speed = -ball_x_speed

		if ballY - ball_rad <= 0:
			ball_y_speed = -ball_y_speed

		if ballY + ball_rad >= display_height - skate_height:
			if (ballX + ball_rad >= skateX) and (ballX-ball_rad <= skateX+skate_width):
				ball_y_speed = - ball_y_speed

			else:
				loose()


		# frontEnd update:- 
		gameDisplay.fill(black)
		Skater(skateX,skateY)
		ballDisplay(color,ballX,ballY,ball_rad)
		pygame.display.update()
		clock.tick(60)


game_loop()
pygame.quit()
quit()
