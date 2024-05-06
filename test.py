import pygame
import sys

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Cercle qui suit la souris")

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Position initiale du cercle
x_cercle, y_cercle = largeur // 2, hauteur // 2
rayon_cercle = 20

# Boucle principale
while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Mise à jour de la position du cercle en fonction de la souris
    x_souris, y_souris = pygame.mouse.get_pos()
    x_cercle, y_cercle = x_souris, y_souris

    # Effacement de l'écran
    fenetre.fill(blanc)

    # Dessin du cercle
    pygame.draw.circle(fenetre, noir, (x_cercle, y_cercle), rayon_cercle)

    # Rafraîchissement de l'écran
    pygame.display.flip()

# Nettoyage et fermeture
pygame.quit()
sys.exit()
