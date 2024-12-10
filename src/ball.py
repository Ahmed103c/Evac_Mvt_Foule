import math
import pymunk
import pygame

# Constantes globales pour le modèle
U = 70.0       # Coefficient d'interaction sociale
delta = 0.1    # Distance interpersonnelle
RED = (255, 0, 0)

class Ball:
    def __init__(self, position, radius, space, screen):
        self.radius = radius
        self.position = position
        self.velocity = (0, 0)
        mass = 1.0
        inertia = pymunk.moment_for_circle(mass, 0, self.radius)
        self.body = pymunk.Body(mass, inertia)
        self.body.position = self.position

        self.shape = pymunk.Circle(self.body, self.radius * 1.43)
        self.space = space
        self.space.add(self.body, self.shape)
        self.screen = screen
        self.passed_line = False

    def calculate_desired_velocity(self, target_point,s):
        diff_x = target_point[0] - self.position[0]
        diff_y = target_point[1] - self.position[1]
        distance = math.sqrt(diff_x**2 + diff_y**2)
        gradient_x = diff_x / distance 
        gradient_y = diff_y / distance *(s/10)
        return U * gradient_x, U * gradient_y


    def calculate_correction_velocity(self, balls):
        correction_velocity = (0, 0)
        for ball in balls:
            if ball != self:
                diff_x = ball.position[0] - self.position[0]
                diff_y = ball.position[1] - self.position[1]
                distance = math.sqrt(diff_x**2 + diff_y**2)
                direction_x = diff_x / distance
                direction_y = diff_y / distance
                direction = [direction_x, direction_y]
                # Calculer la correction de vitesse
                correction = [-U * math.exp(-distance / delta) * d for d in direction]
                correction_velocity = (
                    correction_velocity[0] + correction[0],
                    correction_velocity[1] + correction[1],
                )
        return correction_velocity

    def update(self, balls, target_point, s):
        desired_velocity = self.calculate_desired_velocity(target_point, s)
        correction_velocity = self.calculate_correction_velocity(balls)
        # Calculer la nouvelle vitesse en ajoutant la correction de vitesse
        new_velocity = (
            desired_velocity[0] + correction_velocity[0],
            desired_velocity[1] + correction_velocity[1],
        )
        self.body.velocity = new_velocity
        self.position = self.body.position

    def draw(self):
        pygame.draw.circle(self.screen, RED, (int(self.position[0]), int(self.position[1])), self.radius)
