import rrt
import fabrik
import jacobian
import stomp
import pygame
import random
import math
import screen
import node
import time


# Dimension du robot
ARM_LENGTH = [100, 100, 100]


# Dimensions de la fenêtre
WIDTH, HEIGHT = sum(ARM_LENGTH)*2, sum(ARM_LENGTH)

move = 2
# Initialisation de Pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation de bras mécanique avec FABRIK")
clock = pygame.time.Clock()

fenetre = screen.Screen(WIDTH,HEIGHT)

base = node.Node(WIDTH//2, HEIGHT)

if(move == 1):
    robot_arm = fabrik.RobotArm(base, ARM_LENGTH)
elif(move == 2):
    robot_arm = jacobian.RobotArm(base, ARM_LENGTH)
else:
    robot_arm = jacobian.RobotArm(base, ARM_LENGTH)

robot_arm.initiate()

# Position de la cible
target = None

# Boucle principale du jeu
running = True
while running:
    
    # Effacer l'écran
    window.fill((0,0,0))

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Bouton gauche de la souris
                target_pos = pygame.mouse.get_pos()
                target = node.Node(target_pos[0], target_pos[1])
        
    # Dessiner la cible
    if target is not None:
        target.draw(window, (0, 255, 0))


    # Si une cible est présente, appliquer l'algorithme FABRIK pour atteindre la cible. Avant de l'appliquer, il faut subdiviser cette cible pour éviter les obstacles
    # On créé un écran propre à RRT commençant à la caméra et finissant à la longueur max du bras

    if target is not None:
        first_point = robot_arm.joint_positions[len(robot_arm.joint_positions)-1]
        startPoint = node.Node(round(first_point.x), round(first_point.y))
        rrt_for_target = rrt.RRT(fenetre, startPoint, target, [], 50)
        rrt_for_target.surface_forbidden = (startPoint.x, 0)
        havePath = rrt_for_target.execute(window)
        print("=========================")
        if havePath:
                
            for path in reversed(rrt_for_target.path):
                if path is not None:
                    print(path.getCoordinate())
                    #print(math.dist(robot_arm.joint_positions[len(robot_arm.joint_positions)-1].getCoordinate(), path.getCoordinate()))
                    robot_arm.move_arm(path)
                    robot_arm.draw_arm(window)
                    pygame.display.update()

                time.sleep(1)
            print("++++++++++++++++++")
        target = None
        
        robot_arm.joint_positions[len(robot_arm.joint_positions)-1].x = round(robot_arm.joint_positions[len(robot_arm.joint_positions)-1].x)
        robot_arm.joint_positions[len(robot_arm.joint_positions)-1].y = round(robot_arm.joint_positions[len(robot_arm.joint_positions)-1].y)
            
    # Dessiner le bras
    robot_arm.draw_arm(window)

    
    # Rafraîchir l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()


"""
screen = fabrik.Screen(800,800)
start = rrt.Node(400, 600)
end = rrt.Node(100,100)
obstacles = [rrt.Node(500,300)]

rrt = rrt.RRT(screen, start, end, obstacles, 100)


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
	
"""