FOREGROUND = (0, 0, 100)
BACKGROUND = (200, 200, 230)

import pygame
import os

def main():
	pygame.init()
	pygame.display.set_mode((100, 100))
	original = pygame.image.load('raw.png').convert()
	original.set_colorkey((0, 0, 0))
	fg = pygame.Surface(original.get_size()).convert()
	fg.fill(FOREGROUND)
	fg.blit(original, (0, 0))
	fg.set_colorkey((255, 255, 255))
	height = fg.get_height()
	c = open('widths.txt', 'rt')
	lines = c.read().split('\n')
	x = 0
	for line in lines:
		parts = line.strip().split('\t')
		if len(parts) > 1:
			key = parts[0]
			width = int(parts[1])
			
			img = pygame.Surface((width, height)).convert()
			img.fill(BACKGROUND)
			img.blit(fg, (-x, 0))
			pygame.image.save(img, 'output' + os.sep + key + '.png')
			
			x += width + 1
			


main()