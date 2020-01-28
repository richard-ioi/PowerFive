#! /usr/bin/env python3

"""
    Fichier principal initialisant l'ensemble des classes du jeu.
"""

import pygame
import os
from moteurJeu import *
from modeles import *
from vue import *

pygame.init()
Clock = pygame.time.Clock()
done = False

screenLargeur = 1280
screenHauteur = 720
screen = pygame.display.set_mode((screenLargeur,screenHauteur))
pygame.display.set_caption("Test Animation Forggy")

GrilleDeJeu = Grille()
MoteurDeJeu = MoteurJeu(GrilleDeJeu, Clock)
InterfaceJeu = Interface(screen,GrilleDeJeu)
JoueurH = Joueur()
#JetonActuel = None

imageJeton = scale(pygame.image.load(os.path.join("data","graphismes","jeton_jaune.png")), (32*4,32*4))
posJeton = -10

while not done:
    Clock.tick(60)
    FPS = Clock.get_fps()
    #print(FPS)
    event = pygame.event.Event(pygame.USEREVENT)
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.display.flip()
    
    #posJeton += 5

    #Affichage
    #screen.blit(imageJeton,(screenLargeur//2-imageJeton.get_width()//2-4 , posJeton))
    InterfaceJeu.Affichage()
