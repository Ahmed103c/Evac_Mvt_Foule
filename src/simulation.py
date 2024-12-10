import pygame
import pymunk
import time
from random import randint
from ball import Ball
from utils import create_segment

def simulate(Nombre_Ball):
    pygame.init()
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    space = pymunk.Space()
    WHITE = (255, 255, 255)
    target_point = (WIDTH + 100, HEIGHT / 2)
    positions = set()
    balls = []
    while len(balls) < Nombre_Ball:
        position = (randint(10, 400), randint(10, 550))
        if position not in positions:
            positions.add(position)
            balls.append(Ball(position, 8, space, screen))

    balls_2 = balls.copy()
    create_segment((500, 0), (500, 270), 15, space)
    create_segment((500, 330), (500, 600), 15, space)
    Temps_Sortie_chaque_boule = []
    running = True
    start_time = time.time()
    last_ball = None  # Initialisation de la variable pour stocker la dernière boule
    s = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(WHITE)
        # pygame.draw.circle(screen,(0,255,0),target_point,5)
        for ball in balls:
            ball.update(balls, target_point, s)
            ball.draw()
            # Vérification du passage de chaque boule à travers la ligne
            if ball.body.position.x > 500 and ball in balls_2:
                s += 1
                balls_2.remove(ball)
                middle_time = time.time()
                Temps_Sortie_chaque_boule.append(middle_time - start_time)
                if s == Nombre_Ball:
                    last_ball = ball  # Mettre à jour la dernière boule
        pygame.draw.line(screen, (0, 0, 0), (500, 0), (500, 270), 15)
        pygame.draw.line(screen, (0, 0, 0), (500, 330), (500, 600), 15)
        pygame.display.flip()
        clock.tick(100)
        space.step(1 / 100)
        # Vérification si la dernière boule a passé la ligne
        if last_ball and not last_ball.passed_line:
            last_ball.passed_line = True
            running = False

    pygame.quit()
    return Temps_Sortie_chaque_boule