import pygame
pygame.init()
display= pygame.display.set_mode((500,500))
pygame.display.set_caption("First game")
screenWidth=500
screenHeight=500
x=50
y=50
width=50
height=50
vel=5
isJump=False
jumpCount=10


run = True

while run:
	pygame.time.delay(50)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	# display.fill((255,0,0))
	# pygame.draw.rect(display,(0,255,0),(x,y,width,height))
	# pygame.display.update()
	keys=pygame.key.get_pressed()
	if keys[pygame.K_LEFT] and x > vel:
		x-=vel
	if keys[pygame.K_RIGHT] and x < screenWidth-width-vel:
		x+=vel
	if not(isJump):
		if keys[pygame.K_UP] and y > vel:
			y-=vel
		if keys[pygame.K_DOWN] and y < 500-height-vel:
			y+=vel
		if keys[pygame.K_SPACE]:
			isJump=True
	if isJump:
		if jumpCount>=-10:
			neg=1
			if jumpCount<0:
				neg=-1
			y-=(jumpCount**2)*0.4*neg
			jumpCount-=1

		else:
			isJump = False
			jumpCount = 10
		
		


	display.fill((0,0,0))
	pygame.draw.rect(display,(0,255,0),(x,y,width,height))
	pygame.display.update()
pygame.quit()