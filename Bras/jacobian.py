import numpy as np
import pygame
import math
import node
import pandas as pd

import time

class RobotArm:

    def __init__(self, base, arm_length):
        self.base = base
        self.angles = None
        self.arm_length = arm_length #Liste d'entier
        self.joint_positions = [base]

        #self.joint_positions = joint_positions #Liste de node

    #Position initiale du robot
    def initiate(self):

        self.angles = [135,-45,-90]
        
        for i in range(len(self.arm_length)):
            angle = math.radians(sum(self.angles[:i+1]))
            x = self.joint_positions[i].x + self.arm_length[i] * math.cos(angle)
            y = self.joint_positions[i].y - self.arm_length[i] * math.sin(angle)
            self.joint_positions.append(node.Node(x,y))


    #Mettre à jour les points
    def update_angles(self, delta):
        angle_limits = [(0.5, 2.5), (-0.5, -2.5), (-100, 100)]
        for i in range(len(delta)):
            new_angle = self.angles[i] + delta[i]
            min_angle, max_angle = angle_limits[i]
            self.angles[i] = max(min(new_angle, max_angle), min_angle)
    
    def jacobian(self):
        N = len(self.angles)

        matX = [0] * N

        line = [self.arm_length[i] * math.sin(sum(self.angles[0:i+1])) for i in range(N)]              
        for i in range(N):
            matX[i] = -1 * sum(line)
            line = line[1:]
            
        matY = [0] * N
        line = [self.arm_length[i] * math.cos(sum(self.angles[0:i+1])) for i in range(N)]                            
        for i in range(N):
            matY[i] = sum(line)
            line = line[1:]
        
        return np.array([matX, matY])
    
    def pseudo_J_inv(self):
        J = self.jacobian()
        return np.linalg.pinv(J)

    def calculateError(self, target):
        # Calcul de l'erreur de position
        target_rel = node.Node(target.x - self.base.x, self.base.y - target.y)

        current = 0
        cumul = node.Node(0, 0)
        for i in range(len(self.angles)):
            current += self.angles[i]
            cumul.x += self.arm_length[i] * math.cos(current)
            cumul.y += self.arm_length[i] * math.sin(current)
        
        error_x = target_rel.x - cumul.x
        error_y = target_rel.y - cumul.y
        return np.array([error_x, error_y])

    def move_arm(self, target):
        max_iteration = 100

        for _ in range(max_iteration):
            pseudo_inv_J = self.pseudo_J_inv()
            error = self.calculateError(target)

            # Calcul de la commande de vitesse
            delta_theta = 0.1 * np.dot(pseudo_inv_J, error)

            
            self.update_angles(delta_theta)
            
            current = 0
            cumul = node.Node(0, 0)
            for i in range(len(self.angles)):
                current += self.angles[i]
                cumul.x += self.arm_length[i] * math.cos(current)
                cumul.y += self.arm_length[i] * math.sin(current)
                self.joint_positions[i+1] = node.Node((self.base.x+cumul.x),(self.base.y-cumul.y))

                    
    
    def draw_arm(self, screen):
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)

        # Dessiner le bras robotique
        self.joint_positions[0].draw(screen, RED)
        for i in range(len(self.joint_positions)-1):
            pygame.draw.line(screen, RED, self.joint_positions[i].getCoordinate(), self.joint_positions[i+1].getCoordinate(), 5)
            self.joint_positions[i+1].draw(screen, RED)

def calculer_angle_entre_points(point1, point2):
    # Calcule les différences en coordonnées x et y
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]

    # Utilise atan2 pour calculer l'angle en radians
    angle_radians = math.atan2(delta_y, delta_x)

    # Convertit l'angle en degrés si nécessaire
    angle_degres = math.degrees(angle_radians)

    return angle_degres


if __name__ == '__main__':
    # Initialisation de Pygame
    pygame.init()
    width, height = 600, 300
    window = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # Couleurs
    WHITE = (255, 255, 255)

    # Paramètres du bras robotique
    lengths = [100,100,100]
    base = node.Node((width // 2), height)
    robot_arm = RobotArm(base,lengths)
    robot_arm.initiate()

    # Position initiale du bras robotique

    # Position cible

    target = None

    dataset = []

    # Boucle principale
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                arr = np.asarray(dataset)
                np.savetxt('sample.csv',arr, fmt = '%d', delimiter=",")      
    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Bouton gauche de la souris
                    target_pos = pygame.mouse.get_pos()
                    target = node.Node(target_pos[0], target_pos[1])

        # Effacer l'écran
        window.fill(WHITE)



        if(target!=None):
            dataset.append([])
            for i in range(len(robot_arm.joint_positions)-1): 
                dataset[len(dataset)-1].append(round(calculer_angle_entre_points(robot_arm.joint_positions[i].getCoordinate(), robot_arm.joint_positions[i+1].getCoordinate())))  
            robot_arm.move_arm(target)
            dataset[len(dataset)-1].append(target.x)
            dataset[len(dataset)-1].append(target.y)
            for i in range(len(robot_arm.joint_positions)-1): 
                dataset[len(dataset)-1].append(round(calculer_angle_entre_points(robot_arm.joint_positions[i].getCoordinate(), robot_arm.joint_positions[i+1].getCoordinate())))  
            pygame.draw.circle(window, (255,255,255), target.getCoordinate(), 15)
            target = None

        robot_arm.draw_arm(window)


    
        pygame.display.flip()

    pygame.quit()
