import pygame
import math
import os
import random

class Event:
	def __init__(self, type, key, x, y):
		self.type = type
		self.key = key
		self.x = x
		self.y = y
