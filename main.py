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

largeurFenetre = 1280
hauteurFenetre = 720
Fenetre = pygame.display.set_mode( (largeurFenetre, hauteurFenetre) )
pygame.display.set_caption("PowerFive")

music_pinguTheme = os.path.join("data","sons","pingu_theme.wav")
pygame.mixer.music.load(music_pinguTheme)
pygame.mixer.music.play(loops=-1,start=0.0)

AnimBase = { "Sheriff": Animation(Fenetre, os.path.join("sheriff", "char.png"), 0, 42, 5, True, 62, 64),
             "Froggy": Animation(Fenetre, os.path.join("froggy", "char.png"), 0, 24, 5),
             "Weasel": Animation(Fenetre, os.path.join("weasel", "char.png"), 0, 13, 5, True, 62, 72),
             "Jurassy": Animation(Fenetre, os.path.join("jurassy", "char.png"), 0, 13, 5, True, 62, 72),
             "Pingu": Animation(Fenetre, os.path.join("pingu","char.png"), 0,27,5,True,62,96),
             "PinguBad": Animation(Fenetre, os.path.join("pingu","char_bad.png"), 0,33,5,True,62,96) }
AnimSpec = {}

GrilleDeJeu = Grille()
MoteurDeJeu = MoteurJeu(GrilleDeJeu, Clock)
InterfaceJeu = Interface(Fenetre, largeurFenetre, hauteurFenetre, GrilleDeJeu, AnimBase, AnimSpec)

Joueur = Joueur()
Jeton = Jeton(0,1)
    
#imageJeton = scale(pygame.image.load(os.path.join("data","graphismes","jeton_jaune.png")), (32*4,32*4))
#posJeton = -10

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
