import pygame
import numpy as np
import math
import node

class RobotArm:
    def __init__(self, base, lengths):
        self.base = base
        self.arm_length = lengths
        self.joint_angles = np.zeros(len(lengths))
        self.joint_positions = [base]
        #self.joint_positions[:, 0] = np.cumsum([WIDTH // 2] + lengths)
        #self.joint_positions[:, 1] = HEIGHT

    def initiate(self):
        self.joint_angles = [135,-45,-90]
        for i in range(len(self.arm_length)):
            angle = math.radians(sum(self.joint_angles[:i+1]))
            x = self.joint_positions[i].x + self.arm_length[i] * math.cos(angle)
            y = self.joint_positions[i].y - self.arm_length[i] * math.sin(angle)
            self.joint_positions.append(node.Node(x, y))
            


    def update_joint_positions(self):
        # Mise à jour des positions des joints en fonction des angles
        for i in range(1, len(self.arm_length) + 1):
            angle = np.sum(self.joint_angles[:i])
            x = self.joint_positions[i - 1].x + self.arm_length[i - 1] * np.cos(angle)
            y = self.joint_positions[i - 1].y + self.arm_length[i - 1] * np.sin(angle)
            self.joint_positions[i] = node.Node(x, y)

    def draw_arm(self):
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)

        pygame.draw.circle(window, RED, self.joint_positions[0].getCoordinate(), 8)
        for i in range(len(self.arm_length)):
            pygame.draw.line(window, WHITE, self.joint_positions[i].getCoordinate(), self.joint_positions[i + 1].getCoordinate(), 5)
            pygame.draw.circle(window, BLUE, self.joint_positions[i + 1].getCoordinate(), 8)

    def move_towards_target(self, target_pos, num_iterations, num_samples, learning_rate, noise_scale):
        initial_trajectory = np.copy(self.joint_angles)
        target_trajectory = np.zeros(len(self.arm_length))

        for i in range(num_iterations):
            current_trajectory = np.copy(self.joint_angles)

            # Génération de trajectoires échantillonnées autour de la trajectoire courante
            sampled_trajectories = []
            for _ in range(num_samples):
                noise = np.random.normal(scale=noise_scale, size=len(self.arm_length))
                sampled_trajectory = current_trajectory + noise
                sampled_trajectories.append(sampled_trajectory)

            # Calcul de l'évaluation de chaque trajectoire échantillonnée
            costs = []
            for trajectory in sampled_trajectories:
                self.joint_angles = trajectory
                self.update_joint_positions()
                cost = np.linalg.norm(self.joint_positions[-1].getCoordinate() - target_pos)
                costs.append(cost)

            # Calcul des poids des trajectoires échantillonnées
            weights = np.exp(-np.array(costs))
            if np.sum(weights) != 0:
                weights /= np.sum(weights)


            # Mise à jour de la trajectoire courante en utilisant les poids et les trajectoires échantillonnées
            update = np.zeros(len(self.arm_length))
            for j, trajectory in enumerate(sampled_trajectories):
                update += weights[j] * (trajectory - current_trajectory)
            self.joint_angles += learning_rate * update

            self.update_joint_positions()


    def compute_jacobian(self, end_effector_pos):
        jacobian = np.zeros((2, len(self.arm_length)))

        for i in range(len(self.arm_length)):
            segment_vector = np.array(self.joint_positions[-1].getCoordinate()) - np.array(self.joint_positions[i].getCoordinate())
            jacobian[:, i] = np.array([-segment_vector[1], segment_vector[0]])

        return jacobian

    def move_arm(self, target_pos):
        max_iterations = 100
        epsilon = 1e-5

        for _ in range(max_iterations):
            self.update_joint_positions()
            end_effector_pos = np.array(self.joint_positions[-1].getCoordinate())

            distance = np.linalg.norm(end_effector_pos - target_pos)
            if distance < epsilon:
                break

            jacobian = self.compute_jacobian(end_effector_pos)
            pseudo_inverse = np.linalg.pinv(jacobian)
            delta_angles = np.dot(pseudo_inverse, target_pos - end_effector_pos)

            self.joint_angles += delta_angles

        self.update_joint_positions()


if __name__ == "__main__":
    # Création du bras mécanique
    # Longueurs des segments du bras
    ARM_LENGTHS = [100, 80, 60]
    
    # Dimensions de la fenêtre
    WIDTH, HEIGHT = sum(ARM_LENGTHS)*2, sum(ARM_LENGTHS)

    # Initialisation de Pygame
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulation de bras mécanique avec STOMP")

    clock = pygame.time.Clock()

    # Position de la cible
    target_pos = None
    robot_arm = RobotArm(node.Node(WIDTH//2, HEIGHT), ARM_LENGTHS)
    robot_arm.initiate()

    # Boucle principale
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Bouton gauche de la souris
                    target_pos = pygame.mouse.get_pos()

        # Dessiner la cible
        if target_pos is not None:
            if math.dist(target_pos, robot_arm.joint_positions[0].getCoordinate()) <= sum(ARM_LENGTHS):
                robot_arm.move_arm(target_pos)
            GREEN = (0,255,0)
            pygame.draw.circle(window, GREEN, target_pos, 8)

        # Effacer l'écran
        BLACK = (0, 0, 0)
        window.fill(BLACK)

        # Dessiner le bras mécanique
        robot_arm.draw_arm()

        

        # Rafraîchir l'écran
        pygame.display.flip()
        clock.tick(60)

    # Quitter Pygame
    pygame.quit()
