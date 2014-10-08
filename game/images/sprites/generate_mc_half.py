import pygame
import os

pygame.init()
pygame.display.set_mode((100, 100))

for file in os.listdir('mc'):
	img = pygame.image.load('mc' + os.sep + file)
	width, height = img.get_size()
	half_img = pygame.transform.scale(img, (width // 2, height // 2))
	pygame.image.save(half_img, 'mc_half' + os.sep + file)