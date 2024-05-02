import math
import numpy as np 

def get_distance(p1, p2):
        return np.linalg.norm(p2 - p1)

def get_positions(angles, lengths):
    angles = [math.radians(val) for val in angles]  # Convert angles to radians
    positions = [[0, 0]]  # Initialize with the origin
    prev_angle = 0
    for i in range(len(angles)):
        prev_angle += angles[i]
        x = positions[-1][0] + lengths[i] * math.cos(prev_angle)
        y = positions[-1][1] + lengths[i] * math.sin(prev_angle)
        positions.append([x, y])
    return positions
            
def get_angles(joints_positions):
    angles = [math.atan2(joints_positions[1][1], joints_positions[1][0])]
    prev_angle: float = angles[0]
    for i in range(2, len(joints_positions)):
        p = joints_positions[i] - joints_positions[i - 1]
        abs_angle: float = math.atan2(p[1], p[0])
        angles.append(abs_angle - prev_angle)
        prev_angle = abs_angle
    return [math.degrees(val) for val in angles]

class Robot:

    def __init__(self, joints_positions=[], angles=[], lengths=[]):
        if joints_positions : #Si on commence avec des positions
            if len(joints_positions) == 1 : 
                raise ValueError("Votre robot...n'a qu'une jointure.")
            self.joints_positions = joints_positions
            self.lengths = []
            for i in range(len(self.joints_positions)-1):
                self.lengths.append(get_distance(joints_positions[i], joints_positions[i+1]))
            self.angles = get_angles(joints_positions)
        elif (angles.size != 0 and lengths.size != 0) : # Si on a des angles, des longueurs et une base
            self.angles = angles
            self.lengths = lengths
            self.joints_positions = get_positions(angles, lengths)
        else : 
            raise ValueError("Vos arguments ne sont pas corrects.")

    def can_reach(self, target):
        return sum(self.lengths) >= get_distance(self.joints_positions[0], target)

    def fabrik(self, target, max_iterations, tolerance):

        if self.can_reach(target):
            iterations = 0
            initial_position = self.joints_positions[0]
            while iterations<max_iterations and get_distance(self.joints_positions[-1], target)>=tolerance:
                iterations+=1
                #Forward Reaching
                self.joints_positions[-1] = target
                last = len(self.joints_positions)-1
                for i in reversed(range(0, last)):
                    next, current = self.joints_positions[i+1], self.joints_positions[i]
                    len_share = self.lengths[i] / get_distance(current, next)
                    self.joints_positions[i] = (1 - len_share) * next + len_share * current
                
                #Backward Reaching
                self.joints_positions[0] = initial_position
                for i in range(0, last):
                    next, current = self.joints_positions[i + 1], self.joints_positions[i]
                    len_share = self.lengths[i] / get_distance(current, next)
                    self.joints_positions[i + 1] = (1 - len_share) * current + len_share * next
            self.angles = get_angles(self.joints_positions)
            return iterations
        return False

    def pseudo_jabobian_inverse(self, target, max_iterations, tolerance):

        def forward_kinematics(lengths, angles):
            x = np.sum(lengths * np.cos(np.cumsum(angles)))
            y = np.sum(lengths * np.sin(np.cumsum(angles)))
            return np.array([x, y])
        
        def jacobian(lengths, angles):
            J = np.zeros((2, len(lengths)))
            for i in range(len(lengths)):
                J[0, i] = -np.sum(lengths[i:] * np.sin(np.cumsum(angles[i:])))
                J[1, i] = np.sum(lengths[i:] * np.cos(np.cumsum(angles[i:])))
            return J
        
        def pseudo_inverse(J):
            return np.linalg.inv(J.T.dot(J) + np.eye(J.shape[1]) * 1e-3).dot(J.T)
        iterations = 0
        while iterations<=max_iterations and np.linalg.norm(target - forward_kinematics(self.lengths, self.angles)) > tolerance:
            J = jacobian(self.lengths, self.angles)
            d_theta = pseudo_inverse(J).dot(target - forward_kinematics(self.lengths, self.angles))
            self.angles += d_theta
            iterations+=1
        self.angles = np.degrees(self.angles) % 360
        self.angles = (self.angles + 180) % 360 - 180
        self.joints_positions = get_positions(self.angles, self.lengths)



"""
vectors_test = [np.array([0, 0]),np.array([10, 0]),np.array([20, 0]), np.array([30, 0])] 
fab = Robot(joints_positions=vectors_test)
fab.fabrik(np.array([0, 20]), 10000, 0.01)
print(fab.angles)
print(fab.joints_positions)
print()
"""

"""
lengths = np.array([100, 100])
angles = np.array([float(135),float(-45)])
fab = Robot(lengths=lengths, angles=angles)
fab.pseudo_jabobian_inverse(np.array([0, 200]), 10000, 0.01)
print(fab.angles)
print(fab.joints_positions)
"""