import random
import math
import pygame

""" 
RRT a besoin de plusieurs informations : 
	- La taille de la fenêtre
	- La distance max séparant les nodes
	- la node initiale
	- la node finale
"""

class Node:
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.neightbors = []
	
	def getCoordinate(self):
		return (self.x, self.y)

	def toString(self):
		print(f"({x},{y})")

	def draw(self, color):
		pygame.draw.circle(screen, color, (self.x, self.y), 10)
		for neightbor in self.neightbors:
			pygame.draw.line(screen, color, (self.x, self.y), (neightbor.x, neightbor.y), 10)



width = 800
height = 800

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


base_bras = Node(400, 600)
target = Node(100,100)

# Se remplira avec la stereovision, ça pourrait par ailleur êtrbien de faire un système de mapping pour limiter les recherches, sinon, faire une recherche sur toute l'image est couteux en terme de calcul 
obstacles = [Node(500,300)]


def inObstacle(node, obstacles):
	inObstacle = False
	for obstacle in obstacles:
		if obstacle.x==node[0] and obstacle.y==node[1]:
			inObstacle = True
			break
	return inObstacle

def isInLine(startPoint, endPoint, obstacles): #start = point le plus proche, end = point à atteindre
	for obstacle in obstacles: 
		if (startPoint.x - endPoint.x) * (endPoint.y - obstacle.y) != (endPoint.y - obstacle.x) * (startPoint.y - endPoint.y): 
			return False 
	return True 


"""
Il faut également un tableau pouvant stocker les différentes nodes afin de pouvoir facilement comparer leurs distances
"""
nodes = [base_bras]

path_exist = False

running = True


while running or not path_exist:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	screen.fill("purple")
	if not path_exist:
		nb_points = 300
		for i in range(nb_points):
			
			# Dans un premier temps, il faut générer un x et y random comprit respectivement entre 0 et width/height
			x = random.randint(0, width)
			y = random.randint(0, height)
		    
			# Il faut s'assurer que ce point ne se trouve pas sur un obstacle
			if inObstacle((x,y), obstacles):
				i-=1
				continue
			else: #Si il n'y a pas d'obstacle, on ajoute la node à la liste des nodes
				nodes.append(Node(x,y))

		nodes.append(target)

		#Il faut maintenant trouver les voisins de chaque nodes

		searchArea = 90 # rayon de recherche de 50 px

		for start in nodes:
			for search in nodes:
				if((search.x<=start.x+searchArea and search.x>=start.x-searchArea) and (search.y<=start.y+searchArea and search.y>=start.y-searchArea)) :
					isInLine(start, search, obstacles)
					start.neightbors.append(search)
		path_exist = True

	for node in nodes:
		node.draw((255,0,0))

	for obstacle in obstacles:
		obstacle.draw((0,255,0))

	
	
	pygame.display.update()
	clock.tick(60)  # limits FPS to 60

	

pygame.quit()