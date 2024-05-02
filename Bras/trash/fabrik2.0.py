import pygame
import math



# Dimensions de la fenêtre
WIDTH, HEIGHT = 640, 480

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialisation de Pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation de bras mécanique avec FABRIK")

clock = pygame.time.Clock()

# Longueurs des segments du bras
ARM_LENGTH = 50

# Positions initiales des jointures du bras
joint_positions = [(WIDTH // 2, HEIGHT // 2),
                   (WIDTH // 2 + ARM_LENGTH, HEIGHT // 2),
                   (WIDTH // 2 + ARM_LENGTH * 2, HEIGHT // 2),
                   (WIDTH // 2 + ARM_LENGTH * 3, HEIGHT // 2)]

# Position de la cible
target_pos = None


# Fonction pour dessiner le bras
def draw_arm(joint_positions):
    pygame.draw.circle(window, RED, joint_positions[0], 8)
    for i in range(len(joint_positions) - 1):
        pygame.draw.line(window, WHITE, joint_positions[i], joint_positions[i+1], 5)
        pygame.draw.circle(window, BLUE, joint_positions[i+1], 8)

# Fonction pour dessiner la cible
def draw_target(target_pos):
    pygame.draw.circle(window, GREEN, target_pos, 8)

# Algorithme FABRIK
def fabrik(target_pos, joint_positions):
    epsilon = 1e-5
    max_iterations = 100

    link_lengths = [math.hypot(joint_positions[i][0] - joint_positions[i+1][0],
                               joint_positions[i][1] - joint_positions[i+1][1])
                    for i in range(len(joint_positions) - 1)]

    distance = math.hypot(joint_positions[-1][0] - target_pos[0], joint_positions[-1][1] - target_pos[1])

    if distance <= sum(link_lengths):
        for _ in range(max_iterations):
            # Forward reaching
            joint_positions[-1] = target_pos
            for i in range(len(joint_positions) - 2, -1, -1):
                current_length = math.hypot(joint_positions[i+1][0] - joint_positions[i][0],
                                            joint_positions[i+1][1] - joint_positions[i][1])
                lambda_val = link_lengths[i] / current_length
                joint_positions[i] = ((1 - lambda_val) * joint_positions[i+1][0] + lambda_val * joint_positions[i][0],
                                      (1 - lambda_val) * joint_positions[i+1][1] + lambda_val * joint_positions[i][1])

            # Backward reaching
            joint_positions[0] = (WIDTH // 2, HEIGHT // 2)
            for i in range(len(joint_positions) - 1):
                current_length = math.hypot(joint_positions[i+1][0] - joint_positions[i][0],
                                            joint_positions[i+1][1] - joint_positions[i][1])
                lambda_val = link_lengths[i] / current_length
                joint_positions[i+1] = ((1 - lambda_val) * joint_positions[i][0] + lambda_val * joint_positions[i+1][0],
                                        (1 - lambda_val) * joint_positions[i][1] + lambda_val * joint_positions[i+1][1])

            distance = math.hypot(joint_positions[-1][0] - target_pos[0], joint_positions[-1][1] - target_pos[1])

            if distance < epsilon:
                break

    return joint_positions

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Bouton gauche de la souris
                if target_pos is None:
                    target_pos = pygame.mouse.get_pos()
                else:
                    target_pos = pygame.mouse.get_pos()
        
    # Effacer l'écran
    window.fill(BLACK)

    # Si une cible est présente, appliquer l'algorithme FABRIK pour atteindre la cible
    if target_pos is not None:
        joint_positions = fabrik(target_pos, joint_positions)

    # Dessiner le bras
    draw_arm(joint_positions)

    # Dessiner la cible
    if target_pos is not None:
        draw_target(target_pos)

    # Rafraîchir l'écran
    pygame.display.flip()
    clock.tick(60)

# Quitter Pygame
pygame.quit()