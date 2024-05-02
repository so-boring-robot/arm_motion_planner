import pygame

class Node:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.previous = None
		
	def getCoordinate(self):
		return (self.x, self.y)
	
	def toString(self):
		print(f"({self.x}, {self.y})")
		
	def draw(self, screen, color):
		pygame.draw.circle(screen, color, (round(self.x), round(self.y)), 8)
