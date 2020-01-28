import pygame
from moteurJeu import *
from Joueur import Joueur

pygame.init()
Clock = pygame.time.Clock()

GrilleDeJeu = Grille()
MoteurDeJeu = MoteurJeu(GrilleDeJeu, Clock)
JoueurH = Joueur()
#JetonActuel = None

while True:
    Clock.tick()
    event = pygame.event.Event(pygame.USEREVENT)
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
    
    posSouris = JoueurH.CliqueSouris(event, MOUSEBUTTONDOWN)
    MoteurDeJeu.Placer(posSouris)