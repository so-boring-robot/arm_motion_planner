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
		self.previous = None
		
	def getCoordinate(self):
		return (self.x, self.y)
	
	def __str__(self):
		print(f"({self.x}, {self.y})")

class Screen:
      
    def __init__(self, width, height):
        self.width = width
        self.height = height
		
    def getScreen(self):
        return (self.width, self.height)


class RRT:

    def __init__(self, screen, startPoint, endPoint, obstacles, max_distance):
          self.screen = screen
          self.startPoint = startPoint
          self.endPoint = endPoint
          self.obstacles = obstacles
          self.max_distance = max_distance
          self.surface_forbidden = (0,0)
          self.nodes = []
          self.path = []

    def getPathToTarget(self):
        if self.path[len(self.path)-1].previous==None:
            return
        if self.path[len(self.path)-1].previous.__str__() is not None:
            print(self.path[len(self.path)-1].previous.__str__())
        self.path.append(self.path[len(self.path)-1].previous)
        self.getPathToTarget()

    def nearestNode(self, current_target):
        nearest = self.nodes[0]
        for node in self.nodes:
            if math.dist(nearest.getCoordinate(), current_target.getCoordinate()) > math.dist(node.getCoordinate(), current_target.getCoordinate()):
                nearest = node
        return nearest
        
    def nearTarget(self, node):
        return (math.dist(node.getCoordinate(), self.endPoint.getCoordinate()) <= self.max_distance)

    # Savoir si un obstacle se trouve sur la trajectoire revient à savoir 3 points forment une ligne droite
    # https://www.tutorialspoint.com/program-to-check-whether-list-of-points-form-a-straight-line-or-not-in-python
    def isInLine(self, startPoint, endPoint): #start = point le plus proche, end = point à atteindre
        if len(self.obstacles)==0:
                return False
        for obstacle in self.obstacles: 
            if (startPoint.x - endPoint.x) * (endPoint.y - obstacle.y) != (endPoint.y - obstacle.x) * (startPoint.y - endPoint.y): 
                return False 
        return True 

    # https://math.stackexchange.com/questions/175896/finding-a-point-along-a-line-a-certain-distance-away-from-another-point/1630886#1630886
    def rapprochePoint(self, startPoint, endPoint):
        ratio = self.max_distance/math.dist(startPoint.getCoordinate(), endPoint.getCoordinate())
        x = round(((1-ratio)*startPoint.x+ratio*endPoint.x))
        y = round(((1-ratio)*startPoint.y+ratio*endPoint.y))
        
        new_node = Node(x,y)
        new_node.previous = startPoint
        return new_node
    
    def drawTree(self, color, screen):
        for node in self.nodes[1:]:
            pygame.draw.circle(screen, color, (node.x, node.y), 10)
            pygame.draw.line(screen, color, (node.x, node.y), (node.previous.x, node.previous.y), 10)
			
    def drawPath(self, color, screen):
        for node in self.path:
            if node.previous:
                pygame.draw.circle(screen, color, (node.x, node.y), 10)
                pygame.draw.line(screen, color, (node.x, node.y), (node.previous.x, node.previous.y), 10)
            else:
                pygame.draw.circle(screen, color, (node.x, node.y), 10)
    
    def execute(self, window):
        self.nodes = [self.startPoint]
        path_exist = False
        time_to_abandon = 10000

        while not path_exist and time_to_abandon>0:

            if not path_exist:
                # Dans un premier temps, il faut générer un x et y random comprit respectivement entre 0 et width/height
                x = round(random.randint(round(self.surface_forbidden[0]), self.screen.width))
                y = round(random.randint(round(self.surface_forbidden[1]), self.screen.height))
                new_node = Node(x,y)
                #new_node.__str__()
                
                # Il faut voir quelle node existante est la plus proche
                nearest = self.nearestNode(new_node)
                # Ensuite, il faut trouver un point proportionnel avec une distance convenable
                new_node_near = self.rapprochePoint(nearest, new_node)
                #new_node_near.__str__()
                # Il faut maintenant voir si il n'y a pas d'obstacle entre la node la plus proche et la nouvelle node
                inLine = self.isInLine(nearest, new_node_near)
                if(inLine):
                    continue
                
                self.drawTree((255,0,0), window)
                pygame.display.update()
                self.nodes.append(new_node_near)

                # Pour finir, il faut voir si un chemin existe entre la node courante et la node cible. Pour cela, on peut simplement voir si la dernière node ajouté se trouve aux alentours de la dernière node 			ajoutée, il faudra aussi vérifier qu'il n'y a pas d'obstacles entre ces 2 nodes
                if self.nearTarget(new_node_near):
                    if( not(self.isInLine(new_node_near, self.endPoint)) ):
                        self.endPoint.previous = new_node_near
                        self.nodes.append(self.endPoint)
                        path_exist = True
                        self.drawTree((255,0,0), window)
                        self.path = [self.nodes[len(self.nodes)-1]]
                        self.getPathToTarget()
                        self.drawPath((0,255,0), window)
                        pygame.display.update()
                        
            time_to_abandon -= 1

        return path_exist
        	



if __name__ == '__main__':
    screen = Screen(800,800)
    start = Node(340, 148)
    end = Node(518, 99)
    obstacles = [Node(0,0)]

    rrt = RRT(screen, start, end, obstacles, 100)
    rrt.surface_forbidden = (200, 0)

    pygame.init()
    screen = pygame.display.set_mode(rrt.screen.getScreen())
    clock = pygame.time.Clock()

    running = True



    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("purple")

        if not rrt.path:
            rrt.execute(screen)
                
    pygame.quit()

	

	
	
	
	
	
	
	
	
	
