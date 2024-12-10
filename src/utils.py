import pymunk
import pygame

def create_segment(pos1, pos2, width, space):
    segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    segment_shape = pymunk.Segment(segment_body, pos1, pos2, width)
    segment_shape.elasticity = 1
    segment_body.friction = 0.5
    space.add(segment_body, segment_shape)
    
def draw_exit(screen, largeur_fenetre=60, couleur=(0, 0, 255)):
    hauteur_totale = 600
    y_milieu = hauteur_totale // 2
    demi_largeur = largeur_fenetre // 2

    pygame.draw.line(screen, couleur, (500, 0), (500, y_milieu - demi_largeur), 15)
    pygame.draw.line(screen, couleur, (500, y_milieu + demi_largeur), (500, hauteur_totale), 15)
