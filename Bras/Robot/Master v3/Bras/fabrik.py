import pygame
import math
import node
import screen

class RobotArm:

    def __init__(self, base, arm_length):
        self.base = base
        self.arm_length = arm_length #Liste d'entier
        # Positions initiales des jointures du bras
        self.joint_positions = [node.Node(base.x, base.y)]
        self.angles = None

        #self.joint_positions = joint_positions #Liste de node


    #Position initiale du robot
    def initiate(self):
        self.angles = [135,-45,-90]

        self.angle_limits = [(-135, -20), (-90, 0), (-90, 60)]  # Exemple de limites d'angle en degrés pour chaque articulation
        
        
        for i in range(len(self.arm_length)):
            angle = math.radians(sum(self.angles[:i+1]))
            x = self.joint_positions[i].x + self.arm_length[i] * math.cos(angle)
            y = self.joint_positions[i].y - self.arm_length[i] * math.sin(angle)
            self.joint_positions.append(node.Node(x,y))
        """

        self.joint_positions = [node.Node(300, 300),
                                node.Node(216, 245),
                                node.Node(240, 148),
                                node.Node(340, 148)
                                ]
        
        self.joint_positions = [Node(self.screen.width // 2, self.screen.height),
                   Node(self.screen.width // 2 + self.arm_length[0], self.screen.height),
                   Node(self.screen.width // 2 + self.arm_length[1] + self.arm_length[0], self.screen.height),
                   Node(self.screen.width // 2 + self.arm_length[2] + self.arm_length[1] + self.arm_length[0], self.screen.height)]
        """

    # Algorithme FABRIK
    def move_arm(self, target):
        epsilon = 1e-5
        max_iterations = 100

        link_lengths = [math.hypot(self.joint_positions[i].x - self.joint_positions[i+1].x,
                                self.joint_positions[i].y - self.joint_positions[i+1].y)
                        for i in range(len(self.joint_positions) - 1)]

        distance = math.hypot(self.joint_positions[-1].x - target.x, self.joint_positions[-1].y - target.y)

        if distance <= sum(link_lengths):
            for _ in range(max_iterations):
                # Forward reaching
                self.joint_positions[-1] = target
                for i in range(len(self.joint_positions) - 2, -1, -1):
                    current_length = math.hypot(self.joint_positions[i+1].x - self.joint_positions[i].x,
                                                self.joint_positions[i+1].y - self.joint_positions[i].y)
                    lambda_val = link_lengths[i] / current_length
                    self.joint_positions[i] = node.Node((1 - lambda_val) * self.joint_positions[i+1].x + lambda_val * self.joint_positions[i].x,
                                        (1 - lambda_val) * self.joint_positions[i+1].y + lambda_val * self.joint_positions[i].y)
                    
                # Backward reaching
                self.joint_positions[0] = node.Node(self.base.x, self.base.y)
                for i in range(len(self.joint_positions) - 1):
                    current_length = math.hypot(self.joint_positions[i+1].x - self.joint_positions[i].x,
                                                self.joint_positions[i+1].y - self.joint_positions[i].y)
                    lambda_val = link_lengths[i] / current_length
                    self.joint_positions[i+1] = node.Node((1 - lambda_val) * self.joint_positions[i].x + lambda_val * self.joint_positions[i+1].x,
                                            (1 - lambda_val) * self.joint_positions[i].y + lambda_val * self.joint_positions[i+1].y)

                # Apply angle constraints
                for i in range(len(self.angles)):
                    min_angle, max_angle = self.angle_limits[i]
                    current_angle = math.degrees(math.atan2(self.joint_positions[i + 1].y - self.joint_positions[i].y,
                                                            self.joint_positions[i + 1].x - self.joint_positions[i].x))
                    if current_angle < min_angle:
                        current_angle = min_angle
                    elif current_angle > max_angle:
                        current_angle = max_angle

                    # Update joint positions based on the adjusted angle
                    self.joint_positions[i + 1] = node.Node(
                        self.joint_positions[i].x + self.arm_length[i] * math.cos(math.radians(current_angle)),
                        self.joint_positions[i].y + self.arm_length[i] * math.sin(math.radians(current_angle)))

                distance = math.hypot(self.joint_positions[-1].x - target.x, self.joint_positions[-1].y - target.y)

                if distance < epsilon:
                    break

    # Fonction pour dessiner le bras
    def draw_arm(self, screen):
        self.joint_positions[0].draw(screen, (255,0,0))
        for i in range(len(self.joint_positions) - 1):
            pygame.draw.line(screen, (255,255,255), self.joint_positions[i].getCoordinate(), self.joint_positions[i+1].getCoordinate(), 5)
            self.joint_positions[i+1].draw(screen, (0, 0, 255))


    # Récupérer les angles des jointures
    def getAngles(self):
        return 0



if __name__ == '__main__':

    # Dimensions de la fenêtre
    WIDTH, HEIGHT = 640, 480

    # Initialisation de Pygame
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulation de bras mécanique avec FABRIK")

    clock = pygame.time.Clock()

    # Longueurs des segments du bras
    ARM_LENGTH = [100, 100, 100]
    robot_arm = RobotArm(node.Node(WIDTH//2,HEIGHT), ARM_LENGTH)
    robot_arm.initiate()

    # Position de la cible
    target = None

    # Boucle principale du jeu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Bouton gauche de la souris
                    target_pos = pygame.mouse.get_pos()
                    target = node.Node(target_pos[0], target_pos[1])
            
        # Effacer l'écran
        window.fill((0,0,0))


        # Si une cible est présente, appliquer l'algorithme FABRIK pour atteindre la cible
        if target is not None:
            robot_arm.move_arm(target)

        # Dessiner le bras
        robot_arm.draw_arm(window)

        # Dessiner la cible
        if target is not None:
            target.draw(window, (0, 255, 0))

        # Rafraîchir l'écran
        pygame.display.flip()
        clock.tick(60)

    # Quitter Pygame
    pygame.quit()