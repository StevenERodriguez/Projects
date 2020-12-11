import pygame
import random
import sys

pygame.init()

#Game display size
width = 900
height = 750

#Colors
Pink = (255,105,180)
grey = (47, 79, 79, 255)
black = (255,48,48)
BACKGROUND_COLOR = (235,245,255)

#Box sizes
player_box = 60
enemy_box = 60

player_pos = [width/2,height-2*player_box]
enemy_pos = [random.randint(0,width-enemy_box), 0]
enemy_list = [enemy_pos]


speed = 10

#calls and sets display witdh and height
screen = pygame.display.set_mode((width, height))

end_game = False

score = 0

#timer tracks game time till loss
clock = pygame.time.Clock()

#Score font
myFont = pygame.font.SysFont("monospace", 35)

#speed increases as score increases
def set_level(score, speed):
	if score < 30:
		speed = 8
	elif score < 80:
		speed = 12
	elif score < 140:
		speed = 19

	else:
		speed = 24
	return speed

#the creation and drop of enemy boxes
def drop_enemies(enemy_list):
	delay = random.random()
	if len(enemy_list) < 20 and delay < 0.1:
		x_pos = random.randint(0,width-enemy_box)
		y_pos = 0
		enemy_list.append([x_pos, y_pos])
def draw_enemies(enemy_list):
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, grey, (enemy_pos[0], enemy_pos[1], enemy_box, enemy_box))
def update_enemy_positions(enemy_list, score):
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < height:
			enemy_pos[1] += speed
		else:
			enemy_list.pop(idx)
			score += 1
	return score

#When player gets hit by an enemy box
def collision_check(enemy_list, player_pos):
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos, player_pos):
			return True
	return False

def detect_collision(player_pos, enemy_pos):
	p_x = player_pos[0]
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < (p_x + player_box)) or (p_x >= e_x and p_x < (e_x+enemy_box)):
		if (e_y >= p_y and e_y < (p_y + player_box)) or (p_y >= e_y and p_y < (e_y+enemy_box)):
			return True
	return False

#User key inputs either left or right keys
while not end_game:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:
			x = player_pos[0]
			y = player_pos[1]

			if event.key == pygame.K_LEFT:
				x -= player_box
			elif event.key == pygame.K_RIGHT:
				x += player_box

			player_pos = [x,y]
	screen.fill(BACKGROUND_COLOR)

    #Incoming enemy boxes
	drop_enemies(enemy_list)
	score = update_enemy_positions(enemy_list, score)
	speed = set_level(score, speed)

    #displays score
	text = "Score:" + str(score)
	label = myFont.render(text, 1,black)
	screen.blit(label, (width-200, height-740))

	if collision_check(enemy_list, player_pos):
		end_game = True
		break

	draw_enemies(enemy_list)

	pygame.draw.rect(screen, Pink, (player_pos[0], player_pos[1], player_box, player_box))

	clock.tick(40)

	pygame.display.update()
