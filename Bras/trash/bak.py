import numpy as np
import pygame
import math

# Paramètres du bras robotique
L1 = 100  # Longueur du premier maillon
L2 = 100  # Longueur du deuxième maillon
L3 = 100  # Longueur du troisième maillon

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
theta1 = math.radians(45)
theta2 = math.radians(-45)
theta3 = math.radians(30)  # Nouvel angle pour le troisième maillon

base_x = width // 2
base_y = height

# Position cible
target_x = 300
target_y = 300

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    J = np.array([[-L1 * math.sin(theta1) - L2 * math.sin(theta1 + theta2) - L3 * math.sin(theta1 + theta2 + theta3),
                   -L2 * math.sin(theta1 + theta2) - L3 * math.sin(theta1 + theta2 + theta3),
                   -L3 * math.sin(theta1 + theta2 + theta3)],
                  [L1 * math.cos(theta1) + L2 * math.cos(theta1 + theta2) + L3 * math.cos(theta1 + theta2 + theta3),
                   L2 * math.cos(theta1 + theta2) + L3 * math.cos(theta1 + theta2 + theta3),
                   L3 * math.cos(theta1 + theta2 + theta3)]])

    # Calcul de l'erreur de position
    target_rel_x = target_x - base_x
    target_rel_y = base_y - target_y
    error_x = target_rel_x - (L1 * math.cos(theta1) + L2 * math.cos(theta1 + theta2) + L3 * math.cos(theta1 + theta2 + theta3))
    error_y = target_rel_y - (L1 * math.sin(theta1) + L2 * math.sin(theta1 + theta2) + L3 * math.sin(theta1 + theta2 + theta3))
    error = np.array([error_x, error_y])

    # Calcul de la pseudo-inverse de la jacobienne
    J_pseudo_inv = np.linalg.pinv(J)

    # Calcul de la commande de vitesse
    delta_theta = np.dot(J_pseudo_inv, error)

    # Mise à jour des angles
    theta1 += delta_theta[0]
    theta2 += delta_theta[1]
    theta3 += delta_theta[2]

    # Effacer l'écran
    screen.fill(WHITE)

    # Dessiner le bras robotique
    arm_x = [base_x,
             base_x + L1 * math.cos(theta1),
             base_x + L1 * math.cos(theta1) + L2 * math.cos(theta1 + theta2),
             base_x + L1 * math.cos(theta1) + L2 * math.cos(theta1 + theta2) + L3 * math.cos(theta1 + theta2 + theta3)]
    arm_y = [base_y,
             base_y - L1 * math.sin(theta1),
             base_y - L1 * math.sin(theta1) - L2 * math.sin(theta1 + theta2),
             base_y - L1 * math.sin(theta1) - L2 * math.sin(theta1 + theta2) - L3 * math.sin(theta1 + theta2 + theta3)]
    pygame.draw.lines(screen, RED, False, list(zip(arm_x, arm_y)), 5)

    # Dessiner la cible
    pygame.draw.circle(screen, BLACK, (target_x, target_y), 10)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
