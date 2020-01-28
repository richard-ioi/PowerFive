import pygame
from moteurJeu import *
from Joueur import Joueur

GrilleDeJeu = Grille()
MoteurDeJeu = MoteurJeu(GrilleDeJeu)
JoueurH = Joueur()
#JetonActuel = None

pygame.init()

while True:
    event = pygame.event.Event(pygame.USEREVENT)
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    posSouris = JoueurH.CliqueSouris(event, MOUSEBUTTONDOWN)
    MoteurDeJeu.Placer(posSouris)