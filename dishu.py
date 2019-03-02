###############################################
# 打地鼠 - 小游戏
#
# 开始日期: 02/03/2019
# 结束日期: 
# 作者: Chen
###############################################
import pygame
import random
from pygame import *
from pygame.sprite import *


# 每个地洞的坐标
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


# 地鼠对象
class Mole(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.image = image.load("mole.png")
		self.rect = self.image.get_rect()
		num = random.randint(0,8)
		self.rect.left = hole_positions[8][1]
		self.rect.top = hole_positions[8][0]
	def flee(self):
		num = random.randint(0,8)
		self.rect.left = hole_positions[num][1]
		self.rect.top = hole_positions[num][0]

# 音乐对象
class Sound():
    def __init__(self):
        self.bgMusic = pygame.mixer.music.load("themesong.wav")
        self.popSound = pygame.mixer.Sound("pop.wav")
        self.hurtSound = pygame.mixer.Sound("hurt.wav")
        pygame.mixer.music.play(-1)
    def playPop(self):
        self.popSound.play()
    def playHurt(self):
        self.hurtSound.play()


# 游戏初始化
pygame.init()
display.set_caption("打地鼠")
screen = display.set_mode((740, 540))

# 创建地鼠对象
my_mole = Mole()
all_sprites = Group(my_mole)

# 添加背景颜色 + 加载背景图片
screen.fill((255, 255, 255))
background = image.load("bg.png")

# 显示界面 + 音乐对象
screen.blit(background, (0, 0))
all_sprites.draw(screen)
display.update()
my_sound = Sound()

# 追踪游戏的时间
pygame.time.set_timer(pygame.USEREVENT, 1000)

# 初始化数据
amount = 20
clicks = 20
seconds = 0
wrong_clicks = 0
pause = False


def output(resultStr):
	basicfont = pygame.font.SysFont(None, 48)
	text = basicfont.render(resultStr, True, (255, 0, 0), (255, 255, 255))
	textrect = text.get_rect()
	textrect.centerx = background.get_rect().centerx
	textrect.centery = background.get_rect().centery
	screen.blit(text, textrect)
	display.update()


# 游戏逻辑
while True:
	# 监听游戏事件
	ev = event.wait()
	if ev.type == QUIT:
		pygame.quit()
		break
	# 鼠标点击事件
	elif ev.type == pygame.MOUSEBUTTONDOWN and pause == False:
		clicks -= 1
		if my_mole.rect.collidepoint(mouse.get_pos()):
			my_sound.playHurt()
			screen.blit(background, (0, 0))
			display.update()
		else:
			my_sound.playPop()
			wrong_clicks += 1
			# 点错4次地鼠会输掉游戏
			if wrong_clicks > 4:
				pause = True
				output('YOU LOSE THE GAME !')			
	if ev.type == pygame.USEREVENT:
		seconds += 1
		# 每2秒会刷新地鼠
		if seconds % 2 == 0 and seconds != 0 and pause == False:
			screen.blit(background, (0, 0))
			my_mole.flee()
			all_sprites.draw(screen)
			display.update()
			amount -= 1
			# 游戏胜利并结束
			if amount == 0:
				screen.blit(background, (0, 0))
				pause = True
				output('YOU WIN :) ')
	# 未点击地鼠超过4次游戏结束
	if clicks - amount > 4:
		pause = True
		output('YOU LOSE THE GAME !')
