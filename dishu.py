###############################################
# hit mole - pygame app
#
# StartDate: 02/03/2019
# EndDate: 03/03/2019
# Author: Chen
###############################################
import pygame
import random
from pygame import *
from pygame.sprite import *


# location of each hole
hole_positions = []
hole_positions.append((210, 150))
hole_positions.append((210, 340))
hole_positions.append((215, 535))

hole_positions.append((305, 125))
hole_positions.append((305, 345))
hole_positions.append((305, 542))

hole_positions.append((400, 120))
hole_positions.append((405, 340))
hole_positions.append((410, 563))


# mole
class Mole(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.image = image.load("images/mole.png")
		self.rect = self.image.get_rect()
		num = random.randint(0,8)
		self.rect.left = hole_positions[num][1]
		self.rect.top = hole_positions[num][0]
	def flee(self):
		num = random.randint(0,8)
		self.rect.left = hole_positions[num][1]
		self.rect.top = hole_positions[num][0]

# music
class Sound():
    def __init__(self):
        self.bgMusic = pygame.mixer.music.load("music/themesong.wav")
        self.popSound = pygame.mixer.Sound("music/pop.wav")
        self.hurtSound = pygame.mixer.Sound("music/hurt.wav")
        pygame.mixer.music.play(-1)
    def playPop(self):
        self.popSound.play()
    def playHurt(self):
        self.hurtSound.play()


# init game
pygame.init()
display.set_caption("Get Me!")
screen = display.set_mode((740, 540))

# create mole groups
my_mole = Mole()
all_sprites = Group(my_mole)

# add bg colour + load bg image
screen.fill((255, 255, 255))
background = image.load("images/bg.png")

# display interface + add create music obj
screen.blit(background, (0, 0))
all_sprites.draw(screen)
display.update()
my_sound = Sound()

# track time
pygame.time.set_timer(pygame.USEREVENT, 1000)

# init var
amount = 20
clicks = 20
seconds = 0
wrong_clicks = 0
pause = False

# print result of game
def output(resultStr):
	basicfont = pygame.font.SysFont(None, 48)
	text = basicfont.render(resultStr, True, (255, 0, 0), (255, 255, 255))
	textrect = text.get_rect()
	textrect.centerx = background.get_rect().centerx
	textrect.centery = background.get_rect().centery
	screen.blit(text, textrect)
	display.update()


# Main logic
while True:
	# monitor input
	ev = event.wait()
	if ev.type == QUIT:
		pygame.quit()
		break
	# mouse hit event
	elif ev.type == pygame.MOUSEBUTTONDOWN and pause == False:
		clicks -= 1
		if my_mole.rect.collidepoint(mouse.get_pos()):
			my_sound.playHurt()
			screen.blit(background, (0, 0))
			display.update()
		else:
			my_sound.playPop()
			wrong_clicks += 1
			# more than 4 wrong it will lose game
			if wrong_clicks > 4:
				pause = True
				output('YOU LOSE THE GAME !')			
	if ev.type == pygame.USEREVENT:
		seconds += 1
		# refresh mole every 2 seconds
		if seconds % 2 == 0 and seconds != 0 and pause == False:
			screen.blit(background, (0, 0))
			my_mole.flee()
			all_sprites.draw(screen)
			display.update()
			amount -= 1
			# win te game
			if amount == 0:
				screen.blit(background, (0, 0))
				pause = True
				output('YOU WIN :) ')
	# no hit more than 4 times then lose
	if clicks - amount > 4:
		pause = True
		output('YOU LOSE THE GAME !')
