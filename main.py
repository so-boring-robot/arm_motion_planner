import numpy as np
from robot_arm import Robot
import pygame
import sys

def draw_arm(fenetre, jointures):
    # Couleur du bras
    couleur_bras = (255, 0, 0)  # Rouge
    couleur_jointure = (255, 255, 255)  # Rouge

        # Dessiner le bras robotique
    for i in range(len(jointures)):
        pygame.draw.circle(fenetre, couleur_jointure, jointures[i], 5)
    for i in range(len(jointures) - 1):
        pygame.draw.line(fenetre, couleur_bras, jointures[i], jointures[i + 1], 5)

def transform_coordinates(coordinates):
    return [(x + largeur_fenetre // 2, - y + hauteur_fenetre) for x, y in coordinates]

def inverse_transform_coordinates(transformed_coordinates):
    return [(x - largeur_fenetre // 2, - (y - hauteur_fenetre)) for x, y in transformed_coordinates]

"""
fab = Robot(joints_positions=vectors_test)
fab.fabrik(np.array([0, 20]), 10000, 0.01)
print(fab.angles)
print(fab.joints_positions)
print()
"""


# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
largeur_fenetre = 800
hauteur_fenetre = 600
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
clock = pygame.time.Clock()

"""
coords = [np.array([0, 0]), np.array([-70.71067811865474, 70.71067811865476]), np.array([-70.71067811865474, 150.71067811865476]), np.array([-10.71067811865474, 150.71067811865476])]
fab = Robot(joints_positions=coords)
coords = fab.fabrik(np.array([0, 200]), 10000, 0.01) 
coord_bras = transform_coordinates(fab.joints_positions)
"""
lengths = np.array([100, 80, 60])
angles = np.array([float(135),float(-45),float(-90)])
fab = Robot(lengths=lengths, angles=angles)



target = None
# Boucle principale
while True:

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Bouton gauche de la souris
                    target_pos = pygame.mouse.get_pos()
                    target = np.array([float(target_pos[0]), float(target_pos[1])])
                    print(np.array(target))

    # Effacer l'écran
    fenetre.fill((0, 0, 0))
    if target is not None:
        print(target)
        fab.pseudo_jabobian_inverse(inverse_transform_coordinates(target), 10000, 0.01)
        target = None

    draw_arm(fenetre, transform_coordinates(fab.joints_positions))
    
    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(60)

