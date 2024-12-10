import pygame
import pymunk
import math
from random import randint
import time

# Paramètres du modèle
U = 70.0       # Coefficient d'interaction sociale
delta = 0.1    # Distance interpersonnelle

# Classe Ball 
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Ball:
    def __init__(self, position,radius,space,screen):
        self.radius = radius
        self.position = position
        self.velocity = (0, 0)
        # Création du corps physique
        mass = 1.0
        inertia = pymunk.moment_for_circle(mass, 0, self.radius)
        self.body = pymunk.Body(mass, inertia)
        self.body.position = self.position
        
        self.shape = pymunk.Circle(self.body, self.radius*1.43)
        self.space = space
        self.space.add(self.body, self.shape)
        self.screen = screen
        self.passed_line = False 
        
    def calculate_desired_velocity(self, target_point):
        # Calculer le gradient de la fonction de potentiel
        diff_x = target_point[0] - self.position[0]
        diff_y = target_point[1] - self.position[1]
        distance = math.sqrt(diff_x**2 + diff_y**2)
        gradient_x = diff_x / distance
        gradient_y = diff_y / distance  
        # Calculer la vitesse désirée
        desired_velocity_x = U * gradient_x
        desired_velocity_y = U * gradient_y
        return (desired_velocity_x, desired_velocity_y)
    
    def calculate_correction_velocity(self, balls):
        correction_velocity = (0, 0)
        for ball in balls:
            if ball != self:
                diff_x = ball.position[0] - self.position[0]
                diff_y = ball.position[1] - self.position[1]
                distance = math.sqrt(diff_x**2 + diff_y**2)
                direction_x = diff_x / distance
                direction_y = diff_y / distance #ICI (  ) * (s / 10 )
                direction = [diff_x, diff_y] # ICI 
                # Calculer la correction de vitesse
                correction = [-U * math.exp(-distance/delta) * d for d in direction]
                correction_velocity = (correction_velocity[0] + correction[0], correction_velocity[1] + correction[1]) 
        return correction_velocity
    
    def update(self, balls, target_point):
        desired_velocity = self.calculate_desired_velocity(target_point)
        correction_velocity = self.calculate_correction_velocity(balls)
        # Calculer la nouvelle vitesse en ajoutant la correction de vitesse
        new_velocity = (desired_velocity[0] + correction_velocity[0], desired_velocity[1] + correction_velocity[1])
        self.body.velocity = new_velocity
        self.position = self.body.position
        
    def draw(self):
        pygame.draw.circle(self.screen, RED, (int(self.position[0]), int(self.position[1])), self.radius)
            
# Mur_Porte
def create_segment(pos1,pos2,width,space):
    segment_body = pymunk.Body(body_type= pymunk.Body.STATIC)
    segment_shape = pymunk.Segment(segment_body, pos1,pos2, width)#10 width segment 
    segment_shape.elasticity=1
    segment_body.friction = 0.5
    space.add(segment_body , segment_shape)






# Boucle principale

def simulate(Nombre_Ball):
    pygame.init()
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    space = pymunk.Space()
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    target_point = (WIDTH+100, HEIGHT/2)
    positions = set()
    balls = []
    while len(balls) < Nombre_Ball:
        position = (randint(10, 400), randint(10, 550))
        if position not in positions:
            positions.add(position)
            balls.append(Ball(position, 8, space, screen))

    balls_2=balls.copy()
    Segment21 = create_segment((500,0),(500,270),15,space)
    segment22 = create_segment((500,330), (500,600),15,space)
    Temps_Sortie_chaque_boule=[]
    running = True
    start_time = time.time()
    last_ball = None  # Initialisation de la variable pour stocker la dernière boule
    s=0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(WHITE)
        #pygame.draw.circle(screen,(0,255,0),target_point,5)
        for ball in balls:
            ball.update(balls, target_point)
            ball.draw()
            # Vérification du passage de chaque boule à travers la ligne
            if ball.body.position.x > 500 and ball in balls_2:
                s+=1
                balls_2.remove(ball)
                middle_time=time.time()
                Temps_Sortie_chaque_boule.append(middle_time-start_time) 
                if s==Nombre_Ball:
                    last_ball = ball  # Mettre à jour la dernière boule
        pygame.draw.line(screen, (0,0,0), (500,0),(500,270), 15)
        pygame.draw.line(screen, (0,0,0), (500,330), (500,600), 15)
        pygame.display.flip()
        clock.tick(100)
        space.step(1/100)  
        # Vérification si la dernière boule a passé la ligne
        if last_ball and not last_ball.passed_line:
            last_ball.passed_line = True
            end_time = time.time()
            running = False

    pygame.quit()
    elapsed_time = end_time - start_time
    return(Temps_Sortie_chaque_boule)


simulate(100)

def tracage(nombre_ball,nombre_simulation): 
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression

    Personne_evacuee = np.arange(1, nombre_ball+1)
    Temps_Sortie_Personne = []

    # Effectuer les (nombre_simulation)* simulations
    for i in range(nombre_simulation):
        temps_simulation = simulate(nombre_ball)  
        Temps_Sortie_Personne.append(temps_simulation)

    # Convertir les listes en tableaux numpy
    Personne_evacuee = np.array(Personne_evacuee)
    Temps_Sortie_Personne = np.array(Temps_Sortie_Personne)

    # Tracer les courbes
    plt.figure()
    for i in range(nombre_simulation):
        plt.plot(Temps_Sortie_Personne[i], Personne_evacuee, color='green')

    # Effectuer la régression linéaire
    reg = LinearRegression()
    reg.fit(Temps_Sortie_Personne.mean(axis=0).reshape(-1, 1), Personne_evacuee.reshape(-1, 1))

    # Obtenir les prédictions de la régression linéaire
    x_pred = np.linspace(Temps_Sortie_Personne.min(), Temps_Sortie_Personne.max(), 100)
    y_pred = reg.predict(x_pred.reshape(-1, 1))

    # Tracer la ligne de régression linéaire
    plt.plot(x_pred, y_pred, color='red', label='Régression linéaire')

    plt.xlabel('Temps de sortie')
    plt.ylabel('Nombre de personnes évacuées')
    plt.legend()
    plt.show()

tracage(5,2)
