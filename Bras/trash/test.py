import numpy as np
import pygame
import math

# Paramètres du bras robotique
angles = [math.radians(45), math.radians(-45), math.radians(45), math.radians(45)]
lengths = [80,80,80,80]
angle_limits = [(-90, 90), (-90, 90), (-90, 90), (-90, 90)]

# Vérification et ajustement des angles initiaux
for i in range(len(angles)):
    min_angle, max_angle = angle_limits[i]
    angles[i] = max(min(angles[i], max_angle), min_angle)

# Initialisation de Pygame
pygame.init()
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Position initiale du bras robotique
base_x = width // 2
base_y = height

# Position cible
target_x = 300
target_y = 300

def jacobian(angles, lengths):

    N = len(angles)

    matX = [0] * N
    line = [lengths[i] * math.sin(sum(angles[0:i+1])) for i in range(N)]              
    for i in range(N):
        matX[i] = -1 * sum(line)
        line = line[1:]
        
    matY = [0] * N
    line = [lengths[i] * math.cos(sum(angles[0:i+1])) for i in range(N)]                            
    for i in range(N):
        matY[i] = sum(line)
        line = line[1:]
    
    return np.array([matX, matY])

def pseudo_J_inv(angles, lengths):
    J = jacobian(angles, lengths)
    return np.linalg.pinv(J)

def calculateError(angles, lengths):
    # Calcul de l'erreur de position
    target_rel_x = target_x - base_x
    target_rel_y = base_y - target_y

    current = 0
    cumulX = 0
    cumulY = 0
    for i in range(len(angles)):
        current += angles[i]
        cumulX += lengths[i] * math.cos(current)
        cumulY += lengths[i] * math.sin(current)

    error_x = target_rel_x - cumulX
    error_y = target_rel_y - cumulY
    return np.array([error_x, error_y])

def move_arm(angles, lengths, base_x, base_y):
    pseudo_inv_J = pseudo_J_inv(angles, lengths)
    error = calculateError(angles, lengths)

    # Calcul de la commande de vitesse
    delta_theta = np.dot(pseudo_inv_J, error)

    
    # Mise à jour des angles
    for i in range(len(delta_theta)):
        new_angle = angles[i] + delta_theta[i]
        min_angle, max_angle = angle_limits[i]
        angles[i] = max(min(new_angle, max_angle), min_angle)

    arm_x = [base_x]
    arm_y = [base_y]

    current = 0
    cumulX = 0
    cumulY = 0
    for i in range(len(angles)):
        current += angles[i]
        cumulX += lengths[i] * math.cos(current)
        cumulY += lengths[i] * math.sin(current)
        arm_x.append(base_x+cumulX)
        arm_y.append(base_y-cumulY)

    return arm_x,arm_y

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    arm_x, arm_y = move_arm(angles, lengths, base_x, base_y)
    
    # Effacer l'écran
    screen.fill(WHITE)

    # Dessiner le bras robotique
    
    pygame.draw.lines(screen, RED, False, list(zip(arm_x, arm_y)), 5)

    # Dessiner la cible
    pygame.draw.circle(screen, BLACK, (target_x, target_y), 10)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
